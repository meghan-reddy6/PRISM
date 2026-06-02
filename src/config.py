import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# App Settings
APP_NAME = os.getenv("APP_NAME", "PRISM")
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 100))

# Directories
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / os.getenv("UPLOAD_FOLDER", "uploads")
OUTPUT_DIR = BASE_DIR / os.getenv("OUTPUT_FOLDER", "outputs")
ASSETS_DIR = BASE_DIR / "assets"

# Ensure directories exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Supported formats mapped by MarkItDown
SUPPORTED_EXTENSIONS = {
    ".pdf", ".docx", ".pptx", ".xlsx", ".csv", ".txt", ".jpg", ".jpeg", ".png"
}