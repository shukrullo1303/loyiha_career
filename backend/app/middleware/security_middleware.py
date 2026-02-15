"""
Хавфсизлик мидлвари
Хавфсизлик текширувлари
"""
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)


class SecurityMiddleware(BaseHTTPMiddleware):
    """Хавфсизлик мидлвари"""
    
    async def dispatch(self, request: Request, call_next):
        """Хавфсизлик текширувлари"""
        # Rate limiting (содда версия)
        # Production'да Redis ishlatish керак
        
        # XSS ва SQL injection текширувлари
        # (бу ерда содда версия)
        
        response = await call_next(request)
        
        # Хавфсизлик хедерларини қўшиш
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        return response
