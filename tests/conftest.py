import pytest
import inspect
from trio.testing import trio_test

class _Setup:
    def __init__(self, obj):
        self.obj = obj
        self.cleans = []

    async def setup(self, obj):
        self.obj = obj
        await obj.setUp()

    async def teardown(self):
        await self.obj.tearDown()
        while self.cleans:
            p,a,k = self.cleans.pop()
            await p(*a,**k)

@pytest.fixture
async def set_me_up():
    setup = _Setup()
    try:
        yield setup
    finally:
        await setup.teardown()

# auto-trio-ize all async functions
@pytest.hookimpl(tryfirst=True)
def pytest_pyfunc_call(pyfuncitem):
    if inspect.iscoroutinefunction(pyfuncitem.obj):
        pyfuncitem.obj = trio_test(pyfuncitem.obj)

