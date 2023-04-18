from PIL import Image

with Image.open('out/card/1.png') as img1:
    with Image.open('out/card/2.png') as img2:
        with Image.open('out/card/3.png') as img3:

            l = [img1,img1,img1,img1,img2,img2,img2,img2,img3]

a4page = Image.new('RGBA', (8168, 11552), (256, 256, 256, 256))
try:
    i = 0
    while i < 9:
        characterimg = Image.new('RGBA', (2520, 3520), (0, 0, 0, 256))
        characterimg.paste(l[i], (20,20))
        a4page.paste(characterimg, [(0,0),(2520,0),(5040,0),(0,3520),(2520,3520),(5040,3520),(0,7040),(2520,7040),(5040,7040)][i])
        i += 1
except IndexError:
    pass