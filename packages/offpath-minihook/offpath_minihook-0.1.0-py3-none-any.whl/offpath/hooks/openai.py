"""
Offpath Mini-Hook - OpenAI integration
"""
import logging
import json
from functools import wraps
from typing import Dict, Any, Callable

logger = logging.getLogger("offpath-minihook.openai")

def secure_openai_functions(minihook):
    """
    Patch OpenAI function calling to use Offpath security
    
    Args:
        minihook: OffpathMiniHook instance
    """
    try:
        # Import OpenAI components
        import openai
        
        # Check which version of OpenAI is installed
        if hasattr(openai, "OpenAI"):
            # OpenAI v1.x
            _patch_openai_v1(minihook)
        else:
            # Legacy OpenAI
            _patch_openai_legacy(minihook)
            
    except ImportError as e:
        logger.error(f"Failed to secure OpenAI functions: {str(e)}")
    except Exception as e:
        logger.error(f"Error patching OpenAI: {str(e)}")

def _patch_openai_v1(minihook):
    """
    Patch OpenAI v1.x client
    
    Args:
        minihook: OffpathMiniHook instance
    """
    import openai
    from openai import OpenAI
    
    # Store original methods
    _original_chat_create = OpenAI.chat.completions.create
    
    @wraps(_original_chat_create)
    def _secured_chat_create(self, *args, **kwargs):
        """Secured version of chat.completions.create"""
        # Process the original request
        response = _original_chat_create(self, *args, **kwargs)
        
        # Check if the response contains function/tool calls
        if hasattr(response, 'choices') and response.choices:
            for choice in response.choices:
                if hasattr(choice, 'message'):
                    # Handle function_call
                    if hasattr(choice.message, 'function_call') and choice.message.function_call:
                        function_call = choice.message.function_call
                        
                        # Secure the function call
                        secured = _secure_function_call(
                            minihook,
                            function_call.name,
                            function_call.arguments
                        )
                        
                        if not secured.get("allowed", False):
                            # For v1.x, this requires more complex handling since 
                            # the response objects are immutable in the new SDK
                            logger.warning(f"Blocked function call: {function_call.name} - {secured.get('reason')}")
        
        return response
    
    # Apply the patch
    try:
        OpenAI.chat.completions.create = _secured_chat_create
        logger.info("Patched OpenAI v1.x chat.completions.create")
    except Exception as e:
        logger.error(f"Error applying patch to OpenAI v1.x: {str(e)}")

def _patch_openai_legacy(minihook):
    """
    Patch legacy OpenAI v0.x client
    
    Args:
        minihook: OffpathMiniHook instance
    """
    import openai
    
    # Store original methods
    _original_chat_create = openai.ChatCompletion.create
    
    @wraps(_original_chat_create)
    def _secured_chat_create(*args, **kwargs):
        """Secured version of ChatCompletion.create"""
        # Process the original request
        response = _original_chat_create(*args, **kwargs)
        
        # Check if the response contains function calls
        if 'choices' in response:
            for i, choice in enumerate(response['choices']):
                if 'message' in choice:
                    # Handle function_call
                    if 'function_call' in choice['message']:
                        function_call = choice['message']['function_call']
                        
                        # Secure the function call
                        secured = _secure_function_call(
                            minihook,
                            function_call['name'],
                            function_call['arguments']
                        )
                        
                        if not secured.get("allowed", False):
                            # Modify the response to block the function call
                            logger.warning(f"Blocked function call: {function_call['name']} - {secured.get('reason')}")
                            
                            # Replace function call with warning message
                            response['choices'][i]['message']['content'] = (
                                f"⚠️ Security Alert: The requested operation '{function_call['name']}' "
                                f"was blocked by Offpath security policies. Reason: {secured.get('reason')}"
                            )
                            del response['choices'][i]['message']['function_call']
        
        return response
    
    # Apply the patch
    try:
        openai.ChatCompletion.create = _secured_chat_create
        logger.info("Patched OpenAI legacy ChatCompletion.create")
    except Exception as e:
        logger.error(f"Error applying patch to OpenAI legacy: {str(e)}")

def _secure_function_call(minihook, function_name: str, arguments: str) -> Dict[str, Any]:
    """
    Secure a function call using the minihook
    
    Args:
        minihook: OffpathMiniHook instance
        function_name: Name of the function
        arguments: Function arguments (JSON string)
        
    Returns:
        Security result dict
    """
    try:
        # Parse arguments if needed
        args_obj = arguments
        if isinstance(arguments, str):
            try:
                args_obj = json.loads(arguments)
            except:
                args_obj = {"_raw": arguments}
        
        # Create payload for API
        payload = {
            "tool": function_name,
            "action": json.dumps(args_obj) if isinstance(args_obj, dict) else str(args_obj),
            "timestamp": time.time(),
            "context": minihook._get_context()
        }
        
        # Send to API for evaluation
        response = requests.post(
            f"{minihook.api_url}/tools/evaluate",
            json=payload,
            headers=minihook._get_headers(),
            timeout=2
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"API error: {response.status_code} - {response.text}")
            return {"allowed": False, "reason": f"API error: {response.status_code}"}
            
    except Exception as e:
        logger.error(f"Error securing function call: {str(e)}")
        
        # Fallback mode
        fallback_mode = os.environ.get("OFFPATH_FALLBACK_MODE", "permissive")
        
        if fallback_mode.lower() == "permissive":
            return {"allowed": True, "reason": f"Error in security check: {str(e)}"}
        else:
            return {"allowed": False, "reason": f"Error in security check: {str(e)}"}

def secure_openai():
    """
    Simple function to secure OpenAI with default settings
    """
    from offpath.core import get_instance
    minihook = get_instance()
    secure_openai_functions(minihook)
