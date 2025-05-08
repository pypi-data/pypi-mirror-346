# -*- coding: utf-8 -*-

import requests
import pandas as pd
from .credentials import TNS_ID, TNS_BOT_NAME

http_errors = {
        304: "Error 304: Not Modified: There was no new data to return.",
        400: "Error 400: Bad Request: The request was invalid. "
        "An accompanying error message will explain why.",
        403: "Error 403: Forbidden: The request is understood, but it has "
        "been refused. An accompanying error message will explain why.",
        404: "Error 404: Not Found: The URI requested is invalid or the "
        "resource requested, such as a category, does not exists.",
        500: "Error 500: Internal Server Error: Something is broken.",
        503: "Error 503: Service Unavailable.",
    }

def set_headers() -> dict:
    """Sets the headers for a TNS search.

    Returns
    -------
    headers: TNS headers
    """
    headers = {
        "User-Agent": 'tns_marker{"tns_id": "' + str(TNS_ID) + '", "type": "bot",'
        ' "name": "' + str(TNS_BOT_NAME) + '"}'
    }
    return headers
    
def validate_response(response: requests.Response) -> dict | None:
    """Checks if the content was retrieved.

    Parameters
    ----------
    response : Response object from TNS.

    Returns
    -------
    data: target's data.
    """
    response.raise_for_status()
    # check status
    if response.status_code == 200:
        data = response.json()['data']
        if isinstance(data, list):
            if 'objname' not in data[0]:
                print("Object not found")
                return None
        else:
            if 'objname' not in data:
                print("Object not found")
                return None
        return data
    else:
        global http_errors
        print('Response error:', http_errors[response.status_code])
        print(response.url)
        return None
    
def dict_to_dataframe(obj_dict: dict) -> pd.DataFrame:
    """Converts a TNS data dictionary into a dataframe.

    Parameters
    ----------
    obj_dict: Object's data.
    
    Returns
    -------
    obj_df: Object's dataframe.
    """
    new_dict = {key:[] for key in obj_dict[0].keys()}
    for epoch in obj_dict:
        for key, value in epoch.items():
            if isinstance(value, dict):
                new_dict[key].append(value["name"])
            else:
                new_dict[key].append(value)
    obj_df = pd.DataFrame(new_dict)
    return obj_df
