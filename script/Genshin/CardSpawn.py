from script.Genshin.GKCard import CardBuild
import json
import os

# build_a4_print: bool | 是否生成A4尺寸的打印版图片
build_a4_print = False

# all_character: bool | 是否生成全部角色卡；若为True，忽略character_list
all_character = True

# character_list: list | 生成角色卡的列表
character_list = ['']

# 读取json
with open(os.path.join('json', 'genshin-impact.json'), encoding='UTF-8') as file:
    file_data = json.loads(file.read())
    character_datas = file_data['character_data']
    card_versions = file_data['versions']

if not os.path.exists(os.path.join('output', 'character_card')):
    os.makedirs(os.path.join('output', 'character_card'))

# 角色卡生成
if all_character:
    datas = character_datas
else:
    datas = []
    for data in character_datas:
        if data['id'] in character_list:
            datas.append(data)
for data in datas:
    if data['design_info']:
        ch_img = CardBuild.genshin_character_card(data, card_versions)
        ch_img.save(os.path.join('output', 'character_card', data['id'] + '.png'))
        character_list.append(ch_img)
        if not all_character and len(character_list) == 1:
            ch_img.show()
        print(data['name'] + '构建结束')
    else:
        print(data['name'] + '不构建')

# 生成适用于A4打印的图像
if build_a4_print:
    card_group = [character_list[i:i + 9] for i in range(0, len(character_list), 9)]
    i = 1
    for cards in card_group:
        CardBuild.print_build(cards).save(os.path.join('output', 'print_img', 'a4page-' + str(i) + '.png'))
        i += 1
