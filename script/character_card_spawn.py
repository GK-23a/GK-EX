from PIL import Image, ImageDraw, ImageFont
import json
import time
import os

# --------------------
# 预加载
# --------------------

# 日志系统
no_design_list = ['aloy','paimon', 'traveler', 'traveler_anemo', 'traveler_geo', 'traveler_electro', 'traveler_dendro']
if not os.path.exists('out/character_img'):
    os.makedirs('out/character_img')
with open('out/character_card_spawn.log', 'a', encoding='UTF-8') as log:
    log.write('--------------------\n['+time.asctime(time.localtime(time.time()))[4:19]+'] Info: character_card_spawn.py Working...'+'\n')


# 字体预加载
font = {}
font['title'] = ImageFont.truetype('font/SIMLI.TTF',              encoding='UTF-8', size=94) # 角色称号
font['name'] =  ImageFont.truetype('font/SIMLI.TTF',              encoding='UTF-8', size=300) # 角色名字
font['topic'] = ImageFont.truetype('font/SIMLI.TTF',              encoding='UTF-8', size=120) # 技能标题
font['category'] = ImageFont.truetype('font/MiSans-Semibold.ttf', encoding='UTF-8', size=72) # 技能类型
font['text'] =  ImageFont.truetype('font/MiSans-Regular.ttf',     encoding='UTF-8', size=72) # 技能内容
font['sign'] =  ImageFont.truetype('font/MiSans-Light.ttf',       encoding='UTF-8', size=56) # 卡底标记

# 颜色预定义
element_color = {}
element_color['pyro']    = [(246,136,123),(226,49,29)]
element_color['hydro']   = [(122,176,255),(28,114,253)]
element_color['cryo']    = [(200,230,250),(152,200,232)]
element_color['electro'] = [(236,137,254),(211,118,240)]
element_color['dendro']  = [(182,217,133),(123,180,45)]
element_color['anemo']   = [(137,232,217),(51,204,179)]
element_color['geo']     = [(234,209,128),(207,167,38)]
topicyy_color = (126,126,126,192)

# 中文标点修正预定义量
punctuation = ['，','。','；','：','？','！','、']
left_punctuation  = ['（','【','“']
right_punctuation = ['）','】','”']

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
    if font_style == 'text':
        img.multiline_text(
            position,
            text,
            fill=fill_color,
            font=font[font_style],
            spacing=4,
            align='left',
            direction=way,
            language='zh-Hans')
    else:
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

# json读取
with open('json/characters.json', encoding='UTF-8') as jsonfile:
    character_data = json.loads(jsonfile.read())

with open('out/character_card_spawn.log', 'a', encoding='UTF-8') as log:
    log.write('['+time.asctime(time.localtime(time.time()))[4:19]+'] Info: Pre-Load Over.'+'\n')

# --------------------
# 图层叠加
# --------------------

for ch_id in character_data:
        
    # 图层顺序：空白卡底、角色立绘、技能说明、元素外框、神之眼（底座和图案）、血条、初始护盾、名字、称号
    
    # 空白卡底
    cardimg = Image.new('RGBA', (2480,3480), (255,255,255,0))
    
    # 角色立绘
    try:
        with Image.open('img/character/' + ch_id + '.png') as character_image:
            cardimg.paste(character_image, (380,120))
    except FileNotFoundError:
        with open('out/character_card_spawn.log', 'a', encoding='UTF-8') as log:
            if ch_id not in no_design_list:
                log.write('['+time.asctime(time.localtime(time.time()))[4:19]+'] Error: FileNotFoundError(character_image), error_character: '+ch_id+' .\n')
            else:
                log.write('['+time.asctime(time.localtime(time.time()))[4:19]+'] Info: FileNotFoundError(character_image), but '+ch_id+' lol\n')
    # 技能说明
    try:
        skillimg = Image.new('RGBA', (2000,3240), (253,253,253,138))
        # 技能文本
        # INFO：未包含【技能类别粗体】【花色显示优化】
        height = 50
        length = 45
        color = element_color[character_data[ch_id]['element']]
        for skill_data in character_data[ch_id]['skills']:
            fill_color = color[0]
            if not skill_data['origin']:
                fill_color = 'black'
            imgdraw(skillimg, (50, height), skill_data['name'], fill_color, 'topic', 7, color[1])
            skilltext = ''
            skilltext_origin = skill_data['description']
            while True:
                while True:
                    textline = skilltext_origin[:length]
                    linelen = ImageDraw.Draw(skillimg).multiline_textbbox((50, height+85), textline, font['text'], align='left', direction='ltr', language='zh-Hans')
                    if linelen[2] > 1940:
                        length -= 1
                    else:
                        # 中文标点修正
                        if textline[-1:] in left_punctuation:
                            length -= 1
                        elif linelen[length+1:length+1] in right_punctuation or linelen[length+1:length+1] in punctuation:
                            length += 1
                        textline = skilltext_origin[:length]
                        break
                skilltext += textline + '\n'
                skilltext_origin = skilltext_origin[length:]
                if skilltext[-2:] == '\n\n':
                    skilltext = skilltext[:-2]
                    break
                else:
                    length = 45
            imgdraw(skillimg, (50, height+85), skilltext, 'black')
            height = ImageDraw.Draw(skillimg).multiline_textbbox((50, height+85), skilltext, font['text'], align='left', direction='ltr', language='zh-Hans')[3] + 35
        with open('json/version.json') as config:
            version = json.loads(config.read())
            imgdraw(skillimg, (50, height+10), 'GenshinKill ' + version['version'] + ' | Designer: ' + character_data[ch_id]['developer'] + ' , Artist: miHoYo', 'black', 'sign')
        skillimg = skillimg.crop((0,0,2000,height+100))
        cardimg.alpha_composite(skillimg, (380,3260-height)) # 技能层叠加
    except KeyError:
        with open('out/character_card_spawn.log', 'a', encoding='UTF-8') as log:
            if ch_id not in no_design_list:
                log.write('['+time.asctime(time.localtime(time.time()))[4:19]+'] Error: KeyError(skillimg), error_character: '+ch_id+' .\n')
            else:
                log.write('['+time.asctime(time.localtime(time.time()))[4:19]+'] Info: KeyError(skillimg), but '+ch_id+' lol\n')

    # 元素外框
    try:
        with Image.open('img/frame/' + character_data[ch_id]['element'] + '.png') as frame:
            cardimg.alpha_composite(frame)
    except FileNotFoundError:
        with open('out/character_card_spawn.log', 'a', encoding='UTF-8') as log:
            if ch_id not in no_design_list:
                log.write('['+time.asctime(time.localtime(time.time()))[4:19]+'] Error: FileNotFoundError(frame), error_character: '+ch_id+' .\n')
            else:
                log.write('['+time.asctime(time.localtime(time.time()))[4:19]+'] Info: FileNotFoundError(frame), but '+ch_id+' lol\n')

    # 神之眼
    try:
        with Image.open('img/szy/' + character_data[ch_id]['country'] + '.png') as dizuo:
            cardimg.alpha_composite(dizuo)
        tuanimg = character_data[ch_id]['element']
        if character_data[ch_id]['country'] == 'liyue':
            tuanimg += '_'
        with Image.open('img/szy/' + tuanimg  + '.png') as tuan:
            cardimg.alpha_composite(tuan)
    except FileNotFoundError:
        with open('out/character_card_spawn.log', 'a', encoding='UTF-8') as log:
            if ch_id not in no_design_list:
                log.write('['+time.asctime(time.localtime(time.time()))[4:19]+'] Error: FileNotFoundError(szy), error_character: '+ch_id+' .\n')
            else:
                log.write('['+time.asctime(time.localtime(time.time()))[4:19]+'] Info: FileNotFoundError(szy), but '+ch_id+' lol\n')

    # 血条、初始护盾
    if character_data[ch_id]['max_health_point'] <= 8:
        HP_height = 3100
        HP_value = character_data[ch_id]['health_point']
        while HP_value != 0:
            with Image.open('img/icon/HPyes.png') as HP:
                cardimg.alpha_composite(HP, (160, HP_height))
                HP_height -= 200
                HP_value -= 1
        empty_HP_value =  character_data[ch_id]['max_health_point'] - character_data[ch_id]['health_point']
        while empty_HP_value != 0:
            with Image.open('img/icon/HPno.png') as HP_empty:
                cardimg.alpha_composite(HP_empty, (160, HP_height))
                HP_height -= 200
                empty_HP_value -= 1
        armor_value = character_data[ch_id]['armor_point']
        if armor_value != 0:
            with Image.open('img/icon/Armor.png') as AP:
                cardimg.alpha_composite(AP, (160, HP_height))
                imgdraw(cardimg, (220, HP_height+40), str(armor_value), 'black')
    else:
        with open('out/character_card_spawn.log', 'a', encoding='UTF-8') as log:
            log.write('['+time.asctime(time.localtime(time.time()))[4:19]+'] Info: HP/Armor error, error_character: '+ch_id+' .\n')
    
    # 名字、称号
    text2_img = Image.new('RGBA', (2480,3480), (255,255,255,0))
    imgdraw(text2_img, (245, 490), character_data[ch_id]['name'], 'white', 'name', 8, 'black', 'mt')
    namehigh = ImageDraw.Draw(text2_img).textbbox((245, 490), character_data[ch_id]['name'], font['name'], direction='ttb', language='zh-Hans', anchor='mt')[3]
    imgdraw(text2_img, (245, namehigh), character_data[ch_id]['title'], (255,192,0,255), 'title', 4, 'black', 'mt')
    cardimg.alpha_composite(text2_img)
    
    # --------------------
    # 文件保存
    # --------------------

    cardimg.save('out/character_img/'+ch_id+'.png')

    with open('out/character_card_spawn.log', 'a', encoding='UTF-8') as log:
        log.write('['+time.asctime(time.localtime(time.time()))[4:19]+'] Info: SpawnImage: '+ch_id+' Over.\n')

with open('out/character_card_spawn.log', 'a', encoding='UTF-8') as log:
    log.write('['+time.asctime(time.localtime(time.time()))[4:19]+'] Info: character_card_spawn.py Work over. Exit now...'+'\n--------------------\n')

