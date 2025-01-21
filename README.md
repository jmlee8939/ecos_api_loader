# ECOS API Loader Code

본 문서는 한국은행이 제공하는 ECOS(경제통계시스템) API와  Python 코드베이스에 대한 개요를 제공합니다. 이 코드는 한국은행의 데이터를 쉽게 수집하여 분석 목적으로 활용할 수 있도록 지원합니다. by jaeminiman

## 목차

1. [개요](#개요)
2. [요구사항](#요구사항)
3. [설치](#설치)
4. [클래스와 메서드](#클래스와-메서드)
    - [stats_codes 클래스](#stats_codes-클래스)
    - [api_client 클래스](#api_client-클래스)
5. [사용 예제](#사용-예제)
6. [에러 처리](#에러-처리)
7. [참고사항](#참고사항)

---

## 개요

이 코드는 두 개의 주요 클래스로 구성됩니다:

1. **stats_codes**: 통계 코드의 로드, 갱신, 검색 등 관리 기능을 담당합니다.
2. **api_client**: API와의 상호작용을 관리하며 통계 데이터 검색, API 키 유효성 검증, 주요 통계 조회 기능을 제공합니다.

---

## 요구사항

- Python 3.8+
- 필수 라이브러리:
    - requests
    - pandas
    - selenium
    - tqdm
    - webdriver_manager

---

## 설치

1.  라이브러리를 설치합니다:
    
    ```bash
    pip install requests pandas selenium tqdm webdriver-manager
    ```
    
3. 유효한 ECOS API 키는. [ECOS 한국은행](https://ecos.bok.or.kr/)에서 요청할 수 있습니다.

---

## 클래스와 메서드

### stats_codes 클래스

통계 코드를 관리하며 크롤링, 로드, 검색 기능을 제공합니다.

#### 속성:

- `stats_codes_info` (DataFrame): 통계 코드 정보를 저장합니다.
- `stats_codes` (list): 통계 코드 목록을 저장합니다.

#### 메서드:

1. **`load_stats_code(path)`**:
    
    - CSV 파일에서 통계 코드를 로드합니다.
    - **매개변수:**
        - `path` (str): CSV 파일 경로.
2. **`update_stats_code(api_key)`**:
    
    - API를 통해 데이터를 가져와 통계 코드를 갱신합니다.
    - **매개변수:**
        - `api_key` (str): API 인증 키.
3. **`search_stats_code(name)`**:
    
    - 이름으로 특정 통계 코드를 검색합니다.
    - **매개변수:**
        - `name` (str): 검색할 이름 또는 이름의 일부.
    - **반환값:** 필터링된 DataFrame.
4. **`crawling_stats_code()`**:
    
    - ECOS 웹사이트를 크롤링하여 통계 코드를 추출합니다.

---

### api_client 클래스

API와의 상호작용을 처리하며 데이터 검색 및 키 유효성 검증 메서드를 제공합니다.

#### 속성:

- `api_key` (str): API 인증 키.
- `output_type` (str): API 응답 형식 (기본값: `json`).
- `language` (str): API 응답 언어 (기본값: `kr`).
- `stats_codes` (stats_codes): `stats_codes` 클래스의 인스턴스.

#### 메서드:

1. **`check_api_key()`**:
    
    - 샘플 요청을 보내 API 키를 검증합니다.
2. **`set_output_type(output_type)`**:
    
    - 응답 형식을 설정합니다 (`json` 또는 `xml`).
3. **`set_language(language)`**:
    
    - 응답 언어를 설정합니다 (`kr` 또는 `en`).
4. **`stat_search(...)`**:
    
    - 특정 코드와 매개변수를 사용하여 통계 데이터를 검색합니다.
    - **매개변수:** 코드의 함수 시그니처를 참조하세요.
    - **반환값:** 검색된 데이터가 포함된 DataFrame.
5. **`todays_100_stat()`**:
    
    - 오늘의 100개 주요 통계를 조회합니다.
    - **반환값:** 주요 통계가 포함된 DataFrame.
6. **`stat_search_index(idx)`**:
    
    - `stats_codes_info`의 인덱스를 기반으로 통계 데이터를 검색합니다.
    - **매개변수:**
        - `idx` (int): 통계 코드의 인덱스.
    - **반환값:** 검색된 데이터가 포함된 DataFrame.

---

## 사용 예제

### 예제 1: 통계 코드 로드 및 API 입력

```python
from ecosloader import api_client

api_key = 'your_api_key'
# API 입력
client = api_client(api_key)
# API 확인
client.check_api_key()
# 통계 코드 로드 (csv 파일)
client.stats_codes.load_stats_code(path='https://github.com/jmlee8939/macrowave_investing/raw/refs/heads/main/data/stats_df.csv')
# 통계 코드 검색
result = client.search_stats_code("주식시장")
print(result)
```

### 예제 2: 통계 데이터 검색

```python
from ecosloader import api_client
api_key = 'your_api_key'
client = api_client(api_key)

# 통계 코드로 검색
data = client.stat_search(
    stat_code="102Y004",
    first=1,
    end=10,
    interval="M",
    starttime="202201",
    endtime="202212",
    subcode1="101",
)
print(data)

# 통계코드 index 로 검색
data = client.stat_search_index(idx)
print(data)

# 오늘의 100대 통계코드 
data = client.todays_100_stat()
print(data)
```

### 예제 3: 통계 코드 크롤링

```python
from ecosloader import api_client
api_key = 'your_api_key'
client = api_client(api_key)

# 한국은행 ECOS 홈페이지에서 통계코드 크롤링
client.stats_codes.update_stats_code(api_key)
```

*상세한 예시 코드는 package_test.ipynb를 참조하세요.

---

## 에러 처리

### 유효하지 않은 API 키

- `check_api_key()` 메서드는 API 키를 검증하며, 유효하지 않은 경우 에러 메시지를 출력합니다.

### API 호출 제한

- `update_stats_code()` 메서드는 과도한 API 호출을 방지하기 위해 대기 시간을 포함합니다.

### 연결 문제

- 안정적인 인터넷 연결을 유지하세요. 예외 발생 시 디버깅을 위한 에러 메시지가 출력됩니다.

---

## 참고사항

- ECOS API는 호출 제한이 있으므로 짧은 시간에 과도한 요청을 하지 마세요.
- 일부 메서드(예: `crawling_stats_code`)는 ECOS 웹사이트 변경에 따라 조정이 필요할 수 있습니다.

추가 지원이 필요하면 [ECOS API 문서](https://ecos.bok.or.kr/)를 참조하세요.
