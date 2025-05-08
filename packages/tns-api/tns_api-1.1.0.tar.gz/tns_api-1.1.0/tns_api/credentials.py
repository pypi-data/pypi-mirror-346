import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

import tns_api
api_path = tns_api.__path__[0]

def set_credentials(credentials: dict = None) -> None:
    """Set the TNS credentials for the API.

    Parameters
    ----------
    credentials: dictionary with "tns_id", "tns_bot_name" and "tns_api_key".
    """
    if credentials is None:
        print("🔐 Please enter your TNS credentials:")
        tns_id = input("TNS ID: ")
        tns_bot_name = input("TNS BOT NAME: ")
        tns_api_key = input("TNS API KEY: ")
        cred_dict = {"tns_id": tns_id,
                     "tns_bot_name": tns_bot_name,
                     "tns_api_key": tns_api_key,
                     }
    credentials_file = Path(api_path, ".credentials.yml")
    with open(credentials_file, 'w') as outfile:
        yaml.dump(credentials, outfile, default_flow_style=False)
    print("TNS credentials stored successfully!")
    print("Please, restart your kernel to make the changes effective.")

def load_yml(file: str) -> dict:
    """Simply loads a YAML file.
    """
    with open(file) as stream:
        try:
            return (yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)

# load credentials
try:
    credentials_file = Path(api_path, ".credentials.yml")
    credentials = load_yml(credentials_file)

    TNS_ID = credentials["tns_id"]
    TNS_BOT_NAME = credentials["tns_bot_name"]
    TNS_API_KEY = credentials["tns_api_key"]
except:
    load_dotenv()
    TNS_ID = os.getenv("tns_id")
    TNS_BOT_NAME = os.getenv("tns_bot_name")
    if TNS_BOT_NAME is None:
        TNS_BOT_NAME = os.getenv("name")  # old version
    TNS_API_KEY = os.getenv("tns_api_key")
    if TNS_API_KEY is None:
        TNS_API_KEY = os.getenv("api_key")  # old version
