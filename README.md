# Budget manager

- 한 달 단위로 사용할 예산을 설정하고, 설정한 예산을 기반으로 어떤 소비를 하고 있는지를 통해 올바른 소비 습관을 형성하는 데에 기여하는 서비스입니다.


## 목차
- [개요](#개요)
- [요구사항](#요구사항)
- [개발환경세팅](#개발환경세팅)
- [Installation & Run](#Installation)
- [ER-Diagram](#ER-Diagram)
- [API Documentation](#API)
- [프로젝트 진행 및 이슈 관리](#프로젝트)
- [구현과정(설계 및 의도)](#구현과정)
- [Authors](#Authors)



## 개요
- 본 서비스는 사용자들이 개인 재무를 관리하고 지출을 추적하는 데 도움을 주는 애플리케이션입니다. 이 앱은 사용자들이 예산을 설정하고 지출을 모니터링하며 재무 목표를 달성하는 데 도움이 됩니다. 


### 유저히스토리
- **A. 유저**는 본 사이트에 들어와 회원가입을 통해 서비스를 이용합니다.
- **B. 예산 설정 및 설계 서비스**
    - `월별` 총 예산을 설정합니다.
    - 본 서비스는 `카테고리` 별 예산을 설계(=추천)하여 사용자의 과다 지출을 방지합니다.
- **C. 지출 기록**
    - 사용자는 `지출` 을  `금액`, `카테고리` 등을 지정하여 등록 합니다. 언제든지 수정 및 삭제 할 수 있습니다.
- **D. 지출 컨설팅**
    - `월별` 설정한 예산을 기준으로 오늘 소비 가능한 `지출` 을 알려줍니다.
    - 매일 발생한 `지출` 을 `카테고리` 별로 안내받습니다.
- **E. 지출 통계**
    - `지난 달 대비` , `지난 요일 대비`,  `다른 유저 대비` 등 여러 기준 `카테고리 별` 지출 통계를 확인 할 수 있습니다.


## 요구사항 및 구현사항

### 1. 유저
#### 사용자 회원가입(API)
- 본 서비스에서는 유저 고유 정보가 크게 사용되지 않아 간단히 구현합니다.
- `계정명` , `패스워드` 입력하여 회원가입

#### 사용자 로그인(API)
- `계정`, `비밀번호` 로 로그시 `JWT` 가 발급됩니다.
- 이후 모든 API 요청 Header 에 `JWT` 가 항시 포함되며, `JWT` 유효성을 검증합니다.


### 2. 예산설정 및 설계
- API호출로 동작되는 기능이 아닌 스케쥴러를 통해 매 시간 실행되는 기능들입니다. 클래스, 함수 등 자유롭게 구조하세요.

#### 카테고리 목록(API)
- 유저가 예산설정에 사용할 수 있도록 모든 카테고리 목록을 반환합니다.

#### 예산 설정(API)

- 해당 기간 별 설정한 `예산` 을 설정합니다. 예산은 `카테고리` 를 필수로 지정합니다.
    - ex) `식비` : 40만원, `교통` : 20만원
- 사용자는 언제든지 위 정보를 변경할 수 있습니다.

#### 예산 설계 (=추천) (API)

- 카테고리 별 예산 설정에 어려움이 있는 사용자를 위해 예산 비율 추천 기능이 존재합니다.
- `카테고리` 지정 없이 총액 (ex. 100만원) 을 입력하면, `카테고리` 별 예산을 자동 생성합니다.

- 기존 요구사항(유저들의 평균으로 추천)과 다르게 스타일을 추천하고 스타일에 따른 정해진 비율을 선택하는 것으로 수정했습니다.
- 유저들이 서비스 접근 시 쉽게 설정이 가능하도록 4가지 스타일을 추천합니다.
    - REC_LIST를 통해 스타일 종류를 제시합니다.


### 3.## 지출 기록

### 지출

- `지출 일시`, `지출 금액`, `카테고리` 와 `메모` 를 입력하여 생성합니다
    - 추가적인 필드 자유롭게 사용

### 지출 CRUD (API)

- 지출을 `생성`, `수정`, `읽기(상세)`, `읽기(목록)`, `삭제` , `합계제외` 할 수 있습니다.
- `생성한 유저`만 위 권한을 가집니다.
- `읽기(목록)` 은 아래 기능을 가지고 있습니다.
    - 필수적으로 `기간` 으로 조회 합니다.
    - 조회된 모든 내용의 `지출 합계` , `카테고리 별 지출 합계` 를 같이 반환합니다.
    - 특정 `카테고리` 만 조회.
    - `최소` , `최대` 금액으로 조회.
        - ex) 0~10000원 / 20000원 ~ 100000원
- `합계제외` 처리한 지출은 목록에 포함되지만, 모든 `지출 합계`에서 제외됩니다.



### 4. 지출 컨설팅

#### 오늘 지출 추천(API)

- 설정한 `월별` 예산을 만족하기 위해 오늘 지출 가능한 금액을 `총액` 과 `카테고리 별 금액` 으로 제공합니다.
    - ex) 11월 9일 지출 가능 금액 총 30,000원, 식비 15,000 … 으로 페이지에 노출 예정.
- 고려사항 1. 앞선 일자에서 과다 소비하였다 해서 오늘 예산을 극히 줄이는것이 아니라, 이후 일자에 부담을 분배한다.
    - 앞선 일자에서 사용가능한 금액을 1만원 초과했다 하더라도, 오늘 예산이 1만원 주는것이 아닌 남은 기간 동안 분배해서 부담(10일 남았다면 1천원 씩).
- 고려사항 2. 기간 전체 예산을 초과 하더라도 `0원` 또는 `음수` 의 예산을 추천받지 않아야 한다.
    - 지속적인 소비 습관을 생성하기 위한 서비스이므로 예산을 초과하더라도 적정한 금액을 추천받아야 합니다.
    - `최소 금액`을 자유롭게 설정하세요.
- 유저의 상황에 맞는 1 문장의 `멘트` 노출.
    - 잘 아끼고 있을 때, 적당히 사용 중 일 때, 기준을 넘었을때, 예산을 초과하였을 때 등 유저의 상황에 맞는 메세지를 같이 노출합니다.
    - 조건과 기준은 자유롭게 설정하세요.
    - ex) “절약을 잘 실천하고 계세요! 오늘도 절약 도전!” 등
- 15333원 과 같은 값이라면 백원 단위 반올림 등으로 사용자 친화적이게 변환

- **선택 구현 기능)** 매일 08:00 시 알림 발송
    - Scheduler 까지만 구현하셔도 좋습니다.
    - Discord webhook, 이메일, 카카오톡 등 실제 알림까지 진행하셔도 좋습니다.

#### 오늘 지출 안내(API)

- 오늘 지출한 내용을 `총액` 과 `카테고리 별 금액` 을 알려줍니다.
- `월별`설정한 예산 기준 `카테고리 별` 통계 제공
    - 일자기준 오늘 `적정 금액` : 오늘 기준 사용했으면 적절했을 금액
    - 일자기준 오늘 `지출 금액` : 오늘 기준 사용한 금액
    - `위험도` : 카테고리 별 적정 금액, 지출금액의 차이를 위험도로 나타내며 %(퍼센테이지) 입니다.
        - ex) 오늘 사용하면 적당한 금액 10,000원/ 사용한 금액 20,000원 이면 200%
- **선택 구현 기능)** 매일 20:00 시 알림 발송
    - Scheduler 까지만 구현하셔도 좋습니다.
    - Discord webhook, 이메일, 카카오톡 등 실제 알림까지 진행하셔도 좋습니다.


### 5. 지출 통계
- Redis 를 연동합니다.

#### Dummy 데이터 생성
- 사용자의 통계데이터 생성을 위해 Dummy 데이터를 생성합니다.

#### 지출 통계 (API)

- `지난 달` 대비 `총액`, `카테고리 별` 소비율.
    - 오늘이 10일차 라면, 지난달 10일차 까지의 데이터를 대상으로 비교
    - ex) `식비` 지난달 대비 150%
- `지난 요일` 대비 소비율
    - 오늘이 `월요일` 이라면 지난 `월요일` 에 소비한 모든 기록 대비 소비율
    - ex) `월요일` 평소 대비 80%
- `다른 유저` 대비 소비율
    - 오늘 기준 다른 `유저` 가 예산 대비 사용한 평균 비율 대비 나의 소비율
    - 오늘기준 다른 유저가 소비한 지출이 평균 50%(ex. 예산 100만원 중 50만원 소비중) 이고 나는 60% 이면 120%.
    - ex) `다른 사용자` 대비 120%


## 개발환경세팅
가상환경: venv

언어 및 프레임워크: ![Python](https://img.shields.io/badge/python-3670A0?&logo=python&logoColor=ffdd54) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?&logo=django&logoColor=white&color=ff1709&labelColor=gray)

데이터 베이스: ![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?&logo=mysql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%2300f.svg?&logo=redis&logoColor=#DC382D)


## Installation & Run
### MySQL DB 세팅
- DATABASE생성
    - DB_NAME=foodie
    - DB_HOST=localhost
    - DB_PORT=3306
- USER생성
    - DB_USER=wanted
    - 유저에게 db권한주기

### 환경 세팅

## 2️ 애플리케이션의 실행 방법 (엔드포인트 호출 방법 포함)
(전제) `python >= 3.11` 과 `mysql >= 8.0` 은 설치되어 있습니다.

#### 1. python venv로 가상환경 생성 및 활성화.
1. 가상환경을 만드는 명령어
```shell
python -m venv venv
```
2. 가상환경 활성화 
```shell
source venv/Scripts/activate
```

#### 2. 패키지 설치
```shell
pip install -r requirements.txt
```

#### 3. `manage.py` 가 있는 위치에서 모델 migration을 해줍니다.
```
python manage.py migrate
```
[참고]
- `python manage.py makemigrations` : 아직 데이터베이스에 적용되지 않음, 데이터베이스 스키마 변경사항을 기록하는 용
- `python manage.py migrate` : 위의 명령어에서 생성된 마이그레이션 파일들을 데이터베이스에 적용
(지금은 두번째 명령어만 작성하는게 맞습니다. 변경사항 없이 DB에 적용하기 위함이기 때문입니다.)

#### 4. `manage.py` 가 있는 위치에서 서버를 실행합니다.
```shell
python manage.py runserver 
```
- 필요에 따라 위의 명령어 뒤에 포트번호를 붙입니다.


### 초기 설정 : 데이터
- 더미 데이터는 아직 생성하지 않았습니다.
- 다음 주(~11/24)추후 생성해서 제공할 계획입니다.
<br>

## ER-Diagram

![erd_image](https://user-images.githubusercontent.com/120071955/284055771-8bbb3b65-afed-40b0-bd34-4fc0ee9e4963.png)


<br>

## API Documentation

![api_doc](https://user-images.githubusercontent.com/120071955/284062669-c2987ded-bca8-45e4-b54a-33f66713f7f2.png)

### 1. 회원가입 API
#### Request
```plain
  POST /api/auth/signup
```
- Auth Required: False

| Body Parameter | Type     | Description    |
| :------------- | :------- | :------------- |
| `username`     | `string` | **Required**.  |
| `password`     | `string` | **Required**.  |
```
EX)
{
    "username": "user1",
    "password": "devpassword1"
}
```

#### Response
```http
HTTP 201 Created
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "username": "user1"
}
```

### 2. JWT로그인 API

#### Request
```plain
  POST /api/auth/jwt-login
```
- Auth Required: False

| Body Parameter | Type     | Description    |
| :------------- | :------- | :------------- |
| `username`     | `string` | **Required**.  |
| `password`     | `string` | **Required**.  |

```
EX)
{
    "username": "user1",
    "password": "devpassword1"
}
```

#### Response
```http
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "username": "user1",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpVXCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk5NDM2NTA3LCJpYXQiOjE2OTk0MzI5MDcsImp0aSI6Ijc4Y2E1NzI3NDZkMDQzYzA4ZWZlNWM3NGNjMDFkNDNiIiwidXNlcl9pZCI6MX0.W-z5wAg0zNJWlaLA6mb0xEMPeEdOqenKeKrCsenWCNs"
}
```


### 3. 카테고리 목록 API

#### Request
```plain
  GET /api/budgets/
```
- Auth Required: True

#### Rquest Header

| Parameter       | Type     | Description                             |
| :-------------- | :------- | :-------------------------------------- |
| `Authorization` | `string` | **Required**. 'Bearer eyJhbGciOiJIU...' |
| `Content-Type`  | `string` | **Required**. `application/json`        |

#### Response
```JSON
{
    "message": "get categories",
    "data": [
        {
            "id": 1,
            "name": "undefined"
        },
        {
            "id": 2,
            "name": "쇼핑"
        },
        {
            "id": 3,
            "name": "교통"
        },
        {
            "id": 4,
            "name": "주거비"
        },
        {
            "id": 5,
            "name": "취미"
        },
        {
            "id": 6,
            "name": "교육"
        },
        {
            "id": 7,
            "name": "병원"
        },
        {
            "id": 8,
            "name": "식비"
        },
        {
            "id": 9,
            "name": "저축/투자"
        }
    ]
}
```


### 4. 예산설정 및 설계 - 예산설정 API: 예산생성

#### Request
```plain
  POST /api/budgets/
```
- Auth Required: True

#### Request Header
| Parameter       | Type     | Description                             |
| :-------------- | :------- | :-------------------------------------- |
| `Authorization` | `string` | **Required**. `Bearer eyJhbGciOiJIU...` |
| `Content-Type`  | `string` | **Required**. `application/json`        |


#### Body content
- 아래 항목으로 이루어진 dict를 원소로 가지는 list를 전달

| Body Parameter | Type     | Description                 |
| :------------- | :------- | :-------------------------- |
| `category`     | `integer` | **Required**.            |
| `amount`       | `integer` | **Required**.            |

- Body example
```json
{
    "budget_list": [
        {
            "category": 2,
            "amount": 30
        },
        {
            "category": 3,
            "amount": 50
        },
        {
            "category": 4,
            "amount": 20
        }
    ]
}
```

#### Response
```json
{
    "message": "budget create success!",
    "setup_user": 2,
    "setup_user_total": 100,
    "data": [
        10,
        11,
        12
    ]
}
```


### 5. 예산설정 및 설계 - 예산설정 API: 예산수정

1개의 레코드만 수정합니다.

#### Request
```plain text
  PATCH /api/budgets/
```
#### Request Header
| Parameter       | Type     | Description                             |
| :-------------- | :------- | :-------------------------------------- |
| `Authorization` | `string` | **Required**. `Bearer eyJhbGciOiJIU...` |
| `Content-Type`  | `string` | **Required**. `application/json`        |

#### Body content
- 아래 항목으로 이루어진 dict를 전달

| Body Parameter | Type      | Description                 |
| :------------- | :-------- | :-------------------------- |
| `category`     | `integer` | **Required**.            |
| `amount`       | `integer` | **Required**.            |

#### Body example
```json
{
    "category": 2,
    "amount": 30
}
```

#### Response
```json
{
    "message": "success!",
    "data": "Budget[1] - category쇼핑 is changed.(30)"
}
```

### 6. 예산설정 및 설계 - 추천 API:스타일 목룍

#### Request
```plain
  GET /api/budgets/rec/
```
- Auth Required: True

#### Request Header
| Parameter       | Type     | Description                             |
| :-------------- | :------- | :-------------------------------------- |
| `Authorization` | `string` | **Required**. `Bearer eyJhbGciOiJIU...` |
| `Content-Type`  | `string` | **Required**. `application/json`        |


#### Response
```json
{
    "message": "recommend styles",
    "data": [
        "식비위주",
        "쇼핑위주",
        "취미위주",
        "저축/투자위주"
    ]
}
```

### 7. 예산설정 및 설계 - 추천 API:예산생성

#### Request
```plain
  POST /api/budgets/rec/
```
- Auth Required: True

#### Request Header
| Parameter       | Type     | Description                             |
| :-------------- | :------- | :-------------------------------------- |
| `Authorization` | `string` | **Required**. `Bearer eyJhbGciOiJIU...` |
| `Content-Type`  | `string` | **Required**. `application/json`        |


#### Body content
- 아래 항목으로 이루어진 dict를 전달

| Body Parameter | Type      | Description                 |
| :------------- | :-------- | :-------------------------- |
| `total`        | `integer` | **Required**.            |
| `style`        | `string`  | **Required**.            |

- Body Example
```json
{
    "total": 1200000,
    "style": "식비위주"
}
```

#### Response
```json
{
    "message": "suceess!",
    "setup_user": 2,
    "setup_user_total": 1200000,
    "data": [
        41,
        42,
        43,
        44,
        45
    ]
}
```


### 8. 예산설정 및 설계 - 추천 API:예산수정
예산 수정 스타일 지정 변경이기 때문에 해당되지 않는 카테고리는 0으로 수정하고, 없었던 budget 카테고리 행은 생성합니다.

#### Request
```plain
  PATCH /api/budgets/rec/
```
- Auth Required: True

#### Request Header
| Parameter       | Type     | Description                             |
| :-------------- | :------- | :-------------------------------------- |
| `Authorization` | `string` | **Required**. `Bearer eyJhbGciOiJIU...` |
| `Content-Type`  | `string` | **Required**. `application/json`        |


#### Body content
- 아래 항목으로 이루어진 dict를 전달

| Body Parameter | Type      | Description                 |
| :------------- | :-------- | :-------------------------- |
| `total`        | `integer` | **Required**.            |
| `style`        | `string`  | **Required**.            |

- body example
```json
{
    "total": 1000000,
    "style": "쇼핑위주"
}
```

#### Response
```json
{
    "message": "style change success",
    "data": "쇼핑위주"
}
```


### 9. 지출 기록 - 지출 CRUD API:List조회
유저가 소비한 항목들에 대한 모든 정보와 전체/카테고리별 소비금액 정보를 반환

#### Request
```plain
  GET /api/expenditures/
```
- Auth Required: True

#### Rquest Header
| Parameter       | Type     | Description                             |
| :-------------- | :------- | :-------------------------------------- |
| `Authorization` | `string` | **Required**. `Bearer eyJhbGciOiJIU...` |
| `Content-Type`  | `string` | **Required**. `application/json`        |


#### Response
```json
{
    "message": "success!",
    "data": [
        {
            "id": 1,
            "amount": 22000,
            "appropriate_amount": 10000,
            "memo": "어디어디서 썼습니다",
            "is_exept": false,
            "created_at": "2023-11-15T09:39:37.523988",
            "updated_at": "2023-11-15T10:23:46.735049",
            "user": 2,
            "category": 3
        },
        {
            "id": 2,
            "amount": 25000,
            "appropriate_amount": 10000,
            "memo": "어디어sdfsdfsdf디서 썼습니다",
            "is_exept": false,
            "created_at": "2023-11-15T09:39:52.412771",
            "updated_at": "2023-11-15T09:39:52.412771",
            "user": 2,
            "category": 4
        },
        {
            "id": 3,
            "amount": 68000,
            "appropriate_amount": 10000,
            "memo": "간만에 뭘좀 샀는데 뭘샀을까?",
            "is_exept": false,
            "created_at": "2023-11-15T10:30:42.755083",
            "updated_at": "2023-11-15T10:30:42.755083",
            "user": 2,
            "category": 5
        },
        {
            "id": 4,
            "amount": 68000,
            "appropriate_amount": 10000,
            "memo": "간만에 뭘좀 샀는데 뭘샀을까?",
            "is_exept": false,
            "created_at": "2023-11-16T04:30:05.493767",
            "updated_at": "2023-11-16T04:30:05.494782",
            "user": 2,
            "category": 5
        },
        {
            "id": 5,
            "amount": 68000,
            "appropriate_amount": 10000,
            "memo": "간만에 뭘좀 샀는데 뭘샀을까?",
            "is_exept": false,
            "created_at": "2023-11-16T04:30:30.164717",
            "updated_at": "2023-11-16T04:30:30.165718",
            "user": 2,
            "category": 5
        },
        {
            "id": 6,
            "amount": 15000,
            "appropriate_amount": 10000,
            "memo": "호롤로",
            "is_exept": false,
            "created_at": "2023-11-16T06:01:07.085904",
            "updated_at": "2023-11-16T06:01:07.085904",
            "user": 2,
            "category": 2
        },
        {
            "id": 7,
            "amount": 27000,
            "appropriate_amount": 10000,
            "memo": "호롤로2",
            "is_exept": false,
            "created_at": "2023-11-16T06:01:18.473358",
            "updated_at": "2023-11-16T06:01:18.473358",
            "user": 2,
            "category": 2
        },
        {
            "id": 8,
            "amount": 33300,
            "appropriate_amount": 10000,
            "memo": "33호호호홓ㅎㅎ3332",
            "is_exept": false,
            "created_at": "2023-11-16T06:01:31.638764",
            "updated_at": "2023-11-16T06:01:31.638764",
            "user": 2,
            "category": 3
        },
        {
            "id": 9,
            "amount": 2300,
            "appropriate_amount": 10000,
            "memo": "기타소비1",
            "is_exept": false,
            "created_at": "2023-11-19T16:23:22.261079",
            "updated_at": "2023-11-19T16:23:22.261079",
            "user": 2,
            "category": 1
        },
        {
            "id": 10,
            "amount": 4400,
            "appropriate_amount": 10000,
            "memo": "오늘의소비 카테고리2",
            "is_exept": false,
            "created_at": "2023-11-19T16:23:40.198193",
            "updated_at": "2023-11-19T16:23:40.198193",
            "user": 2,
            "category": 2
        },
        {
            "id": 11,
            "amount": 12000,
            "appropriate_amount": 10000,
            "memo": "오늘의소비 카테고리2",
            "is_exept": false,
            "created_at": "2023-11-19T16:23:50.713640",
            "updated_at": "2023-11-19T16:23:50.713640",
            "user": 2,
            "category": 2
        },
        {
            "id": 12,
            "amount": 52000,
            "appropriate_amount": 10000,
            "memo": "오늘의소비 카테고리2",
            "is_exept": false,
            "created_at": "2023-11-19T16:23:55.347926",
            "updated_at": "2023-11-19T16:23:55.348941",
            "user": 2,
            "category": 2
        },
        {
            "id": 13,
            "amount": 24000,
            "appropriate_amount": 10000,
            "memo": "오늘의소비 카테고리3",
            "is_exept": false,
            "created_at": "2023-11-19T16:24:05.103259",
            "updated_at": "2023-11-19T16:24:05.104258",
            "user": 2,
            "category": 3
        },
        {
            "id": 14,
            "amount": 28900,
            "appropriate_amount": 10000,
            "memo": "오늘의소비 카테고리5",
            "is_exept": false,
            "created_at": "2023-11-19T16:24:23.814410",
            "updated_at": "2023-11-19T16:24:23.814410",
            "user": 2,
            "category": 5
        },
        {
            "id": 15,
            "amount": 37580,
            "appropriate_amount": 10000,
            "memo": "오늘의소비 카테고리5",
            "is_exept": false,
            "created_at": "2023-11-19T16:24:34.861078",
            "updated_at": "2023-11-19T16:24:34.861078",
            "user": 2,
            "category": 7
        },
        {
            "id": 16,
            "amount": 4600,
            "appropriate_amount": 10000,
            "memo": "오늘의소비 카테고리5",
            "is_exept": false,
            "created_at": "2023-11-19T16:24:44.307684",
            "updated_at": "2023-11-19T16:24:44.307684",
            "user": 2,
            "category": 5
        }
    ],
    "static_data": {
        "category_group": [
            {
                "undefined": {
                    "count": 1,
                    "sum": 2300
                }
            },
            {
                "쇼핑": {
                    "count": 5,
                    "sum": 110400
                }
            },
            {
                "교통": {
                    "count": 3,
                    "sum": 79300
                }
            },
            {
                "주거비": {
                    "count": 1,
                    "sum": 25000
                }
            },
            {
                "취미": {
                    "count": 5,
                    "sum": 237500
                }
            },
            {
                "교육": {
                    "count": 0,
                    "sum": 0
                }
            },
            {
                "병원": {
                    "count": 1,
                    "sum": 37580
                }
            },
            {
                "식비": {
                    "count": 0,
                    "sum": 0
                }
            },
            {
                "저축/투자": {
                    "count": 0,
                    "sum": 0
                }
            }
        ],
        "total_sum": 492080
    }
}
```

### 10. 지출 기록 - 지출 CRUD API:생성

#### Request
```plain
  POST /api/expenditures/
```
- Auth Required: True

#### Rquest Header
| Parameter       | Type     | Description                             |
| :-------------- | :------- | :-------------------------------------- |
| `Authorization` | `string` | **Required**. `Bearer eyJhbGciOiJIU...` |
| `Content-Type`  | `string` | **Required**. `application/json`        |


#### Request Body
| Body Parameter | Type      | Description                   |
| :------------- | :-------- | :---------------------------- |
| `category`     | `integer` | **Required**.                 |
| `amount`       | `integer` | **Required**.                 |
| `memo`         | `string`  | **Required**.                 |

- body example
```json
{
    "category": 3,
    "amount": 200,
    "memo": "카테고리덧ㄷ러ㅣㄴ소비소빗"
}
```

#### Response
```json
{
    "message": "success!",
    "data": {
        "category": 3,
        "amount": 200,
        "memo": "카테고리덧ㄷ러ㅣㄴ소비소빗",
        "user": 2,
        "appropriate_amount": 10000
    }
}
```

### 11. 지출 기록 - 지출 CRUD API:조회 상세보기
1개 지출에 대한 모든 내용을 확인하는 API

#### Request
```plain
  GET /api/expenditures/<int:expenditure_id>/
  GET /api/expenditures/15/
```
- Auth Required: True

#### Rquest Header
| Parameter       | Type     | Description                             |
| :-------------- | :------- | :-------------------------------------- |
| `Authorization` | `string` | **Required**. `Bearer eyJhbGciOiJIU...` |
| `Content-Type`  | `string` | **Required**. `application/json`        |

#### Response
```json
{
    "message": "get sucess!",
    "data": {
        "id": 15,
        "amount": 37580,
        "appropriate_amount": 10000,
        "memo": "오늘의소비 카테고리5",
        "is_exept": false,
        "created_at": "2023-11-19T16:24:34.861078",
        "updated_at": "2023-11-19T16:24:34.861078",
        "user": 2,
        "category": 7
    }
}
```

### 11. 지출 기록 - 지출 CRUD API:수정
#### Request
```plain
  PATCH /api/expenditures/<int:expenditure_id>/
  GET /api/expenditures/15/
```
- Auth Required: True

#### Rquest Header
| Parameter       | Type     | Description                             |
| :-------------- | :------- | :-------------------------------------- |
| `Authorization` | `string` | **Required**. `Bearer eyJhbGciOiJIU...` |
| `Content-Type`  | `string` | **Required**. `application/json`        |


#### Request Body
| Body Parameter | Type      | Description                   |
| :------------- | :-------- | :---------------------------- |
| `category`     | `integer` | **Required**.                 |
| `amount`       | `integer` | **Required**.                 |
| `memo`         | `string`  | **Required**.                 |

- body example
```json
{
    "category": 3,
    "amount": 22000,
    "memo": "어디어디서 썼습니다",
    "appropriate_amount": 10000,
    "is_exept": false
}
```

#### Response
```json
{
    "message": "update sucess!"
}
```

### 12. 지출 기록 - 지출 CRUD API:삭제

#### Request
```plain
  DELETE /api/expenditures/<int:expenditure_id>/
  DELETE /api/expenditures/15/
```
- Auth Required: True

#### Rquest Header
| Parameter       | Type     | Description                             |
| :-------------- | :------- | :-------------------------------------- |
| `Authorization` | `string` | **Required**. `Bearer eyJhbGciOiJIU...` |
| `Content-Type`  | `string` | **Required**. `application/json`        |

#### Response
```json
{
    "message": "delete sucess!",
    "data": {
        "id": 15,
        "amount": 22000,
        "appropriate_amount": 10000,
        "memo": "어디어디서 썼습니다",
        "is_exept": false,
        "created_at": "2023-11-19T16:24:34.861078",
        "updated_at": "2023-11-19T23:38:12.157585",
        "user": 2,
        "category": 3
    }
}
```

### 13. 지출 컨설팅 - 오늘 지출 추천 API
이번 달 지출과 예산 내용을 조합해서 오늘 지출 내용을 추천해줍니다.

#### Request
```plain
  GET /api/expenditures/rec/
```
- Auth Required: True

#### Rquest Header
| Parameter       | Type     | Description                             |
| :-------------- | :------- | :-------------------------------------- |
| `Authorization` | `string` | **Required**. `Bearer eyJhbGciOiJIU...` |
| `Content-Type`  | `string` | **Required**. `application/json`        |

#### Response
```json
{
    "message": "today(2023-11-19)'s message: you have to save your money!",
    "data": {
        "today_recommand": 168530,
        "period": "2023-11-01 00:00:00 ~ 2023-11-19 00:00:00",
        "쇼핑": 25600,
        "교통": 3700,
        "주거비": 14500,
        "취미": 3330,
        "식비": 20800,
        "저축/투자": 0
    }
}
```

### 14. 지출 컨설팅 - 오늘 지출 안내 API
소비 내용에 대한 비율과 카테고리별 소비 비용을 알려줍니다.
예산에 없는 범위에 소비 내용이 있을 경우 -1로 처리했습니다.

```plain
  GET /api/expenditures/noti/
```
- Auth Required: True

#### Rquest Header
| Parameter       | Type     | Description                             |
| :-------------- | :------- | :-------------------------------------- |
| `Authorization` | `string` | **Required**. `Bearer eyJhbGciOiJIU...` |
| `Content-Type`  | `string` | **Required**. `application/json`        |

#### Response
```json
{
    "message": "success!",
    "data": {
        "total": 76,
        "undefined": -1,
        "쇼핑": 267,
        "교통": 654,
        "주거비": 0,
        "취미": 1006,
        "교육": -1,
        "병원": -1,
        "식비": 0,
        "저축/투자": -1,
        "unit": "percent"
    },
    "recommend_data": {
        "today_recommand": 168530,
        "period": "2023-11-01 00:00:00 ~ 2023-11-19 00:00:00",
        "쇼핑": 25600,
        "교통": 3700,
        "주거비": 14500,
        "취미": 3330,
        "식비": 20800,
        "저축/투자": 0
    }
}
```

## Scheduler 기능
- `APScheduler`를 사용해서 지출알림과 지출추천 기능을 주기적으로 실행하도록 기능 추가 예정(~11/24)


## 프로젝트 진행 및 이슈 관리
- [깃헙_이슈_click](https://github.com/I-deul-of-zoo/jinsoo-budget-management/issues) 으로 등록해서 관리했습니다.

<br>

## 구현과정(설계 및 의도)

1. RESTful API 설계
    - 리소스 간 계층 구조를 나타내는 URI로 구현했습니다.
    - 각 API의 Response에 맞는 HTTP status code를 적절하게 사용하였고, 발생할 수 있는 에러 상황에 대한 예외처리를 진행하였습니다.

2. 모델링
    - 예산이나 지출 관련하여 `시작 기준일`과 `총예산`은 지속적으로 확인해야 하고 고정적인 값이기 때문에 `User` 모델에 필드를 추가하여 확인하도록 결정했습니다.
    - 추가적으로 추천 예산에 대해서는 테이블을 하나 추가로 추가하여 매일 자정이 지나면 자동으로 수정하는 기능을 추가하는 것도 좋은 방법으로 생각됩니다. 이 방법으로 개선할 경우, 함수로 모듈화를 진행한 부분을 스케쥴러 부분으로 옮겨지고, 계산 대신 DB에서 조회해오면 되기 때문에 views의 코드가 매우 가독성 높아집니다.

3. 서비스 사용자 관점에서
    - 서비스 사용자 관점에서 다른 유저들의 소비 형태보다 나에게 맞는 비율을 추천해주는 것이 훨씬 편리하다고 생각했습니다.
    - 왜냐하면 사람마다 스타일이 매우 다르기 때문에 평균을 내어 추천하는 것이 의미가 크지 않다고 생각했습니다.
    - 또한, 내 소비 스타일(쇼핑, 저축 등)만 고르면 바로 편리하게 설정이 되고, 나머지는 예산 생성/수정 기능을 활용하는 방식이 좋다고 생각했습니다.

4. Scheduler 설계
    - 주기적인 실행이 필요한 지출 추천 및 지출 알림 기능을 구현 위해 APscheduler를 사용하고자 하였습니다.
    - APScheduler만 적용한 상태이고 아직 연동 및 테스트 전입니다.


<br>

## Authors

|이름|github주소|
|---|---------|
|유진수|https://github.com/YuJinsoo|
