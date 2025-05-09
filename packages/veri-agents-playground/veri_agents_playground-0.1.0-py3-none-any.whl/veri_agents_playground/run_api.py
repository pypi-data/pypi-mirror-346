from dotenv import load_dotenv
import uvicorn
import logging
import sys
import argparse
from veri_agents_playground.api import app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logging.getLogger("qdrant").setLevel(logging.WARNING)
logging.getLogger("actix_web").setLevel(logging.WARNING)
load_dotenv()


# get port from argparse
parser = argparse.ArgumentParser(description="Run the API server.")
parser.add_argument(
    "--port",
    type=int,
    default=80,
    help="Port to run the API server on (default: 8000)",
)
parser.add_argument(
    "--host",
    type=str,
    default="0.0.0.0",
    help="Host to run the API server on (default: 0.0.0.0)",
)
args = parser.parse_args()

uvicorn.run(app, host=args.host, port=args.port)
