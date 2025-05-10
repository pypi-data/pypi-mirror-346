"""
Rainbow ASCII Art Generator - Core functionality
"""

from art import text2art
from colorama import init, Fore
import shutil
import os
import re

# Initialize colorama
init(autoreset=True)

# Rainbow color cycle
RAINBOW = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]

def render_ascii_lines(lines):
    """
    Render a list of text lines as colorful ASCII art
    
    Args:
        lines (list): List of strings to render
        
    Returns:
        list: Rendered ASCII art lines with color
    """
    output_lines = []
    for text in lines:
        ascii_art_lines = []
        for char in text:
            if char == ' ':
                # Insert moderate spacing between words (5 spaces)
                space_width = 5
                space_block = [' ' * space_width] * 6  # height will be normalized below
                ascii_art_lines.append(space_block)
            else:
                ascii_art_lines.append(text2art(char).split('\n'))
                
        # Skip if no valid characters
        if not ascii_art_lines:
            continue
            
        max_height = max(len(char_lines) for char_lines in ascii_art_lines)
        
        # Normalize height
        for char_lines in ascii_art_lines:
            while len(char_lines) < max_height:
                char_lines.append(' ' * len(char_lines[0]))
                
        # Merge horizontally
        composed = []
        for i in range(max_height):
            line = ''
            for idx, char_lines in enumerate(ascii_art_lines):
                color = RAINBOW[idx % len(RAINBOW)]
                line += color + char_lines[i]
            composed.append(line)
            
        output_lines.extend(composed)
        output_lines.append('')  # blank line between blocks
        
    return output_lines

def strip_ansi_codes(text):
    """
    Remove ANSI color codes from text for accurate width calculation
    
    Args:
        text (str): Text with ANSI color codes
        
    Returns:
        str: Text without ANSI color codes
    """
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def center_ascii_output(lines, vertical=True):
    """
    Center the ASCII art in the terminal (horizontally and optionally vertically)
    
    Args:
        lines (list): ASCII art lines
        vertical (bool): Whether to center vertically as well
        
    Returns:
        list: Centered ASCII art lines
    """
    # Get terminal dimensions
    try:
        terminal_width = shutil.get_terminal_size().columns
        terminal_height = shutil.get_terminal_size().lines
    except Exception:
        # Fallback if we can't get terminal size
        terminal_width = 80
        terminal_height = 24
    
    # Horizontal centering - properly handle ANSI color codes
    horizontally_centered = []
    for line in lines:
        # Calculate true width (ignoring ANSI color codes)
        true_width = len(strip_ansi_codes(line))
        
        # Calculate padding
        padding = max(0, (terminal_width - true_width) // 2)
        
        # Add padding at the start
        centered_line = ' ' * padding + line
        horizontally_centered.append(centered_line)
    
    # Vertical centering (if requested)
    if vertical:
        art_height = len(horizontally_centered)
        
        # Only add vertical padding if terminal is larger than the art
        if terminal_height > art_height:
            padding_lines = (terminal_height - art_height) // 2
            
            # Add empty lines before and after, ensuring we don't exceed terminal height
            vertically_centered = []
            
            # Add top padding (blank lines)
            for _ in range(padding_lines):
                vertically_centered.append('')
                
            # Add the art
            vertically_centered.extend(horizontally_centered)
            
            # Add bottom padding (blank lines)
            remaining_lines = terminal_height - len(vertically_centered)
            for _ in range(min(padding_lines, remaining_lines)):
                vertically_centered.append('')
                
            return vertically_centered
    
    return horizontally_centered

def generate_rainbow_ascii(text, center=True, vertical_center=True):
    """
    Generate rainbow ASCII art from text
    
    Args:
        text (str): Text to convert to ASCII art
        center (bool): Whether to center the output horizontally in the terminal
        vertical_center (bool): Whether to center the output vertically in the terminal
        
    Returns:
        str: The generated ASCII art as a string
    """
    logical_lines = text.split("  ")
    colored_output = render_ascii_lines(logical_lines)
    
    if center:
        colored_output = center_ascii_output(colored_output, vertical=vertical_center)
        
    return "\n".join(colored_output)