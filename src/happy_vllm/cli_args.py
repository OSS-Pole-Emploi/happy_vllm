import argparse

from vllm.engine.arg_utils import AsyncEngineArgs

def make_arg_parser():
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
    parser = AsyncEngineArgs.add_cli_args(parser)
    cli_args = parser.parse_args()
