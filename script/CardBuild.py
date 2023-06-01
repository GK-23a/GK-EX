from PIL import Image, ImageDraw, ImageFont
from os import path as os_path, makedirs as os_makedirs

from ExtraF import wlog
import gk_card

# if not os_path.exists('out/character_img'):
#     os_makedirs('out/character_img')

# 预加载

# 字体
font = {
    'sign': ImageFont.truetype('data/font/MiSans-Light.ttf', size=56, encoding='utf-8'),  # 卡底标记
    'category': ImageFont.truetype('data/font/MiSans-Semibold.ttf', size=72, encoding='utf-8'),  # 技能类型
    'text': ImageFont.truetype('data/font/MiSans-Regular.ttf', size=72, encoding='utf-8'),  # 技能内容
    'suit': ImageFont.truetype('data/font/有爱新黑CN-Regular.ttf', size=72, encoding='utf-8'),  # 花色图标
    'title': ImageFont.truetype('data/font/SIMLI.TTF', size=94, encoding='utf-8'),  # 角色称号
    'HP': ImageFont.truetype('data/font/MiSans-Semibold.ttf', size=100, encoding='utf-8'),  # 特殊血条
    'topic': ImageFont.truetype('data/font/SIMLI.TTF', size=120, encoding='utf-8'),  # 技能标题
    'name': ImageFont.truetype('data/font/SIMLI.TTF', size=300, encoding='utf-8')  # 角色名字
}
# 颜色
topicyy_color = (126, 126, 126, 192)
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


def imgcut(img_path, width=2000, height=3240):
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


def imgdraw(bg,
            position,
            text,
            fill_color,
            font_style='text',
            side_width=0,
            side_color=None,
            md='lt'):
    """简化的ImageDraw函数"""
    img = ImageDraw.Draw(bg)
    way = 'ltr'
    if font_style in ['title', 'name']:
        way = 'ttb'
    if font_style in ['title', 'topic']:
        img.text((position[0] + 4, position[1] + 4),
                 text,
                 fill=topicyy_color,
                 font=font[font_style],
                 anchor=md,
                 direction=way,
                 language='zh-Hans',
                 stroke_width=side_width,
                 stroke_fill=topicyy_color,
                 encoding='UTF-8')
    elif font_style == 'name':
        img.text((position[0] + 4, position[1] + 4),
                 text,
                 fill=topicyy_color,
                 font=font[font_style],
                 anchor=md,
                 direction=way,
                 language='zh-Hans',
                 stroke_width=side_width + 4,
                 stroke_fill=(126, 126, 126, 160),
                 encoding='UTF-8')
    img.text(position,
             text,
             fill=fill_color,
             font=font[font_style],
             anchor=md,
             direction=way,
             language='zh-Hans',
             stroke_width=side_width,
             stroke_fill=side_color,
             encoding='UTF-8')


def build_card


def cardbuild_func(character_data: dict,
                   versions: str,
                   wlog_path='out/debug.log',
                   img_path='data/img/character/',
                   img_cut=False,
                   progress_bar=None,
                   ignore_designer=False):
    """生成GK-23a卡牌的完整函数，返回PIL.Image对象(或返回空值)"""
    if ignore_designer:
        design_tag = True
    elif character_data['design_info'] == 1:
        design_tag = True
    else:
        design_tag = False

    if design_tag:
        # 空白卡底
        card_img = Image.new('RGBA', (2480, 3480), (255, 255, 255, 0))
        if progress_bar: progress_bar.setValue(5)  # progressBar - Setting

        # 角色立绘
        try:
            if img_cut:
                character_image = imgcut(img_path + character_data['id'] + '.png')
            else:
                character_image = Image.open(img_path + character_data['id'] + '.png')
            card_img.paste(character_image, (380, 120))
        except Exception as error_info:
            wlog(__file__, wlog_path, character_data['id'] + '在角色立绘阶段发生错误：' + str(error_info), 'Error')
        if progress_bar: progress_bar.setValue(12)  # progressBar - Setting
        # 技能说明
        try:
            skill_img = Image.new('RGBA', (2000, 3240), (253, 253, 253, 138))
            # 技能文本
            height = 50
            length = 45
            color = element_color[character_data['element']]
            for skill_data in character_data['skills']:
                fill_color = color[0]
                if not skill_data['origin']:
                    fill_color = 'black'
                imgdraw(skill_img, (50, height), skill_data['name'], fill_color,
                        'topic', 7, color[1])
                skilltext_origin = skill_data['description']
                # 花色标记
                suit_sign = []
                point_sign = []
                suit_exist = False
                point = 0

                suit_dict = {'♥': ('heart',), '♠': ('spade',), '♦': ('diamond',), '♣': ('club',)}
                while point < len(skilltext_origin):
                    char = skilltext_origin[point:point + 1]
                    if char in suit_dict:
                        skilltext_origin = skilltext_origin[:point] + '　' + skilltext_origin[point + 1:]
                        suit_sign.extend(suit_dict[char])
                        suit_exist = True
                    elif char == '':
                        break
                    point += 1

                # 换行计算
                body_height = height
                body_skilltext_origin = skilltext_origin
                while True:
                    while True:
                        textline = skilltext_origin[:length]
                        linelen = ImageDraw.Draw(skill_img).textbbox(
                            (50, height + 95),
                            textline,
                            font['text'],
                            align='left',
                            direction='ltr',
                            language='zh-Hans')
                        if linelen[2] > 1940:
                            length -= 1
                        else:
                            # 中文标点修正
                            if skilltext_origin[length:length + 1] in punctuation:
                                length += 1
                            elif skilltext_origin[length:length + 1] in right_punctuation:
                                if skilltext_origin[length + 1:length + 2] in punctuation:
                                    length -= 2
                                else:
                                    length += 1
                            elif skilltext_origin[
                                 length - 1:length] in left_punctuation:
                                length -= 1
                            textline = skilltext_origin[:length]
                            break
                    imgdraw(skill_img, (50, height + 95), textline, 'black')
                    if suit_exist:
                        point = 0
                        while point <= len(textline):
                            if textline[:point][-1:] == '　':
                                point_sign.append(
                                    ImageDraw.Draw(skill_img).textbbox(
                                        (50, height + 95),
                                        textline[:point - 1],
                                        font['text'],
                                        align='left',
                                        direction='ltr',
                                        language='zh-Hans'))
                            point += 1
                    skilltext_origin = skilltext_origin[length:]
                    height += 77
                    if skilltext_origin == '':
                        height += 110
                        break
                    else:
                        length = 45
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
                        imgdraw(
                            skill_img,
                            (point_sign[point][2], point_sign[point][3] - 84),
                            suit_text, suit_color, 'suit')
                        point += 1
                # 技能类别粗体覆盖
                boldtext = ''
                while True:
                    if body_skilltext_origin[:4] not in skill_categories:
                        break
                    boldtext += body_skilltext_origin[:4]
                    body_skilltext_origin = body_skilltext_origin[4:]
                while True:
                    while True:
                        textline = boldtext[:length]
                        linelen = ImageDraw.Draw(skill_img).textbbox(
                            (50, body_height + 95),
                            textline,
                            font['text'],
                            align='left',
                            direction='ltr',
                            language='zh-Hans')
                        if linelen[2] > 1940:
                            length -= 1
                        else:
                            # 中文标点修正
                            if boldtext[length:length + 1] in punctuation:
                                length += 1
                            elif boldtext[length:length +
                                                 1] in right_punctuation:
                                if boldtext[length + 1:length +
                                                       2] in punctuation:
                                    length -= 2
                                else:
                                    length += 1
                            elif boldtext[length -
                                          1:length] in left_punctuation:
                                length -= 1
                            textline = boldtext[:length]
                            break
                    imgdraw(skill_img, (50, body_height + 95), textline,
                            'black', 'category')
                    boldtext = boldtext[length:]
                    body_height += 77
                    if boldtext == '':
                        body_height += 110
                        break
                    else:
                        length = 45
            imgdraw(skill_img, (50, height + 10),
                    'GenshinKill ' + versions + ' | Designer: ' +
                    character_data['designer'] +
                    ' , Artist: miHoYo',
                    'black',
                    font_style='sign')
            if progress_bar: progress_bar.setValue(55)  # progressBar - Setting
            # 技能图层剪切
            skill_img = skill_img.crop((0, 0, 2000, height + 100))
            card_img.alpha_composite(skill_img, (380, 3260 - height))  # 技能层叠加
        except Exception as error_info:
            wlog(__file__, wlog_path, character_data['id'] + '在技能生成阶段发生错误：' + str(error_info), 'Error')
        if progress_bar: progress_bar.setValue(60)  # progressBar - Setting

        # 元素外框
        try:
            with Image.open(os_path.join('data', 'img', 'frame', character_data['element'] + '.png')) as frame:
                card_img.alpha_composite(frame)
        except Exception as error_info:
            wlog(__file__, wlog_path, character_data['id'] + '在元素外框生成阶段发生错误：' + str(error_info), 'Error')
        if progress_bar: progress_bar.setValue(68)  # progressBar - Setting

        # 神之眼
        try:
            with Image.open(os_path.join('data', 'img', 'szy', character_data['country'] + '.png')) as dizuo:
                card_img.alpha_composite(dizuo)
            tuanimg = character_data['element']
            if character_data['country'] == 'liyue':
                tuanimg += '_'
            with Image.open(os_path.join('data', 'img', 'szy', tuanimg + '.png')) as tuan:
                card_img.alpha_composite(tuan)
        except Exception as error_info:
            wlog(__file__, wlog_path, character_data['id'] + '在神之眼生成阶段发生错误：' + str(error_info), 'Error')
        if progress_bar: progress_bar.setValue(76)  # progressBar - Setting

        # 名字、称号
        try:
            infoimg = Image.new('RGBA', (2480, 3480), (255, 255, 255, 0))
            imgdraw(infoimg, (245, 490), character_data['name'],
                    'white', 'name', 8, 'black', 'mt')
            namehigh = ImageDraw.Draw(infoimg).textbbox(
                (245, 490),
                character_data['name'],
                font['name'],
                direction='ttb',
                language='zh-Hans',
                anchor='mt')[3]
            imgdraw(infoimg, (245, namehigh), character_data['title'],
                    (255, 192, 0, 255), 'title', 4, 'black', 'mt')
            card_img.alpha_composite(infoimg)

            # 体力值、初始护甲
            HPimg = Image.new('RGBA', (2480, 3480), (255, 255, 255, 0))
            HP_height = 3100
            HP_value = character_data['health_point']
            while HP_value != 0:
                with Image.open(os_path.join('data', 'img', 'icon', 'HPyes.png')) as HP:
                    HPimg.alpha_composite(HP, (160, HP_height))
                    HP_height -= 200
                    HP_value -= 1
            empty_HP_value = character_data[
                                 'max_health_point'] - character_data['health_point']
            while empty_HP_value != 0:
                with Image.open(os_path.join('data', 'img', 'icon', 'HPno.png')) as HP_empty:
                    HPimg.alpha_composite(HP_empty, (160, HP_height))
                    HP_height -= 200
                    empty_HP_value -= 1
            armor_value = character_data['armor_point']
            if armor_value != 0:
                with Image.open(os_path.join('data', 'img', 'icon', 'Armor.png')) as AP:
                    HPimg.alpha_composite(AP, (160, HP_height))
                    imgdraw(HPimg, (225, HP_height + 55), str(armor_value),
                            'black')
            if progress_bar: progress_bar.setValue(84)  # progressBar - Setting
            # 体力值区域后续结算：与称号和名字的防冲突（简单）
            textheight = ImageDraw.Draw(infoimg).textbbox(
                (245, namehigh),
                character_data['title'],
                font['title'],
                stroke_width=4,
                direction='ttb',
                language='zh-Hans',
                anchor='mt')[3]
            if HP_height <= textheight:
                HPimg = Image.new('RGBA', (2480, 3480), (255, 255, 255, 0))
                with Image.open(os_path.join('data', 'img', 'icon', 'HPyes.png')) as HP:
                    HPimg.alpha_composite(HP, (160, 2700))
                ImageDraw.Draw(HPimg).text(
                    (215, 2900),
                    str(character_data['health_point']) + '\n/\n' +
                    str(character_data['max_health_point']),
                    fill=(30, 140, 30),
                    spacing=4,
                    font=font['HP'],
                    language='zh-Hans',
                    stroke_width=8,
                    stroke_fill=(0, 115, 0))
                if armor_value != 0:
                    with Image.open(os_path.join('data', 'img', 'icon', 'Armor.png')) as AP:
                        HPimg.alpha_composite(AP, (160, 2500))
                        imgdraw(HPimg, (225, 2540), str(armor_value), 'black')
            card_img.alpha_composite(HPimg)
            if progress_bar: progress_bar.setValue(96)  # progressBar - Setting
        except Exception as error_info:
            wlog(__file__, wlog_path,
                 character_data['id'] + '在名字、称号、及初始体力与护甲计算阶段发生错误：' + str(error_info), 'Error')
        message = character_data['name'] + ' (' + character_data['id'] + ')' + '已成功完成生成。'
        wlog(__file__, wlog_path, message)
        if progress_bar: progress_bar.setValue(100)  # progressBar - Setting
        return card_img
    else:
        wlog(__file__, 'out/debug.log', character_data['id'] + ' 未设计完成，已跳过生成。')
        return None


def print_build(nine_cards_list: list):
    """创建A4的打印张图像"""
    printpoint = [
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
            characterimg = Image.new('RGBA', (2520, 3520), (0, 0, 0, 256))
            characterimg.paste(nine_cards_list[i], (20, 20))
            a4page.paste(characterimg, printpoint[i])
            i += 1
    except IndexError:
        pass
    # a4page.thumbnail((0,0))
    return a4page
