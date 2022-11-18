from PIL import Image
from PIL import ImageDraw


def num_to_pic(values, name):
    ar = values
    wert = (round(len(ar)/10))+1
    img = Image.new('RGB', (10, wert), color = 'white')
    ar.append((255,255,255))
    while len(ar)%10 != 0:
        ar.append((0,0,0))
    for g in range(10):
        ar.append((0,0,0))
    i=0
    p=0
    while i < wert:
        for j in range(0,10):
            draw = ImageDraw.Draw(img)
            draw.point((j, i), fill=ar[p])
            p += 1
        i += 1
            
    img.save(name + '.png')

def pic_to_num(filename):
    im = Image.open(filename + '.png',"r")
    result = []
    for j in range(im.height):
        for i in range(im.width):
            result.append(im.getpixel((i,j)))
            r,g,b = result[len(result)-1]
            if r == 255 and g == 255 and b == 255:
                result.pop()
                return result
    #rem = len(result)
    #del result[rem-10:rem]
    return result
