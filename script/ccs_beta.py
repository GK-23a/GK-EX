from PIL import Image, ImageDraw, ImageFont
import json

# 字体预加载
font = {}
font['title'] =    ImageFont.truetype('font/SIMLI.TTF',           encoding='UTF-8', size=94  ) # 角色称号
font['name'] =     ImageFont.truetype('font/SIMLI.TTF',           encoding='UTF-8', size=300 ) # 角色名字
font['topic'] =    ImageFont.truetype('font/SIMLI.TTF',           encoding='UTF-8', size=120 ) # 技能标题
font['category'] = ImageFont.truetype('font/MiSans-Semibold.ttf', encoding='UTF-8', size=72  ) # 技能类型
font['HP'] =       ImageFont.truetype('font/MiSans-Semibold.ttf', encoding='UTF-8', size=100  ) # 特殊血条
font['text'] =     ImageFont.truetype('font/MiSans-Regular.ttf',  encoding='UTF-8', size=72  ) # 技能内容
font['sign'] =     ImageFont.truetype('font/MiSans-Light.ttf',    encoding='UTF-8', size=56  ) # 卡底标记

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

def punctuation_fix(text, length):
    if text[:length-1] in left_punctuation:
        length -= 1
    elif text[length:length+1] in right_punctuation + punctuation:
        length += 1
        if text[length:length+1] in right_punctuation + punctuation:
            length -= 2
    return [text, length]
# --------------------
# 预加载结束
# --------------------

character_data = {
    'traveler': {
        'title': '测试角色', 
        'name': '旅行者', 
        'sex': 'male', 
        'element': 'geo', 
        'country': 'mondstadt', 
        'developer': 'goldsheep3', 
        'health_point': 4, 
        'max_health_point': 3, 
        'armor_point': 1, 
        'skills': [
            {
                'name': '拟造', 
                'id': 'nizao', 
                'description': '出牌阶段开始时，若场上没有【阳华】，则你可以弃置一张），使得', 
                'category': [], 
                'origin': True
                }]}}
ch_id = 'traveler'

try:
    try:
# --------------------
# 技能层原文
# --------------------

    # 技能说明
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
                        # 中文标点习惯修正
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
            imgdraw(skillimg, (50, height+10), 'GenshinKill ' + version['version'] + ' | Designer: ' + character_data[ch_id]['developer'] + ' , Artist: miHoYo', 'black', 'sign')
        skillimg = skillimg.crop((0,0,2000,height+100))

# --------------------
    except:
        raise
except:
    raise