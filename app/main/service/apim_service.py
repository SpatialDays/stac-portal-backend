import requests
import json
import logging
from flask import current_app
from typing import Dict, Any
from ..custom_exceptions import *


def get_apim_auth_token():
    tenant_id = current_app.config["APIM_CONFIG_APIM_TENANT_ID"]
    client_id = current_app.config["APIM_CONFIG_APIM_SERVICE_PRINCIPAL_CLIENT_ID"]
    client_secret = current_app.config["APIM_CONFIG_APIM_SERVICE_PRINCIPAL_CLIENT_SECRET"]
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    body = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'resource': "https://management.azure.com/"
    }

    response = requests.post(url, headers=headers, data=body)
    response.raise_for_status()  # raise exception if the request failed
    res_json = response.json()
    return res_json["access_token"]


def create_user_on_apim(user_id: str, email: str, first_name: str, last_name: str) -> Dict[str, Any]:
    """
    Creates a user on APIM.

    Args:
        user_id (str): Unique identifier for the user.
        email (str): User's email (must be unique).
        first_name (str): First name of the user.
        last_name (str): Last name of the user.

    Returns:
        Dict[str, str]: Newly created user details.

    Examples:
        >>> print(create_user_on_apim("123-unique-id-for-subscription-123", "test.user@spatialdays.com", "test", "user"))
        {
           "id":"<redacted>",
           "type":"Microsoft.ApiManagement/service/users",
           "name":"123-unique-id-for-subscription-123",
           "properties":{
              "firstName":"test",
              "lastName":"user",
              "email":"test.user@spatialdays.com",
              "state":"active",
              "registrationDate":"2023-06-01T09:33:15.997Z",
              "note":"None",
              "groups":[
                 {
                    "id":"<redacted>",
                    "name":"Developers",
                    "description":"Developers is a built-in group. Its membership is managed by the system. Signed-in users fall into this group.",
                    "builtIn":true,
                    "type":"system",
                    "externalId":"None"
                 }
              ],
              "identities":[
                 {
                    "provider":"Basic",
                    "id":"test.user@spatialdays.com"
                 }
              ]
           }
        }
    """
    subscription_id = current_app.config["APIM_CONFIG_APIM_SUBSCRIPTION_ID"]
    rg_name = current_app.config["APIM_CONFIG_APIM_RESOURCE_GROUP_NAME"]
    apim_name = current_app.config["APIM_CONFIG_APIM_NAME"]
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{rg_name}/providers/Microsoft.ApiManagement/service/{apim_name}/users/{user_id}?api-version=2022-08-01"

    headers = {
        "Authorization": f"Bearer {get_apim_auth_token()}",
        "Content-Type": "application/json",
    }

    body = json.dumps({
        "properties": {
            "email": email,
            "firstName": first_name,
            "lastName": last_name
        }
    })

    response = requests.put(url, headers=headers, data=body)

    if response.status_code == 200:
        raise APIMUserAlreadyExistsError(
            f"User with id {user_id} already exists. Status code: {response.status_code}, Response: {response.text}")
    elif response.status_code == 201:
        logging.info(f"User with id {user_id} created successfully")
        return response.json()
    else:
        raise APIMUserCreationError(
            f"Failed to create user. Status code: {response.status_code}, Response: {response.text}")


def get_user_from_apim(user_id: str) -> Dict[str, Any]:
    """
    Gets a user from APIM

    Args:
        user_id: The unique identifier of the user

    Returns:
        Dict[str, str]: Details of the user from APIM

    Examples:
        >>> print(get_user_from_apim("123-unique-id-for-subscription-123"))
        {
            'id': '/subscriptions/<redacted>/resourceGroups/<redacted>/providers/Microsoft.ApiManagement/service/<redacted>/users/123-unique-id-for-subscription-123',
            'type': 'Microsoft.ApiManagement/service/users',
            'name': '123-unique-id-for-subscription-123',
            'properties': {
                'firstName': 'test',
                'lastName': 'user',
                'email': 'test.user@spatialdays.com',
                'state': 'active',
                'registrationDate': '2023-06-01T09:33:15.997Z',
                'note': None,
                'identities': [{
                    'provider': 'Basic',
                    'id': 'test.user@spatialdays.com'
                }]
            }
        }
    """
    subscription_id = current_app.config["APIM_CONFIG_APIM_SUBSCRIPTION_ID"]
    rg_name = current_app.config["APIM_CONFIG_APIM_RESOURCE_GROUP_NAME"]
    apim_name = current_app.config["APIM_CONFIG_APIM_NAME"]
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{rg_name}/providers/Microsoft.ApiManagement/service/{apim_name}/users/{user_id}?api-version=2022-08-01"

    headers = {
        "Authorization": f"Bearer {get_apim_auth_token()}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise APIMUserNotFoundError(
            f"User with id {user_id} not found. Status code: {response.status_code}, Response: {response.text}")


def delete_user_from_apim(user_id: str) -> str:
    """
    Deletes a user from APIM

    Args:
        user_id: The unique identifier of the user to be deleted

    Returns:
        str: The user_id of the deleted user

    Examples:
        >>> print(delete_user_from_apim("123-unique-id-for-subscription-123"))
        123-unique-id-for-subscription-123
    """

    subscription_id = current_app.config["APIM_CONFIG_APIM_SUBSCRIPTION_ID"]
    rg_name = current_app.config["APIM_CONFIG_APIM_RESOURCE_GROUP_NAME"]
    apim_name = current_app.config["APIM_CONFIG_APIM_NAME"]
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{rg_name}/providers/Microsoft.ApiManagement/service/{apim_name}/users/{user_id}?api-version=2022-08-01"

    headers = {
        "Authorization": f"Bearer {get_apim_auth_token()}",
        "Content-Type": "application/json",
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        return user_id
    elif response.status_code == 204:
        raise APIMUserNotFoundError(
            f"User with id {user_id} not found or couldn't be deleted. Status code: {response.status_code}, Response: {response.text}")
    else:
        raise APIMUserNotFoundError(
            f"User with id {user_id} not found or couldn't be deleted. Status code: {response.status_code}, Response: {response.text}")


def make_subscription_for_user_on_all_apis(user_id: str) -> Dict[str, Any]:
    """
    Makes a subscription for a user on all APIs

    Args:
        user_id: The unique identifier of the user to be subscribed on all APIs.

    Returns:
        dict: A dictionary containing subscription information.

    Examples:
        >>> print(make_subscription_for_user_on_all_apis("123-unique-id-for-subscription-123"))
        {
            'id': '/subscriptions/<redacted>/resourceGroups/<redacted>/providers/Microsoft.ApiManagement/service/<redacted>/subscriptions/123-unique-id-for-subscription-123',
            'type': 'Microsoft.ApiManagement/service/subscriptions',
            'name': '123-unique-id-for-subscription-123',
            'properties': {
                'ownerId': '/subscriptions/<redacted>/resourceGroups/<redacted>/providers/Microsoft.ApiManagement/service/<redacted>/users/123-unique-id-for-subscription-123',
                'user': {
                    'id': '/subscriptions/<redacted>/resourceGroups/<redacted>/providers/Microsoft.ApiManagement/service/<redacted>/users/123-unique-id-for-subscription-123',
                    'firstName': 'test',
                    'lastName': 'user',
                    'email': 'test.user@spatialdays.com',
                    'state': 'active',
                    'registrationDate': '2023-06-01T09:33:15.997Z',
                    'note': None,
                    'groups': [],
                    'identities': []
                },
                'scope': '/subscriptions/<redacted>/resourceGroups/<redacted>/providers/Microsoft.ApiManagement/service/<redacted>/apis',
                'displayName': '123-unique-id-for-subscription-123',
                'state': 'active',
                'createdDate': '2023-06-01T09:37:51.0432183Z',
                'startDate': '2023-06-01T00:00:00Z',
                'expirationDate': None,
                'endDate': None,
                'notificationDate': None,
                'primaryKey': '<redacted>',
                'secondaryKey': '<redacted>',
                'stateComment': None,
                'allowTracing': False
            }
        }
    """

    subscription_id = current_app.config["APIM_CONFIG_APIM_SUBSCRIPTION_ID"]
    rg_name = current_app.config["APIM_CONFIG_APIM_RESOURCE_GROUP_NAME"]
    apim_name = current_app.config["APIM_CONFIG_APIM_NAME"]

    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{rg_name}/providers/Microsoft.ApiManagement/service/{apim_name}/subscriptions/{user_id}?api-version=2022-08-01"

    headers = {
        "Authorization": f"Bearer {get_apim_auth_token()}",
        "Content-Type": "application/json",
    }

    body = json.dumps({
        "properties": {
            "scope": "/apis",
            "displayName": user_id,
            "state": "active",
            "ownerId": f"/users/{user_id}",
        }
    })

    response = requests.put(url, headers=headers, data=body)

    if response.status_code == 201:
        return response.json()
    elif response.status_code == 200:
        raise APIMSubscriptionAlreadyExistsError(
            f"Subscription for user with id {user_id} already exists. Status code: {response.status_code}, Response: {response.text}")
    else:
        raise APIMSubscriptionCreationError(
            f"Failed to create subscription. Status code: {response.status_code}, Response: {response.text}")


def get_subscription_for_user(user_id: str) -> Dict[str, Any]:
    """
    Retrieves a subscription for a user from the API Management (APIM) service.

    Args:
        user_id (str): The unique identifier of the user for whom the subscription is to be retrieved.


    Returns:
        dict: A dictionary containing the details of the user's subscription. This includes the subscription ID, type,
        name, associated properties such as owner ID, scope, display name, state, creation date, start date, expiration date,
        end date, notification date, state comment and whether tracing is allowed.

    Examples:
        >>> print(get_subscription_for_user("123-unique-id-for-subscription-123"))
        {
            'id': '/subscriptions/<redacted>/resourceGroups/<redacted>/providers/Microsoft.ApiManagement/service/<redacted>/subscriptions/123-unique-id-for-subscription-123',
            'type': 'Microsoft.ApiManagement/service/subscriptions',
            'name': '123-unique-id-for-subscription-123',
            'properties': {
                'ownerId': '/subscriptions/<redacted>/resourceGroups/<redacted>/providers/Microsoft.ApiManagement/service/<redacted>/users/123-unique-id-for-subscription-123',
                'scope': '/subscriptions/<redacted>/resourceGroups/<redacted>/providers/Microsoft.ApiManagement/service/<redacted>/apis',
                'displayName': '123-unique-id-for-subscription-123',
                'state': 'active',
                'createdDate': '2023-06-01T09:37:51.043Z',
                'startDate': '2023-06-01T00:00:00Z',
                'expirationDate': None,
                'endDate': None,
                'notificationDate': None,
                'stateComment': None,
                'allowTracing': False
            }
        }
    """
    subscription_id = current_app.config["APIM_CONFIG_APIM_SUBSCRIPTION_ID"]
    rg_name = current_app.config["APIM_CONFIG_APIM_RESOURCE_GROUP_NAME"]
    apim_name = current_app.config["APIM_CONFIG_APIM_NAME"]

    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{rg_name}/providers/Microsoft.ApiManagement/service/{apim_name}/subscriptions/{user_id}?api-version=2022-08-01"

    headers = {
        "Authorization": f"Bearer {get_apim_auth_token()}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise APIMSubscriptionNotFoundError(
            f"Subscription for user with id {user_id} not found. Status code: {response.status_code}, Response: {response.text}")


def get_subscription_secrets_for_user(user_id: str) -> Dict[str, str]:
    """
    Retrieves the primary and secondary keys for a user's subscription from the API Management (APIM) service.

    Args:
        user_id (str): The unique identifier of the user for whom the subscription keys are to be retrieved.

    Returns:
        dict: A dictionary containing the primary and secondary keys for the user's subscription.

    Examples:
        >>> print(get_subscription_secrets_for_user("123-unique-id-for-subscription-123"))
        {
            'primaryKey': '<redacted>',
            'secondaryKey': '<redacted>'
        }
    """

    subscription_id = current_app.config["APIM_CONFIG_APIM_SUBSCRIPTION_ID"]
    rg_name = current_app.config["APIM_CONFIG_APIM_RESOURCE_GROUP_NAME"]
    apim_name = current_app.config["APIM_CONFIG_APIM_NAME"]

    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{rg_name}/providers/Microsoft.ApiManagement/service/{apim_name}/subscriptions/{user_id}/listSecrets?api-version=2022-08-01"

    headers = {
        "Authorization": f"Bearer {get_apim_auth_token()}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise APIMSubscriptionNotFoundError(
            f"Subscription for user with id {user_id} not found. Status code: {response.status_code}, Response: {response.text}")


def delete_subscription_for_user(user_id: str) -> str:
    """
    Deletes a subscription for a user in the API Management (APIM) service.

    Args:
        user_id (str): The unique identifier of the user for whom the subscription is to be deleted.

    Returns:
        str: The unique identifier of the user for whom the subscription was deleted.

    Examples:
        >>> print(delete_subscription_for_user("123-unique-id-for-subscription-123"))
        '123-unique-id-for-subscription-123'
    """

    subscription_id = current_app.config["APIM_CONFIG_APIM_SUBSCRIPTION_ID"]
    rg_name = current_app.config["APIM_CONFIG_APIM_RESOURCE_GROUP_NAME"]
    apim_name = current_app.config["APIM_CONFIG_APIM_NAME"]

    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{rg_name}/providers/Microsoft.ApiManagement/service/{apim_name}/subscriptions/{user_id}?api-version=2022-08-01"

    headers = {
        "Authorization": f"Bearer {get_apim_auth_token()}",
        "Content-Type": "application/json",
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        return user_id
    elif response.status_code == 204:
        raise APIMSubscriptionNotFoundError(
            f"Subscription for user with id {user_id} not found or couldn't be deleted. Status code: {response.status_code}, Response: {response.text}")
    else:
        raise APIMSubscriptionNotFoundError(
            f"Subscription for user with id {user_id} not found or couldn't be deleted. Status code: {response.status_code}, Response: {response.text}")


def regenerate_subscription_for_user(user_id: str) -> str:
    """
    Regenerates the subscription keys for a user in the API Management (APIM) service.

    Args:
        user_id (str): The unique identifier of the user for whom the subscription keys are to be regenerated.

    Returns:
        str: The unique identifier of the user for whom the subscription keys were regenerated.

    Examples:
        >>> print(regenerate_subscription_for_user("123-unique-id-for-subscription-123"))
        '123-unique-id-for-subscription-123'
    """

    subscription_id = current_app.config["APIM_CONFIG_APIM_SUBSCRIPTION_ID"]
    rg_name = current_app.config["APIM_CONFIG_APIM_RESOURCE_GROUP_NAME"]
    apim_name = current_app.config["APIM_CONFIG_APIM_NAME"]

    urls = [
        f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{rg_name}/providers/Microsoft.ApiManagement/service/{apim_name}/subscriptions/{user_id}/regeneratePrimaryKey?api-version=2022-08-01",
        f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{rg_name}/providers/Microsoft.ApiManagement/service/{apim_name}/subscriptions/{user_id}/regenerateSecondaryKey?api-version=2022-08-01"
    ]

    headers = {
        "Authorization": f"Bearer {get_apim_auth_token()}",
        "Content-Type": "application/json",
    }
    responses = []
    for url in urls:
        response = requests.post(url, headers=headers)
        responses.append(response)

    if all(response.status_code == 204 for response in responses):
        return user_id
    else:
        raise APIMSubscriptionKeyRefreshError(
            f"Failed to refresh subscription keys for user with id {user_id}. Status codes: {[response.status_code for response in responses]}, Responses: {[response.text for response in responses]}")
