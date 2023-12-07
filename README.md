![logo](https://github.com/ssu-uky/LSH_WikiPage/assets/101565486/a74c3503-8274-4ce5-8dfc-765acbed7daa)

<br>

## Table of Contents
- [개요](#개요)
- [요구사항](#요구사항)
- [Skills](#skills)
- [Installation](#installation)
- [Dummy Data](#dummy-data)
- [Test Code](#test-code)
- [API Reference](#api-reference)

<br>
<br>


## 개요
강의와 관련된 정보에 대한 게시판을 만들고 게시글을 작성한다. <br>
게시글은 admin만 작성, 수정, 삭제가 가능하며,
게시글이 생성되면 연관된 게시글과 연결한다.

<br>

## 요구사항
- 전체게시글 중에 60%이상에서 발견되는 단어는 연관 게시글을 파악할때 제외합니다.
- 연관게시글이 되는 기준은 전체 게시글에 존재하는 단어를 기준으로 40% 이하 빈도 단어가 두개 이상 동시에 나타나는 것입니다.
- 연관게시글에서 위에서 계산한 40% 이하 빈도로 나타나는 단어중 더 빈번하게 나타날수록 연관이 더 있는것으로 파악하고, 연관도가 높은 순서대로 연관게시글을 보여줍니다.
- 연관게시글이 보여지는 순서는 연관도가 높은것을 우선적으로 보여줍니다.
- 게시글을 작성하고, 목록을 보여주고, 내용을 보여주는 프로그램을 만들어주시고, 게시글내용과 연관 게시글을 같이 표시해주세요.

<br>

## Skills
<img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=Python&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/SQLite-003B57?style=flat&logo=SQLite&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Pytest-0A9EDC?style=flat&logo=SQLite&logoColor=white"/>

<br>

## Installation
가상환경 진입 후, 패키지 다운로드

```
python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

root 폴더에 `.env` 파일 추가

https://djecrety.ir/ 에서 SECRET_KEY 생성 후 
.env/SECRET_KEY 에 복사

```py
SECRET_KEY="secret-key"
```

<br>

## Dummy Data
더미데이터 생성하기 (default : 50개 생성)

```py
python manage.py seed_board
```

<br>

## Test Code

```
pytest
```

<details>

<summary> Test Code - click </summary>

#### user test
```
pytest users/tests.py
```

#### board test
```
pytest boards/tests.py
```

</details>

<br>

## API Reference

<details>
<summary> Boards - click </summary>

#### Request

`POST` - 게시글 작성 <br>
http://127.0.0.1:8000/api/v1/boards/post/

`IsAdminUser`

```py
{
  "title":" Python 가장 쉬운 강의",
  "content":"이보다 쉬운 강의는 없었다! 누구나 쉽게 이해 가능한 Python , HTML , CSS "
}
```

#### Response

```py
HTTP 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "message": "게시글 작성 완료",
    "data": {
        "id": 158,
        "title": "Python 가장 쉬운 강의",
        "content": "이보다 쉬운 강의는 없었다! 누구나 쉽게 이해 가능한 Python , HTML , CSS"
    }
}

```

<br><br>

---

#### Request

`GET` - 게시글 목록 조회 <br>
http://127.0.0.1:8000/api/v1/boards/list/?page=3
<br>

> pagination 적용 / 한 페이지에 10개씩 <br>
> http://127.0.0.1:8000/api/v1/boards/list/?page="숫자"


#### Response

```py
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "count": 158, # 게시물 총 갯수
    "results": [
        {
            "id": 158,
            "title": "Python 가장 쉬운 강의",
            "created_at": "2023-12-07"
        },
        {
            "id": 157,
            "title": "Python 공부",
            "created_at": "2023-12-07"
        },
        {
            "id": 127,
            "title": "Spring 강의",
            "created_at": "2023-12-05"
        },
        {
            "id": 126,
            "title": "React 강의",
            "created_at": "2023-12-04"
        },
        {
            "id": 125,
            "title": "Vue 강의",
            "created_at": "2023-12-04"
        },
        {
            "id": 124,
            "title": "C 강의",
            "created_at": "2023-11-30"
        },
        {
            "id": 123,
            "title": "React 강의",
            "created_at": "2023-11-28"
        },
        {
            "id": 122,
            "title": "Spring 강의",
            "created_at": "2023-11-26"
        },
        {
            "id": 121,
            "title": "C++ 강의",
            "created_at": "2023-11-24"
        },
        {
            "id": 120,
            "title": "Vue 강의",
            "created_at": "2023-11-24"
        }
    ]
}
```

---

#### Request

`GET` , `PUT` , `DELETE` - 게시글 상세조회 (연관게시물 포함), 수정, 삭제 
<br>
`GET` : `AllowAny` <br>
`PUT`, `DELETE` : `IsAdminUser`
<br>

http://127.0.0.1:8000/api/v1/boards/9/ <br>
> http://127.0.0.1:8000/api/v1/boards/<int:board_id>/


```py
{
    "id": 9, # 조회 한 게시판 번호
    "title": "CSS 강의",
    "content": "안녕하세요. 오늘의 강의는 없습니다. React 에 대해 자세히 배워봅시다. Labore aliquid nulla laborum iure ea. Vue 는 매우 중요한 주제입니다. Java 을 기억하세요. Java 도 잊지마세요.",
    "related_boards_count": 18, # 연관 게시물 총 갯수
    "related_board" = [ ~~~ ],
    "created_at": "2023-01-13 08:02:32",
    "updated_at": "2023-12-07 23:39:45"
}
```

#### Response

```py
HTTP 200 OK
Allow: GET, PUT, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 9,
    "title": "CSS 강의",
    "content": "안녕하세요. 오늘은 C++ , React 에 대해 자세히 배워봅시다. Labore aliquid nulla laborum iure ea. Vue 는 매우 중요한 주제입니다. Java 을 기억하세요. Java 도 잊지마세요.",
    "related_boards_count": 30, # 연관 게시물 갯수
    "related_board": [
        {
            "id": 18,
            "title": "C++ 강의",
            "content": "안녕하세요. 오늘의 강의는 C++ 입니다. C++ 에 대해 자세히 배워봅시다. Ad occaecati ratione quasi quia. CSS 는 매우 중요한 주제입니다. Vue 을 기억하세요. Vue 도 잊지마세요.",
            "total_count": 4, # 연관된 단어의 총 갯수
            "word_counts": {
                "Vue": 2, # 연관 된 단어 각자 갯수
                "C++": 2 # 연관 된 단어 각자 갯수
            }
        },
        {
            "id": 130,
            "title": "Java 강의",
            "content": "안녕하세요. 오늘의 강의는 Java 입니다. JavaScript 에 대해 자세히 배워봅시다. Doloribus placeat praesentium sint. C++ 는 매우 중요한 주제입니다. Java 을 기억하세요. C++ 도 잊지마세요.",
            "total_count": 4,
            "word_counts": {
                "Java": 2,
                "C++": 2
            }
        },
        {
            "id": 26,
            "title": "C++ 강의",
            "content": "안녕하세요. 오늘의 강의는 C++ 입니다. Vue 에 대해 자세히 배워봅시다. Perferendis dicta maiores vero tempora corporis. C++ 는 매우 중요한 주제입니다. HTML 을 기억하세요. C++ 도 잊지마세요.",
            "total_count": 3,
            "word_counts": {
                "C++": 3
            }
        },
        {
            "id": 109,
            "title": "CSS 강의",
            "content": "안녕하세요. 오늘의 강의는 CSS 입니다. Java 에 대해 자세히 배워봅시다. Dolore odit aliquid vero nihil maxime omnis. Java 는 매우 중요한 주제입니다. Django 을 기억하세요. Java 도 잊지마세요.",
            "total_count": 3,
            "word_counts": {
                "Java": 3
            }
        },
        ...
        ],
    "created_at": "2023-01-13 08:02:32",
    "updated_at": "2023-12-07 23:39:45"
}
```
</details>

<details>

<summary> Users - click </summary>

#### Request

`POST` - 회원가입 <br>
http://127.0.0.1:8000/api/v1/users/signup/

```py
{
    "username":"happy",
    "name":"happy",
    "password":"qpqp1010"
}
```

#### Response
```py
{
    "user_pk": "87bf0407-6114-400c-8fe7-3e0fe7d568b4",
    "name": "happy",
    "username": "happy",
    "message": "happy님, 회원가입이 완료되었습니다."
}
```

---

#### Request

`POST` - 로그인 <br>
http://127.0.0.1:8000/api/v1/users/login/

```py
{
  "username":"happy",
  "password":"qpqp1010"
}
```

#### Response
```py
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "message": "happy님, 로그인 되었습니다."
}
```

---

#### Request

`POST` - 로그아웃 <br>
http://127.0.0.1:8000/api/v1/users/logout/


#### Response

```py
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "message": "로그아웃 되었습니다."
}
```

</details>

<br>
