from dotenv import load_dotenv

load_dotenv()


def handle_response(response) -> any:
    """ Helper function to handle common response logic. """
    if response.ok:
        content_type_ = response.headers.get('Content-Type', '')
        parsed_response = response.json() if 'application/json' in content_type_ else response.text
        return parsed_response
    else:
        raise ValueError(f"HTTP Error {response.status_code}: {response.reason} {response.text}")
