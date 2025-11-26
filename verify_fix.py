
import sys
import os

# Add current directory to sys.path to allow importing src
sys.path.append(os.getcwd())

try:
    print("Importing src.create_docx1 to trigger the patch...")
    import src.create_docx1
    
    import PIL.Image
    
    if hasattr(PIL.Image, 'ANTIALIAS'):
        print(f"SUCCESS: Image.ANTIALIAS exists and is {PIL.Image.ANTIALIAS}")
    else:
        print("FAILURE: Image.ANTIALIAS is still missing!")
        sys.exit(1)

except Exception as e:
    print(f"Verification failed with error: {e}")
    sys.exit(1)
