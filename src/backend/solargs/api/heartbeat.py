from fastapi import APIRouter

from solargs.model.heartbeat import HeartbeatResult

health_router = APIRouter()


@health_router.get("", tags=["health"], name="heartbeat")
def get_heartbeat() -> HeartbeatResult:
    """
    Retrieves the heartbeat status of the server.

    Returns:
        HeartbeatResult: An instance of the HeartbeatResult class representing the heartbeat status.
    """
    heartbeat = HeartbeatResult(is_alive=True)
    return heartbeat
