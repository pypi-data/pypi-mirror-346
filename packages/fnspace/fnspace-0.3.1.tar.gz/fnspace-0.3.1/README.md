# FnSpace

`FnSpace` 패키지는 에프앤가이드에서 개발한 금융데이터 분석용 파이썬 패키지로 API로 금융데이터를 불러오고 분석하는 기능을 제공합니다.

- `FnSpace` API의 API KEY 발급과 상세 I/O는 아래의 웹사이트를 참조하시기 바랍니다.
  - [https://www.fnspace.com](https://www.fnspace.com)


## Install

`FnSpace` 패키지는 pip install 명령으로 설치할 수 있습니다.

```bash
pip install fnspace
```

## Requirements

`FnSpace` 패키지를 사용하기 위해서는 [https://www.fnspace.com](https://www.fnspace.com)에서 API KEY를 발급받으셔야 합니다.


## 사용법

```python
from fnspace import FnSpace

api_key = "Your API key"
fs = FnSpace(api_key)
```

## 1. 출력 변수 목록 불러오기

출력 변수 리스트를 조회합니다. 출력 결과에는 각 항목의 API 지원 여부를 나타내는 `IS_AVAILABLE` 컬럼이 포함됩니다.

```python
item_df = fs.get_data(category="item_list", data_type="account") # 재무 데이터의 출력 변수 리스트
```

출력 변수의 Item Code는 본 github의 `ITEM_LIST.csv`를 참조하셔도 됩니다.

## 2. 재무 데이터 불러오기

종목코드와 출력 변수를 지정하여 재무 데이터를 조회합니다.

```python
account_df = fs.get_data(
    category = 'account',
    code = ['005930', '005380'], # 종목코드 리스트. 예) 삼성전자, 현대자동차
    item = ['M122700', 'M123955'], # 출력 변수 리스트. 예) 당기순이익, 보고서발표일 (default : 전체 item)
    consolgb = 'M', # 회계기준. 주재무제표(M)/연결(C)/별도(I) (default : 주재무제표(M))
    annualgb = 'A', # 연간(A)/분기(QQ)/분기누적(QY) (default : 연간(A))
    accdategb = 'C', # 컨센서스 결산년월 선택 기준. Calendar(C)/Fiscal(F) (default : Calendar(C))
    from_year = '2020', # 조회 시작 연도 (default : 직전 연도)
    to_year = '2020', # 조회 종료 연도 (default : 직전 연도)
    kor_item_name = True # 컬럼명 한글 출력 여부 (default : ITEM_CD 그대로)
)
```

## 3. 주식 리스트 데이터 불러오기

특정 시장의 주식 리스트 데이터를 조회합니다.

```python
stock_list_df = fs.get_data(
    category = 'stock_list',
    mkttype ='4', # KOSPI(1)/KOSDAQ(2)/KONEX(3)/KOSPI+KOSDAQ(4)/KOSPI200(5)/KOSDAQ150(6)
    date ='20240624' # 조회 기준일 (default : 오늘 일자)
)
```

## 4. 주가 데이터 불러오기

주가 데이터를 조회합니다.

```python
price_df = fs.get_data(
    category = 'stock_price',
    code = ['005930', '005380'], # 종목코드 리스트. 예) 삼성전자, 현대자동차
    item = ['S100300'], # 출력 변수 리스트. 예) 시가, 고가 (default : 수정 OLHCV)
    from_date = '20230101', # 조회 시작 일자 (default : to_date-365일)
    to_date ='20240624' # 조회 종료 일자 (default : 오늘 일자)
)
```

## 5. 경제 데이터 불러오기

경제 데이터를 조회합니다. ITEM_LIST의 IS_AVAILABLE 컬럼이 'Y'인 항목만 조회 가능합니다.

```python
macro_df = fs.get_data(
    category = 'macro',
    item = ['aKONA10NIGDPW', 'aKONA10GSGSR'], # 출력 변수 리스트. 예) 국민총소득(명목,원화)(십억원), 총저축률(명목)(%)
    from_date = '20230101', # 조회 시작 일자 (default : to_date-365일)
    to_date ='20240624', # 조회 종료 일자 (default : 오늘 일자)
    kor_item_name=True # 컬럼명 한글 출력 여부 (default : ITEM_CD 그대로)
)
```

## 6. 컨센서스 데이터 불러오기

### 6-1) 컨센서스 - 투자의견 & 목표주가

```python
consensus_price_df = fs.get_data(
    category = 'consensus-price',
    item = ['E612500'], # 출력 변수 리스트
    code = ['005930', '005380'],
    from_date = '20230101', # 조회 시작 일자 (default : to_date-365일)
    to_date ='20240624', # 조회 종료 일자
    kor_item_name=True # 컬럼명 한글 출력 여부 (default : ITEM_CD 그대로)
)
```

### 6-2) 컨센서스 - 추정실적 - Fiscal 조회

```python
consensus_earning_df = fs.get_data(
    category = 'consensus-earning-fiscal',
    item = ['E122700'], # 출력 변수 리스트. 예) 당기순이익
    code = ['005930', '005380'],
    consolgb = "M", # 회계기준. 주재무제표(M)/연결(C)/별도(I) (default : 주재무제표(M))
    annualgb = "A", # 연간(A)/분기(Q) (default : 연간(A))
    from_year = "2023", # 조회 시작 연도 (default : 직전 연도)
    to_year = "2024", # 조회 종료 연도 (default : 직전 연도)
    kor_item_name=True # 컬럼명 한글 출력 여부 (default : ITEM_CD 그대로)
)
```

### 6-3) 컨센서스 - 추정실적 - daily 조회

```python
consensus_earning_df = fs.get_data(
    category = 'consensus-earning-daily',
    item = ['E121500'], # 출력 변수 리스트. 예) 당기순이익
    code = ['005930', '005380'],
    consolgb = "M", # 회계기준. 주재무제표(M)/연결(C)/별도(I) (default : 주재무제표(M))
    annualgb = "A", # 연간(A)/분기(Q) (default : 연간(A))
    accdategb = "C", # 컨센서스 결산년월 선택 기준. Calendar(C)/Fiscal(F)/Present Base(P) (default : Calendar(C))
    from_year = "2023", # 조회 시작 연도 (default : 직전 연도)
    to_year = "2024", # 조회 종료 연도 (default : 직전 연도)
    from_date = "20230101", # 조회 시작 일자 (default : to_date-365일)
    to_date = "20240620", # 조회 종료 일자 (default : 오늘 일자)
    kor_item_name=True # 컬럼명 한글 출력 여부 (default : ITEM_CD 그대로)
)
```

### 6-4) 컨센서스 - Forward 지표

```python
consensus_forward_df = fs.get_data(
    category = 'consensus-forward',
    item = ['E121560'], # 출력 변수 리스트. 예) 영업이익(Fwd.12M)
    code = ['005930', '005380'],
    consolgb = "M", # 회계기준. 주재무제표(M)/연결(C)/별도(I) (default : 주재무제표(M))
    from_date = "20230101", # 조회 시작 일자 (default : to_date-365일)
    to_date = "20240620", # 조회 종료 일자 (default : 오늘 일자)
    kor_item_name=True # 컬럼명 한글 출력 여부 (default : ITEM_CD 그대로)
)
```

## 7. 항목 가용성 활용하기

모든 API는 ITEM_LIST.csv의 IS_AVAILABLE 컬럼을 확인하여 'Y'인 항목만 API 요청에 포함합니다.
사용 가능한 항목만 확인하려면 다음과 같이 필터링할 수 있습니다:

```python
# 사용 가능한 경제 데이터 항목만 필터링
available_macro = fs.item_df[(fs.item_df['DATA_TYPE'] == 'macro') & 
                           (fs.item_df['IS_AVAILABLE'] == 'Y')]

# 카테고리별 사용 가능한 항목 수 확인
categories = fs.item_df['DATA_TYPE'].unique()
for category in categories:
    available = len(fs.item_df[(fs.item_df['DATA_TYPE'] == category) & 
                              (fs.item_df['IS_AVAILABLE'] == 'Y')])
    total = len(fs.item_df[fs.item_df['DATA_TYPE'] == category])
    print(f"{category}: {available}/{total} ({available/total*100:.1f}%)")
```

## 배포 기록

### v0.3.1 (2025-05-07)

- 코드 구조 개선 및 중복 제거를 위한 리팩토링
  - 공통 기능을 위한 헬퍼 메서드 추가: `_filter_available_items`, `_make_api_request`, `_process_json_response`
  - 각 API 카테고리별 메서드 간소화 및 표준화
- ITEM_LIST.csv에 IS_AVAILABLE 컬럼 추가
  - 항목별 API 지원 여부를 'Y'/'N'으로 표시
  - 사용 불가능한 항목은 자동으로 API 요청에서 제외
  - item_list 카테고리 조회 시 IS_AVAILABLE 컬럼 함께 제공
- consensus-earning-daily API 수정
  - accdategb 파라미터 추가 및 오류 수정
  - 응답 처리 개선
- consensus-earning-fiscal API에 accdategb 파라미터 추가
- 에러 처리 및 로깅 개선
  - 다양한 예외 유형 처리 강화
  - 상세한 에러 메시지 제공
  - URL, 파라미터, 응답 정보 표시
- 전체적인 API 응답 처리 일관성 강화

### v0.2 (2024-07-02)

- fnspace 홈페이지의 기능 수록 및 example 폴더 추가
