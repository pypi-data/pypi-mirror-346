"""
Offpath Mini-Hook - LangChain integration
"""
import logging
import inspect
from functools import wraps
from typing import List, Any, Dict, Optional, Callable

logger = logging.getLogger("offpath-minihook.langchain")

def secure_langchain_tools(minihook):
    """
    Patch LangChain tools to use Offpath security
    
    Args:
        minihook: OffpathMiniHook instance
    """
    try:
        # Import LangChain components
        from langchain.tools import BaseTool
        from langchain.agents import AgentExecutor
        
        # Patch BaseTool._run
        _original_base_tool_run = BaseTool._run
        
        @wraps(_original_base_tool_run)
        def _secured_base_tool_run(self, tool_input: str, **kwargs: Any) -> str:
            """Secured version of BaseTool._run"""
            tool_name = getattr(self, "name", self.__class__.__name__)
            
            # Create a wrapper function to secure
            @minihook.secure_tool(tool_name)
            def run_tool(input_str):
                return _original_base_tool_run(self, input_str, **kwargs)
            
            # Call the secured function
            result = run_tool(tool_input)
            
            # Handle security denial result
            if isinstance(result, dict) and "status" in result and result["status"] == "denied":
                return f"Tool execution denied: {result.get('reason', 'Not allowed by policy')}"
            
            return result
        
        # Apply the patch
        BaseTool._run = _secured_base_tool_run
        logger.info("Patched LangChain BaseTool._run")
        
        # Also patch AgentExecutor.run to provide context
        _original_agent_executor_run = AgentExecutor.run
        
        @wraps(_original_agent_executor_run)
        def _secured_agent_executor_run(self, *args, **kwargs):
            """Secured version of AgentExecutor.run"""
            # TODO: Add context gathering for better policy decisions
            return _original_agent_executor_run(self, *args, **kwargs)
        
        # Apply the agent executor patch
        AgentExecutor.run = _secured_agent_executor_run
        logger.info("Patched LangChain AgentExecutor.run")
        
    except ImportError as e:
        logger.error(f"Failed to secure LangChain tools: {str(e)}")
    except Exception as e:
        logger.error(f"Error patching LangChain: {str(e)}")

def secure_langchain():
    """
    Simple function to secure LangChain with default settings
    """
    from offpath.core import get_instance
    minihook = get_instance()
    secure_langchain_tools(minihook)
