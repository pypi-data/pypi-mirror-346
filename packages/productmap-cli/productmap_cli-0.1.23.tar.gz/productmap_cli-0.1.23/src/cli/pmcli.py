import json
import os
import click
import httpx

from http import HTTPStatus

PRODUCT_MAP_DOMAIN_URL = "https://product-map.ai"
PRODUCT_MAP_API_DOMAIN_URL = "https://api.product-map.ai"

# PRODUCT_MAP_DOMAIN_URL = "http://localhost:5173"
# PRODUCT_MAP_API_DOMAIN_URL = "http://localhost:8000"

WORKFLOW_VALIDATE_PATH = "/llm/upload/workflow/validate"
WORKFLOW_GENERATE_PATH = "/llm/upload/workflow"
WORKFLOW_ANALYZE_REQUIREMENTS_PATH = "/llm/upload/workflow"
WORKFLOW_SHARE_PATH = "/llm/upload/workflow/share"

VALIDATE_PATH = "/llm/upload/validate"
GENERATE_PATH = "/llm/upload"
SHARE_PATH = "/llm/upload/share"

EXTENDED_TIMEOUT = 10
EXTENDED_REQUIREMENT_ANALYSIS_TIMEOUT = 100000
SECRET_KEY = "PM129037XASDF"
def get_payload(username: str, email: str, url:str) -> dict:
    """
    Generate the payload for the Request
    :param username: Username
    :param email: Email
    :return: Encoded string
    """
    return {
        "sub": f"github/{username}",
        "email": email,
        "username": username,
        "url": url,
    }


def read_file(ctx: click.Context, file_path: str) -> None:
    """
    Read the file from the given path
    :param ctx: Click context
    :param file_path: File path
    :return: None
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_path}' does not exist.")

        # Read the file as binary
        with open(file_path, 'rb') as file:
            file.read()
            file_size = os.path.getsize(file_path)
            click.echo(f"File '{file_path}' successfully read! Size: {file_size} bytes.")

    except FileNotFoundError as e:
        ctx.fail(str(e))
    except Exception as e:
        ctx.fail(f"An unexpected error occurred: {e}")


def set_map_sharing_status_auth(ctx: click.Context, salt: str, is_shared: bool, token: str) -> None:
    """
    Set the sharing status of the map
    :param ctx: Click context
    :param salt: Map salt
    :param is_shared: Sharing status
    :param optional token: Auth token
    :return: None
    """

    url = f"{PRODUCT_MAP_API_DOMAIN_URL}{SHARE_PATH}/{salt}"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "shared": is_shared
    }

    request_map_sharing_status_change(ctx, url, payload, headers)


def request_map_sharing_status_change(ctx: click.Context, url: str, payload: dict,
                                      headers: dict | None = None) -> None:
    """
    Request the map sharing status change to the API
    :param ctx: Click context
    :param url: ProductMap API URL
    :param optional headers: Headers for the request
    :param payload: Payload for the request
    :return:
    """

    click.secho(f"Setting public sharing status to : {payload.get('shared')}")
    try:
        # Open the file and send it to the API
        response = httpx.put(
            url,
            headers=headers,
            json=payload,
            timeout=EXTENDED_TIMEOUT,
        )

        if response.status_code != HTTPStatus.OK:
            raise click.ClickException(
                f"Failed to switching sharing status. Server response: {response.text}"
            )

        map_status = "Public" if payload.get("shared") is True else "Restricted"
        click.secho(f"Public map status set to {map_status}", fg="green")

    except Exception as e:
        ctx.fail(f"An error occurred during validation: {e}")


def validate_file_auth(ctx: click.Context, file: str, token: str) -> str:
    """
    Validate the file to identify if it is a valid file for map generation
    :param ctx: Click context
    :param file: File URL
    :param token: Auth token
    :return: Validation result
    """
    url = f"{PRODUCT_MAP_API_DOMAIN_URL}{VALIDATE_PATH}"
    headers = {"Authorization": f"Bearer {token}"}

    return request_validate_file_auth(ctx, file, url, headers)


def request_validate_file_auth(ctx: click.Context, file: str, url: str, headers: dict | None = None) -> str:
    """
    Request the file validation to the API
    :param ctx: Click context
    :param file: File path
    :param url: ProductMap API URL
    :param optional headers: Headers for the request
    :return: Validation result
    """
    click.secho(f"Validating file {file}")
    read_file(ctx, file)

    try:
        # Open the file and send it to the API
        with open(file, "rb") as f:
            response = httpx.post(
                url,
                headers=headers,
                files={"file": f},
                timeout=EXTENDED_TIMEOUT,
            )

        if response.status_code != HTTPStatus.OK:
            raise click.ClickException(
                f"Failed to validate file '{file}'. Server response: {response.text}"
            )

        click.secho(f"File '{file}' validated successfully!")
        return response.text

    except Exception as e:
        ctx.fail(f"An error occurred during validation: {e}")


def generate_map_auth(ctx: click.Context, file: str, token: str) -> str:
    """
    Generate the map for the given file
    :param ctx: Click context
    :param file: File path
    :param username: Username
    :param email: Email
    :param optional token: Auth token
    :return: Map generation result
    """
    url = f"{PRODUCT_MAP_API_DOMAIN_URL}{GENERATE_PATH}"
    headers = {"Authorization": f"Bearer {token}"}

    return request_generate_map_auth(ctx, file, url, token, headers)


def request_generate_map_auth(ctx: click.Context, file: str, url: str, token: str = None, headers: dict | None = None) -> str:
    """
    Request the map generation to the API
    :param ctx: Click context
    :param file: File path
    :param url: URL for the map generation API
    :param optional headers: Headers for the request
    :param token: Auth token
    :return: Map generation result
    """
    click.secho(f"Generating map for file: {file}")
    read_file(ctx, file)

    try:
        # Send the file to the map generation API
        with open(file, "rb") as f:
            response = httpx.post(
                url,
                headers=headers,
                files={"file": f},
                timeout=EXTENDED_TIMEOUT,
            )
        if response.status_code != HTTPStatus.OK:
            raise click.ClickException(
                f"Failed to generate map from file '{file}'. Server response: {response.text}"
            )

        # Parse response and construct output
        json_data = response.json()
        salt = json_data.get("salt")
        public_salt = json_data.get("public_salt")
        status_name = json_data.get("status_name")
        public_url = f"{PRODUCT_MAP_DOMAIN_URL}/app/public/{public_salt}"
        url = f"{PRODUCT_MAP_DOMAIN_URL}/app/{salt}"

        set_map_sharing_status_auth(
            ctx,
            salt,
            is_shared=True,
            token=token,
        )
        click.secho(f"Map being processed for file '{file}'.", fg="blue")
        click.secho(f"Map can be visualized once the generation process finishes...", fg="blue")
        click.echo(json.dumps({
            "salt": salt,
            "url": url,
            "public_url": public_url,
            "status_name": status_name
        }))

    except Exception as e:
        click.echo(json.dumps({
            "status": "error",
            "message": "An error occurred during map generation request.",
            "details": str(e)
        }))


def get_map_generation_status(token: str, salt: str):
    """
    Get the map generation status for the given salt
    :param token: Auth token
    :param salt: Map salt
    :return: Map generation status
    """
    try:
        response = httpx.get(
            f"{PRODUCT_MAP_API_DOMAIN_URL}/llm/upload/result/{salt}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=EXTENDED_TIMEOUT,
        )

        if response.status_code != HTTPStatus.OK:
            # Send structured error response
            click.echo(json.dumps({
                "status": "error",
                "message": f"Failed to get map generation status for salt '{salt}'.",
                "details": response.text
            }))
        data = response.json()
        status_name = data.get("status_name")
        public_url = f"{PRODUCT_MAP_DOMAIN_URL}/app/public/{data.get('public_salt')}"
        url = f"{PRODUCT_MAP_DOMAIN_URL}/app/{salt}"

        # Send structured success response
        click.echo(json.dumps({
            "salt": salt,
            "url": url,
            "public_url": public_url,
            "status_name": status_name
        }))

    except Exception as e:
        # Send structured error response for unexpected errors
        click.echo(json.dumps({
            "status": "error",
            "message": "An error occurred during map generation status retrieval.",
            "details": str(e)
        }))


def validate_file(ctx: click.Context, file_url: str, username: str, email: str) -> str:
    """
    Validate the file to identify if it is a valid file for map generation
    :param ctx: Click context
    :param file_url: File URL
    :param username: Username
    :param email: Email
    :return: Validation result
    """
    url = f"{PRODUCT_MAP_API_DOMAIN_URL}{WORKFLOW_VALIDATE_PATH}"
    payload = get_payload(username, email, file_url)

    return request_validate_file(ctx, url, payload)


def request_validate_file(ctx: click.Context, url: str, payload: dict) -> str:
    """
    Request the file validation to the API
    :param ctx: Click context
    :param url: ProductMap API URL
    :param payload: Payload for the request
    :return: Validation result
    """
    click.secho(f"Validating file {payload.get('url')}")

    try:
        # Open the file and send it to the API
        response = httpx.post(
            url,
            json=payload,
            timeout=EXTENDED_TIMEOUT,
        )

        if response.status_code != HTTPStatus.OK:
            raise click.ClickException(
                f"Failed to validate file '{payload.get('url')}'. Server response: {response.text}"
            )

        click.secho(f"File '{payload.get('url')}' validated successfully!")
        return response.text

    except Exception as e:
        ctx.fail(f"An error occurred during validation: {e}")


def generate_map(file_url: str, username: str, email: str) -> str:
    """
    Generate the map for the given file
    :param file_url: File URL
    :param username: Username
    :param email: Email
    :return: Map generation result
    """
    url = f"{PRODUCT_MAP_API_DOMAIN_URL}{WORKFLOW_GENERATE_PATH}"
    payload = get_payload(username, email, file_url)
    request_generate_map(url, payload)

def generate_map_analyze_requirements(file_url: str, username: str, email: str) -> str:
    """
    Generate the map and analyze requirements for the given repo URL
    :param file_url: File URL
    :param username: Username
    :param email: Email
    :return: Map generation result
    """
    url = f"{PRODUCT_MAP_API_DOMAIN_URL}{WORKFLOW_ANALYZE_REQUIREMENTS_PATH}"
    payload = get_payload(username, email, file_url)
    request_generate_map_analyze_requirements(url, payload)




def request_generate_map(url: str, payload: dict) -> None:
    """
    Request the map generation to the API
    :param url: URL for the map generation API
    :param payload: Payload for the request
    :return: Map generation result
    """
    click.secho(f"Generating map for file: {payload.get('url')}")

    try:
        # Send the file to the map generation API
        print(url)
        response = httpx.post(
            url,
            json=payload,
            timeout=EXTENDED_TIMEOUT,
        )
        if response.status_code != HTTPStatus.OK:
            raise click.ClickException(
                f"Failed to generate map from file '{payload.get('url')}'. Server response: {response.text}"
            )

        # Parse response and construct output
        json_data = response.json()
        salt = json_data.get("salt")
        status_name = json_data.get("status_name")
        public_url = f"{PRODUCT_MAP_DOMAIN_URL}/app/public?url={payload.get('url')}"
        url = f"{PRODUCT_MAP_DOMAIN_URL}/app/{salt}"

        click.secho(f"Map being processed for file '{payload.get('url')}'.", fg="blue")
        click.secho(f"Map can be visualized once the generation process finishes...", fg="blue")
        click.echo(json.dumps({
            "salt": salt,
            "url": url,
            "public_url": public_url,
            "status_name": status_name
        }))

    except Exception as e:
        click.echo(json.dumps({
            "status": "error",
            "message": "An error occurred during map generation request.",
            "details": str(e)
        }))


def request_generate_map_analyze_requirements(url: str, payload: dict) -> None:
    """
    Request the map generation to the API
    :param url: URL for the map generation API
    :param payload: Payload for the request
    :return: Map generation result
    """
    click.secho(f"Generating map for file: {payload.get('url')}")

    try:
        # Send the file to the map generation API
        print(url)
        response = httpx.post(
            url,
            json=payload,
            timeout=EXTENDED_REQUIREMENT_ANALYSIS_TIMEOUT,
        )
        if response.status_code != HTTPStatus.OK:
            raise click.ClickException(
                f"Failed to analyze requirements from repo URL '{payload.get('url')}'. Server response: {response.text}"
            )

        # Parse response and construct output
        json_data = response.json()

        click.secho(f"Map processed for URL '{payload.get('url')}'.", fg="blue")
        click.echo(json.dumps(json_data))

    except Exception as e:
        click.echo(json.dumps({
            "status": "error",
            "message": "An error occurred during requirement analysis request.",
            "details": str(e)
        }))
