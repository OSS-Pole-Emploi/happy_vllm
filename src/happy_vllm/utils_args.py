import ssl
import json
import argparse
from typing import Literal, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

from vllm.engine.arg_utils import AsyncEngineArgs


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5000
DEFAULT_EXPLICIT_ERRORS = False
DEFAULT_ALLOW_CREDENTIALS = False
DEFAULT_ALLOWED_ORIGINS = ["*"]
DEFAULT_ALLOWED_METHODS = ["*"]
DEFAULT_ALLOWED_HEADERS = ["*"]
DEFAULT_UVICORN_LOG_LEVEL = 'info'
CHOICES_UVICORN_LOG_LEVEL = ['debug', 'info', 'warning', 'error', 'critical', 'trace']
DEFAULT_SSL_KEYFILE = None
DEFAULT_SSL_CERTFILE = None
DEFAULT_SSL_CA_CERTS = None
DEFAULT_SSL_CERT_REQS = int(ssl.CERT_NONE)
DEFAULT_ROOT_PATH = None


class ApplicationSettings(BaseSettings):
    """Download settings

    This class is used for settings management purpose, have a look at the pydantic
    documentation for more details : https://pydantic-docs.helpmanual.io/usage/settings/

    By default, it looks for environment variables (case insensitive) to set the settings
    if a variable is not found, it looks for a file name .env in your working directory
    where you can declare the values of the variables and finally it sets the values
    to the default ones one can define below
    """
    host : str = DEFAULT_HOST
    port: int = DEFAULT_PORT
    explicit_errors: bool = DEFAULT_EXPLICIT_ERRORS
    allow_credentials: bool = DEFAULT_ALLOW_CREDENTIALS
    allowed_origins: list = DEFAULT_ALLOWED_ORIGINS
    allowed_methods: list = DEFAULT_ALLOWED_METHODS
    allowed_headers: list = DEFAULT_ALLOWED_HEADERS
    uvicorn_log_level: Literal[*CHOICES_UVICORN_LOG_LEVEL] = DEFAULT_UVICORN_LOG_LEVEL
    ssl_keyfile: Optional[str] = DEFAULT_SSL_KEYFILE
    ssl_certfile: Optional[str] = DEFAULT_SSL_CERTFILE
    ssl_ca_certs: Optional[str] = DEFAULT_SSL_CA_CERTS
    ssl_cert_reqs: int = DEFAULT_SSL_CERT_REQS
    root_path: Optional[str] = DEFAULT_ROOT_PATH

    model_config = SettingsConfigDict(env_file=".env", extra='ignore', protected_namespaces=('settings', ))


def parse_args():
    parser = argparse.ArgumentParser(description="REST API server for vLLM, production ready")

    application_settings = ApplicationSettings()

    parser.add_argument("--host",
                        type=str,
                        default=application_settings.host,
                        help="host name")
    parser.add_argument("--port",
                        type=int,
                        default=application_settings.port,
                        help="port number")
    parser.add_argument("--model-name",
                        type=str,
                        default='?',
                        help="The name of the model given by the /info endpoint of the API")
    parser.add_argument("--explicit-errors",
                        default=application_settings.explicit_errors,
                        action=argparse.BooleanOptionalAction,
                        help="If True, the underlying python errors are sent back via the API")
    parser.add_argument('--allow-credentials',
                        default=application_settings.allow_credentials,
                        action=argparse.BooleanOptionalAction,
                        help="allow credentials")
    parser.add_argument("--allowed-origins",
                        type=json.loads,
                        default=application_settings.allowed_origins,
                        help="allowed origins")
    parser.add_argument("--allowed-methods",
                        type=json.loads,
                        default=application_settings.allowed_methods,
                        help="allowed methods")
    parser.add_argument("--allowed-headers",
                        type=json.loads,
                        default=application_settings.allowed_headers,
                        help="allowed headers")
    parser.add_argument("--uvicorn-log-level",
                        type=str,
                        default=application_settings.uvicorn_log_level,
                        choices=CHOICES_UVICORN_LOG_LEVEL,
                        help="log level for uvicorn")
    parser.add_argument("--ssl-keyfile",
                        type=str,
                        default=application_settings.ssl_keyfile,
                        help="The file path to the SSL key file")
    parser.add_argument("--ssl-certfile",
                        type=str,
                        default=application_settings.ssl_certfile,
                        help="The file path to the SSL cert file")
    parser.add_argument("--ssl-ca-certs",
                        type=str,
                        default=application_settings.ssl_ca_certs,
                        help="The CA certificates file")
    parser.add_argument("--ssl-cert-reqs",
                        type=int,
                        default=application_settings.ssl_cert_reqs,
                        help="Whether client certificate is required (see stdlib ssl module's)")
    parser.add_argument("--root-path",
                        type=str,
                        default=application_settings.root_path,
                        help="FastAPI root_path when app is behind a path based routing proxy")
    parser = AsyncEngineArgs.add_cli_args(parser)
    args = parser.parse_args()

    return args