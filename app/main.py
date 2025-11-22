"""
Main FastAPI application for fetching app metadata from the Aptoide app store.

This service exposes a single endpoint:

    GET /aptoide?package_name=<package_id>

It retrieves data from the public Aptoide API, formats it, parses certificate
information, and returns a structured response using Pydantic models.
"""

from fastapi import FastAPI, HTTPException
import httpx
from .models import AppResponse

# Initialize FastAPI with metadata for automatic documentation
app = FastAPI(
    title="Aptoide Scraper API",
    description="A FastAPI service that fetches and formats app metadata from Aptoide.",
    version="1.0.0",
)

# Aptoide API endpoint
APTOIDE_URL = "https://ws75.aptoide.com/api/7/apps/search"


async def fetch_from_aptoide(package_name: str) -> dict:
    """
    Fetch raw JSON data from the Aptoide search API.

    Args:
        package_name (str): The app's package identifier.

    Returns:
        dict: Parsed JSON from the Aptoide API.

    Raises:
        HTTPException:
            - If the request cannot be completed.
            - If the remote server returns a non-200 status code.
    """
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            response = await client.get(APTOIDE_URL, params={"query": package_name})
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Connection error while requesting Aptoide: {str(e)}",
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail=f"Aptoide API error: HTTP {response.status_code}",
            )

        return response.json()


def format_size(bytes_value: int):
    """
    Convert a size in bytes into a human-readable representation.

    Examples:
        1048576 -> "1 MB"
        153600000 -> "147 MB"

    Args:
        bytes_value (int): File size in bytes.

    Returns:
        str | None: Human-readable size, or None if missing/invalid.
    """
    if not bytes_value:
        return None

    units = ["B", "KB", "MB", "GB"]
    size = float(bytes_value)

    for unit in units:
        if size < 1024:
            return f"{size:.0f} {unit}"
        size /= 1024

    return f"{size:.0f} TB"


def format_downloads(downloads: int):
    """
    Convert a download count into shorthand notation (K, M, B).

    Args:
        downloads (int): Raw number of downloads.

    Returns:
        str | None: Formatted download count or None.
    """
    if not downloads:
        return None

    if downloads >= 1_000_000_000:
        return f"{downloads / 1_000_000_000:.0f}B"
    if downloads >= 1_000_000:
        return f"{downloads / 1_000_000:.0f}M"
    if downloads >= 1_000:
        return f"{downloads / 1_000:.0f}K"

    return str(downloads)


def parse_certificate(cert_obj: dict) -> dict:
    """
    Parse the certificate 'owner' field returned by Aptoide into structured metadata.

    Example input string:
        "CN=Facebook Corporation, O=Facebook Mobile, L=Palo Alto, ST=CA, C=US"

    Args:
        cert_obj (dict): Certificate object containing fields like 'sha1' and 'owner'.

    Returns:
        dict: Parsed metadata including developer, organization, location, etc.
    """
    if not cert_obj or "owner" not in cert_obj:
        return {}

    owner = cert_obj["owner"]
    kv_pairs = {}

    # Break "key=value" pairs into a dictionary
    for kv in owner.split(","):
        if "=" in kv:
            key, value = kv.split("=", 1)
            kv_pairs[key.strip()] = value.strip()

    return {
        "developer_cn": kv_pairs.get("CN"),
        "organization": kv_pairs.get("O"),
        "local": kv_pairs.get("L"),
        "state_city": kv_pairs.get("ST"),
        "country": kv_pairs.get("C"),
    }


@app.get("/aptoide", response_model=AppResponse)
async def get_aptoide_app(package_name: str):
    """
    REST endpoint for fetching app metadata from Aptoide.

    Query Parameters:
        package_name (str): The app's package ID to look up.

    Returns:
        AppResponse: Pydantic model containing a normalized metadata response.

    Raises:
        HTTPException:
            - 404 if the app cannot be found.
            - Propagated exceptions from the Aptoide fetch process.
    """
    # Step 1: Request data from Aptoide
    data = await fetch_from_aptoide(package_name)

    # Step 2: Ensure at least one result exists
    apps = data.get("datalist", {}).get("list", [])
    if not apps:
        raise HTTPException(status_code=404, detail="Package not found")

    # Use the most relevant result (first entry)
    app_data = apps[0]
    file_data = app_data.get("file", {})
    signature = file_data.get("signature", {})

    # Step 3: Parse certificate metadata
    cert_fields = parse_certificate(signature)

    # Step 4: Build and return the structured response
    return AppResponse(
        name=app_data.get("name"),
        size=format_size(app_data.get("size")),
        downloads=format_downloads(app_data.get("downloads")),
        version=file_data.get("vername"),
        release_date=file_data.get("added"),
        min_screen=file_data.get("screensize"),
        supported_cpu=file_data.get("cpu"),
        package_id=app_data.get("package"),
        sha1_signature=signature.get("sha1"),
        **cert_fields,
    )

