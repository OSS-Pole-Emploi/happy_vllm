import ssl
import json
import argparse

from vllm.engine.arg_utils import AsyncEngineArgs


def parse_args():
    parser = argparse.ArgumentParser(description="REST API server for vLLM, production ready")

    parser.add_argument("--host",
                        type=str,
                        default='127.0.0.1',
                        help="host name")
    parser.add_argument("--port",
                        type=int,
                        default=8000,
                        help="port number")
    parser.add_argument("--model_name",
                        type=str,
                        default='?',
                        help="The name of the model given by the /info endpoint of the API")
    parser.add_argument("--explicit_errors",
                        action='store_true',
                        help="If True, the underlying python errors are sent back via the API")
    parser.add_argument("--allow-credentials",
                        action="store_true",
                        help="allow credentials")
    parser.add_argument("--allowed-origins",
                        type=json.loads,
                        default=["*"],
                        help="allowed origins")
    parser.add_argument("--allowed-methods",
                        type=json.loads,
                        default=["*"],
                        help="allowed methods")
    parser.add_argument("--allowed-headers",
                        type=json.loads,
                        default=["*"],
                        help="allowed headers")
    parser.add_argument("--uvicorn-log-level",
                        type=str,
                        default="info",
                        choices=['debug', 'info', 'warning', 'error', 'critical', 'trace'],
                        help="log level for uvicorn")
    parser.add_argument("--ssl-keyfile",
                        type=str,
                        default=None,
                        help="The file path to the SSL key file")
    parser.add_argument("--ssl-certfile",
                        type=str,
                        default=None,
                        help="The file path to the SSL cert file")
    parser.add_argument("--ssl-ca-certs",
                        type=str,
                        default=None,
                        help="The CA certificates file")
    parser.add_argument("--ssl-cert-reqs",
                        type=int,
                        default=int(ssl.CERT_NONE),
                        help="Whether client certificate is required (see stdlib ssl module's)")
    parser.add_argument("--root-path",
                        type=str,
                        default=None,
                        help="FastAPI root_path when app is behind a path based routing proxy")
    parser = AsyncEngineArgs.add_cli_args(parser)
    args = parser.parse_args()

    return args
