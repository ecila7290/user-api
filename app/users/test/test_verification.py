from fastapi import status
from fastapi.testclient import TestClient

from app.users.entities.schemas.verification import RequestPath


class TestVerificationCRUD:
    def test_user_verification(self, client: TestClient):
        # GIVEN
        verification_data = {"phone": "+821012345678", "request_path": RequestPath.SIGNUP}

        # WHEN
        response = client.post(f"/verification", json=verification_data)
        created_entity = response.json()

        # THEN
        assert len(created_entity["code"]) == 6

        # GIVEN
        invalid_verification_data = {"phone": "01012345678", "request_path": RequestPath.SIGNUP}

        # WHEN
        response = client.post(f"/verification", json=invalid_verification_data)

        # THEN
        assert response.status_code == status.HTTP_400_BAD_REQUEST
