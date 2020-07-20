"""
This module starts the application server
"""
import argparse
import os

from application.factory import create_app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mono Server")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="host")
    parser.add_argument("--port", type=int, default=8080, help="port")
    parser.add_argument("--debug", action="store_true", help="debug mode")
    parser.add_argument("--auto_reload", action="store_true", help="auto reload")
    parser.add_argument("--worker", type=int, default=os.cpu_count(), help="worker")
    args = parser.parse_args()
    app = create_app()
    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug,
        auto_reload=args.auto_reload,
        workers=args.worker,
    )
