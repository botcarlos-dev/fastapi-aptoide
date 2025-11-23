# fastapi-aptoide

A simple FastAPI service for the Aptoide coding challenge, fetching and formatting metadata for Android apps from Aptoide.

---

## Requirements

- Python 3.9+
- Git (optional, for cloning the repo)

---

## Setup

1. **Clone the repository (if using Git)**

```bash
git clone https://github.com/botcarlos-dev/fastapi-aptoide.git
cd fastapi-aptoide
```

2. **Create a virtual environment**

```bash
python3 -m venv venv
```

3. **Activate the virtual environment**

- On Linux/macOS:

```bash
source venv/bin/activate
```

- On Windows:

```bash
venv\Scripts\activate
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## Running the API

```bash
uvicorn app.main:app --reload
```

- The API will be available at: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## API Endpoint

### GET `/aptoide?package_name=<package_id>`

**Query parameter:**

- `package_name` → The app’s package ID (e.g., `com.facebook.katana`)

**Example Request:**

```
GET /aptoide?package_name=com.facebook.katana
```

**Example Response:**

```json
{
  "name": "Facebook",
  "size": "152 MB",
  "downloads": "2B",
  "version": "532.0.0.55.71",
  "release_date": "2025-09-30 17:06:59",
  "min_screen": "SMALL",
  "supported_cpu": "arm64-v8a",
  "package_id": "com.facebook.katana",
  "sha1_signature": "8A:3C:4B:26:2D:72:1A:CD:49:A4:BF:97:D5:21:31:99:C8:6F:A2:B9",
  "developer_cn": "Facebook Corporation",
  "organization": "Facebook Mobile",
  "local": "Palo Alto",
  "country": "US",
  "state_city": "CA"
}
```

---

## Running Tests

1. Make sure the virtual environment is activated.
2. Run:

```bash
pytest -v
```

All tests are located in `tests/test_api.py`.

---

## Notes

- Only the first result from Aptoide search is returned.
- Certificate metadata is parsed if available.
- Uses Pydantic models for validation and response consistency.
- This project is specifically built for the Aptoide coding challenge.

