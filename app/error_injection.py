"""
Random Error Injection Module for Testing
Injects various types of errors randomly to simulate real-world issues
"""
import random
import time
import asyncio
from typing import Dict, Any
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from app.logger import logger


class ErrorInjector:
    """Class to handle random error injection"""
    
    def __init__(self, error_rate: float = 0.15):
        """
        Initialize error injector
        
        Args:
            error_rate: Probability of injecting an error (0.0 to 1.0)
        """
        self.error_rate = error_rate
        self.error_types = {
            "database_timeout": 0.25,     # 25% of errors
            "validation_error": 0.20,     # 20% of errors  
            "auth_error": 0.15,           # 15% of errors
            "rate_limit": 0.15,           # 15% of errors
            "internal_server": 0.15,      # 15% of errors
            "network_error": 0.10,        # 10% of errors
        }
    
    def should_inject_error(self) -> bool:
        """Determine if an error should be injected"""
        return random.random() < self.error_rate
    
    def get_random_error_type(self) -> str:
        """Select a random error type based on weights"""
        rand_val = random.random()
        cumulative = 0.0
        
        for error_type, weight in self.error_types.items():
            cumulative += weight
            if rand_val <= cumulative:
                return error_type
        
        return "internal_server"  # fallback
    
    async def inject_error(self, request: Request) -> HTTPException:
        """Inject a random error"""
        error_type = self.get_random_error_type()
        request_id = getattr(request.state, 'request_id', 'unknown')
        
        error_details = {
            "request_id": request_id,
            "path": str(request.url.path),
            "method": request.method,
            "error_type": error_type
        }
        
        if error_type == "database_timeout":
            # Simulate database timeout
            await asyncio.sleep(random.uniform(2, 5))  # Random delay
            logger.error(f"[ERROR_INJECTION] Database timeout simulated", extra=error_details)
            raise HTTPException(
                status_code=503,
                detail="Database connection timeout - please try again later"
            )
        
        elif error_type == "validation_error":
            logger.error(f"[ERROR_INJECTION] Validation error simulated", extra=error_details)
            raise HTTPException(
                status_code=422,
                detail={
                    "message": "Validation failed due to system constraints",
                    "errors": [{"field": "random_validation", "message": "Simulated validation failure"}]
                }
            )
        
        elif error_type == "auth_error":
            logger.error(f"[ERROR_INJECTION] Authentication error simulated", extra=error_details)
            raise HTTPException(
                status_code=401,
                detail="Authentication required - token expired or invalid"
            )
        
        elif error_type == "rate_limit":
            logger.warning(f"[ERROR_INJECTION] Rate limit exceeded simulated", extra=error_details)
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded - too many requests"
            )
        
        elif error_type == "network_error":
            # Simulate network issues with random delay
            await asyncio.sleep(random.uniform(1, 3))
            logger.error(f"[ERROR_INJECTION] Network error simulated", extra=error_details)
            raise HTTPException(
                status_code=502,
                detail="Upstream service unavailable"
            )
        
        else:  # internal_server
            logger.error(f"[ERROR_INJECTION] Internal server error simulated", extra=error_details)
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error - correlation ID: {request_id}"
            )


# Global error injector instance
error_injector = ErrorInjector(error_rate=0.15)  # 15% error rate


async def random_error_middleware(request: Request, call_next):
    """
    Middleware to inject random errors for testing
    """
    # Skip error injection for health checks and docs
    if request.url.path in ["/", "/docs", "/openapi.json", "/health"]:
        return await call_next(request)
    
    # Add request ID for tracking
    import uuid
    request.state.request_id = str(uuid.uuid4())[:8]
    
    # Check if we should inject an error
    if error_injector.should_inject_error():
        try:
            await error_injector.inject_error(request)
        except HTTPException as e:
            # Log the injected error
            logger.warning(f"[ERROR_INJECTION] Injected error: {e.status_code} - {e.detail}")
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail}
            )
    
    # Normal request processing
    response = await call_next(request)
    return response


# Manual error injection functions for specific scenarios
def random_database_error():
    """Randomly inject database errors in operations"""
    if random.random() < 0.1:  # 10% chance
        logger.error("[ERROR_INJECTION] Simulated database connection failure")
        raise Exception("Database connection lost - simulated error")


def random_processing_delay():
    """Add random processing delays"""
    if random.random() < 0.2:  # 20% chance
        delay = random.uniform(0.5, 2.0)
        logger.warning(f"[ERROR_INJECTION] Simulated processing delay: {delay:.2f}s")
        time.sleep(delay)


def random_validation_failure(data: Dict[str, Any]) -> Dict[str, Any]:
    """Randomly corrupt data to cause validation failures"""
    if random.random() < 0.1:  # 10% chance
        logger.error("[ERROR_INJECTION] Simulating data corruption")
        # Randomly corrupt some fields
        corrupted_data = data.copy()
        if random.choice([True, False]):
            corrupted_data["email"] = "invalid_email_format"
        if random.choice([True, False]) and "username" in corrupted_data:
            corrupted_data["username"] = ""  # Empty username
        return corrupted_data
    return data