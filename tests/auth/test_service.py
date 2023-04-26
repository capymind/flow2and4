import pytest

from sqlalchemy.exc import IntegrityError
from csduck.auth.schemas import UserCreate


user_in = [
    UserCreate(username="choco", nickname="choco", password="choco"),
]


@pytest.mark.parametrize("user_in", user_in)
def test_create_user_with_duplicates(db, user_in):

    from csduck.auth.service import create_user
    user = create_user(user_in=user_in)
    
    with pytest.raises(IntegrityError):
        user = create_user(user_in=user_in)
   




@pytest.mark.parametrize("user_in", user_in)
def test_create_user(db_session, user_in):

    from csduck.auth.service import create_user

    user = create_user(user_in=user_in)
    
    assert user.username == user_in.username
