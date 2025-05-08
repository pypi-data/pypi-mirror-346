import os
import sys
from typing import List

from eventix.functions.eventix_client import EventixClient
from eventix.pydantic.task import EventixTaskStatusEnum

try:
    import fastapi
    from fastapi import APIRouter, Body, Query
    from fastapi import Request, Response

except:
    pass


def fastapi_eventix_router_wrapper(self):
    if 'fastapi' not in sys.modules:  # pragma: no cover
        raise Exception('fastapi not installed but required by fastapi_eventix_router_wrapper')

    eventix_router = APIRouter(prefix="", tags=["eventix"])

    @eventix_router.get("/task/by_unique_key/{unique_key}")
    def router_task_by_unique_key_for_namespace_get(unique_key: str, stati: list[EventixTaskStatusEnum] = Query(None)):
        if stati is None:
            stati = [EventixTaskStatusEnum.scheduled.value, EventixTaskStatusEnum.retry.value]
        namespace = os.environ.get("EVENTIX_NAMESPACE", None)
        r = EventixClient.get_task_by_unique_key_and_namespace(unique_key, namespace=namespace, stati=stati)
        return r.json()

    self.include_router(eventix_router)
