import asyncio
import random
from enum import Enum
from typing import Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import tracemalloc


timeout_seconds = timedelta(seconds=3).total_seconds()
timeout = timedelta(seconds=3)


class Response(Enum):
    Success = 1
    RetryAfter = 2
    Failure = 3


class ApplicationStatusResponse(Enum):
    Success = 1
    Failure = 2


@dataclass
class ApplicationResponse:
    application_id: str
    status: ApplicationStatusResponse
    description: str
    last_request_time: datetime
    retriesCount: Optional[int]


async def get_application_status1(identifier: str) -> Response:
    # Метод, возвращающий статус заявки
    return Response(random.randrange(1, 4))


async def get_application_status2(identifier: str) -> Response:
    # Метод, возвращающий статус заявки
    return Response(random.randrange(1, 4))


async def perform_operation(identifier: str) -> ApplicationResponse:
    # TODO дополнить реализацию
    retries_counter = 0
    timer = datetime.now()
    if identifier == 1:
        func = get_application_status1
    else:
        func = get_application_status2
    result = await func(identifier)
    if result.value == 1:
        value = 1
    else:
        value = 2
    response = ApplicationResponse(
        application_id=identifier,
        status=ApplicationStatusResponse(value),
        description="First try",
        last_request_time=timer,
        retriesCount=retries_counter
    )
    while response.status.value == 2:
        time_to = datetime.now() - timer
        if time_to.total_seconds() > timeout_seconds:
            return ApplicationResponse(
              application_id=identifier,
              status=ApplicationStatusResponse(value=2),
              description="Out of time",
              last_request_time=datetime.now(),
              retriesCount=retries_counter
            )
        await asyncio.sleep(1.5)
        retries_counter += 1
        result = await func(identifier)
        if result.value == 1:
            value = 1
        else:
            value = 2
        response = ApplicationResponse(
            application_id=identifier,
            status=ApplicationStatusResponse(value),
            description="Standard",
            last_request_time=datetime.now(),
            retriesCount=retries_counter
        )
    return response


async def main():
    tracemalloc.start()
    with ThreadPoolExecutor(max_workers=5) as executor:
        while True:
            future_1 = await executor.submit(perform_operation, "1").result()
            print(future_1)
            future_2 = await executor.submit(perform_operation, "2").result()
            print(future_2)

if __name__ == "__main__":
    asyncio.run(main())
