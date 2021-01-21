import pytest

import foo.foo
from foo.foo import Foo


@pytest.fixture
def foo():
    foo = Foo()
    return foo

def test_bar(foo):
    assert foo.bar(2) == 4