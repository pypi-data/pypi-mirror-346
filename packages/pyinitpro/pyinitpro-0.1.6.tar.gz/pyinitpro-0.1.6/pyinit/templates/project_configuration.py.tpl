import logging
import os

import requests
from dotenv import load_dotenv

load_dotenv()

mailslurp_base_url = os.environ.get("MAILSLURP_BASE_URL")
base_url = os.environ.get("BASE_URL")
application_url = os.environ.get("APPLICATION_URL")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mailosaur_api_key = os.getenv("MAILOSAUR_API_KEY")
server_id = os.getenv("SERVER_ID")

session = requests.session()