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

- `package_name` → The app’s package ID (e.g., `com.whatsapp`)

**Example Request:**

```
GET /aptoide?package_name=com.whatsapp
```

**Example Response:**

```json
{
 "name": "WhatsApp Messenger",
  "size": "130 MB",
  "downloads": null,
  "version": "2.25.35.73",
  "release_date": null,
  "min_screen": null,
  "supported_cpu": null,
  "package_id": "com.whatsapp",
  "sha1_signature": "38:A0:F7:D5:05:FE:18:FE:C6:4F:BF:34:3E:CA:AA:F3:10:DB:D7:99",
  "developer_cn": "Brian Acton",
  "organization": "WhatsApp Inc.",
  "local": "Santa Clara",
  "country": "US",
  "state_city": "California"
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

