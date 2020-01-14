from PIL import Image
minX = 640
minY = 480


def get_thumb_size(width, height):
    while width/2 > minX and height/2 > minY:
       width = int(width / 2)
       height = int(height /2)
    return width, height


for i in range(11):
    print(i)
    img_filename = "pics\\test%d.jpg" % i
    im = Image.open(img_filename)
    w, h = im.size
    width, height = get_thumb_size(w, h)
    print(width, height)
    thumb = im.resize((width, height))
    thumb.save("pics\\small-test%d.jpg" % i)
