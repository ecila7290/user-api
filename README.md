# User API

회원가입, 로그인, 비밀번호 재설정이 가능한 User API입니다.

## Prerequisites

- Python 3.9 - pyenv & virtualenv / venv등의 가상환경에서 실행할 것을 권장합니다.
- SQLite - Local에서 실행할 때 사용하게 될 DB입니다.

## Tech Stack

- Framework - [FastAPI](https://fastapi.tiangolo.com/)
- Formatter - [Black](https://github.com/psf/black)

## Start Guide

- 이 repository를 클론하거나 zip 파일을 다운받아 압축을 풀어 사용합니다.

- 개발 환경 세팅

  ```
  $ make init
  ```

- 로컬 서버 실행

  ```
  $ make run
  ```

- Unit test

  ```
  $ make test
  ```

- DB Schema 변경사항 기록(필요한 경우에만)

  ```
  $ make revision msg="Update Users example"
  ```

- DB Schema 변경사항 적용(필요한 경우에만)
  ```
  $ make migrate
  ```

## API Documentation

FastAPI에서 기본적으로 제공하는 Swagger를 사용합니다.

`$ make run`으로 서버 실행 후 http://localhost:8000/api/v1/docs 에서 API의 상세 정보를 확인하고 테스트도 할 수 있습니다.

## Usage Guide

사용자 인증, 인가와 관련된 내용이 있어 특정 단계를 수행하지 않고서는 진행이 불가능한 경우가 있습니다.

이하 API에서는 반드시 기술된 과정을 거쳐서 실행해 주시기 바랍니다.

### /api/v1/users/signup

회원가입을 위해 인증번호가 필요하므로 먼저 `/api/v1/users/verification`를 호출합니다.

```bash
# 호출 예시
$ curl -XPOST -H "Content-type: application/json" -d '{
  "phone": "+821012345678",
  "request_path": "signup"
}' 'http://localhost:8000/api/v1/users/verification'
```

```json
// 응답 예시
{
  "phone": "+821012345678",
  "id": "ed1cd4fb-2635-4156-b3f3-9462e9fd9e2f",
  "code": "208771",
  "created_at": "2022-09-05T06:46:35.010682+00:00"
}
```

응답에서 나온 phone과 code 값을 회원가입 API의 request body에 넣어줍니다.

### /api/v1/users/signin

`/users/signup`에서 회원가입을 한 후에 진행이 가능합니다.

### /api/v1/users/mypage

`/users/signin`에서 로그인 후 발행되는 access token을 Authorization header 넣어주어야 합니다.

### /api/v1/users/passwordReset

`/users/signup`에서 회원가입을 한 후에 진행이 가능합니다.
비밀번호 재설정을 위해 인증번호가 필요하므로 회원가입과 동일하게 `/api/v1/users/verification`를 호출합니다.

응답에서 나온 phone과 code 값을 API의 request body에 넣어줍니다.

## 기능 요구사항 중 최종 구현된 범위

- [x] 회원 가입 기능

  - [x] 전화번호 인증 후 가입 가능

- [x] 로그인 기능

  - [x] 식별 가능한 모든 정보로 로그인 가능
  - [x] 닉네임, 이메일과 비밀번호를 사용해 로그인 가능

- [x] 내 정보 보기 기능

- [x] 비밀번호 찾기(재설정) 기능

  - [x] 로그인되어 있지 않은 상태에서 비밀번호 재설정 가능
  - [x] 전화번호 인증 후 재설정 가능
