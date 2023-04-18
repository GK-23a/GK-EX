from PIL import Image, ImageDraw, ImageFont
from os import path as os_path, makedirs as os_makedirs
from customlog import wlog
import json


if not os_path.exists('out/character_img'):
    os_makedirs('out/character_img')

# 字体预加载
font = {}
font['sign'] =     ImageFont.truetype('font/MiSans-Light.ttf',      encoding='UTF-8', size=56  ) # 卡底标记
font['category'] = ImageFont.truetype('font/MiSans-Semibold.ttf',   encoding='UTF-8', size=72  ) # 技能类型
font['text'] =     ImageFont.truetype('font/MiSans-Regular.ttf',    encoding='UTF-8', size=72  ) # 技能内容
font['suit'] =     ImageFont.truetype('font/有爱新黑CN-Regular.ttf', encoding='UTF-8', size=72  ) # 花色图标
font['title'] =    ImageFont.truetype('font/SIMLI.TTF',             encoding='UTF-8', size=94  ) # 角色称号
font['HP'] =       ImageFont.truetype('font/MiSans-Semibold.ttf',   encoding='UTF-8', size=100 ) # 特殊血条
font['topic'] =    ImageFont.truetype('font/SIMLI.TTF',             encoding='UTF-8', size=120 ) # 技能标题
font['name'] =     ImageFont.truetype('font/SIMLI.TTF',             encoding='UTF-8', size=300 ) # 角色名字

# 颜色预定义
topicyy_color = (126,126,126,192)
element_color = {
    'pyro'    : [ ( 246, 136, 123 ) , ( 226,  49,  29 ) ],
    'hydro'   : [ ( 122, 176, 255 ) , (  28, 114, 253 ) ],
    'cryo'    : [ ( 200, 230, 250 ) , ( 152, 200, 232 ) ],
    'electro' : [ ( 236, 137, 254 ) , ( 211, 118, 240 ) ],
    'dendro'  : [ ( 182, 217, 133 ) , ( 123, 180,  45 ) ],
    'anemo'   : [ ( 137, 232, 217 ) , (  51, 204, 179 ) ],
    'geo'     : [ ( 234, 209, 128 ) , ( 207, 167,  38 ) ],
}

# 预定义中文标点习惯修复
punctuation = ['，','。','；','：','？','！','、']
left_punctuation  = ['（','【','“']
right_punctuation = ['）','】','”']

# 预定义技能类型字符串
skill_categories = ['锁定技，','转换技，','限定技，','觉醒技，','使命技，']

# 预定义简化ImageDraw函数
def imgdraw(bg,position,text,fill_color,font_style='text',side_width=0,side_color=None,md='lt'):
    img= ImageDraw.Draw(bg)
    way = 'ltr'
    if font_style in ['title','name']:
        way = 'ttb'
    if font_style in ['title','topic']:
        img.text(
            (position[0]+4,position[1]+4),
            text,
            fill=topicyy_color,
            font=font[font_style],
            anchor=md,
            direction=way,
            language='zh-Hans',
            stroke_width=side_width,
            stroke_fill=topicyy_color)
    elif font_style == 'name':
        img.text(
            (position[0]+4,position[1]+4),
            text,
            fill=topicyy_color,
            font=font[font_style],
            anchor=md,
            direction=way,
            language='zh-Hans',
            stroke_width=side_width+4,
            stroke_fill=(126,126,126,160))
    img.text(
        position,
        text,
        fill=fill_color,
        font=font[font_style],
        anchor=md,
        direction=way,
        language='zh-Hans',
        stroke_width=side_width,
        stroke_fill=side_color)

# 预定义图像生成函数
def cardbuild(ch_id, character_data, wlog_path='out/debug.log', info_path='json/info.json'):
    if character_data[ch_id]['design_info'] == 1:
        
        # 空白卡底
        cardimg = Image.new('RGBA', (2480,3480), (255,255,255,0))
        
        # 角色立绘
        try:
            with Image.open('img/character/' + ch_id + '.png') as character_image:
                cardimg.paste(character_image, (380,120))
        except Exception as errorinfo:
            wlog(__file__, wlog_path, ch_id + '在角色立绘阶段发生错误：' + str(errorinfo), 'Error')
    
        # 技能说明
        try:
            skillimg = Image.new('RGBA', (2000,3240), (253,253,253,138))
            # 技能文本
            height = 50
            length = 45
            color = element_color[character_data[ch_id]['element']]
            for skill_data in character_data[ch_id]['skills']:
                fill_color = color[0]
                if not skill_data['origin']:
                    fill_color = 'black'
                imgdraw(skillimg, (50, height), skill_data['name'], fill_color, 'topic', 7, color[1])
                skilltext_origin = skill_data['description']
                # 花色标记
                suit_sign = []
                point_sign = []
                if 'suit' in skilltext_origin:
                    suit_exist = True
                    point = 0   
                    while True:
                        if skilltext_origin[point:point+12] == '<suit:heart>':
                            skilltext_origin = skilltext_origin.replace('<suit:heart>', '　', 1)
                            suit_sign.append('heart')
                        elif skilltext_origin[point:point+12] == '<suit:spade>':
                            skilltext_origin = skilltext_origin.replace('<suit:spade>', '　', 1)
                            suit_sign.append('spade')
                        elif skilltext_origin[point:point+14] == '<suit:diamond>':
                            skilltext_origin = skilltext_origin.replace('<suit:diamond>', '　', 1)
                            suit_sign.append('diamond')
                        elif skilltext_origin[point:point+11] == '<suit:club>':
                            skilltext_origin = skilltext_origin.replace('<suit:club>', '　', 1)
                            suit_sign.append('club')
                        elif skilltext_origin[point:point+14] == '':
                            break
                        point += 1
                else:
                    suit_exist = False
                # 换行计算
                body_height = height
                body_skilltext_origin = skilltext_origin
                while True:
                    while True:
                        textline = skilltext_origin[:length]
                        linelen = ImageDraw.Draw(skillimg).textbbox((50, height+95), textline, font['text'], align='left', direction='ltr', language='zh-Hans')
                        if linelen[2] > 1940:
                            length -= 1
                        else:
                            # 中文标点修正
                            if skilltext_origin[length:length+1] in punctuation:
                                length += 1
                            elif skilltext_origin[length:length+1] in right_punctuation:
                                if skilltext_origin[length+1:length+2] in punctuation:
                                    length -= 2
                                else:
                                    length += 1
                            elif skilltext_origin[length-1:length] in left_punctuation:
                                length -= 1
                            textline = skilltext_origin[:length]
                            break
                    imgdraw(skillimg, (50, height+95), textline, 'black')
                    if suit_exist:
                        point = 0
                        while point <= len(textline):
                            if textline[:point][-1:] == '　':
                                point_sign.append(ImageDraw.Draw(skillimg).textbbox((50, height+95), textline[:point-1], font['text'], align='left', direction='ltr', language='zh-Hans'))
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
                        imgdraw(skillimg, (point_sign[point][2], point_sign[point][3]-84), suit_text, suit_color, 'suit')
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
                        linelen = ImageDraw.Draw(skillimg).textbbox((50, body_height+95), textline, font['text'], align='left', direction='ltr', language='zh-Hans')
                        if linelen[2] > 1940:
                            length -= 1
                        else:
                            # 中文标点修正
                            if boldtext[length:length+1] in punctuation:
                                length += 1
                            elif boldtext[length:length+1] in right_punctuation:
                                if boldtext[length+1:length+2] in punctuation:
                                    length -= 2
                                else:
                                    length += 1
                            elif boldtext[length-1:length] in left_punctuation:
                                length -= 1
                            textline = boldtext[:length]
                            break
                    imgdraw(skillimg, (50, body_height+95), textline, 'black', 'category')
                    boldtext = boldtext[length:]
                    body_height += 77
                    if boldtext == '':
                        body_height += 110
                        break
                    else:
                        length = 45
            with open(info_path) as config:
                version = json.loads(config.read())
                imgdraw(skillimg, (50, height+10), 'GenshinKill ' + version['version'] + ' | Designer: ' + character_data[ch_id]['designer'] + ' , Artist: miHoYo', 'black', font_style='sign')
            # 技能图层剪切
            skillimg = skillimg.crop((0,0,2000,height+100))
            cardimg.alpha_composite(skillimg, (380,3260-height)) # 技能层叠加
        except Exception as errorinfo:
            wlog(__file__, wlog_path, ch_id + '在技能生成阶段发生错误：' + str(errorinfo), 'Error')
    
        # 元素外框
        try:
            with Image.open('img/frame/' + character_data[ch_id]['element'] + '.png') as frame:
                cardimg.alpha_composite(frame)
        except Exception as errorinfo:
            wlog(__file__, wlog_path, ch_id + '在元素外框生成阶段发生错误：' + str(errorinfo), 'Error')
    
        # 神之眼
        try:
            with Image.open('img/szy/' + character_data[ch_id]['country'] + '.png') as dizuo:
                cardimg.alpha_composite(dizuo)
            tuanimg = character_data[ch_id]['element']
            if character_data[ch_id]['country'] == 'liyue':
                tuanimg += '_'
            with Image.open('img/szy/' + tuanimg  + '.png') as tuan:
                cardimg.alpha_composite(tuan)
        except Exception as errorinfo:
            wlog(__file__, wlog_path, ch_id + '在神之眼生成阶段发生错误：' + str(errorinfo), 'Error')
    
        # 名字、称号
        try:
            infoimg = Image.new('RGBA', (2480,3480), (255,255,255,0))
            imgdraw(infoimg, (245, 490), character_data[ch_id]['name'], 'white', 'name', 8, 'black', 'mt')
            namehigh = ImageDraw.Draw(infoimg).textbbox((245, 490), character_data[ch_id]['name'], font['name'], direction='ttb', language='zh-Hans', anchor='mt')[3]
            imgdraw(infoimg, (245, namehigh), character_data[ch_id]['title'], (255,192,0,255), 'title', 4, 'black', 'mt')
            cardimg.alpha_composite(infoimg)
    
        # 体力值、初始护甲
            HPimg = Image.new('RGBA', (2480,3480), (255,255,255,0))
            HP_height = 3100
            HP_value = character_data[ch_id]['health_point']
            while HP_value != 0:
                with Image.open('img/icon/HPyes.png') as HP:
                    HPimg.alpha_composite(HP, (160, HP_height))
                    HP_height -= 200
                    HP_value -= 1
            empty_HP_value =  character_data[ch_id]['max_health_point'] - character_data[ch_id]['health_point']
            while empty_HP_value != 0:
                with Image.open('img/icon/HPno.png') as HP_empty:
                    HPimg.alpha_composite(HP_empty, (160, HP_height))
                    HP_height -= 200
                    empty_HP_value -= 1
            armor_value = character_data[ch_id]['armor_point']
            if armor_value != 0:
                with Image.open('img/icon/Armor.png') as AP:
                    HPimg.alpha_composite(AP, (160, HP_height))
                    imgdraw(HPimg, (225, HP_height+55), str(armor_value), 'black')
            # 体力值区域后续结算：与称号和名字的防冲突（简单）
            textheight = ImageDraw.Draw(infoimg).textbbox((245, namehigh), character_data[ch_id]['title'], font['title'], stroke_width=4, direction='ttb', language='zh-Hans', anchor='mt')[3]
            if HP_height <= textheight:
                HPimg = Image.new('RGBA', (2480,3480), (255,255,255,0))
                with Image.open('img/icon/HPyes.png') as HP:
                    HPimg.alpha_composite(HP, (160, 2700))
                ImageDraw.Draw(HPimg).text(
                    (215,2900),
                    str(character_data[ch_id]['health_point'])+'\n/\n'+str(character_data[ch_id]['max_health_point']),
                    fill=(30,140,30),
                    spacing=4,
                    font=font['HP'],
                    language='zh-Hans',
                    stroke_width=8,
                    stroke_fill=(0,115,0))
                if armor_value != 0:
                    with Image.open('img/icon/Armor.png') as AP:
                        HPimg.alpha_composite(AP, (160, 2500))
                        imgdraw(HPimg, (225, 2540), str(armor_value), 'black')
            cardimg.alpha_composite(HPimg)
        except Exception as errorinfo:
            wlog(__file__, wlog_path, ch_id + '在名字、称号、及初始体力与护甲计算阶段发生错误：' + str(errorinfo), 'Error')
        message = character_data[ch_id]['name'] + ' (' + ch_id + ')' + '已成功完成生成。'
        wlog(__file__, wlog_path, message)
        return cardimg
    else:
        wlog(__file__, 'out/debug.log', ch_id + ' 未设计完成，已跳过生成。')
        return False

# 预定义打印张生成函数
printpoint = [
    (0,0),(2520,0),(5040,0),
    (0,3520),(2520,3520),(5040,3520),
    (0,7040),(2520,7040),(5040,7040)
    ]
def print_build(nine_cards_list):
    a4page = Image.new('RGBA', (8168, 11552), (256, 256, 256, 256))
    try:
        i = 0
        while i < 9:
            characterimg = Image.new('RGBA', (2520, 3520), (0, 0, 0, 256))
            characterimg.paste(nine_cards_list[i], (20,20))
            a4page.paste(characterimg, printpoint[i])
            i += 1
    except IndexError:
        pass
    # a4page.thumbnail((0,0))
    return a4page
        
