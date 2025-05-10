from httpx import AsyncClient

from ...state.context import TimbalPlatformConfig


async def get_apps(
    # TODO Think how we can get this without passing it explicitly as an argument.
    timbal_platform_config: TimbalPlatformConfig, 
    org_id: str, # Possible filter
) -> list[dict]:
    apps = []

    return apps


if __name__ == "__main__":
    timbal_platform_config = TimbalPlatformConfig.model_validate({
        "host": "https://dev.timbal.ai",
        "auth_config": {
            "type": "bearer",
            "token": ""
        }
    })
        