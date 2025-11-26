
import sys
try:
    from PIL import Image
    print(f"Pillow version: {Image.__version__}")
    try:
        print(f"Image.ANTIALIAS: {Image.ANTIALIAS}")
    except AttributeError:
        print("Image.ANTIALIAS is missing")
except ImportError:
    print("Pillow not installed")

print("Importing easyocr...")
try:
    import easyocr
    print("easyocr imported successfully")
except Exception as e:
    print(f"easyocr import failed: {e}")

print("Importing fitz...")
try:
    import fitz
    print("fitz imported successfully")
except Exception as e:
    print(f"fitz import failed: {e}")

print("Importing docx2pdf...")
try:
    import docx2pdf
    print("docx2pdf imported successfully")
except Exception as e:
    print(f"docx2pdf import failed: {e}")
