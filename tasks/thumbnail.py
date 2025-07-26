from utils.celery import app
from PIL import Image
import os

@app.task
def generate_thumbnail(file_path, file_name):
    """
    Generate a thumbnail for the given file.
    
    :param file_path: Path to the file for which the thumbnail is to be generated.
    :param file_name: Name of the file.
    """
    thumbnails_path = 'storage/thumbnails/'
    os.makedirs(thumbnails_path, exist_ok=True)

    image = Image.open(file_path)
    image.thumbnail((128, 128))
    thumbnail_path = f"{thumbnails_path}{file_name}_thumbnail.jpg"
    image.save(thumbnail_path, "JPEG")
    return f"Thumbnail for {file_name} generated successfully."