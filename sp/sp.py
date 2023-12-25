from cards.CardSpawn import spawn_a4_image
from PIL import Image

ttbj = Image.open('sp/1.png')
klab = Image.open('sp/2.png')
yang = Image.open('sp/3.png')

lst = [ttbj]*3 + [klab]*3 + [yang]
print(lst)
# spawn_a4_image()