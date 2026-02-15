"""
Логирование мидлвари
Барча сўровларни логирлайди
"""
import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Логирование мидлвари"""
    
    async def dispatch(self, request: Request, call_next):
        """Сўровни логирлаш"""
        start_time = time.time()
        
        # Сўров маълумотлари
        method = request.method
        url = str(request.url)
        client_ip = request.client.host if request.client else "unknown"
        
        # Жавоб
        response = await call_next(request)
        
        # Вақт
        process_time = time.time() - start_time
        
        # Логирование
        logger.info(
            f"{method} {url} - "
            f"Status: {response.status_code} - "
            f"Time: {process_time:.3f}s - "
            f"IP: {client_ip}"
        )
        
        return response
