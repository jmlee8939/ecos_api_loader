# ReadMe for ECOS API Integration Code

This document provides an overview of the Python codebase used to interact with the ECOS (Economic Statistics System) API provided by Bank of Korea. The code facilitates retrieving and managing statistical data for analytical purposes.

## Table of Contents
1. [Overview](#overview)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Classes and Methods](#classes-and-methods)
    - [stats_codes Class](#stats_codes-class)
    - [api_client Class](#api_client-class)
5. [Usage Examples](#usage-examples)
6. [Error Handling](#error-handling)
7. [Notes](#notes)

---

## Overview
The code consists of two primary classes:
1. **stats_codes**: Handles statistical code management, including loading, updating, and searching for codes.
2. **api_client**: Manages API interactions, including retrieving statistical data, validating API keys, and fetching key statistics.

This setup allows users to efficiently manage and query statistical data using Python.

---

## Requirements
- Python 3.8+
- Libraries:
  - requests
  - pandas
  - selenium
  - tqdm
  - webdriver_manager

---

## Installation

1. Ensure you have a valid ECOS API key. You can request one from the [ECOS website](https://ecos.bok.or.kr/).
3. Install the required dependencies :
   ```bash
   pip install requests pandas selenium tqdm webdriver-manager
   ```


---

## Classes and Methods

### stats_codes Class
Manages statistical codes and provides utilities for crawling, loading, and searching codes.

#### Attributes:
- `stats_codes_info` (DataFrame): Stores statistical code information.
- `stats_codes` (list): Stores the list of statistical codes.

#### Methods:
1. **`load_stats_code(path)`**:
   - Loads statistical codes from a CSV file.
   - **Args:**
     - `path` (str): Path to the CSV file.

2. **`update_stats_code(api_key)`**:
   - Updates statistical codes by fetching data through the API.
   - **Args:**
     - `api_key` (str): API authentication key.

3. **`search_stats_code(name)`**:
   - Searches for a specific statistical code by name.
   - **Args:**
     - `name` (str): Name or partial name to search for.
   - **Returns:** Filtered DataFrame.

4. **`crawling_stats_code()`**:
   - Crawls the ECOS website to extract statistical codes.

---

### api_client Class
Handles API interactions and provides methods for data retrieval and key validation.

#### Attributes:
- `api_key` (str): API authentication key.
- `output_type` (str): Format for API responses (default: `json`).
- `language` (str): Language for API responses (default: `kr`).
- `stats_codes` (stats_codes): Instance of the `stats_codes` class.

#### Methods:
1. **`check_api_key()`**:
   - Validates the API key by making a sample request.

2. **`set_output_type(output_type)`**:
   - Sets the response format (`json` or `xml`).

3. **`set_language(language)`**:
   - Sets the response language (`kr` or `en`).

4. **`stat_search(...)`**:
   - Searches for statistical data using a specific code and parameters.
   - **Args:** Refer to the function signature in the code.
   - **Returns:** DataFrame with the retrieved data.

5. **`todays_100_stat()`**:
   - Retrieves today’s 100 key statistics.
   - **Returns:** DataFrame with key statistics.

6. **`stat_search_index(idx)`**:
   - Searches for statistical data based on an index from `stats_codes_info`.
   - **Args:**
     - `idx` (int): Index of the statistical code.
   - **Returns:** DataFrame with the retrieved data.

---

## Usage Examples

### Example 1: Loading and Searching Statistical Codes
```python
from your_module import stats_codes

sc = stats_codes()
sc.load_stats_code("path_to_csv.csv")
result = sc.search_stats_code("Inflation")
print(result)
```

### Example 2: Fetching Statistical Data
```python
from your_module import api_client

api = api_client(api_key="your_api_key")
data = api.stat_search(
    stat_code="102Y004",
    first=1,
    end=10,
    interval="M",
    starttime="202201",
    endtime="202212",
    subcode1="101",
)
print(data)
```

### Example 3: Crawling Statistical Codes
```python
sc.crawling_stats_code()
print(sc.stats_codes)
```

---

## Error Handling
- **Invalid API Key:**
  - The `check_api_key()` method will validate the API key and display an error message if it is invalid.

- **API Rate Limiting:**
  - The `update_stats_code()` method includes a sleep interval to prevent excessive API calls.

- **Connection Issues:**
  - Ensure stable internet connectivity. Exceptions will display error messages for debugging.

---

## Notes
- The ECOS API has rate limits; avoid making excessive requests in a short time.
- Some methods (e.g., `crawling_stats_code`) may require adjustments based on changes to the ECOS website.
- For headless browser usage, uncomment the `chrome_options.add_argument("--headless")` line in `crawling_stats_code()`.

For further assistance, refer to the [ECOS API Documentation](https://ecos.bok.or.kr/).

