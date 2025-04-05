from httpx import AsyncClient
import pytest


# async def test_register_user(ac: AsyncClient):
#     response = await ac.post("/auth/register", json={"email": "test1@pytest.com", "password": "1234567890", "id":5})
#     assert response.status_code == 200
#
#
# @pytest.mark.parametrize("email, password, status_code", [
#     ("user@example.com", "string", 200),
#     ("user", "string", 401),
# ])
# async def test_login_user(email, password, status_code, ac: AsyncClient):
#     response = await ac.post("auth/login", json=
#     {"email": email,
#      "password": password
#      })
#
#     assert response.status_code == status_code