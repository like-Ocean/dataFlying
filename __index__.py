from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

import os

from database import db
from models import (User, Device, Session, Feature, Plan, PlanFeature, Subscription,
                    Flight, Accelerometer, Gps, Gyroscope, Temperature,
                    Magnetometer, Barometer)
from routers import routes


load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.connect()
    yield
    db.close()

app = FastAPI(lifespan=lifespan)

for router in routes:
    app.include_router(router, prefix="/api")


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == '__main__':
    with db:
        db.create_tables([User, Device, Session, Feature, Plan, PlanFeature, Subscription,
                          Flight, Accelerometer, Gps, Gyroscope,
                          Temperature, Magnetometer, Barometer])
    uvicorn.run(
        "__index__:app",
        host=os.environ.get("HOST"),
        port=int(os.environ.get("PORT")),
        log_level="debug",
        reload=True
    )
