from datetime import timedelta

from fastapi import status
from fastapi.testclient import TestClient

from app.common.utils.datetime_helper import utcnow
from app.users.entities.schemas.verification import RequestPath
from app.users.entities.models.verification import Verification
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

        # WHEN
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

        # WHEN
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

        # WHEN
        response = client.post(f"/signup", json=expired_code_user_data)

        # THEN
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Code Expired" in response.json()["detail"]
