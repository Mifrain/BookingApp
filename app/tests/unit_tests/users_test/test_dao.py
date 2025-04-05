import pytest

from app.users.services import UserService

@pytest.mark.parametrize("id, email, exists", [
    (1, "fedor@moloko.ru", True),
    (2, "wrong@email.ru", False),
])
async def test_find_user_by_id(id, email, exists):
    user = await UserService.find_by_id(id)


    assert (user.email == email) == exists