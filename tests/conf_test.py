import pytest

from e_store.users.models import User


@pytest.fixture(autouse=True)
def create_dummy_user(tmpdir):
    """Fixture to execute asserts before and after a test is run"""

    from test_db import get_test_session

    db = next(get_test_session())
    new_user = User(name="John", email="john@gmail.com", password="jhon123")
    db.add(new_user)
    db.commit()
