from pydantic import BaseModel, Field
from .cli import AutoCLI, snake_to_pascal, snake_to_kebab
import logging

def param(default_value, *, s=None, l=None, choices=None, **kwargs):
    """Create a Field object with CLI-specific parameters.
    
    Args:
        default_value: The default value for the field
        s: Short form argument (e.g., "-n")
        l: Long form argument (e.g., "--name")
        choices: List of allowed values
        **kwargs: Additional arguments passed to Field
    """
    json_schema_extra = {}
    if l:
        json_schema_extra["l"] = l
    if s:
        json_schema_extra["s"] = s
    if choices:
        json_schema_extra["choices"] = choices
    
    if json_schema_extra:
        kwargs["json_schema_extra"] = json_schema_extra
    
    return Field(default_value, **kwargs)

def set_log_level(level):
    """Set the log level for pydantic-autocli.
    
    Args:
        level: A logging level (e.g., logging.DEBUG, logging.INFO)
    """
    logger = logging.getLogger("pydantic_autocli")
    logger.setLevel(level)

__all__ = [
    "AutoCLI", 
    "BaseModel", 
    "Field", 
    "param",
    "set_log_level",
]



