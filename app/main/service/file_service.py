import logging
from datetime import datetime, timedelta

import azure.core.exceptions
import requests
import xmltodict
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from flask import current_app


def check_blob_status():
    """Check if the blob storage is available.

    :return: A tuple containing the status and the message.
    """
    try:
        connection_string = current_app.config["AZURE_STORAGE_CONNECTION_STRING"]
        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )
        blob_service_client.close()

        return True, "Blob storage is available."
    except Exception as e:
        return False, str(e)


def upload_filestream_to_blob(filename: str, filestream) -> str:
    logging.info("Uploading file : " + filename)
    connection_string = current_app.config["AZURE_STORAGE_CONNECTION_STRING"]
    blob_service_client_settings = {
        "max_single_put_size": 64 * 1024 * 1024,  # split to 4MB chunks`
        "max_single_get_size": 64 * 1024 * 1024,  # split to 4MB chunks
    }
    blob_service_client = BlobServiceClient.from_connection_string(
        connection_string, **blob_service_client_settings
    )
    blob_client = blob_service_client.get_blob_client(
        container=current_app.config["AZURE_STORAGE_BLOB_NAME_FOR_STAC_ITEMS"],
        blob=filename,
    )
    try:
        blob_client.upload_blob(filestream, overwrite=False)
        return "File uploaded successfully."
    except azure.core.exceptions.ResourceExistsError:
        raise FileExistsError
    finally:
        blob_service_client.close()


def return_file_url(filename: str):
    connection_string = current_app.config["AZURE_STORAGE_CONNECTION_STRING"]
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_name = current_app.config["AZURE_STORAGE_BLOB_NAME_FOR_STAC_ITEMS"]

    try:
        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=filename
        )
        return blob_client.url
    except azure.core.exceptions.ResourceNotFoundError:
        blob_service_client.close()
        raise FileNotFoundError
    finally:
        blob_service_client.close()


def retrieve_file(file_url: str):
    try:
        _, file_url_with_sas_read_token = get_read_sas_token(file_url)
        response = requests.get(file_url_with_sas_read_token)
        response.raise_for_status()
        try:
            return response.json()
        except:
            return xmltodict.parse(response.content)

    except requests.exceptions.HTTPError as http_err:
        raise http_err
    except Exception as err:
        raise err


def get_write_sas_token(filename: str):
    connection_string = current_app.config["AZURE_STORAGE_CONNECTION_STRING"]
    account_key = connection_string.split("AccountKey=")[1].split(";")[0]
    connection_string_split = connection_string.split(";")
    azure_params = {}
    for param in connection_string_split:
        param_split = param.split("=")
        azure_params[param_split[0]] = param_split[1]
    azure_params["AccountKey"] = account_key
    account_name = azure_params["AccountName"]
    account_key = azure_params["AccountKey"]
    endpoint_suffix = azure_params["EndpointSuffix"]
    container_name = current_app.config["AZURE_STORAGE_BLOB_NAME_FOR_STAC_ITEMS"]
    blob_name = filename

    sas_token = generate_blob_sas(
        account_name=account_name,
        account_key=account_key,
        container_name=container_name,
        blob_name=blob_name,
        permission=BlobSasPermissions(write=True),
        expiry=datetime.utcnow() + timedelta(hours=1),
    )

    blob_url = f"https://{account_name}.blob.{endpoint_suffix}/{container_name}/{blob_name}?{sas_token}"
    return sas_token, blob_url


def get_read_sas_token(filename: str):
    # if filename begins with http, it is url, only take the filename
    if filename.startswith("http"):
        filename = filename.split("/")[-1]

    connection_string = current_app.config["AZURE_STORAGE_CONNECTION_STRING"]
    account_key = connection_string.split("AccountKey=")[1].split(";")[0]
    connection_string_split = connection_string.split(";")
    azure_params = {}
    for param in connection_string_split:
        param_split = param.split("=")
        azure_params[param_split[0]] = param_split[1]
    azure_params["AccountKey"] = account_key
    account_name = azure_params["AccountName"]
    account_key = azure_params["AccountKey"]
    endpoint_suffix = azure_params["EndpointSuffix"]
    container_name = current_app.config["AZURE_STORAGE_BLOB_NAME_FOR_STAC_ITEMS"]
    # create read sas token
    sas_token = generate_blob_sas(
        account_name=account_name,
        account_key=account_key,
        container_name=container_name,
        blob_name=filename,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1),
    )
    return sas_token, f"https://{account_name}.blob.{endpoint_suffix}/{container_name}/{filename}?{sas_token}"
