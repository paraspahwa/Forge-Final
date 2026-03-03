"""
GeoIP service for country detection
"""

import os
from typing import Optional

import maxminddb
from maxminddb import Reader

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# Cache for GeoIP reader
_geoip_reader: Optional[Reader] = None


def get_geoip_reader() -> Optional[Reader]:
    """Get or create GeoIP reader"""
    global _geoip_reader
    
    if _geoip_reader is None:
        db_path = settings.MAXMIND_DB_PATH
        
        if os.path.exists(db_path):
            try:
                _geoip_reader = maxminddb.open_database(db_path)
                logger.info(f"GeoIP database loaded: {db_path}")
            except Exception as e:
                logger.error(f"Failed to load GeoIP database: {e}")
    
    return _geoip_reader


async def get_country_from_ip(ip_address: str) -> str:
    """
    Get country code from IP address
    
    Returns:
        ISO 3166-1 alpha-2 country code (e.g., 'US', 'IN')
    """
    # Handle localhost/private IPs
    if ip_address in ("127.0.0.1", "localhost", "::1"):
        return "US"
    
    # Check for private IP ranges
    if ip_address.startswith(("10.", "172.16.", "172.17.", "172.18.", "172.19.",
                              "172.20.", "172.21.", "172.22.", "172.23.",
                              "172.24.", "172.25.", "172.26.", "172.27.",
                              "172.28.", "172.29.", "172.30.", "172.31.",
                              "192.168.")):
        return "US"
    
    reader = get_geoip_reader()
    
    if reader is None:
        logger.warning("GeoIP database not available, defaulting to US")
        return "US"
    
    try:
        response = reader.get(ip_address)
        
        if response and "country" in response:
            country_code = response["country"].get("iso_code", "US")
            logger.debug(f"IP {ip_address} -> {country_code}")
            return country_code
        
        return "US"
        
    except Exception as e:
        logger.error(f"GeoIP lookup failed for {ip_address}: {e}")
        return "US"


async def download_geoip_database():
    """Download GeoIP database (run during setup)"""
    import httpx
    
    url = f"https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-Country&license_key={settings.MAXMIND_LICENSE_KEY}&suffix=tar.gz"
    
    logger.info("Downloading GeoIP database...")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=120.0)
        response.raise_for_status()
        
        # Save and extract
        import tarfile
        import io
        
        tar = tarfile.open(fileobj=io.BytesIO(response.content), mode="r:gz")
        
        # Extract .mmdb file
        for member in tar.getmembers():
            if member.name.endswith(".mmdb"):
                member.name = os.path.basename(member.name)
                tar.extract(member, path=".")
                logger.info(f"Extracted: {member.name}")
                break