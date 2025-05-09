# gologin_api

Tiny wrapper for GoLogin profile + fingerprint management via pre-deployed Google Apps Script Web-Apps.

## Install

```bash
pip install gologin_api
```

## Usage

```python
from gologin_api import get_profiles, change_fingerprint, create_profile

token = "YOUR_API_TOKEN"

# 1) Lấy profiles
profiles = get_profiles(token)
print(profiles)

# 2) Đổi fingerprint
res = change_fingerprint(token, profiles[0]["id"])
print(res)

# 3) Tạo profile mới
new = create_profile(token, name="TestProfile", proxy="host:port:user:pass")
print(new)
```

## Development

1. Install build tools:
   ```bash
   pip install build twine
   ```

2. Build package:
   ```bash
   python -m build
   ```

3. Upload to PyPI:
   ```bash
   twine upload dist/*
   ```

4. Local installation:
   ```bash
   pip install .
   ```
