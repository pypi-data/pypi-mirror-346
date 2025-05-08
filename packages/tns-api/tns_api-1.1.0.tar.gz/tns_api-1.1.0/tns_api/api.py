import json
import requests
from pathlib import Path
from collections import OrderedDict
from tns_api.credentials import TNS_API_KEY
from tns_api.utils import (set_headers, validate_response, 
                           dict_to_dataframe)


def search(object_coords: dict | str) -> dict | None:
    """Looks for an object with the given coordinates.

    Parameters
    ----------
    object_info: Object's information.

    Returns
    -------
    object_data: Object's data.
    """
    url_tns_api = "https://www.wis-tns.org/api"
    search_url = url_tns_api + "/get/search"
    headers = set_headers()
    
    # create search object
    split_info = object_coords.split()
    if len(split_info) == 2:
        # assume coordinates
        search_obj = [("ra", split_info[0]), ("dec", split_info[1])]
    search_obj = OrderedDict(search_obj)
    
    search_data = {'api_key': TNS_API_KEY, 'data': json.dumps(search_obj)}
    response = requests.post(search_url, headers=headers, data=search_data)
    object_data = validate_response(response)[0]
    return object_data

def get_object(iau_name: str, photometry: bool=True, spectra: bool=True) -> dict | None:
    """Obtains the objects information.

    Parameters
    ----------
    iau_name: IAU name of the object (e.g. 2020xne).
    photometry: Whether to get photometry info.
    spectra: Whether to get spectra info.

    Returns
    -------
    object_data: Object's data.
    """
    url_tns_api = "https://www.wis-tns.org/api"
    search_url = url_tns_api + "/get/object"
    headers = set_headers()
    
    # create search object
    search_obj = [("objname", iau_name), ("photometry", photometry), ("spectra", spectra)]
    search_obj = OrderedDict(search_obj)
    
    search_data = {'api_key': TNS_API_KEY, 'data': json.dumps(search_obj)}
    response = requests.post(search_url, headers=headers, data=search_data)
    object_data = validate_response(response)
    return object_data

def get_photometry(iau_name: str, parent_dir: str=".") -> None:
    """Downloads the photometry for an object.

    Parameters
    ----------
    iau_name: Object's IAU name (e.g. 2004eo).
    parent_dir: Where to download the data.
    """
    phot_data = get_object(iau_name, photometry=True, spectra=False)["photometry"]
    phot_df = dict_to_dataframe(phot_data)
    # save spec info
    obj_dir = Path(parent_dir, iau_name)
    obj_dir.mkdir(parents=True, exist_ok=True)
    outfile = obj_dir / "phot_data.csv"
    phot_df.to_csv(outfile, index=False)
    
def get_spectra(iau_name: str, parent_dir: str=".", verbose: bool=True) -> None:
    """Downloads the spectra for an object.

    Parameters
    ----------
    iau_name: Object's IAU name (e.g. 2004eo).
    parent_dir: Where to download the data.
    verbose: Whether to print if the file was downloaded or not.
    """
    spec_data = get_object(iau_name, photometry=False, spectra=True)["spectra"]
    spec_df = dict_to_dataframe(spec_data)
    # save spec info
    obj_dir = Path(parent_dir, iau_name)
    obj_dir.mkdir(parents=True, exist_ok=True)
    outfile = obj_dir / "spectra.csv"
    spec_df.to_csv(outfile, index=False)
    # download files
    outdir = obj_dir / "spectra"
    outdir.mkdir(parents=True, exist_ok=True)
    for file_url in spec_df.asciifile.values:
        download_file(file_url, outdir, verbose)
        
def download_file(file_url, outdir, verbose: bool=True):
    """Downloads files from TNS.

    Parameters
    ----------
    file_url: File to download.
    outdir: Where to download the file.
    verbose: Whether to print if the file was downloaded or not.
    """
    headers = set_headers()
    api_data = {'api_key': TNS_API_KEY}
    response = requests.post(file_url, headers=headers, data=api_data, stream=True)    
    if response.status_code == 200:
        outfile = Path(outdir, file_url.split("/")[-1])
        with open(outfile, 'wb') as file:
            for chunk in response:
                file.write(chunk)
        if verbose:
            print (f"File was successfully downloaded: {file_url}\n")
    elif verbose:
        print (f"File was not downloaded: {file_url}\n")

