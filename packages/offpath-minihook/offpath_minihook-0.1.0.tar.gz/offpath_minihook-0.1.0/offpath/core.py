"""
Offpath Mini-Hook - Core implementation for lightweight agent hook
"""
import os
import json
import uuid
import time
import logging
import importlib
import requests
from typing import Dict, Any, Optional, List, Callable, Union
from functools import wraps

logger = logging.getLogger("offpath-minihook")

class OffpathMiniHook:
    """
    Lightweight hook for tool execution security
    """
    
    def __init__(
        self, 
        api_url: str = os.environ.get("OFFPATH_API_URL", "https://api.offpath.ai"),
        api_key: str = os.environ.get("OFFPATH_API_KEY", ""),
        session_id: Optional[str] = None
    ):
        """
        Initialize the Mini-Hook
        
        Args:
            api_url: Offpath API URL
            api_key: Offpath API key
            session_id: Optional session ID
        """
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.session_id = session_id or f"sess-{uuid.uuid4()}"
        
        # Set up logging
        self._setup_logging()
        
        # Check if API key is set
        if not self.api_key:
            logger.warning("No Offpath API key provided. Set OFFPATH_API_KEY environment variable.")
        
        # Test connection if API key is set
        if self.api_key:
            self._test_connection()
        
        # Detected frameworks
        self.detected_frameworks = self._detect_frameworks()
        
        logger.info(f"Offpath Mini-Hook initialized (Session: {self.session_id})")
        if self.detected_frameworks:
            logger.info(f"Detected frameworks: {', '.join(self.detected_frameworks)}")
    
    def _setup_logging(self) -> None:
        """Set up logging"""
        log_level = os.environ.get("OFFPATH_LOG_LEVEL", "INFO").upper()
        logging.basicConfig(
            level=getattr(logging, log_level),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    
    def _test_connection(self) -> None:
        """Test connection to Offpath API"""
        try:
            response = requests.get(
                f"{self.api_url}/health",
                headers=self._get_headers(),
                timeout=2
            )
            
            if response.status_code == 200:
                logger.info("Successfully connected to Offpath API")
            else:
                logger.warning(f"Connection to Offpath API returned status {response.status_code}")
        except Exception as e:
            logger.error(f"Failed to connect to Offpath API: {str(e)}")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Offpath-Session": self.session_id,
            "User-Agent": "Offpath-MiniHook/0.1.0"
        }
    
    def _detect_frameworks(self) -> List[str]:
        """
        Detect which LLM frameworks are installed
        
        Returns:
            List of detected frameworks
        """
        frameworks = []
        
        # Check for LangChain
        try:
            importlib.import_module("langchain")
            frameworks.append("langchain")
        except ImportError:
            pass
        
        # Check for LlamaIndex
        try:
            importlib.import_module("llama_index")
            frameworks.append("llama_index")
        except ImportError:
            pass
        
        # Check for OpenAI
        try:
            importlib.import_module("openai")
            frameworks.append("openai")
        except ImportError:
            pass
        
        return frameworks
    
    def secure_tool(self, tool_name: str) -> Callable:
        """
        Decorator to secure a tool function
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Decorated function
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                # Extract action details
                if args:
                    action = str(args[0]) if args else ""
                else:
                    action = json.dumps(kwargs) if kwargs else ""
                
                # Create payload for API
                payload = {
                    "tool": tool_name,
                    "action": action,
                    "timestamp": time.time(),
                    "context": self._get_context()
                }
                
                # Send to API for evaluation
                try:
                    response = requests.post(
                        f"{self.api_url}/tools/evaluate",
                        json=payload,
                        headers=self._get_headers(),
                        timeout=2  # Short timeout to avoid blocking execution
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # If allowed, execute the original function
                        if result.get("allowed", False):
                            logger.debug(f"Tool execution allowed: {tool_name}")
                            return func(*args, **kwargs)
                        else:
                            # Log the denial
                            logger.warning(f"Tool execution denied: {tool_name} - {result.get('reason')}")
                            
                            # Return structured denial information
                            return {
                                "status": "denied",
                                "reason": result.get("reason", "Action not allowed by policy"),
                                "details": result.get("details", {})
                            }
                    else:
                        logger.error(f"API error: {response.status_code} - {response.text}")
                        
                except Exception as e:
                    logger.error(f"Error evaluating tool: {str(e)}")
                    
                    # Fall back to permissive mode if configured
                    fallback_mode = os.environ.get("OFFPATH_FALLBACK_MODE", "permissive")
                    if fallback_mode.lower() == "permissive":
                        logger.warning(f"Falling back to permissive mode for {tool_name}")
                        return func(*args, **kwargs)
                    else:
                        logger.warning(f"Falling back to restrictive mode for {tool_name}")
                        return {
                            "status": "error",
                            "reason": f"Offpath evaluation error: {str(e)}",
                            "details": {"exception": str(e)}
                        }
                
                # In case of unexpected flow, execute original function
                return func(*args, **kwargs)
            
            return wrapper
        
        return decorator
    
    def _get_context(self) -> Dict[str, Any]:
        """
        Get execution context information
        
        Returns:
            Context dictionary
        """
        import sys
        import platform
        
        return {
            "python_version": platform.python_version(),
            "system": platform.system(),
            "hostname": platform.node(),
            "pid": os.getpid()
        }
    
    def secure_langchain(self) -> None:
        """
        Secure LangChain tools with Offpath
        """
        if "langchain" not in self.detected_frameworks:
            logger.warning("LangChain not detected, skipping")
            return
            
        try:
            from offpath.hooks.langchain import secure_langchain_tools
            secure_langchain_tools(self)
            logger.info("LangChain tools secured with Offpath")
        except Exception as e:
            logger.error(f"Error securing LangChain: {str(e)}")
    
    def secure_openai(self) -> None:
        """
        Secure direct OpenAI function calling with Offpath
        """
        if "openai" not in self.detected_frameworks:
            logger.warning("OpenAI not detected, skipping")
            return
            
        try:
            from offpath.hooks.openai import secure_openai_functions
            secure_openai_functions(self)
            logger.info("OpenAI function calling secured with Offpath")
        except Exception as e:
            logger.error(f"Error securing OpenAI: {str(e)}")
    
    def secure_all(self) -> None:
        """
        Secure all detected frameworks
        """
        self.secure_langchain()
        self.secure_openai()

# Global singleton instance
_instance = None

def get_instance(
    api_url: Optional[str] = None,
    api_key: Optional[str] = None,
    session_id: Optional[str] = None
) -> OffpathMiniHook:
    """
    Get or create the global OffpathMiniHook instance
    
    Args:
        api_url: Offpath API URL
        api_key: Offpath API key
        session_id: Optional session ID
        
    Returns:
        OffpathMiniHook instance
    """
    global _instance
    
    if _instance is None:
        _instance = OffpathMiniHook(
            api_url=api_url or os.environ.get("OFFPATH_API_URL", "https://api.offpath.ai"),
            api_key=api_key or os.environ.get("OFFPATH_API_KEY", ""),
            session_id=session_id
        )
    
    return _instance

def secure() -> None:
    """
    Secure all detected frameworks with default settings
    """
    instance = get_instance()
    instance.secure_all()

def secure_all() -> None:
    """
    Alias for secure() function
    """
    secure()
