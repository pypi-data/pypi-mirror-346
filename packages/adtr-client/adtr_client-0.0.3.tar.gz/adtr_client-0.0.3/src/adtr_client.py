from requests import Session
import logging


def translate(
    user_id: int,
    api_key: str,
    text: str,
    target_language: str = "russian",
    timeout: int = 30,
    verbose: bool = False,
) -> str:
    """
    Translate text to the specified target language.

    Args:
        user_id: User ID from rkn.name service
        api_key: Api key from rkn.name service
        text (str): Text to translate (max 300 characters)
        target_language (str, optional): Target language for translation. Defaults to "russian".
        timeout (int, optional): Request timeout in seconds. Defaults to 30.
        verbose (bool, optional): Enable verbose output for debugging. Defaults to False.

    Returns:
        str: translated text

    Raises:
        requests.exceptions.HTTPError: If the API returns an error
        ValueError: If input validation fails
    """
    if verbose:
        print(f"[DEBUG] Starting translation request")
        print(
            f"[DEBUG] Parameters: text length={len(text)}, target_language={target_language}"
        )

    if not text.strip():
        if verbose:
            print(f"[DEBUG] Error: Empty text provided")
        raise ValueError("Text cannot be empty")

    if len(text) > 300:
        if verbose:
            print(f"[DEBUG] Error: Text exceeds maximum length (300 characters)")
        raise ValueError("Text must be 300 characters or less")

    base_url = "https://aitr.webnova.one"
    endpoint = f"{base_url}/translate"

    payload = {
        "user_id": user_id,
        "api_key": api_key,
        "text": text,
        "target_language": target_language,
    }

    if verbose:
        print(f"[DEBUG] Endpoint: {endpoint}")
        print(f"[DEBUG] Payload: {payload}")

    session = Session()

    if verbose:
        print(f"[DEBUG] Sending POST request")

    response = session.post(endpoint, json=payload, timeout=timeout)

    if verbose:
        print(f"[DEBUG] Response status code: {response.status_code}")
        print(f"[DEBUG] Response headers: {response.headers}")

    try:
        response.raise_for_status()
    except Exception as e:
        if verbose:
            print(f"[DEBUG] Error occurred: {str(e)}")
            print(f"[DEBUG] Response content: {response.text}")
        raise

    data = response.json()

    if verbose:
        print(f"[DEBUG] Response data: {data}")
        print(f"[DEBUG] Translation completed successfully")

    return data["result"]
