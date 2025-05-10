import os
from .colors import ToolsCordColors

def display_banner(base_color=ToolsCordColors.CYAN, style=ToolsCordColors.BOLD):
    """
    Display a centered TOOLSCORD banner in the terminal with gradient colors.
    
    Args:
        base_color: Base color from ToolsCordColors (default: CYAN)
        style: Style from ToolsCordColors (default: BOLD)
    """
    banner = [
        "████████╗ ██████╗  ██████╗ ██╗     ███████╗     ██████╗ ██████╗ ██████╗ ██████╗ ",
        "╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝    ██╔════╝██╔═══██╗██╔══██╗██╔══██╗",
        "   ██║   ██║   ██║██║   ██║██║     ███████╗    ██║     ██║   ██║██████╔╝██║  ██║",
        "   ██║   ██║   ██║██║   ██║██║     ╚════██║    ██║     ██║   ██║██╔══██╗██║  ██║",
        "   ██║   ╚██████╔╝╚██████╔╝███████╗███████║    ╚██████╗╚██████╔╝██║  ██║██████╔╝",
        "   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝     ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ "
    ]
    
    terminal_width = os.get_terminal_size().columns
    
    # Gradient colors - from cyan to blue
    gradient_colors = [
        ToolsCordColors.CYAN, 
        "\033[38;5;51m",  # Light cyan
        "\033[38;5;45m",  # Light cyan/blue
        "\033[38;5;39m",  # Blue-ish
        "\033[38;5;33m",  # More blue
        ToolsCordColors.DEEPBLUE
    ]
    
    print("\n")
    for i, line in enumerate(banner):
        # Center the line in the terminal
        padding = (terminal_width - len(line)) // 2
        
        # Get the gradient color for this line
        color = gradient_colors[i % len(gradient_colors)]
        
        print(" " * padding + color + style + line + ToolsCordColors.ENDC)
    print("\n") 