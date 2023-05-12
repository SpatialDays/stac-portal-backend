from datetime import datetime, timedelta

from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from flask import current_app


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
    blob_url_without_sas_token = f"https://{account_name}.blob.{endpoint_suffix}/{container_name}/{blob_name}"
    return sas_token, blob_url, blob_url_without_sas_token


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

    return sas_token, f"https://{account_name}.blob.{endpoint_suffix}/{container_name}/{filename}?{sas_token}", f"https://{account_name}.blob.{endpoint_suffix}/{container_name}/{filename}"
