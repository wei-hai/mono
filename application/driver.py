"""
This module starts the application server
"""
import argparse

import psutil

from application.factory import create_app
app = create_app()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mono service")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="host")
    parser.add_argument("--port", type=int, default=8080, help="port")
    parser.add_argument("--debug", action="store_true", help="debug mode")
    parser.add_argument(
        "--worker", type=int, default=psutil.cpu_count(logical=False), help="worker"
    )

    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=args.debug, workers=args.worker)
