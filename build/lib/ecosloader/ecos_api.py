import requests
import pandas as pd
import time
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from difflib import SequenceMatcher
from webdriver_manager.chrome import ChromeDriverManager


class stats_codes:
    def __init__(self):
        # 클래스 초기화: stats_codes_info와 stats_codes를 None으로 초기화
        self.stats_codes_info = None
        self.stats_codes = None

    def load_stats_code(self, path):
        """
        파일에서 통계 코드를 로드하여 DataFrame으로 변환.
        
        Args:
            path (str): 통계 코드가 저장된 파일 경로
        """
        # 통계코드 csv 파일 가져오기
        self.stats_codes_info = pd.read_csv(path)  

    def update_stats_code(self, api_key):
        """
        API를 통해 통계 코드를 업데이트하고 데이터를 DataFrame으로 저장.
        
        Args:
            api_key (str): API 호출에 사용될 인증 키
        """
        # 통계 코드 목록 크롤링
        self.crawling_stats_code()
        stats_list = []  # API 응답 데이터를 저장할 리스트
        idx_no = 0  # 진행 상태 확인용 인덱스

        # 각 통계 코드에 대해 API 호출
        for stats_code in tqdm(self.stats_codes, desc="Processing stats codes"):
            # API 호출 URL 생성
            url = 'https://ecos.bok.or.kr/api/StatisticItemList/{}/json/kr/1/10/{}'.format(api_key, stats_code)

            # API 호출 및 응답 처리
            response = requests.get(url)

            if response.status_code == 200:
                # 응답 데이터를 JSON으로 변환
                data = response.json()
            else:
                print(f"Error: {response.status_code}, {response.text}")

            # 진행 상태 출력 및 대기 시간 설정
            idx_no += 1
            if idx_no % 100 == 0:
                time.sleep(60)  # 과도한 호출을 방지하기 위해 대기

            try:
                # 통계 데이터를 리스트에 추가
                stats_list = stats_list + data['StatisticItemList']['row']
            except:
                pass

        # 통계 데이터를 DataFrame으로 변환
        self.stats_codes_info = pd.DataFrame(stats_list)

    def search_stats_code(self, name):
        """
        통계 코드 정보에서 특정 이름을 포함하는 코드 검색.
        
        Args:
            name (str): 검색할 코드 이름
        
        Returns:
            DataFrame: 검색된 통계 코드 정보
        """
        
        def similar_name(name1, name2):
            """
            유사한 이름을 가진 통계 코드 검색.
            
            Args:
                name (str): 검색할 이름
            
            Returns:
                DataFrame: 검색된 통계 코드 정보
            """
            return SequenceMatcher(None, name1, name2).ratio()
            
        
        if self.stats_codes_info is None:
            print('Empty stats codes info')  # 데이터가 없을 경우 메시지 출력


        elif self.stats_codes_info['STAT_NAME'].str.contains(name).sum() != 0:
            # STAT_NAME 열에서 name을 포함하는 행 필터링
            return self.stats_codes_info.loc[self.stats_codes_info['STAT_NAME'].str.contains(name), :]
        
        else :
            print('searching similar names')
            similar_names = sorted(self.stats_codes_info['STAT_NAME'].unique(), key=lambda x: similar_name(name, x), reverse=True)
            return self.stats_codes_info.loc[self.stats_codes_info['STAT_NAME'].str.contains(similar_names[0]), :] 

    def crawling_stats_code(self):
        """
        웹 페이지를 크롤링하여 통계 코드 목록을 수집.
        """
        # 크롬 드라이버 옵션 설정
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # 브라우저 창을 열지 않고 실행 (필요 시 활성화)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # 크롬 드라이버 초기화
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            # 크롤링할 URL 열기
            url = "https://ecos.bok.or.kr/api/#/DevGuide/StatisticalCodeSearch"
            driver.get(url)
            time.sleep(3)  # 페이지 로드 대기

            # 스크롤 대상 요소 가져오기
            scroll_down = driver.find_element(By.CLASS_NAME, "rg-scroll-down")

            # 이미 찾은 mark 태그를 저장할 집합
            found_marks = set()

            # 스크롤을 통해 데이터 수집
            while True:
                pre_marks_num = len(found_marks)  # 스크롤 전 찾은 mark 태그 수
                for i in range(10):
                    scroll_down.click()  # 스크롤 내리기
                time.sleep(0.2)  # 대기

                # mark 태그 수집
                marks = driver.find_elements(By.CSS_SELECTOR, "mark")
                for mark in marks:
                    found_marks.add(mark.text)

                # 스크롤이 더 이상 진행되지 않을 경우 종료
                if pre_marks_num == len(found_marks):
                    break

            # 수집된 데이터에서 통계 코드 추출
            self.stats_codes = [i.split('[')[1].split(']')[0] for i in list(found_marks)]

        finally:
            driver.quit()  # 드라이버 종료

        print('통계 코드 총 {} 개 확인'.format(len(self.stats_codes)))



class api_client:
    def __init__(self, api_key):
        """
        API 클라이언트 초기화.

        Args:
            api_key (str): API 호출에 사용될 인증 키
        """
        self.api_key = api_key  # API 인증 키
        self.output_type = 'json'  # 출력 형식 (기본값: JSON)
        self.language = 'kr'  # 언어 설정 (기본값: 한국어)
        self.stats_codes = stats_codes()  # stats_codes 클래스 인스턴스 생성

    def check_api_key(self):
        """
        API 키의 유효성을 확인.
        """
        try:
            # 샘플 URL을 사용하여 API 키 확인
            sample_url = 'https://ecos.bok.or.kr/api/StatisticTableList/{}/xml/kr/1/10/102Y004'.format(self.api_key)
            response = requests.get(sample_url)
            print('Valid API key: {}'.format(self.api_key))
        except Exception as e:
            print('Invalid API key: {}. Error: {}'.format(self.api_key, e))

    def set_output_type(self, output_type):
        """
        API 출력 형식을 설정.

        Args:
            output_type (str): 출력 형식 ('xml' 또는 'json')
        """
        assert output_type in ['xml', 'json'], 'Output type should be "xml" or "json"'
        self.output_type = output_type
        print('Set output type: {}'.format(self.output_type))

    def set_language(self, language):
        """
        API 언어 설정.

        Args:
            language (str): 언어 설정 ('kr' 또는 'en')
        """
        assert language in ['kr', 'en'], 'Language should be "kr" or "en"'
        self.language = language
        print('Language set to: {}'.format(self.language))

    def stat_search(self, stat_code, first, end, interval, starttime, endtime, subcode1, subcode2='?', subcode3='?', subcode4='?'):
        """
        특정 통계 코드를 사용하여 통계 데이터 검색.

        Args:
            stat_code (str): 통계 코드
            first (int): 시작 인덱스
            end (int): 종료 인덱스
            interval (str): 검색 간격 (e.g., "M")
            starttime (str): 시작 시간 (YYYYMM)
            endtime (str): 종료 시간 (YYYYMM)
            subcode1 (str): 하위 코드 1
            subcode2 (str): 하위 코드 2 (기본값: '?')
            subcode3 (str): 하위 코드 3 (기본값: '?')
            subcode4 (str): 하위 코드 4 (기본값: '?')

        Returns:
            DataFrame: 검색된 통계 데이터
        """
        # API 호출 URL 생성
        url = f'https://ecos.bok.or.kr/api/StatisticSearch/{self.api_key}/{self.output_type}/{self.language}/{first}/{end}/{stat_code}/{interval}/{starttime}/{endtime}/{subcode1}/{subcode2}/{subcode3}/{subcode4}'
        response = requests.get(url)

        # 응답 데이터 확인
        if response.status_code == 200:
            data = response.json()
            self.source_stats_df = pd.DataFrame(data['StatisticSearch']['row'])  # 결과를 DataFrame으로 변환
            return self.source_stats_df
        else:
            print(f"Error: {response.status_code}, {response.text}")

    def todays_100_stat(self):
        """
        오늘의 주요 통계 데이터 100개를 가져옴.

        Returns:
            DataFrame: 오늘의 주요 통계 데이터
        """
        # API 호출 URL 생성
        url = f'https://ecos.bok.or.kr/api/KeyStatisticList/{self.api_key}/{self.output_type}/{self.language}/1/101'
        response = requests.get(url)

        # 응답 데이터 확인
        if response.status_code == 200:
            data = response.json()
            self.source_stats_df = pd.DataFrame(data['KeyStatisticList']['row'])  # 결과를 DataFrame으로 변환
            return self.source_stats_df
        else:
            print(f"Error: {response.status_code}, {response.text}")

    def stat_search_index(self, idx):
        """
        stats_codes_info DataFrame에서 인덱스를 기반으로 통계 데이터를 검색.

        Args:
            idx (int): stats_codes_info의 행 인덱스

        Returns:
            DataFrame: 검색된 통계 데이터
        """
        idx_stat_dict = self.stats_codes.stats_codes_info.loc[idx].to_dict()  # 인덱스에 해당하는 행 데이터를 딕셔너리로 변환

        # P_ITEM_CODE가 None인 경우 기본값으로 설정
        if idx_stat_dict['P_ITEM_CODE'] is None:
            idx_stat_dict['P_ITEM_CODE'] = '?'

        # API 호출 URL 생성
        url = 'https://ecos.bok.or.kr/api/StatisticSearch/{}/{}/{}/1/{}/{}/{}/{}/{}/{}/?/?/?'.format(
            self.api_key, self.output_type, self.language, idx_stat_dict['DATA_CNT'], idx_stat_dict['STAT_CODE'],
            idx_stat_dict['CYCLE'], idx_stat_dict['START_TIME'], idx_stat_dict['END_TIME'], idx_stat_dict['ITEM_CODE'],
            idx_stat_dict['P_ITEM_CODE']
        )
        response = requests.get(url)

        # 응답 데이터 확인
        if response.status_code == 200:
            data = response.json()
            self.source_stats_df = pd.DataFrame(data['StatisticSearch']['row'])  # 결과를 DataFrame으로 변환
            return self.source_stats_df
        else:
            print(f"Error: {response.status_code}, {response.text}")

    def stat_search_indexes(self, idx_list):
        """
        주어진 지표 인덱스 목록(idx_list)에 대해 각 지표의 데이터를 조회하고, 
        주기에 맞게 날짜를 변환한 후, 결측치를 처리하고 병합하여 일별 데이터프레임을 반환하는 함수.

        Args:
            idx_list : list
                지표 인덱스 목록. 각 인덱스는 self.stats_codes.stats_codes_info에서 
                고유하게 지표를 식별하는 값.

        Returns:
            self.source_stats_df : pandas DataFrame
                병합된 지표들의 데이터프레임. 일별('D') 주기로 변환되며 결측치는 
                이전 값으로 채워져 반환됨.
        """


        self.df_list = []
        for i in idx_list:
            # 필요한 정보 가져오기
            stat_info = self.stats_codes.stats_codes_info.loc[i, ['STAT_NAME', 'ITEM_NAME', 'UNIT_NAME', 'CYCLE']]
            stat_name, item_name, unit_name, cycle = stat_info.to_numpy()

            # 지표명 생성
            stat_name = f"{stat_name.split('.')[-1]} {item_name} {unit_name} {cycle}"

            # 데이터 가져오기
            t_df = self.stat_search_index(i)[['TIME', 'DATA_VALUE']]

            # TIME 컬럼 변환
            if cycle == 'M':
                t_df.loc[:,'TIME'] = pd.to_datetime(t_df['TIME'], format='%Y%m')

            elif cycle == 'Q':
                quarter_map = {"Q1": "01", "Q2": "04", "Q3": "07", "Q4": "10"}
                t_df.loc[:,'TIME'] = pd.to_datetime(t_df['TIME'].str[:4] + "-" + t_df["TIME"].str[5:].replace(quarter_map))

            else:
                t_df.loc[:,'TIME'] = pd.to_datetime(t_df['TIME'])

            # 첫번째 데이터만 남도록 수정
            t_df = t_df.sort_values('TIME').drop_duplicates(subset=['TIME'], keep='first')


            # 인덱스 설정 및 컬럼명 변경
            t_df.index = pd.Index(t_df['TIME'], dtype='datetime64[ns]')
            t_df.columns = ['TIME', stat_name]
            t_df = t_df[stat_name]

            self.df_list.append(t_df)

        # 병합 및 결측치 처리
        tmp_df = pd.DataFrame(self.df_list).T
        tmp_df = tmp_df.astype('float')

        self.source_stats_df = tmp_df.asfreq("D").ffill()
        return self.source_stats_df