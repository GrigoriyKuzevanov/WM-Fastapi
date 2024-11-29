from pydantic import BaseModel
from pydantic_settings import BaseSettings


class RunConfig(BaseModel):
    """A class for app running settings.

    Attributes:
        app (str): Entrypoint to start fastapi app by uvicorn. "main:app" by default
        host (str): Host to start app on. "0.0.0.0" by default
        port (int): Port to start app on. 8000 by default
    """

    app: str = "main:app"
    host: str = "0.0.0.0"
    port: int = 8000


class ApiPrefix(BaseModel):
    """A class for api prefix settings.

    Attributes:
        prefix (str): An api's url prefix. "/api" by default
    """

    prefix: str = "/api"


class Settings(BaseSettings):
    """A base class for app's settings. Settings values might be overriden by environmet
    variables.

    Attributes:
        run (RunConfig): RunConfig class's instance of settings for running the main
        application
        api (ApiPrefix): ApiPrefix class's instance of settings for api prefix
    """

    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()


settings = Settings()
