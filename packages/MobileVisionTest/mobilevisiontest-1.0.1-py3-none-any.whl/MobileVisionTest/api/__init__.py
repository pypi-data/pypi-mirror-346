"""
API Layer - Provides high-level interfaces for testers to interact with mobile apps.
"""

from .MobileVisionAPI import OCRHandler, UIElementRecognizer

__all__ = ["OCRHandler", "UIElementRecognizer"]