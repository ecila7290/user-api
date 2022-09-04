from datetime import timedelta

from fastapi import status
from fastapi.testclient import TestClient
from jose import jwt

from app.common.config import settings
from app.common.utils.datetime_helper import utcnow
from app.common.utils.password_helper import hash_password
from app.common.utils.uuid import uuid4
from app.users.entities.schemas.verification import RequestPath
from app.users.entities.models.user import User
from app.users.entities.models.verification import Verification
from app.users.repositories.user_repository import UserRepository
from app.users.repositories.verification_repository import VerificationRepository


class TestUserCRUD:
    def test_user_create(self, client: TestClient, monkeypatch):
        # GIVEN monkeypatch verification code
        GET_VERIFICATION_DATA = [
            Verification(phone="+821012345678", request_path=RequestPath.SIGNUP, code="123456", created_at=utcnow()),
            Verification(phone="+821012345678", request_path=RequestPath.SIGNUP, code="123456", created_at=utcnow()),
            Verification(phone="+821012345678", request_path=RequestPath.SIGNUP, code="987654", created_at=utcnow()),
            Verification(
                phone="+821012345678", request_path=RequestPath.SIGNUP, code="123456", created_at=utcnow() - timedelta(days=1)
            ),
        ]

        class MockVerificationRepository(VerificationRepository):
            def query(self, **kwargs):
                return [GET_VERIFICATION_DATA.pop(0)]

        monkeypatch.setattr("app.users.routers.user.VerificationRepository", MockVerificationRepository)

        # GIVEN
        user_data = {
            "name": "testname",
            "email": "test@example.com",
            "phone": "+821012345678",
            "nickname": "testnick",
            "password": "secret",
            "verification_code": "123456",
        }

        # WHEN
        response = client.post(f"/signup", json=user_data)
        created_entity = response.json()

        # THEN
        assert response.status_code == 201
        assert created_entity.get("verification_code") is None
        assert created_entity.get("password") is None
        assert created_entity["is_active"] is True

        # GIVEN
        duplicated_user_data = {
            "name": "testname",
            "email": "test@example.com",
            "phone": "+821012345678",
            "nickname": "testnick",
            "password": "secret",
            "verification_code": "123456",
        }

        # WHEN 이미 존재하는 사용자인 경우
        response = client.post(f"/signup", json=duplicated_user_data)

        # THEN
        assert response.status_code == status.HTTP_409_CONFLICT

        # GIVEN
        wrong_code_user_data = {
            "name": "testname",
            "email": "test@example.com",
            "phone": "+821012345678",
            "nickname": "testnick",
            "password": "secret",
            "verification_code": "123456",
        }

        # WHEN 인증번호를 틀린 경우
        response = client.post(f"/signup", json=wrong_code_user_data)

        # THEN
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Incorrect verification code" in response.json()["detail"]

        # GIVEN
        expired_code_user_data = {
            "name": "testname",
            "email": "test@example.com",
            "phone": "+821012345678",
            "nickname": "testnick",
            "password": "secret",
            "verification_code": "123456",
        }

        # WHEN 인증번호가 만료된 경우
        response = client.post(f"/signup", json=expired_code_user_data)

        # THEN
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Code Expired" in response.json()["detail"]

    def test_user_signin(self, client: TestClient, monkeypatch):
        # GIVEN monkeypatch user data
        GET_USER_DATA = [
            [User(id=uuid4(), email="user1@email.com", nickname="user1", password=hash_password("secret"))],
            [User(id=uuid4(), email="user3@email.com", nickname="user2", password=hash_password("secret"))],
            [],
        ]

        class MockUserRepository(UserRepository):
            def query(self, **kwargs):
                return GET_USER_DATA.pop(0)

        monkeypatch.setattr("app.users.routers.user.UserRepository", MockUserRepository)

        # GIVEN
        user1_info = {"email": "user@test.com", "password": "secret"}

        # WHEN
        response = client.post(f"/signin", json=user1_info)

        # THEN
        response.status_code == status.HTTP_200_OK
        jwt.decode(response.json()["access_token"], settings.SECRET_KEY, algorithms=settings.ALGORITHM)[
            "email"
        ] == "user1@email.com"

        # GIVEN
        user2_info = {"password": "secret"}

        # WHEN email && nickname 둘 다 없는 경우
        response = client.post(f"/signin", json=user2_info)

        # THEN
        response.status_code == status.HTTP_400_BAD_REQUEST
        response.json()["detail"] == "Email or nickname required"

        # GIVEN
        user3_info = {"email": "user3@test.com", "password": "wrong-password"}

        # WHEN 비밀번호가 틀린 경우
        response = client.post(f"/signin", json=user3_info)

        # THEN
        response.status_code == status.HTTP_401_UNAUTHORIZED
        response.json()["detail"] == "Incorrect id or password"

        # GIVEN
        user4_info = {"email": "non-exsiting-user@test.com", "password": "secret"}

        # WHEN 존재하지 않는 사용자
        response = client.post(f"/signin", json=user4_info)

        # THEN
        response.status_code == status.HTTP_401_UNAUTHORIZED
        response.json()["detail"] == "Incorrect id or password"
