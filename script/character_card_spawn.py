from PIL import Image, ImageDraw, ImageFont
from os import path as os_path, makedirs as os_makedirs
from customlog import wlog
import json

# --------------------
# 预加载
# --------------------
wlog('out/debug.log', '角色图像构建开始。')
wlog('out/debug.log', '进行初始化预加载。')

if not os_path.exists('out/character_img'):
    os_makedirs('out/character_img')
    wlog('out/debug.log', '未检测到 out/character_img 文件夹，已创建。')

# 字体预加载
font = {}
font['title'] =    ImageFont.truetype('font/SIMLI.TTF',           encoding='UTF-8', size=94  ) # 角色称号
font['name'] =     ImageFont.truetype('font/SIMLI.TTF',           encoding='UTF-8', size=300 ) # 角色名字
font['topic'] =    ImageFont.truetype('font/SIMLI.TTF',           encoding='UTF-8', size=120 ) # 技能标题
font['category'] = ImageFont.truetype('font/MiSans-Semibold.ttf', encoding='UTF-8', size=72  ) # 技能类型
font['HP'] =       ImageFont.truetype('font/MiSans-Semibold.ttf', encoding='UTF-8', size=100  ) # 特殊血条
font['text'] =     ImageFont.truetype('font/MiSans-Regular.ttf',  encoding='UTF-8', size=72  ) # 技能内容
font['sign'] =     ImageFont.truetype('font/MiSans-Light.ttf',    encoding='UTF-8', size=56  ) # 卡底标记
wlog('out/debug.log', '字体预加载完成。')

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
wlog('out/debug.log', '元素颜色预加载完成。')

# 预定义中文标点习惯修复
def punctuation_fix(text, length):
    punctuation = ['，','。','；','：','？','！','、']
    left_punctuation  = ['（','【','“']
    right_punctuation = ['）','】','”']
    if text[:length-1] in left_punctuation:
        length -= 1
    elif text[length:length+1] in right_punctuation + punctuation:
        length += 1
        if text[length:length+1] in right_punctuation + punctuation:
            length -= 2
    return [text, length]
wlog('out/debug.log', '中文标点习惯修复函数预加载完成。')

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
wlog('out/debug.log', 'ImageDraw 简化函数 imgdraw() 预加载完成。')

# json读取
with open('json/characters.json', encoding='UTF-8') as jsonfile:
    character_data = json.loads(jsonfile.read())

wlog('out/debug.log', '"characters.json"读取完成。')
wlog('out/debug.log', '预加载内容全部完成。')

# --------------------
# 图层叠加
# --------------------


for ch_id in character_data:

    if character_data[ch_id]['design_info'] == 1:
        
        # 空白卡底
        cardimg = Image.new('RGBA', (2480,3480), (255,255,255,0))
        
        # 角色立绘
        try:
            with Image.open('img/character/' + ch_id + '.png') as character_image:
                cardimg.paste(character_image, (380,120))
        except Exception as errorinfo:
            wlog('out/debug.log', ch_id + '在角色立绘阶段发生 ' + str(errorinfo) + ' 错误。', 'Error')
    
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
                            # 中文标点修正【有严重bug】
                            fixer = punctuation_fix(skilltext_origin, length)
                            skilltext_origin = fixer[0]
                            length = fixer[1]
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
                imgdraw(skillimg, (50, height+10), 'GenshinKill ' + version['version'] + ' | Designer: ' + character_data[ch_id]['designer'] + ' , Artist: miHoYo', 'black', font_style='sign')
            skillimg = skillimg.crop((0,0,2000,height+100))
            cardimg.alpha_composite(skillimg, (380,3260-height)) # 技能层叠加
        except Exception as errorinfo:
            wlog('out/debug.log', ch_id + '在技能生成阶段发生 ' + str(errorinfo) + ' 错误。', 'Error')
    
    
        # 元素外框
        try:
            with Image.open('img/frame/' + character_data[ch_id]['element'] + '.png') as frame:
                cardimg.alpha_composite(frame)
        except Exception as errorinfo:
            wlog('out/debug.log', ch_id + '在元素外框生成阶段发生 ' + str(errorinfo) + ' 错误。', 'Error')
    
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
            wlog('out/debug.log', ch_id + '在神之眼生成阶段发生 ' + str(errorinfo) + ' 错误。', 'Error')
    
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
                    imgdraw(HPimg, (225, HP_height+40), str(armor_value), 'black')
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
            wlog('out/debug.log', ch_id + '在名字、称号、及初始体力与护甲计算阶段发生 ' + str(errorinfo) + ' 错误。', 'Error')
    
        # --------------------
        # 文件保存
        # --------------------
    
        cardimg.save('out/character_img/'+ch_id+'.png')
    
        wlog('out/debug.log', character_data[ch_id]['name'] + ' ( ' + ch_id + ' )' + '已成功完成生成，并保存为 "' + ch_id + '.png" 。')
    else:
        wlog('out/debug.log', ch_id + ' 未设计完成，已跳过生成。')

wlog('out/debug.log', '角色图像生成已完成全部构建与保存。\n')

