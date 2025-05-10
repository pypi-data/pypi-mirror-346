from typing import Callable, Dict, Any

class CommandRegistry:
    def __init__(self):
        self._commands: Dict[str, Callable] = {}
    
    def register(self, name: str, func: Callable):
        """Decorator to register a command function"""
        self._commands[name] = func
    
    def execute(self, command_str: str) -> str:
        """Parse and execute a raw command string (e.g. '/greet John')"""
        parts = command_str.strip().split(maxsplit=1)
        cmd_name = parts[0]
        args_str = parts[1] if len(parts) > 1 else ""
        
        if cmd_name not in self._commands:
            return f"Unknown command: {cmd_name}. Type /help for available commands."
        
        try:
            # Get the command function and its parameter annotations
            cmd_func = self._commands[cmd_name]
            param_types = cmd_func.__annotations__
            
            args = []
            kwargs = {}
            if args_str:
                for i, arg in enumerate(args_str.split()):
                    if "=" in arg:
                        k, v = arg.split("=", 1)
                        # Convert kwargs based on type annotation if available
                        if k in param_types:
                            kwargs[k] = param_types[k](v)
                        else:
                            kwargs[k] = v
                    else:
                        # Convert args based on type annotation if available
                        param_name = f'arg_{i}'  # Default for *args
                        if i < len(cmd_func.__code__.co_varnames):
                            param_name = cmd_func.__code__.co_varnames[i]
                        if param_name in param_types:
                            args.append(param_types[param_name](arg))
                        else:
                            args.append(arg)
            
            result = cmd_func(*args, **kwargs)
            return str(result)
        
        except Exception as e:
            return f"Error executing {cmd_name}: {str(e)}"

    def help(self) -> str:
        """Generate a help message for all registered commands"""
        help_text = "Available commands:<br>"
        for cmd in self._commands:
            help_text += f"- /{cmd}<br>"
            help_text += f"  {self._commands[cmd].__doc__}<br>"
        return help_text

# Global registry instance
registry = CommandRegistry()

def register(name: str, func: Callable):
    """Register a command function"""
    registry.register(name, func)

def execute(command_str: str) -> str:
    """Execute a command string"""
    return registry.execute(command_str)

def show_help() -> str:
    """Generate a help message"""
    return registry.help()

# User-facing decorator
def command(name: str) -> Callable:
    """Decorator to register a chat command"""
    def decorator(func: Callable) -> Callable:
        register(name, func)
        return func
    return decorator
