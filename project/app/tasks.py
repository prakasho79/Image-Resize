# project/app/tasks.py


import celery
import os

from PIL import Image


CELERY_BROKER = os.environ.get('CELERY_BROKER')
CELERY_BACKEND = os.environ.get('CELERY_BACKEND')
IMG_RESIZE = (100, 100)
STORAGE_PATH = './images/thumbnail/'

app = celery.Celery('tasks', broker=CELERY_BROKER, backend=CELERY_BACKEND)

@app.task
def resize_image(org_image_file):
    file_name = os.path.split(org_image_file)[1]

    im = Image.open(org_image_file)
    original_size = im.size

    im.thumbnail(IMG_RESIZE)
    thumbnail_size = im.size
    thumbnail_image_file = STORAGE_PATH+file_name

    # Image File format supported
    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
    im.save(thumbnail_image_file)

    return {
                'Original':{
                    'file_path': org_image_file,
                    'Size':tuple(original_size)
                },
                'Thumbnail':{
                    'file_path': thumbnail_image_file,
                    'Size':tuple(thumbnail_size)
                }
            }

