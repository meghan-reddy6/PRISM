import os
import re
import logging
from datetime import datetime
from werkzeug.utils import secure_filename

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def format_file_size(size_in_bytes: int) -> str:
    """Format bytes into a human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} TB"

def get_safe_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal and invalid characters."""
    return secure_filename(filename)

def generate_default_output_name(original_filename: str) -> str:
    """Generate the default markdown filename."""
    base_name = os.path.splitext(original_filename)[0]
    # Clean up base name
    clean_name = re.sub(r'[^a-zA-Z0-9_]', '_', base_name)
    return f"{clean_name}_markdown"

def count_text_stats(text: str) -> tuple[int, int]:
    """Return character and word count for the converted text."""
    char_count = len(text)
    word_count = len(text.split())
    return char_count, word_count

def cleanup_file(filepath: str):
    """Safely delete a temporary file."""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.info(f"Cleaned up file: {filepath}")
    except Exception as e:
        logger.error(f"Error cleaning up file {filepath}: {e}")