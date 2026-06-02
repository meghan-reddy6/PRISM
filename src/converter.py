import logging
from markitdown import MarkItDown
from src.utils import logger

def convert_to_markdown(file_path: str) -> str:
    """
    Converts a supported document to Markdown using MarkItDown.
    Returns the markdown text content.
    Raises an exception if conversion fails.
    """
    try:
        logger.info(f"Starting conversion for: {file_path}")
        md = MarkItDown()
        result = md.convert(file_path)
        logger.info("Conversion successful.")
        return result.text_content
    except Exception as e:
        logger.error(f"Conversion failed: {str(e)}")
        raise Exception(f"Failed to convert file: {str(e)}")