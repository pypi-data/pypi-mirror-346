import string

from devtools import debug
from fastapi.applications import FastAPI
from fastapi.params import Depends

from tidelog import FailureDetail, LogRecord, SuccessDetail

app = FastAPI()


def exc_dep():
    # raise HTTPException(400, detail="lalala")
    raise ValueError("2333")


class A:
    def __init__(self, name: int) -> None:
        self.name = name


def get(*args, __: SuccessDetail | FailureDetail, **kwds):
    print(__)
    return "hahaha"


log_record = LogRecord(
    success="lalalala",
    failure=string.Template("$get lalala"),
    success_handlers=[lambda detail: print(detail)],
    failure_handlers=[lambda detail: debug(detail.message)],
    functions=[get],
    # dependencies=[Depends(exc_dep)],
)


@app.get(
    "/",
)
@log_record
def aaaa(
    b=Depends(exc_dep),
    a=Depends(A),
):
    return id(object())
