from utils.celery import app
from PIL import Image
import os
import subprocess

@app.task
def generate_thumbnail(file_path, file_name):
    """
    Generate a thumbnail for the given file.
    
    :param file_path: Path to the file for which the thumbnail is to be generated.
    :param file_name: Name of the file.
    """
    thumbnails_path = 'storage/thumbnails/'
    os.makedirs(thumbnails_path, exist_ok=True)

    file_extension = os.path.splitext(file_name)[1].lower()
    base_name = os.path.splitext(file_name)[0]

    if file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
        try:
            image = Image.open(file_path)
            image.thumbnail((128, 128))

            if file_extension in ['.jpg', '.jpeg']:
                thumbnail_path = f"{thumbnails_path}{base_name}_thumbnail.jpg"
                if image.mode in ['RGBA', 'LA']:
                    background = Image.new("RGB", image.size, (255, 255, 255))
                    background.paste(image, mask=image.split()[-1])  # Use alpha channel
                    image = background
                else:
                    image = image.convert("RGB")
                image.save(thumbnail_path, "JPEG")

            elif file_extension == '.png':
                thumbnail_path = f"{thumbnails_path}{base_name}_thumbnail.png"
                image.save(thumbnail_path, "PNG")

            elif file_extension == '.gif':
                thumbnail_path = f"{thumbnails_path}{base_name}_thumbnail.gif"
                image.save(thumbnail_path, "GIF")

        except Exception as e:
            return f"Error generating thumbnail for {file_name}: {str(e)}"

    else:
        try:
            thumbnail_path = f"{thumbnails_path}{base_name}_thumbnail.jpg"
            subprocess.run([
                'ffmpeg', '-i', file_path, '-ss', '00:00:01.000',
                '-vframes', '1', '-s', '128x128', thumbnail_path
            ], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            return f"Error generating thumbnail for {file_name}: {e.stderr.decode()}"

    return f"Thumbnail for {file_name} generated successfully."
