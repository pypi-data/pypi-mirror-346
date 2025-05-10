import datetime
from .colors import ToolsCordColors

class Logger:
    """
    A customizable logger with different log types, colors, and formatting options.
    Personal style format: {time} • {type} > message
    """
    
    # Log type display names
    TYPE_NAMES = {
        "info": "INFO",
        "success": "SUCCESS",
        "warning": "WARN",
        "error": "ERROR",
        "debug": "DEBUG",
        "input": "INPUT",
        "loading": "LOADING",
        "important": "IMPORTANT",
        "note": "NOTE",
        "question": "QUESTION",
        "star": "STAR",
    }
    
    # Default colors for different log types
    COLORS = {
        "info": ToolsCordColors.CYAN,          # Cyan for general information
        "success": ToolsCordColors.SUCCESS,     # Green for success messages
        "warning": ToolsCordColors.WARNING,     # Yellow for warnings
        "error": ToolsCordColors.FAIL,          # Red for errors
        "debug": ToolsCordColors.PURPLE,        # Purple for debug info
        "input": ToolsCordColors.DEEPBLUE,      # Blue for input prompts
        "loading": ToolsCordColors.OKBLUE,      # Light blue for loading messages
        "important": ToolsCordColors.WHITE,     # White for important messages
        "note": ToolsCordColors.CYAN,           # Cyan for notes
        "question": ToolsCordColors.DEEPBLUE,   # Blue for questions
        "star": ToolsCordColors.CLOUDFLARE_ORANGE, # Orange for starred items
    }
    
    def __init__(self, show_time=True, bullet_style="•"):
        """
        Initialize the logger.
        
        Args:
            show_time (bool): Whether to show timestamps in logs
            bullet_style (str): The bullet character to use between time and type
        """
        self.show_time = show_time
        self.bullet_style = bullet_style
        
    def _get_timestamp(self):
        """Get current timestamp string."""
        if self.show_time:
            return f"{datetime.datetime.now().strftime('%H:%M:%S')}"
        return ""
    
    def _format_message(self, message, log_type, bold=False, underline=False, 
                       color=None, bg_color=None):
        """Format the log message with colors and styles."""
        result = ""
        
        # Get type color
        msg_color = color if color else self.COLORS.get(log_type, ToolsCordColors.WHITE)
        
        # Format: {time} • {type} > message
        if self.show_time:
            # Time part with dimmed style
            result += ToolsCordColors.TIME + self._get_timestamp() + ToolsCordColors.ENDC
            # Bullet
            result += f" {msg_color}{self.bullet_style}{ToolsCordColors.ENDC} "
        
        # Type part
        type_text = self.TYPE_NAMES.get(log_type, log_type.upper())
        result += f"{msg_color}{ToolsCordColors.BOLD}{type_text}{ToolsCordColors.ENDC} > "
        
        # Apply formatting to message
        message_styled = ""
        
        # Apply text color
        message_styled += msg_color
            
        # Apply styles
        if bold:
            message_styled += ToolsCordColors.BOLD
        if underline:
            message_styled += ToolsCordColors.UNDERLINE
            
        # Add the message with styling
        message_styled += str(message)
        
        # Reset all formatting
        message_styled += ToolsCordColors.ENDC
        
        result += message_styled
        
        return result
    
    def log(self, message, log_type="info", bold=False, underline=False, 
           color=None, bg_color=None):
        """
        Log a message with custom formatting.
        
        Args:
            message: The message to log
            log_type: Type of log (info, success, warning, error, etc.)
            bold: Whether to make the text bold
            underline: Whether to underline the text
            color: Custom color (use ToolsCordColors color)
            bg_color: Not used (kept for compatibility)
        """
        formatted_msg = self._format_message(
            message, log_type, bold, underline, color, bg_color
        )
        print(formatted_msg)
    
    # Convenience methods for common log types
    def info(self, message, **kwargs):
        """Log an info message."""
        self.log(message, "info", **kwargs)
    
    def success(self, message, **kwargs):
        """Log a success message."""
        self.log(message, "success", **kwargs)
    
    def warning(self, message, **kwargs):
        """Log a warning message."""
        self.log(message, "warning", **kwargs)
    
    def error(self, message, **kwargs):
        """Log an error message."""
        self.log(message, "error", **kwargs)
    
    def debug(self, message, **kwargs):
        """Log a debug message."""
        self.log(message, "debug", **kwargs)
    
    def input(self, message, **kwargs):
        """Format an input prompt."""
        self.log(message, "input", **kwargs)
        
    def important(self, message, **kwargs):
        """Log an important message."""
        self.log(message, "important", bold=True, **kwargs)
    
    def note(self, message, **kwargs):
        """Log a note."""
        self.log(message, "note", **kwargs)
    
    def question(self, message, **kwargs):
        """Format a question."""
        self.log(message, "question", **kwargs)
        
    def divider(self, char="-", length=50, color=None):
        """Print a divider line."""
        line = char * length
        color = color if color else ToolsCordColors.WHITE
        print(color + line + ToolsCordColors.ENDC) 