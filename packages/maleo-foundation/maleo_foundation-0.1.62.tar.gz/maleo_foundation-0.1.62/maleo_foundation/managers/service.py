from fastapi import FastAPI, APIRouter
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.types import Lifespan, AppType
from pydantic_settings import BaseSettings
from pydantic import BaseModel, Field
from sqlalchemy import MetaData
from typing import Optional
from maleo_foundation.client.manager import MaleoFoundationClientManager
from maleo_foundation.enums import BaseEnums
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.transfers.general.token import BaseTokenGeneralTransfers
from maleo_foundation.models.transfers.parameters.token import BaseTokenParametersTransfers
from maleo_foundation.managers.db import DatabaseConfigurations, DatabaseManager
from maleo_foundation.managers.client.google.secret import GoogleSecretManager
from maleo_foundation.managers.client.google.storage import GoogleCloudStorage
from maleo_foundation.managers.middleware import MiddlewareConfigurations, BaseMiddlewareConfigurations, CORSMiddlewareConfigurations, GeneralMiddlewareConfigurations, MiddlewareLoggers, MiddlewareManager
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_foundation.utils.loaders.json import JSONLoader
from maleo_foundation.utils.loaders.yaml import YAMLLoader
from maleo_foundation.utils.logging import SimpleConfig, ServiceLogger, MiddlewareLogger
from maleo_foundation.utils.mergers import BaseMergers

class Settings(BaseSettings):
    ENVIRONMENT:BaseEnums.EnvironmentType = Field(..., description="Environment")
    GOOGLE_CREDENTIALS_PATH:str = Field("credentials/maleo-google-service-account.json", description="Internal credential's file path")
    INTERNAL_CREDENTIALS_PATH:str = Field("credentials/maleo-internal-service-account.json", description="Internal credential's file path")
    STATIC_CONFIGURATIONS_PATH:str = Field("configs/static.yaml", description="Maleo's static configurations path")
    RUNTIME_CONFIGURATIONS_PATH:str = Field("configs/runtime.yaml", description="Service's runtime configurations path")

class GoogleCredentials(BaseModel):
    type:str = Field(..., description="Credentials type")
    project_id:str = Field(..., description="Google project ID")
    private_key_id:str = Field(..., description="Private key ID")
    private_key:str = Field(..., description="Private key")
    client_email:str = Field(..., description="Client email")
    client_id:str = Field(..., description="Client ID")
    auth_uri:str = Field(..., description="Authorization URI")
    token_uri:str = Field(..., description="Token URI")
    auth_provider_x509_cert_url:str = Field(..., description="Authorization provider x509 certificate URL")
    client_x509_cert_url:str = Field(..., description="Client x509 certificate URL")
    universe_domain:str = Field(..., description="Universe domains")

class InternalCredentials(BaseModel):
    system_role:str = Field(..., description="System role")
    username:str = Field(..., description="Username")
    email:str = Field(..., description="Email")
    user_type:str = Field(..., description="User type")

class Credentials(BaseModel):
    google:GoogleCredentials = Field(..., description="Google's credentials")
    internal:InternalCredentials = Field(..., description="Internal's credentials")

    class Config:
        arbitrary_types_allowed=True

class MiddlewareRuntimeConfigurations(BaseModel):
    base:BaseMiddlewareConfigurations = Field(..., description="Base middleware's configurations")

    class Config:
        arbitrary_types_allowed=True

class ServiceConfigurations(BaseModel):
    key:str = Field(..., description="Service's key")
    name:str = Field(..., description="Service's name")
    host:str = Field(..., description="Service's host")
    port:int = Field(..., description="Service's port")

class RuntimeConfigurations(BaseModel):
    service:ServiceConfigurations = Field(..., description="Service's configurations")
    middleware:MiddlewareRuntimeConfigurations = Field(..., description="Middleware's runtime configurations")
    database:str = Field(..., description="Database's name")

    class Config:
        arbitrary_types_allowed=True

class MiddlewareStaticConfigurations(BaseModel):
    general:GeneralMiddlewareConfigurations = Field(..., description="Middleware's general configurations")
    cors:CORSMiddlewareConfigurations = Field(..., description="CORS middleware's configurations")

    class Config:
        arbitrary_types_allowed=True

class MaleoClientConfiguration(BaseModel):
    key:str = Field(..., description="Client's key")
    name:str = Field(..., description="Client's name")
    url:str = Field(..., description="Client's URL")

class MaleoClientConfigurations(BaseModel):
    metadata:MaleoClientConfiguration = Field(..., description="MaleoMetadata client's configuration")
    security:MaleoClientConfiguration = Field(..., description="MaleoSecurity client's configuration")
    storage:MaleoClientConfiguration = Field(..., description="MaleoStorage client's configuration")
    identity:MaleoClientConfiguration = Field(..., description="MaleoIdentity client's configuration")
    access:MaleoClientConfiguration = Field(..., description="MaleoAccess client's configuration")
    soapie:MaleoClientConfiguration = Field(..., description="MaleoSOAPIE client's configuration")
    fhir:MaleoClientConfiguration = Field(..., description="MaleoFHIR client's configuration")
    dicom:MaleoClientConfiguration = Field(..., description="MaleoDICOM client's configuration")
    scribe:MaleoClientConfiguration = Field(..., description="MaleoScribe client's configuration")
    cds:MaleoClientConfiguration = Field(..., description="MaleoCDS client's configuration")
    imaging:MaleoClientConfiguration = Field(..., description="MaleoImaging client's configuration")
    mcu:MaleoClientConfiguration = Field(..., description="MaleoMCU client's configuration")

    class Config:
        arbitrary_types_allowed=True

class ClientConfigurations(BaseModel):
    maleo:MaleoClientConfigurations = Field(..., description="Maleo client's configurations")

    class Config:
        arbitrary_types_allowed=True

class StaticConfigurations(BaseModel):
    middleware:MiddlewareStaticConfigurations = Field(..., description="Middleware's static configurations")
    client:ClientConfigurations = Field(..., description="Client's configurations")

    class Config:
        arbitrary_types_allowed=True

class Configurations(BaseModel):
    service:ServiceConfigurations = Field(..., description="Service's configurations")
    middleware:MiddlewareConfigurations = Field(..., description="Middleware's configurations")
    database:DatabaseConfigurations = Field(..., description="Database's configurations")
    client:ClientConfigurations = Field(..., description="Client's configurations")

    class Config:
        arbitrary_types_allowed=True

class Loggers(BaseModel):
    application:ServiceLogger = Field(..., description="Application logger")
    database:ServiceLogger = Field(..., description="Database logger")
    middleware:MiddlewareLoggers = Field(..., description="Middleware logger")

    class Config:
        arbitrary_types_allowed=True

class GoogleClientManagers(BaseModel):
    secret:GoogleSecretManager = Field(..., description="Google secret manager's client manager")
    storage:GoogleCloudStorage = Field(..., description="Google cloud storage's client manager")

    class Config:
        arbitrary_types_allowed=True

class MaleoClientManagers(BaseModel):
    foundation:MaleoFoundationClientManager = Field(..., description="MaleoFoundation's client manager")

    class Config:
        arbitrary_types_allowed=True

class ClientManagers(BaseModel):
    google:GoogleClientManagers = Field(..., description="Google's client managers")
    maleo:MaleoClientManagers = Field(..., description="Maleo's client managers")

    class Config:
        arbitrary_types_allowed=True

class ServiceManager:
    def __init__(
        self,
        db_metadata:MetaData,
        log_config:SimpleConfig,
        settings:Optional[Settings] = None
    ):
        self._db_metadata = db_metadata #* Declare DB Metadata
        self._log_config = log_config #* Declare log config
        self._settings = settings if settings is not None else Settings() #* Initialize settings
        #* Disable google cloud logging if environment is local
        if self._settings.ENVIRONMENT == "local":
            self._log_config.google_cloud_logging = None
        self._load_credentials()
        self._load_configs()
        self._initialize_secret_manager()
        #* Declare environment for configurations and client
        environment = BaseEnums.EnvironmentType.STAGING if self._settings.ENVIRONMENT == BaseEnums.EnvironmentType.LOCAL else self._settings.ENVIRONMENT
        self._initialize_configs(environment=environment)
        self._initialize_keys()
        self._initialize_loggers()
        self._initialize_db()
        self._initialize_clients(environment=environment)

    @property
    def log_config(self) -> SimpleConfig:
        return self._log_config

    @property
    def settings(self) -> Settings:
        return self._settings

    def _load_credentials(self) -> None:
        #* Load google credentials
        data = JSONLoader.load(self._settings.GOOGLE_CREDENTIALS_PATH)
        google = GoogleCredentials.model_validate(data)
        #* Load internal credentials
        data = JSONLoader.load(self._settings.INTERNAL_CREDENTIALS_PATH)
        internal = InternalCredentials.model_validate(data)
        self._credentials = Credentials(google=google, internal=internal)

    @property
    def credentials(self) -> Credentials:
        return self._credentials

    def _load_configs(self) -> None:
        static_configurations = YAMLLoader.load(self._settings.STATIC_CONFIGURATIONS_PATH)
        self._static_configs = StaticConfigurations.model_validate(static_configurations)
        runtime_configurations = YAMLLoader.load(self._settings.RUNTIME_CONFIGURATIONS_PATH)
        self._runtime_configs = RuntimeConfigurations.model_validate(runtime_configurations)

    def _initialize_secret_manager(self) -> None:
        self._secret_manager = GoogleSecretManager(log_config=self._log_config, service_key=self._runtime_configs.service.key, credentials_path=self._settings.GOOGLE_CREDENTIALS_PATH)

    @property
    def secret_manager(self) -> None:
        return self._secret_manager

    def _initialize_configs(self, environment:BaseEnums.EnvironmentType) -> None:
        password = self._secret_manager.get(name=f"maleo-db-password-{environment}")
        host = self._secret_manager.get(name=f"maleo-db-host-{environment}")
        database = DatabaseConfigurations(password=password, host=host, database=self._runtime_configs.database)
        merged_configs = BaseMergers.deep_merge(self._static_configs.model_dump(), self._runtime_configs.model_dump(exclude={"database"}), {"database": database.model_dump()})
        self._configs = Configurations.model_validate(merged_configs)

    @property
    def configs(self) -> Configurations:
        return self._configs

    def _initialize_keys(self) -> None:
        password = self._secret_manager.get(name="maleo-key-password")
        private = self._secret_manager.get(name="maleo-private-key")
        public = self._secret_manager.get(name="maleo-public-key")
        self._keys = BaseGeneralSchemas.RSAKeys(password=password, private=private, public=public)

    @property
    def keys(self) -> BaseGeneralSchemas.RSAKeys:
        return self._keys

    def _initialize_loggers(self) -> None:
        #* Service's loggers
        application = ServiceLogger(type=BaseEnums.LoggerType.APPLICATION, service_key=self._configs.service.key, **self._log_config.model_dump())
        database = ServiceLogger(type=BaseEnums.LoggerType.DATABASE, service_key=self._configs.service.key, **self._log_config.model_dump())
        #* Middleware's loggers
        base = MiddlewareLogger(middleware_type=BaseEnums.MiddlewareLoggerType.BASE, service_key=self._configs.service.key, **self._log_config.model_dump())
        authentication = MiddlewareLogger(middleware_type=BaseEnums.MiddlewareLoggerType.AUTHENTICATION, service_key=self._configs.service.key, **self._log_config.model_dump())
        middleware = MiddlewareLoggers(base=base, authentication=authentication)
        self._loggers = Loggers(application=application, database=database, middleware=middleware)

    @property
    def loggers(self) -> Loggers:
        return self._loggers

    def _initialize_db(self) -> None:
        self._database = DatabaseManager(metadata=self._db_metadata, logger=self._loggers.database, url=self._configs.database.url)

    @property
    def database(self) -> DatabaseManager:
        return self._database

    def _initialize_clients(self, environment:BaseEnums.EnvironmentType) -> None:
        secret = self._secret_manager
        storage = GoogleCloudStorage(log_config=self._log_config, service_key=self._runtime_configs.service.key, bucket_name=f"maleo-suite-{environment}", credentials_path=self._settings.GOOGLE_CREDENTIALS_PATH)
        self._google_clients = GoogleClientManagers(secret=secret, storage=storage)
        foundation = MaleoFoundationClientManager(log_config=self._log_config, service_key=self._runtime_configs.service.key)
        self._maleo_clients = MaleoClientManagers(foundation=foundation)
        self._clients = ClientManagers(google=self._google_clients, maleo=self._maleo_clients)

    @property
    def google_clients(self) -> GoogleClientManagers:
        self._google_clients

    @property
    def maleo_clients(self) -> MaleoClientManagers:
        self._maleo_clients

    @property
    def clients(self) -> ClientManagers:
        self._clients

    @property
    def token(self) -> str:
        payload = BaseTokenGeneralTransfers.BaseEncodePayload(
            sr=self._credentials.internal.system_role,
            u_u=self._credentials.internal.username,
            u_e=self._credentials.internal.email,
            u_ut=self._credentials.internal.user_type
        )
        parameters = BaseTokenParametersTransfers.Encode(key=self._keys.private, password=self._keys.password, payload=payload)
        result = self._clients.maleo.foundation.services.token.encode(parameters=parameters)
        if not result.success:
            return ""
        return result.data.token

    def create_app(self, router:APIRouter, lifespan:Optional[Lifespan[AppType]] = None) -> FastAPI:
        self._loggers.application.info("Creating FastAPI application")
        self._app = FastAPI(title=self._configs.service.name, lifespan=lifespan)
        self._loggers.application.info("FastAPI application created successfully")

        #* Add middleware(s)
        self._loggers.application.info("Configuring middlewares")
        self._middleware = MiddlewareManager(
            app=self._app,
            configurations=self._configs.middleware,
            keys=self._keys,
            loggers=self._loggers.middleware,
            maleo_foundation=self._clients.maleo.foundation
        )
        self._middleware.add_all()
        self._loggers.application.info("Middlewares addedd successfully")

        #* Add exception handler(s)
        self._loggers.application.info("Adding exception handlers")
        self._app.add_exception_handler(RequestValidationError, BaseExceptions.validation_exception_handler)
        self._app.add_exception_handler(HTTPException, BaseExceptions.http_exception_handler)
        self._loggers.application.info("Exception handlers addedd successfully")

        #* Include router
        self._loggers.application.info("Including routers")
        self._app.include_router(router)
        self._loggers.application.info("Routers included successfully")

        return self._app

    @property
    def app(self) -> FastAPI:
        return self._app

    async def dispose(self) -> None:
        self._loggers.application.info("Disposing service manager")
        if self._database is not None:
            self._database.dispose()
            self._database = None
        self._loggers.application.info("Service manager disposed successfully")
        if self._loggers is not None:
            self._loggers.application.info("Disposing logger")
            self._loggers.application.dispose()
            self._loggers.database.info("Disposing logger")
            self._loggers.database.dispose()
            self._loggers.middleware.base.info("Disposing logger")
            self._loggers.middleware.base.dispose()
            self._loggers.middleware.authentication.info("Disposing logger")
            self._loggers.middleware.authentication.dispose()
            self._loggers = None