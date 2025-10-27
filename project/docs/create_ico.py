"""
Convert PNG image to ICO file for Windows application icon.
"""
from PIL import Image
import os

def convert_png_to_ico(png_file, ico_file):
    """Convert a PNG file to ICO format."""
    try:
        # Open the PNG file
        img = Image.open(png_file)
        
        # Create a list of different icon sizes
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128)]
        
        # Create the icon file
        img.save(ico_file, format='ICO', sizes=icon_sizes)
        
        print(f"Successfully created {ico_file} from {png_file}")
        return True
    except Exception as e:
        print(f"Error converting {png_file} to {ico_file}: {e}")
        return False

if __name__ == "__main__":
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define input and output files
    png_file = os.path.join(current_dir, "PP_Logo.png")
    ico_file = os.path.join(current_dir, "PP_Logo.ico")
    
    # Convert PNG to ICO
    convert_png_to_ico(png_file, ico_file) 