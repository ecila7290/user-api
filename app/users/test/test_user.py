import pytest
from fastapi import status
from fastapi.testclient import TestClient


class TestUserCRUD:
    def test_user_create_success(self, client: TestClient):
        # GIVEN
        user_data = {
            "name": "testname",
            "email": "test@example.com",
            "phone": "01012345678",
            "nickname": "testnick",
            "password": "secret",
            "verification_code": "1234",
        }

        # WHEN
        response = client.post(f"/signup", json=user_data)
        created_entity = response.json()

        # THEN
        assert response.status_code == 201
        assert created_entity.get("verification_code") is None
        assert created_entity["is_active"] is True
        assert created_entity["password"] != "secret"

        # GIVEN
        duplicated_user_data = {
            "name": "testname",
            "email": "test@example.com",
            "phone": "01012345678",
            "nickname": "testnick",
            "password": "secret",
            "verification_code": "1234",
        }

        # WHEN
        response = client.post(f"/signup", json=duplicated_user_data)

        # THEN
        assert response.status_code == status.HTTP_409_CONFLICT
