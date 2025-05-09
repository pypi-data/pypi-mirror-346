"""
Core functionality for pypccl package.
"""


class ExampleClass:
    """
    Example class demonstrating pypccl functionality.
    """
    
    def __init__(self, value=None):
        """
        Initialize with an optional value.
        
        Args:
            value: Initial value (default: None)
        """
        self.value = value
    
    def get_value(self):
        """
        Get the current value.
        
        Returns:
            The current value
        """
        return self.value
    
    def set_value(self, value):
        """
        Set a new value.
        
        Args:
            value: New value to set
        """
        self.value = value


def example_function(param1, param2=None):
    """
    Example function demonstrating pypccl functionality.
    
    Args:
        param1: First parameter
        param2: Second parameter (default: None)
        
    Returns:
        Result of the operation
    """
    if param2 is None:
        return param1
    return param1, param2
