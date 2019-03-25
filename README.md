# 사전과제

주택 금융 서비스 API 개발

## Requirement
### API 기능 명세에 나온 API 를 개발하세요.
• JPA(Hibernate)를 사용하여 각 엔티티를 정의하고 레퍼지토리를 개발하세요.  
• 단, 엔티티 디자인은 지원자의 문제해결 방법에 따라 자유롭게 합니다.  
• 단, 주택금융 공급기관은 독립 엔티티(기관명과 기관코드)로 디자인합니다. {“institute_name”, “institute_code”}  
• 단위 테스트 (Unit Test) 코드를 개발하여 각 기능을 검증하세요.  
• 모든 입/출력은 JSON 형태로 주고 받습니다.  
• README.md 파일을 추가하여, 개발 프레임워크, 문제해결 전략, 빌드 및 실행 방법을 기술하세요.  
• 단, 프로그램 언어는 평가에 반영되지 않으니 자유롭게 선택하세요.  
• 단, 각 API 의 HTTP Method 들( GET | POST | PUT | DEL )은 알아서 선택하세요.  

### 추가 제약사항(옵션):
• API 인증을 위해 JWT(Json Web Token)를 이용해서 Token 기반 API 인증 기능을 개 발하고 
각 API 호출 시에 HTTP Header 에 발급받은 토큰을 가지고 호출하세요.  
• signup 계정 생성 API: 입력으로 ID, PW 받아 내부 DB 에 계정 저장하고 토큰 생성하여 출력  
• 단, 패스워드는 인코딩하여 저장한다.  
• 단, 토큰은 특정 secret 으로 서명하여 생성한다.  
• signin 로그인 API: 입력으로 생성된 계정 (ID, PW)으로 로그인 요청하면 토큰을 발급한다.  
• refresh 토큰 재발급 API: 기존에 발급받은 토큰을 Authorization 헤더에 “Bearer Token”으로 입력 요청을 하면 토큰을 재발급한다.

## 문제 해결
DB는 Institude Table과 Bank Table 두가지로 디자인  
전체 프레임워크는 async모듈을 사용하여 비동기 호출  

해당 파일이 enc-kr인코딩이라 utf-8로 변환후에 진행을 하려고 했으나, 당장은 원본 인코딩으로 진행  
csv파일로드는 csv라이브러리 사용. path따로 입력받지 않고 builtin파일을 로드하게 설계 (cli는 최대한 간단하게)  

백앤드관련 작업을 처음하는것이라 우선 구현자체를 목표로 진행.  
orm사용은 우선 sql문을 만들고 컨버팅하는 방식으로 진행  
비밀번호는 당장 원본으로 바로 저장(디버깅)  
로직이 어렵다는 느낌보다는 기반 구현 자체가 어려운 과제였다.  
선택옵션이 정말 알고리즘적으로 접근해야 할듯 보이나, 
이번 기한에서 그것까지 도전하기에는 시간이 부족하다고 판단하여 진행 종료

## Getting Started

### Prerequisites
- Python  
    + Make Virtual Env for Python 3.6.5+
    + check your python version
        ```shell
        $ python3 -V
        ```

### Building source code
First, clone this project.  
Then go to the project folder and create a user environment and  
run build script.

```shell
$ virtualenv -p python3 venv  # Create a virtual environment.
$ source venv/bin/activate    # Enter the virtual environment.
(venv)$ ./build.sh            # run build script
(venv)$ ls dist/              # check result wheel file
kakakopay-x.x.x-py3-none-any.whl
```

### Test source code
First, clone this project.  
Then go to the project folder and create a user environment and  
run build script.

```shell
$ virtualenv -p python3 venv  # Create a virtual environment.
$ source venv/bin/activate    # Enter the virtual environment.
(venv)$ ./test.sh            # run pytest script
```

### Run backend server
``` bash
(venv)$ pip install dist/kakakopay-x.x.x-py3-none-any.whl
(venv)$ kakaopay start
2. Run Application
URL : http://localhost:8000/
```

### Dependencies
sqlalchemy - orm  
sanic - async server  
sanic -restful - restful api  
pyjwt - jwt  
pytest - test  
pytest-sanic - test  
pytest-ordering - test  


## API Specifications

- data type : JSON 

| 구분    | 내용             | 비고                             |
| :------ | :--------------- | :------------------------------- |
| code    | 응답코드         | 200, 400, 500 등                 |
| message | 메시지           | 성공 : success, 실패 : 실패 사유 |
| data    | 요청에 대한 내용 |                                  |

### API LIST

#### signup 계정 생성 API

> URL : http://127.0.0.1:8000/signup
>
> Method : POST  
> Params : {"id": "kakao", "pw": "1234"}  
> Response : {"token": "ey............"}

#### signin 로그인 API

> URL : http://127.0.0.1:8000/signin
>
> Method : PUT  
> Params : {"id": "kakao", "pw": "1234"}  
> Response : {"token": "ey............"}

#### refresh 토큰 재발급 API

> URL : http://127.0.0.1:8000/refreshtoken
>
> Method : PUT  
> Header : {"Authorization": "bearer" "old_token"}  
> Response : {"token": "ey............"}

#### 데이터 파일에서 각 레코드를 데이터베이스에 저장하는 API 개발

> URL : http://127.0.0.1:8000/api1
>
> Method : POST  
> Header : {"Authorization": "basic" "token"}  
> Response : {"msg":  "init db}

#### 주택 금융 공급 금융기관(은행) 목록을 출력하는 API 를 개발하세요.

> URL : http://127.0.0.1:8000/api2
>
> Method : GET  
> Header : {"Authorization": "basic" "token"}  
> Response : {"bank":  [...]}

#### 연도별 각 금융기관의 지원금액 합계를 출력하는 API 를 개발하세요.


> URL : http://127.0.0.1:8000/api3
>
> Method : GET  
> Header : {"Authorization": "basic" "token"}  
> Response : {"name": "주택금융 공급현황", "content": [{...}, ..., {...}]}

#### 각 연도별 각 기관의 전체 지원금액 중에서 가장 큰 금액의 기관명을 출력하는 API 개발

> URL : http://127.0.0.1:8000/api4
>
> Method : GET  
> Header : {"Authorization": "basic" "token"}  
> Response : {"bank": "xxxxx", "year": 0000}

#### 전체 년도에서 외환은행의 지원금액 평균 중에서 가장 작은 금액과 큰 금액을 출력하는 API 개발

> URL : http://127.0.0.1:8000/api5
>
> Method : GET  
> Header : {"Authorization": "basic" "token"}  
> Response : {"bank": "외환은행", "support_amount": [{...}, {...}]}
