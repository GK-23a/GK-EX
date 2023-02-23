from PIL import Image, ImageDraw, ImageFont
import json

# --------------------
# 预加载
# --------------------

# 字体预加载
font = {}
font['title'] = ImageFont.truetype('font/SIMLI.TTF',              encoding='UTF-8', size=74) # 角色称号
font['name'] =  ImageFont.truetype('font/SIMLI.TTF',              encoding='UTF-8', size=74) # 角色名字
font['topic'] = ImageFont.truetype('font/SIMLI.TTF',              encoding='UTF-8', size=120) # 技能标题
font['category'] = ImageFont.truetype('font/MiSans-Semibold.ttf', encoding='UTF-8', size=72) # 技能类型
font['text'] =  ImageFont.truetype('font/MiSans-Regular.ttf',     encoding='UTF-8', size=72) # 技能内容
font['sign'] =  ImageFont.truetype('font/MiSans-Light.ttf',       encoding='UTF-8', size=72) # 卡底标记

# 颜色预定义
element_color = {}
element_color['pyro']    = [(0,0,0),(0,0,0)]
element_color['hydro']   = [(122,176,255),(28,114,253)]
element_color['cryo']    = [(0,0,0),(0,0,0)]
element_color['electro'] = [(0,0,0),(0,0,0)]
element_color['dendro']  = [(0,0,0),(0,0,0)]
element_color['anemo']   = [(0,0,0),(0,0,0)]
element_color['geo']     = [(0,0,0),(0,0,0)]
topicyy_color = (126,126,126,192)

# 中文标点修正预定义量
left_punctuation  = ['，','。','；','：','？','！','、','（','【','“']
right_punctuation = ['）','】','”']

# 预定义简化ImageDraw函数
def imgdraw(bg,position,text,fill_color,font_style='text',side_width=0,side_color=None):
    """简化的ImageDraw函数，对text和topic有其他优化。"""
    img= ImageDraw.Draw(bg)
    way = 'ltr'
    if font_style in ['title','name']:
        way = 'ttb'
    if font_style == 'topic':
        img.text(
            (position[0]+2,position[1]+2),
            text,
            fill=topicyy_color,
            font=font[font_style],
            anchor='lt',
            direction=way,
            language='zh-Hans',
            stroke_width=side_width,
            stroke_fill=topicyy_color)
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
            anchor='lt',
            direction=way,
            language='zh-Hans',
            stroke_width=side_width,
            stroke_fill=side_color)

# json读取
with open('json/characters.json', encoding='UTF-8') as jsonfile:
    character_data = json.loads(jsonfile.read())

# --------------------
# 图层叠加
# --------------------

# DEBUG
ch_id = 'xiao'
# for ch_id in character_data:
    
# 图层顺序：空白卡底、角色立绘、技能说明、元素外框、神之眼（底座和图案）、称号、名称、血条、初始护盾   

# 空白卡底
cardbg = Image.new('RGBA', (2480,3480), (255,255,255,0))
# 角色立绘
with Image.open('img/character/' + ch_id + '.png') as character_image:
    cardbg.paste(character_image, (380,120))

# 技能说明

skillbg = Image.new('RGBA', (2000,3240), (253,253,253,138))


# 技能文本
# INFO：未包含【技能类别粗体】【花色显示优化】
height = 50
number = 0
color = element_color[character_data[ch_id]['element']]
imgdraw(skillbg, (50, height), character_data[ch_id]['skills'][number]['name'], color[0], 'topic', 4, color[1])
length = 45
skilltext = ''
skilltext_origin = character_data[ch_id]['skills'][number]['description']
while True:
    while True:
        textline = skilltext_origin[:length]
        linelen = ImageDraw.Draw(skillbg).multiline_textbbox((50, height+86), textline, font['text'], align='left', direction='ltr', language='zh-Hans')
        if linelen[2] > 1940:
            length -= 1
        else:
            # 中文标点修正
            if textline[-1:] in left_punctuation:
                length -= 1
            elif linelen[length+1:length+1] in right_punctuation:
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
imgdraw(skillbg, (50, height+85), skilltext, 'black')
linelen = ImageDraw.Draw(skillbg).multiline_textbbox((50, height+86), textline, font['text'], align='left', direction='ltr', language='zh-Hans')
# DEBUG
skillbg.show()
# skillbg.show()




# 技能循环处
# 
# 写标题
#     字符串切片
#     计算字符串字体长度
#     如果小于最大长度，进入中文标点修正
#         最后一个为左括号，放到下一行
#         最后一个是右标点，忽略
#         下一行第一个是右标点，放到上一行
#     字符串传递
#     原字符串切片
#     确认行高，计算行高
#     循环
# 尾部增加行高
# 写底附字
# 
# 角色立绘为2000宽
# 卡牌大小2480*3480
# 技能层大小2000宽

# DEBUG
# cardbg.show()

