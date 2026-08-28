import os
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timezone, timedelta
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)


class AuthenticatedUser(BaseModel):
    """
    Authenticated user context injected into route handlers.
    """
    user_id: str = Field(..., description="Unique user identifier")
    email: Optional[str] = Field(None, description="User email address")
    role: str = Field(default="authenticated", description="User role")
    is_authenticated: bool = Field(default=True)


class SupabaseAuthService:
    """
    Validates Supabase JWTs and manages authentication tokens.
    """

    @staticmethod
    def get_jwt_secret() -> str:
        return (
            os.getenv("SUPABASE_JWT_SECRET")
            or os.getenv("JWT_SECRET_KEY")
            or "fidel_development_secret_key_32_bytes_long_minimum!"
        )

    @classmethod
    def decode_token(cls, token: str) -> Dict[str, Any]:
        """
        Decodes and validates a Supabase or local JWT token.
        """
        secret = cls.get_jwt_secret()
        try:
            # Attempt verification with HS256 (standard Supabase JWT secret)
            payload = jwt.decode(
                token,
                secret,
                algorithms=["HS256", "RS256"],
                options={"verify_aud": False}
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication token has expired."
            )
        except jwt.PyJWTError as e:
            # Attempt unverified decode in development for custom dev tokens
            env = os.getenv("ENVIRONMENT", "development")
            if env == "development":
                try:
                    return jwt.decode(token, options={"verify_signature": False})
                except Exception:
                    pass
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid authentication token: {str(e)}"
            )

    @classmethod
    def create_development_token(cls, user_id: str = "user_demo_01", email: str = "demo@fidel.finance") -> str:
        """
        Creates a signed development JWT for instant testing.
        """
        secret = cls.get_jwt_secret()
        now = datetime.now(timezone.utc)
        payload = {
            "sub": user_id,
            "email": email,
            "role": "authenticated",
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(days=7)).timestamp()),
            "iss": "supabase",
        }
        return jwt.encode(payload, secret, algorithm="HS256")


def get_current_user(
    auth_header: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> AuthenticatedUser:
    """
    FastAPI dependency that extracts and validates the authenticated user.
    Supports Supabase Bearer JWTs with development fallback for offline testing.
    """
    if auth_header and auth_header.credentials:
        token = auth_header.credentials
        payload = SupabaseAuthService.decode_token(token)
        user_id = payload.get("sub") or payload.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing user identity subject claim."
            )
        return AuthenticatedUser(
            user_id=user_id,
            email=payload.get("email"),
            role=payload.get("role", "authenticated"),
            is_authenticated=True,
        )

    # In development mode, allow default demo user when no auth header is supplied
    environment = os.getenv("ENVIRONMENT", "development")
    if environment == "development":
        return AuthenticatedUser(
            user_id="user_demo_01",
            email="demo@fidel.finance",
            role="authenticated",
            is_authenticated=True,
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing Authorization header."
    )
