import requests

# Hard-code sẵn các URL web-app từ .env
GOLOGIN_LIST_URL       = "https://script.google.com/macros/s/AKfycbw1XmQSIO6Vgbr1ztKdm0kM5PF8YURy6r4sVd6ZOedgf7orP2KqJhwOdvGRqwXNz4wZAQ/exec?token="
API_FINGERPRINT_URL    = "https://script.google.com/macros/s/AKfycbyEhtLTkvt7D8twZH5vyk9W87-aIctXVemwOgw11VEQ6hA73-4oWmTJ2AX_uzwVWYmdZg/exec?token="
API_CREATE_PROFILE_URL = "https://script.google.com/macros/s/AKfycbzM17y9UFaT67bpixYhqlCC9Vy3ve6zlW3Jk88p_qsUvO3E0BZnPAUtPi3pTuyfsufn/exec?token="

def get_profiles(token: str) -> list:
    """Lấy list profile từ GoLogin."""
    resp = requests.get(GOLOGIN_LIST_URL + token)
    resp.raise_for_status()
    return resp.json().get("profiles", [])

def change_fingerprint(token: str, profile_id: str) -> dict:
    """Đổi fingerprint cho profile_id."""
    url = API_FINGERPRINT_URL + token + "&id=" + profile_id
    resp = requests.get(url)
    resp.raise_for_status()
    try:
        return resp.json()
    except ValueError:
        return {"result": resp.text}

def create_profile(token: str, name: str, proxy: str = "") -> dict:
    """Tạo profile mới với name và proxy."""
    # quote nếu cần dấu cách, ký tự đặc biệt
    from requests.utils import quote
    url = (
        API_CREATE_PROFILE_URL
        + token
        + "&name="  + quote(name)
        + "&proxy=" + quote(proxy)
    )
    resp = requests.get(url)
    resp.raise_for_status()
    try:
        return resp.json()
    except ValueError:
        return {"result": resp.text}
