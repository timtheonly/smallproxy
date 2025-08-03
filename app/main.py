from fastapi import FastAPI
from app.internals.bootstrap import bootstrap_routers, setup_logging
from app.internals.middleware.correlation_id import CorrelationId
from app.internals.middleware.request_logger import RequestLogger
from app.internals.middleware.exception import ExceptionMiddleware

app = FastAPI()
app = bootstrap_routers(app)
setup_logging()
app.add_middleware(ExceptionMiddleware)
app.add_middleware(RequestLogger)
app.add_middleware(CorrelationId)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/e")
async def err():
    raise TypeError


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
