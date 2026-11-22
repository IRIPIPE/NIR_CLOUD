import logging
import os
from dataclasses import dataclass
from typing import Literal

import psycopg
from fastapi import FastAPI, Response, status


logger = logging.getLogger(__name__)
app = FastAPI(title="NIR Cloud API")


@dataclass(frozen=True)
class HealthStatus:
    status: Literal["ok", "unavailable"]
    database: Literal["ok", "unavailable"]


@app.get("/health", response_model=HealthStatus, responses={503: {"model": HealthStatus}})
def health(response: Response) -> HealthStatus:
    try:
        with psycopg.connect(
            host=os.environ["POSTGRES_HOST"],
            dbname=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            connect_timeout=2,
            options="-c statement_timeout=1000",
            autocommit=True,
        ) as connection:
            connection.execute("SELECT 1").fetchone()
    except psycopg.Error as error:
        logger.warning("Database health check failed (%s)", type(error).__name__)
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return HealthStatus(status="unavailable", database="unavailable")

    return HealthStatus(status="ok", database="ok")
