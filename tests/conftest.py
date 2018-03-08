import pytest
import pytest_trio
import inspect

# auto-trio-ize all async functions
@pytest.hookimpl(tryfirst=True)
def pytest_pyfunc_call(pyfuncitem):
    if inspect.iscoroutinefunction(pyfuncitem.obj):
        pyfuncitem.obj = pytest.mark.trio(pyfuncitem.obj)

@pytest.fixture
async def set_me_up():
    obj = None
    cleans = []
    def addCleanup(p,*a,**k):
        cleans.append((p,a,k))
        
    async def fn(self):
        nonlocal obj
        obj = self
        obj.addCleanup = addCleanup
        await self.setUp()

    yield fn

    await obj.tearDown()
    while cleans:
        p,a,k = cleans.pop()
        await p(*a,**k)

