from PIL import Image, ImageDraw, ImageFont
import os

# 预加载

# 字体
font = {
    'sign': ImageFont.truetype(os.path.join('font', 'MiSans-Light.ttf'), size=56, encoding='utf-8'),  # 卡底标记
    'category': ImageFont.truetype(os.path.join('font', 'MiSans-Semibold.ttf'), size=72, encoding='utf-8'),  # 技能类型
    'text': ImageFont.truetype(os.path.join('font', 'MiSans-Regular.ttf'), size=72, encoding='utf-8'),  # 技能内容
    'suit': ImageFont.truetype(os.path.join('font', '有爱新黑CN-Regular.ttf'), size=72, encoding='utf-8'),  # 花色图标
    'title': ImageFont.truetype(os.path.join('font', 'SIMLI.ttf'), size=94, encoding='utf-8'),  # 角色称号
    'HP': ImageFont.truetype(os.path.join('font', 'MiSans-Semibold.ttf'), size=100, encoding='utf-8'),  # 特殊血条
    'topic': ImageFont.truetype(os.path.join('font', 'SIMLI.ttf'), size=120, encoding='utf-8'),  # 技能标题
    'name': ImageFont.truetype(os.path.join('font', 'SIMLI.ttf'), size=300, encoding='utf-8')  # 角色名字
}
# 颜色
shadow_color = (126, 126, 126, 192)
element_color = {
    'pyro': [(246, 136, 123), (226, 49, 29)],
    'hydro': [(122, 176, 255), (28, 114, 253)],
    'cryo': [(200, 230, 250), (152, 200, 232)],
    'electro': [(236, 137, 254), (211, 118, 240)],
    'dendro': [(182, 217, 133), (123, 180, 45)],
    'anemo': [(137, 232, 217), (51, 204, 179)],
    'geo': [(234, 209, 128), (207, 167, 38)],
}
# 中文标点习惯修复
punctuation = ['，', '。', '；', '：', '？', '！', '、']
left_punctuation = ['（', '【', '“']
right_punctuation = ['）', '】', '”']
# 技能名
skill_categories = ['锁定技，', '转换技，', '限定技，', '觉醒技，', '使命技，']


def img_cut(img_path, width=2000, height=3240):
    """裁切立绘图像"""
    img = Image.open(img_path)
    w, h = img.size
    scale = width / w
    new_size = (int(w * scale), int(h * scale))
    new_img = img.resize(new_size)
    if new_size[1] < height:
        bg_img = Image.new('RGB', (width, height), (255, 255, 255))
        left = (width - new_img.width) // 2
        top = (height - new_img.height) // 2
        bg_img.paste(new_img, (left, top))
    else:
        box = (0, 0, width, height)
        bg_img = new_img.crop(box)
    return bg_img


def img_draw(bg,
             position,
             text,
             fill_color,
             font_style='text',
             side_width=0,
             side_color=None,
             md='lt'):
    """简化的ImageDraw.Draw().text()函数"""
    img = ImageDraw.Draw(bg)
    if font_style == 'title':
        img.text((position[0] + 4, position[1] + 4),
                 text,
                 fill=shadow_color,
                 font=font[font_style],
                 anchor=md,
                 direction='ttb',
                 language='zh-Hans',
                 stroke_width=side_width,
                 stroke_fill=shadow_color,
                 encoding='UTF-8')
        img.text(position,
                 text,
                 fill=fill_color,
                 font=font[font_style],
                 anchor=md,
                 direction='ttb',
                 language='zh-Hans',
                 stroke_width=side_width,
                 stroke_fill=side_color,
                 encoding='UTF-8')
    elif font_style == 'topic':
        img.text((position[0] + 4, position[1] + 4),
                 text,
                 fill=shadow_color,
                 font=font[font_style],
                 anchor=md,
                 direction='ltr',
                 language='zh-Hans',
                 stroke_width=side_width,
                 stroke_fill=shadow_color,
                 encoding='UTF-8')
        img.text(position,
                 text,
                 fill=fill_color,
                 font=font[font_style],
                 anchor=md,
                 direction='ltr',
                 language='zh-Hans',
                 stroke_width=side_width,
                 stroke_fill=side_color,
                 encoding='UTF-8')
    elif font_style == 'name':
        img.text((position[0] + 4, position[1] + 4),
                 text,
                 fill=shadow_color,
                 font=font[font_style],
                 anchor=md,
                 direction='ttb',
                 language='zh-Hans',
                 stroke_width=side_width + 4,
                 stroke_fill=(126, 126, 126, 160),
                 encoding='UTF-8')
        img.text(position,
                 text,
                 fill=fill_color,
                 font=font[font_style],
                 anchor=md,
                 direction='ttb',
                 language='zh-Hans',
                 stroke_width=side_width,
                 stroke_fill=side_color,
                 encoding='UTF-8')
    else:
        img.text(position,
                 text,
                 fill=fill_color,
                 font=font[font_style],
                 anchor=md,
                 direction='ltr',
                 language='zh-Hans',
                 stroke_width=side_width,
                 stroke_fill=side_color,
                 encoding='UTF-8')


def genshin_character_card(character_data: dict,
                           versions: str,
                           img_path=os.path.join('img', 'character'),
                           progress_bar=None) -> Image:
    """生成角色卡，返回Pillow的图像对象。如果进度条为'Qt'，则中途会传递至函数genshin_character_card_with_qt_progress_bar()。"""

    # 图层：背景
    card_img = Image.new('RGBA', (2480, 3480), (255, 255, 255, 0))

    # 图层：角色图像
    character_image = Image.open(os.path.join(img_path, character_data['id'] + '.png'))
    if character_image.size != (2000, 3240):
        character_image = img_cut(character_image)
    card_img.paste(character_image, (380, 120))

    # 函数传递
    if progress_bar == 'Qt':
        return genshin_character_card_with_qt_progress_bar(
            character_data=character_data,
            versions=versions,
            card_img=card_img,
            progress_bar=progress_bar)

    # 图层组：技能说明、卡片信息
    skill_img = Image.new('RGBA', (2000, 3240), (253, 253, 253, 138))
    color = element_color[character_data['element']]
    # 技能说明
    skill_text_length, skill_text_height = (45, 50)
    for skill_data in character_data['skills']:
        if skill_data['origin']:
            fill_color = color[0]
        else:
            fill_color = 'black'
        img_draw(skill_img, (50, skill_text_height), skill_data['name'], fill_color, 'topic', 7, color[1])
        skill_text = skill_data['description']

        # 花色标记
        suit_sign = []
        point_sign = []
        suit_exist = False
        point = 0
        suit_dict = {'♥': 'heart', '♠': 'spade', '♦': 'diamond', '♣': 'club'}
        while point < len(skill_text):
            char = skill_text[point:point + 1]
            if char in suit_dict:
                skill_text = skill_text[:point] + '　' + skill_text[point + 1:]
                suit_sign.append(suit_dict[char])
                suit_exist = True
            elif char == '':
                break
            point += 1

        # 换行计算
        body_height = skill_text_height
        skill_text_body = skill_text
        while True:
            while True:
                liner_text = skill_text[:skill_text_length]
                line_len = ImageDraw.Draw(skill_img).textbbox(
                    (50, skill_text_height + 95),
                    liner_text,
                    font['text'],
                    align='left',
                    direction='ltr',
                    language='zh-Hans')
                if line_len[2] > 1940:
                    skill_text_length -= 1
                else:
                    # 中文标点修正
                    if skill_text[skill_text_length:skill_text_length + 1] in punctuation:
                        skill_text_length += 1
                    elif skill_text[skill_text_length:skill_text_length + 1] in right_punctuation:
                        if skill_text[skill_text_length + 1:skill_text_length + 2] in punctuation:
                            skill_text_length -= 2
                        else:
                            skill_text_length += 1
                    elif skill_text[skill_text_length - 1:skill_text_length] in left_punctuation:
                        skill_text_length -= 1
                    liner_text = skill_text[:skill_text_length]
                    break
            img_draw(skill_img, (50, skill_text_height + 95), liner_text, 'black')
            if suit_exist:
                point = 0
                while point <= len(liner_text):
                    if liner_text[:point][-1:] == '　':
                        point_sign.append(
                            ImageDraw.Draw(skill_img).textbbox(
                                (50, skill_text_height + 95),
                                liner_text[:point-1],
                                font['text'],
                                align='left',
                                direction='ltr',
                                language='zh-Hans'))
                    point += 1
            skill_text = skill_text[skill_text_length:]
            skill_text_height += 77
            if skill_text == '':
                skill_text_height += 110
                break
            else:
                skill_text_length = 45
        # 花色覆盖绘制
        if suit_exist:
            point = 0
            suit_color = ''
            suit_text = ''
            while point < len(suit_sign):
                if suit_sign[point] == 'heart':
                    suit_color = 'red'
                    suit_text = '♥'
                elif suit_sign[point] == 'spade':
                    suit_color = 'black'
                    suit_text = '♠'
                elif suit_sign[point] == 'diamond':
                    suit_color = 'red'
                    suit_text = '♦'
                elif suit_sign[point] == 'club':
                    suit_color = 'black'
                    suit_text = '♣'
                img_draw(
                    skill_img,
                    (point_sign[point][2], point_sign[point][3] - 84),
                    suit_text, suit_color, 'suit')
                point += 1
        # 技能类别粗体覆盖
        bold_text = ''
        while True:
            if skill_text_body[:4] not in skill_categories:
                break
            bold_text += skill_text_body[:4]
            skill_text_body = skill_text_body[4:]
        while True:
            while True:
                liner_text = bold_text[:skill_text_length]
                line_len = ImageDraw.Draw(skill_img).textbbox(
                    (50, body_height + 95),
                    liner_text,
                    font['text'],
                    align='left',
                    direction='ltr',
                    language='zh-Hans')
                if line_len[2] > 1940:
                    skill_text_length -= 1
                else:
                    # 中文标点修正
                    if bold_text[skill_text_length:skill_text_length+1] in punctuation:
                        skill_text_length += 1
                    elif bold_text[skill_text_length:skill_text_length+1] in right_punctuation:
                        if bold_text[skill_text_length + 1:skill_text_length+2] in punctuation:
                            skill_text_length -= 2
                        else:
                            skill_text_length += 1
                    elif bold_text[skill_text_length-1:skill_text_length] in left_punctuation:
                        skill_text_length -= 1
                    liner_text = bold_text[:skill_text_length]
                    break
            img_draw(skill_img, (50, body_height + 95), liner_text, 'black', 'category')
            bold_text = bold_text[skill_text_length:]
            body_height += 77
            if bold_text == '':
                body_height += 110
                break
            else:
                skill_text_length = 45
    sign_text = 'GenshinKill ' + versions + ' | Designer: ' + character_data.get('designer', 'None') \
                + ' , Artist: ' + character_data.get('Artist', 'miHoYo')
    img_draw(skill_img, (50, skill_text_height + 10), sign_text, 'black', font_style='sign')

    # 技能图层剪切
    skill_img = skill_img.crop((0, 0, 2000, skill_text_height + 100))
    card_img.alpha_composite(skill_img, (380, 3260 - skill_text_height))  # 技能层叠加

    # 元素外框
    with Image.open(os.path.join('img', 'frame', character_data['element'] + '.png')) as frame:
        card_img.alpha_composite(frame)

    # 神之眼
    with Image.open(os.path.join('img', 'vision', 'country', character_data['country'] + '.png')) as country:
        card_img.alpha_composite(country)
    icon_img = character_data['element']
    if character_data['country'] == 'liyue':
        icon_img += '_diamond'
    else:
        icon_img += '_circle'
    with Image.open(os.path.join('img', 'vision', 'element', icon_img + '.png')) as element:
        card_img.alpha_composite(element, (70, 80))

    # 名字、称号
    info_img = Image.new('RGBA', (2480, 3480), (255, 255, 255, 0))
    img_draw(info_img, (245, 470), character_data['name'], 'white', 'name', 8, 'black', 'mt')
    name_height = ImageDraw.Draw(info_img).textbbox(
        (245, 490),
        character_data['name'],
        font['name'],
        direction='ttb',
        language='zh-Hans',
        anchor='mt')[3]
    img_draw(info_img, (245, name_height), character_data['title'], (255, 192, 0, 255), 'title', 4, 'black', 'mt')
    card_img.alpha_composite(info_img)

    # 体力值、初始护甲
    hp_img = Image.new('RGBA', (2480, 3480), (255, 255, 255, 0))
    hp_height = 3100
    hp_value = character_data['health_point']
    while hp_value != 0:
        with Image.open(os.path.join('img', 'icon', 'HPyes.png')) as HP:
            hp_img.alpha_composite(HP, (160, hp_height))
            hp_height -= 200
            hp_value -= 1
    hp_value_empty = character_data['max_health_point'] - character_data['health_point']
    while hp_value_empty != 0:
        with Image.open(os.path.join('img', 'icon', 'HPno.png')) as HP_empty:
            hp_img.alpha_composite(HP_empty, (160, hp_height))
            hp_height -= 200
            hp_value_empty -= 1
    hp_height += 200
    armor_value = character_data['armor_point']
    if armor_value != 0:
        with Image.open(os.path.join('img', 'icon', 'Armor.png')) as AP:
            hp_img.alpha_composite(AP, (160, hp_height+200))
            img_draw(hp_img, (225, hp_height + 255), str(armor_value), 'black')
    # 体力值区域后续结算：与称号和名字的防冲突（简单）
    text_height = ImageDraw.Draw(info_img).textbbox(
        (245, name_height),
        character_data['title'],
        font['title'],
        stroke_width=4,
        direction='ttb',
        language='zh-Hans',
        anchor='mt')[3]
    if hp_height <= text_height:
        hp_img = Image.new('RGBA', (2480, 3480), (255, 255, 255, 0))
        with Image.open(os.path.join('img', 'icon', 'HPyes.png')) as HP:
            hp_img.alpha_composite(HP, (160, 2700))
        ImageDraw.Draw(hp_img).text(
            (215, 2900),
            str(character_data['health_point']) + '\n/\n' + str(character_data['max_health_point']),
            fill=(30, 140, 30),
            spacing=4,
            font=font['HP'],
            language='zh-Hans',
            stroke_width=8,
            stroke_fill=(0, 115, 0))
        if armor_value != 0:
            with Image.open(os.path.join('img', 'icon', 'Armor.png')) as AP:
                hp_img.alpha_composite(AP, (160, 2500))
                img_draw(hp_img, (225, 2540), str(armor_value), 'black')
    card_img.alpha_composite(hp_img)
    return card_img


def genshin_character_card_with_qt_progress_bar(
        character_data: dict,
        versions: str,
        card_img: Image,
        progress_bar) -> Image:

    if progress_bar:
        progress_bar.setValue(5)  # progressBar - Setting
    # 图层组：技能说明、卡片信息
    skill_img = Image.new('RGBA', (2000, 3240), (253, 253, 253, 138))
    color = element_color[character_data['element']]
    # 技能说明
    skill_text_length, skill_text_height = (45, 50)
    for skill_data in character_data['skills']:
        if skill_data['origin']:
            fill_color = color[0]
        else:
            fill_color = 'black'
        img_draw(skill_img, (50, skill_text_height), skill_data['name'], fill_color, 'topic', 7, color[1])
        skill_text = skill_data['description']

        # 花色标记
        suit_sign = []
        point_sign = []
        suit_exist = False
        point = 0
        suit_dict = {'♥': 'heart', '♠': 'spade', '♦': 'diamond', '♣': 'club'}
        while point < len(skill_text):
            char = skill_text[point:point + 1]
            if char in suit_dict:
                skill_text = skill_text[:point] + '　' + skill_text[point + 1:]
                suit_sign.append(suit_dict[char])
                suit_exist = True
            elif char == '':
                break
            point += 1

        # 换行计算
        body_height = skill_text_height
        skill_text_body = skill_text
        while True:
            while True:
                liner_text = skill_text[:skill_text_length]
                line_len = ImageDraw.Draw(skill_img).textbbox(
                    (50, skill_text_height + 95),
                    liner_text,
                    font['text'],
                    align='left',
                    direction='ltr',
                    language='zh-Hans')
                if line_len[2] > 1940:
                    skill_text_length -= 1
                else:
                    # 中文标点修正
                    if skill_text[skill_text_length:skill_text_length + 1] in punctuation:
                        skill_text_length += 1
                    elif skill_text[skill_text_length:skill_text_length + 1] in right_punctuation:
                        if skill_text[skill_text_length + 1:skill_text_length + 2] in punctuation:
                            skill_text_length -= 2
                        else:
                            skill_text_length += 1
                    elif skill_text[skill_text_length - 1:skill_text_length] in left_punctuation:
                        skill_text_length -= 1
                    liner_text = skill_text[:skill_text_length]
                    break
            img_draw(skill_img, (50, skill_text_height + 95), liner_text, 'black')
            if suit_exist:
                point = 0
                while point <= len(liner_text):
                    if liner_text[:point][-1:] == '　':
                        point_sign.append(
                            ImageDraw.Draw(skill_img).textbbox(
                                (50, skill_text_height + 95),
                                liner_text[:point-1],
                                font['text'],
                                align='left',
                                direction='ltr',
                                language='zh-Hans'))
                    point += 1
            skill_text = skill_text[skill_text_length:]
            skill_text_height += 77
            if skill_text == '':
                skill_text_height += 110
                break
            else:
                skill_text_length = 45
        # 花色覆盖绘制
        if suit_exist:
            point = 0
            suit_color = ''
            suit_text = ''
            while point < len(suit_sign):
                if suit_sign[point] == 'heart':
                    suit_color = 'red'
                    suit_text = '♥'
                elif suit_sign[point] == 'spade':
                    suit_color = 'black'
                    suit_text = '♠'
                elif suit_sign[point] == 'diamond':
                    suit_color = 'red'
                    suit_text = '♦'
                elif suit_sign[point] == 'club':
                    suit_color = 'black'
                    suit_text = '♣'
                img_draw(
                    skill_img,
                    (point_sign[point][2], point_sign[point][3] - 84),
                    suit_text, suit_color, 'suit')
                point += 1
        # 技能类别粗体覆盖
        bold_text = ''
        while True:
            if skill_text_body[:4] not in skill_categories:
                break
            bold_text += skill_text_body[:4]
            skill_text_body = skill_text_body[4:]
        while True:
            while True:
                liner_text = bold_text[:skill_text_length]
                line_len = ImageDraw.Draw(skill_img).textbbox(
                    (50, body_height + 95),
                    liner_text,
                    font['text'],
                    align='left',
                    direction='ltr',
                    language='zh-Hans')
                if line_len[2] > 1940:
                    skill_text_length -= 1
                else:
                    # 中文标点修正
                    if bold_text[skill_text_length:skill_text_length + 1] in punctuation:
                        skill_text_length += 1
                    elif bold_text[skill_text_length:skill_text_length+1] in right_punctuation:
                        if bold_text[skill_text_length + 1:skill_text_length+2] in punctuation:
                            skill_text_length -= 2
                        else:
                            skill_text_length += 1
                    elif bold_text[skill_text_length-1:skill_text_length] in left_punctuation:
                        skill_text_length -= 1
                    liner_text = bold_text[:skill_text_length]
                    break
            img_draw(skill_img, (50, body_height + 95), liner_text, 'black', 'category')
            bold_text = bold_text[skill_text_length:]
            body_height += 77
            if bold_text == '':
                body_height += 110
                break
            else:
                skill_text_length = 45
    sign_text = 'GenshinKill ' + versions + ' | Designer: ' + character_data.get('designer', 'None') \
                + ' , Artist: ' + character_data.get('Artist', 'miHoYo')
    img_draw(skill_img, (50, skill_text_height + 10), sign_text, 'black', font_style='sign')

    # 技能图层剪切
    skill_img = skill_img.crop((0, 0, 2000, skill_text_height + 100))
    card_img.alpha_composite(skill_img, (380, 3260 - skill_text_height))  # 技能层叠加

    # 元素外框
    with Image.open(os.path.join('img', 'frame', character_data['element'] + '.png')) as frame:
        card_img.alpha_composite(frame)

    # 神之眼
    with Image.open(os.path.join('img', 'vision', 'country', character_data['country'] + '.png')) as country:
        card_img.alpha_composite(country)
    icon_img = character_data['element']
    if character_data['country'] == 'liyue':
        icon_img += '_diamond'
    else:
        icon_img += '_circle'
    with Image.open(os.path.join('img', 'vision', 'element', icon_img + '.png')) as element:
        card_img.alpha_composite(element, (70, 80))

    # 名字、称号
    info_img = Image.new('RGBA', (2480, 3480), (255, 255, 255, 0))
    img_draw(info_img, (245, 470), character_data['name'], 'white', 'name', 8, 'black', 'mt')
    name_height = ImageDraw.Draw(info_img).textbbox(
        (245, 490),
        character_data['name'],
        font['name'],
        direction='ttb',
        language='zh-Hans',
        anchor='mt')[3]
    img_draw(info_img, (245, name_height), character_data['title'], (255, 192, 0, 255), 'title', 4, 'black', 'mt')
    card_img.alpha_composite(info_img)

    # 体力值、初始护甲
    hp_img = Image.new('RGBA', (2480, 3480), (255, 255, 255, 0))
    hp_height = 3100
    hp_value = character_data['health_point']
    while hp_value != 0:
        with Image.open(os.path.join('img', 'icon', 'HPyes.png')) as HP:
            hp_img.alpha_composite(HP, (160, hp_height))
            hp_height -= 200
            hp_value -= 1
    hp_value_empty = character_data['max_health_point'] - character_data['health_point']
    while hp_value_empty != 0:
        with Image.open(os.path.join('img', 'icon', 'HPno.png')) as HP_empty:
            hp_img.alpha_composite(HP_empty, (160, hp_height))
            hp_height -= 200
            hp_value_empty -= 1
    hp_height += 200
    armor_value = character_data['armor_point']
    if armor_value != 0:
        with Image.open(os.path.join('img', 'icon', 'Armor.png')) as AP:
            hp_img.alpha_composite(AP, (160, hp_height+200))
            img_draw(hp_img, (225, hp_height + 255), str(armor_value), 'black')
    # 体力值区域后续结算：与称号和名字的防冲突（简单）
    text_height = ImageDraw.Draw(info_img).textbbox(
        (245, name_height),
        character_data['title'],
        font['title'],
        stroke_width=4,
        direction='ttb',
        language='zh-Hans',
        anchor='mt')[3]
    if hp_height <= text_height:
        hp_img = Image.new('RGBA', (2480, 3480), (255, 255, 255, 0))
        with Image.open(os.path.join('img', 'icon', 'HPyes.png')) as HP:
            hp_img.alpha_composite(HP, (160, 2700))
        ImageDraw.Draw(hp_img).text(
            (215, 2900),
            str(character_data['health_point']) + '\n/\n' + str(character_data['max_health_point']),
            fill=(30, 140, 30),
            spacing=4,
            font=font['HP'],
            language='zh-Hans',
            stroke_width=8,
            stroke_fill=(0, 115, 0))
        if armor_value != 0:
            with Image.open(os.path.join('img', 'icon', 'Armor.png')) as AP:
                hp_img.alpha_composite(AP, (160, 2500))
                img_draw(hp_img, (225, 2540), str(armor_value), 'black')
    card_img.alpha_composite(hp_img)
    return card_img


def print_build(nine_cards_list: list):
    """创建A4的打印张图像"""
    print_points = [
        (0, 0),
        (2520, 0),
        (5040, 0),
        (0, 3520),
        (2520, 3520),
        (5040, 3520),
        (0, 7040),
        (2520, 7040),
        (5040, 7040)
    ]
    a4page = Image.new('RGBA', (8168, 11552), (256, 256, 256, 256))
    try:
        i = 0
        while i < 9:
            character_img = Image.new('RGBA', (2520, 3520), (0, 0, 0, 256))
            character_img.paste(nine_cards_list[i], (20, 20))
            a4page.paste(character_img, print_points[i])
            i += 1
    except IndexError:
        pass
    # a4page.thumbnail((0,0))
    return a4page
