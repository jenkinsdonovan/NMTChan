from flask import current_app
from werkzeug.utils import secure_filename
import tempfile, os
from PIL import Image
from ffmpy import FFmpeg
 
# returns media, thumb on success, exception on error
def uploadFile(media, request) -> (str, str):
    # check size
    if not request.headers.get("content_length"):
        raise Exception("content_length header has to be set")

    size = request.headers.get("content_length")
    size = int(size)/10000000 # convert to MB

    if size == 0:
        raise Exception("bro wtf")

    if size > 10: # 10 MB
        raise Exception("media too large: {}/10MB".format(str(size)))

    if '.' not in media.filename:
        raise Exception("filename needs extension")
    
    allowed = ["webm", "png", "jpg", "jpeg", "mp4"]
    if media.filename.rsplit('.', 1)[1].lower() not in allowed:
        raise Exception("invalid file type")

    # media
    extension = secure_filename(media.filename.rsplit('.', 1)[1].lower())
    medianame = tempfile.NamedTemporaryFile(
        mode='w+b', delete=False, prefix=current_app.config["MEDIA_FOLDER"],
        suffix="." + extension).name
    media.save(os.path.join(medianame))

    # thumbnail
    thumbname = "".join(medianame.split(".")[:-1]) + "_thumb." + extension
    try:
        if extension != "webm" and extension != "mp4":
            with open(thumbname, 'w+b') as t:
                media.seek(0)
                t.write(media.read())

            i = Image.open(thumbname)
            i.thumbnail((200, 200))
            i.save(thumbname)
        else:
            thumbname = "".join(thumbname.split(".")[:-1]) + ".png"
            ff = FFmpeg(inputs={medianame: None}, outputs={thumbname: ['-ss', '00:00:00.500', '-vframes', '1']})
            ff.run()
            i = Image.open(thumbname)
            i.thumbnail((200, 200))
            i.save(thumbname)
    except Exception as e:
        os.remove(medianame)
        raise Exception(e)

    medianame = "/instance" + medianame.split("/instance")[-1]
    thumbname = "/instance" + thumbname.split("/instance")[-1]
    return thumbname, medianame