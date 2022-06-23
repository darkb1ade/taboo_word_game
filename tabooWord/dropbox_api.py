from dropbox.exceptions import AuthError
import dropbox
import numpy as np
from PIL import Image
import io

DROPBOX_ACCESS_TOKEN = 'sl.BJVI3S84V1rVceCt5OMi-Yoxpc5brro07I3E3W6id2ojJeEHc7_4h6TeUtIQmyJ9yLb9iVV356yPMK29hBmmuZfbZHdJAdKaPLd5v_smtOsdVqka80GwnbiCjIVeQnRaPic4WNo'
def dropbox_connect():
    """Create a connection to Dropbox."""
    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        print('Connected to Dropbox successfully')
    except AuthError as e:
        print('Error connecting to Dropbox with access token: ' + str(e))
    return dbx


def load_image(filepath: str) -> bytes:
    image = Image.open(filepath)  # any image
    l = np.array(image.getdata())

    # To transform an array into image using PIL:
    channels = l.size // (image.height * image.width)
    l = l.reshape(image.height, image.width, channels).astype(
        "uint8"
    )  # unit8 is necessary to convert
    im = Image.fromarray(l).convert("RGB")

    # to transform the image into bytes:
    with io.BytesIO() as output:
        im.save(output, format="PNG")
        contents = output.getvalue()
    return contents
dbx = dropbox_connect()
def upload_img(path):

    contents = load_image(path)
    print(path)
    path = path.replace('\\', '/')
    path = '/'.join(path.split('/')[1:])
    dbx.files_upload(
        contents, f"/{path}", dropbox.files.WriteMode.add, mute=True
    )