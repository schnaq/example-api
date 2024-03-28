from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from loguru import logger
from starlette import status

tokens = [
    "dev",  # debug token
    "9462fdefbbc960607c186e6dcd650002a9cd5f7845a2edf201aee22e883af570",  # schnaq API Key
    "61e421921e6d42b36d178e843e5e35f82cd07b184c03461c6e5185c4cf786a46",  # other customer
]
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_api_key(token: str = Security(api_key_header)):
    if token not in tokens:
        if token:
            logger.debug(f"Received token: {token}")
        logger.debug(f"Token not in tokens")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )
