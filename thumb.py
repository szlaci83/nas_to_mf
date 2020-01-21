from PIL import Image
import os
import logging

minX = 640
minY = 480


def get_thumb_size(width, height):
    while width/2 > minX and height/2 > minY:
       width = int(width / 2)
       height = int(height /2)
    return width, height


def process_all(source, dest, func):
    for root, dirs, files in os.walk(source):
        dest_root = root.replace(source, dest)
        if not os.path.exists(dest_root):
            os.makedirs(dest_root)
        for file in files:
            if file.endswith(".jpg"):
                func(os.path.join(root,  file), os.path.join(dest_root,  file))


def create_thumb(source_img, dest_img):
    im = Image.open(source_img)
    w, h = im.size
    width, height = get_thumb_size(w, h)
    logging.info("Resizing %s  -> %s, size: [%d * %d] -> [%d * %d]", source_img, dest_img, w, h, width, height)
    thumb = im.resize((width, height))
    thumb = thumb.convert('RGB')
    thumb.save(dest_img)


if __name__ == '__main__':
    s_path = "/home/laci/git/nas_to_mf/downloads/"
    thumb_path = "/home/laci/git/nas_to_mf/thumb/"
    logfile = "/home/laci/git/nas_to_mf/log/"	
    logging.basicConfig(filename="", level=logging.DEBUG,
                        format="%(asctime)s:%(levelname)s:%(message)s")
    process_all(s_path, thumb_path, create_thumb)
