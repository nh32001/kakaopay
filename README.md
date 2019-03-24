# 사전과제

주택 금융 서비스 API 개발

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

### test source code
First, clone this project.  
Then go to the project folder and create a user environment and  
run build script.

```shell
$ virtualenv -p python3 venv  # Create a virtual environment.
$ source venv/bin/activate    # Enter the virtual environment.
(venv)$ ./test.sh            # run pytest script
```

#### Run backend server
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
