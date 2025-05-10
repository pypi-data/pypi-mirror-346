"""
Command-line interface for pmoschos_art_gen
"""

import argparse
from .ascii_generator import generate_rainbow_ascii

def main():
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(description="Rainbow ASCII Art Generator")
    parser.add_argument("text", nargs="?", help="Text to convert to rainbow ASCII art (use double space for new line)")
    parser.add_argument("--no-center", action="store_true", help="Don't center the output horizontally in the terminal")
    parser.add_argument("--no-vcenter", action="store_true", help="Don't center the output vertically in the terminal")
    
    args = parser.parse_args()
    
    if not args.text:
        print("\n🎨 Rainbow ASCII Art Generator (Double-space = newline) 🎨\n")
        text = input("📝 Enter your text: ").strip()
    else:
        text = args.text
        
    if not text:
        print("⚠️ Text cannot be empty.")
        return 1
        
    result = generate_rainbow_ascii(
        text, 
        center=not args.no_center, 
        vertical_center=not args.no_vcenter
    )
    print(result)
    return 0

if __name__ == "__main__":
    main()