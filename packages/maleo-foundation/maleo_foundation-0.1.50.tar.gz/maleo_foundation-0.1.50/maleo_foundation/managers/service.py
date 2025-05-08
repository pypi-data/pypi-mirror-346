from fastapi import FastAPI, APIRouter
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.types import Lifespan, AppType
from pydantic_settings import BaseSettings
from pydantic import BaseModel, Field
from sqlalchemy import MetaData
from typing import Optional
from maleo_foundation.enums import BaseEnums
from maleo_foundation.models.transfers.general.token import BaseTokenGeneralTransfers
from maleo_foundation.models.transfers.parameters.token import BaseTokenParametersTransfers
from maleo_foundation.managers.db import DatabaseConfigurations, DatabaseManager
from maleo_foundation.managers.middleware import MiddlewareConfigurations, BaseMiddlewareConfigurations, CORSMiddlewareConfigurations, GeneralMiddlewareConfigurations, MiddlewareLoggers, MiddlewareManager
from maleo_foundation.middlewares.base import RequestProcessor
from maleo_foundation.services.token import BaseTokenService
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_foundation.utils.loaders.json import JSONLoader
from maleo_foundation.utils.loaders.key import KeyLoader
from maleo_foundation.utils.loaders.yaml import YAMLLoader
from maleo_foundation.utils.logging import SimpleConfig, ServiceLogger, MiddlewareLogger
from maleo_foundation.utils.mergers import BaseMergers

class Settings(BaseSettings):
    ENVIRONMENT:BaseEnums.EnvironmentType = Field(..., description="Environment")
    GOOGLE_CREDENTIALS_PATH:str = Field("credentials/maleo-google-service-account.json", description="Internal credential's file path")
    INTERNAL_CREDENTIALS_PATH:str = Field("credentials/maleo-internal-service-account.json", description="Internal credential's file path")
    PRIVATE_KEY_PATH:str = Field("keys/maleo-private-key.pem", description="Maleo's private key path")
    PUBLIC_KEY_PATH:str = Field("keys/maleo-public-key.pem", description="Maleo's public key path")
    KEY_PASSWORD:str = Field(..., description="Maleo key's password")
    STATIC_CONFIGURATIONS_PATH:str = Field("configs/static.yaml", description="Maleo's static configurations path")
    RUNTIME_CONFIGURATIONS_PATH:str = Field("configs/runtime.yaml", description="Service's runtime configurations path")
    DB_PASSWORD:str = Field(..., description="Database's password")

class Keys(BaseModel):
    password:str = Field(..., description="Key's password")
    private:str = Field(..., description="Private key")
    public:str = Field(..., description="Public key")

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
    database:DatabaseConfigurations = Field(..., description="Database's configurations")

    class Config:
        arbitrary_types_allowed=True

class MiddlewareStaticConfigurations(BaseModel):
    general:GeneralMiddlewareConfigurations = Field(..., description="Middleware's general configurations")
    cors:CORSMiddlewareConfigurations = Field(..., description="CORS middleware's configurations")

    class Config:
        arbitrary_types_allowed=True

class GoogleCloudStorageConfigurations(BaseModel):
    bucket_name:str = Field(..., description="Bucket's name")

class GoogleClientConfigurations(BaseModel):
    storage:GoogleCloudStorageConfigurations = Field(..., description="Google cloud storage client configurations")

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
    google:GoogleClientConfigurations = Field(..., description="Google client's configurations")
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

class ServiceManager:
    def __init__(
        self,
        db_metadata:MetaData,
        log_config:SimpleConfig,
        settings:Optional[Settings] = None
    ):
        self._db_metadata = db_metadata #* Declare DB Metadata

        #* Initialize settings
        if settings is None:
            self._settings = Settings()
        else:
            self._settings = settings

        self._load_configs()
        self._log_config = log_config #* Declare log config
        self._initialize_loggers()
        self._load_credentials()
        self._parse_keys()
        self._initialize_db()

    @property
    def log_config(self) -> SimpleConfig:
        return self._log_config

    @property
    def settings(self) -> Settings:
        return self._settings

    def _load_configs(self) -> None:
        static_configurations = YAMLLoader.load(self._settings.STATIC_CONFIGURATIONS_PATH)
        self._static_configs = StaticConfigurations.model_validate(static_configurations)
        runtime_configurations = YAMLLoader.load(self._settings.RUNTIME_CONFIGURATIONS_PATH)
        self._runtime_configs = RuntimeConfigurations.model_validate(runtime_configurations)
        merged_configs = BaseMergers.deep_merge(self._static_configs.model_dump(), self._runtime_configs.model_dump())
        self._configs = Configurations.model_validate(merged_configs)

    @property
    def configs(self) -> Configurations:
        return self._configs

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

    def _parse_keys(self) -> None:
        #* Parse private key
        key_type = BaseEnums.KeyType.PRIVATE
        private = KeyLoader.load_rsa(
            type=key_type,
            path=self._settings.PRIVATE_KEY_PATH,
            password=self._settings.KEY_PASSWORD
        )
        #* Parse public key
        key_type = BaseEnums.KeyType.PUBLIC
        public = KeyLoader.load_rsa(
            type=key_type,
            path=self._settings.PUBLIC_KEY_PATH
        )
        self._keys = Keys(password=self._settings.KEY_PASSWORD, private=private, public=public)

    @property
    def keys(self) -> Keys:
        return self._keys

    def _initialize_db(self) -> None:
        self._database = DatabaseManager(metadata=self._db_metadata, logger=self._loggers.database, url=self._configs.database.url)

    @property
    def database(self) -> DatabaseManager:
        return self._database

    @property
    def token(self) -> str:
        payload = BaseTokenGeneralTransfers.BaseEncodePayload(
            sr=self._credentials.internal.system_role,
            u_u=self._credentials.internal.username,
            u_e=self._credentials.internal.email,
            u_ut=self._credentials.internal.user_type
        )
        parameters = BaseTokenParametersTransfers.Encode(
            key=self.keys.private,
            password=self.keys.password,
            payload=payload
        )
        result = BaseTokenService.encode(parameters=parameters)
        if not result.success:
            raise ValueError("Failed generating token")
        return result.data.token

    def create_app(self, router:APIRouter, lifespan:Optional[Lifespan[AppType]] = None, request_processor:Optional[RequestProcessor] = None) -> FastAPI:
        self._loggers.application.info("Creating FastAPI application")
        self._app = FastAPI(title=self._configs.service.name, lifespan=lifespan)
        self._loggers.application.info("FastAPI application created successfully")

        #* Add middleware(s)
        self._loggers.application.info("Configuring middlewares")
        self._middleware = MiddlewareManager(app=self._app, configurations=self._configs.middleware)
        self._middleware.add_all(loggers=self.loggers.middleware, key=self._keys.public, request_processor=request_processor)
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