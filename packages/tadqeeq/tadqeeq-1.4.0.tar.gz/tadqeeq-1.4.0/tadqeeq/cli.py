""" 
Tadqeeq - Image Annotator Tool
An interactive image annotation tool for efficient labeling.
Developed by Mohamed Behery @ RTR Software Development (2025-04-27).
Licensed under the MIT License.
"""

from PyQt5.QtWidgets import QApplication
import sys, os
from .implementations import ImageAnnotatorWindow

def main():
    
    if len(sys.argv) < 3:
        print("Usage: tadqeeq [--autosave|--use_bounding_boxes]* <images_directory_path> <annotations_directory_path>")
        sys.exit(1)
    
    images_directory_path, annotations_directory_path = sys.argv[-2:]
    if not os.path.isdir():
        print(f'Error: The directory "{images_directory_path}" does not exist.')
        sys.exit(2)
    
    app = QApplication(sys.argv)
    window = ImageAnnotatorWindow(
        images_directory_path, annotations_directory_path,
        use_bounding_boxes='--use_bounding_boxes' in sys.argv,
        autosave='--autosave' in sys.argv
    )
    window.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()