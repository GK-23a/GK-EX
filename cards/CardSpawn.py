import json
import os

from PIL import Image

from CardBuild import character_card_build

# build_a4_print: bool | 是否生成A4尺寸的打印版图片
build_a4_print = True

# all_character: bool | 是否生成全部角色卡；若为True，忽略character_list
all_character = False

# character_list: list | 生成角色卡的列表
character_list = ['nilou', 'venti', 'zhongli', 'cyno', 'nahida', 'diluc', 'albedo', 'amber', 'beidou']

# 读取json
with open(os.path.join('assets', 'card_data.json'), encoding='UTF-8') as file:
    file_data = json.loads(file.read())
    character_datas = file_data['character_data']
    card_versions = file_data['character_data_versions']

if not os.path.exists(os.path.join('output', 'character_card')):
    os.makedirs(os.path.join('output', 'character_card'))

character_images = []  # 创建一个空的列表来存储角色卡的图像对象

# 角色卡生成
if all_character:
    datas = character_datas
else:
    datas = []
    for data in character_datas:
        if data['id'] in character_list:
            datas.append(data)
for data in datas:
    if data['design_state']:
        ch_img = character_card_build(data, card_versions)
        ch_img.save(os.path.join('output', 'character_card', data['id'] + '.png'))
        character_images.append(ch_img)  # 将生成的图像对象添加到列表中
        print(data['name'] + '构建结束')
    else:
        print(data['name'] + '不构建')

# 生成适用于A4打印的图像
if build_a4_print:
    if not os.path.exists(os.path.join('output', 'print_img')):
        os.makedirs(os.path.join('output', 'print_img'))
    card_group = [character_images[i:i + 9] for i in range(0, len(character_images), 9)]
    i = 1
    for j, nine_cards_list in enumerate(card_group):
        print(f'打印张生成开始: 第 {j} 张')
        card_size_point = (2560, 3520)
        card_point = []
        for y in range(3):
            for x in range(3):
                card_point.append((x * card_size_point[0], y * card_size_point[1]))
        a4page = Image.new('RGBA', (8168, 11552), (256, 256, 256, 256))
        try:
            i = 0
            while i < 9:
                character_image = Image.new('RGBA', (card_size_point[0], card_size_point[1]), (0, 0, 0, 256))
                character_image.paste(nine_cards_list[i], (20, 20))
                a4page.paste(character_image, card_point[i])
                i += 1
                print(f'打印张生成: 第 {j} 张，第 {i} / 9 个')
        except IndexError:
            pass
        a4page.save(os.path.join('output', 'print_img', 'a4page-' + str(i) + '.png'))
        i += 1
    print('打印张生成结束')
