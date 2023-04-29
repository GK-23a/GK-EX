from customlog import wlog
import xlrd3 as xlrd
import json

wlog(__file__, 'out/debug.log', 'json 构建开始。')

# 预加载
work_book = xlrd.open_workbook('data/database.xlsx')  #打开工作表
ga_data = work_book.sheet_by_index(0)  #卡牌表
de_data = work_book.sheet_by_index(1)  #牌堆表
sk_data = work_book.sheet_by_index(2)  #技能表
ch_data = work_book.sheet_by_index(3)  #角色表

wlog(__file__, 'out/debug.log', '已加载"database.xlsx"。')

# ga_data行值：0id，1名称，2类型，3延时，4装备类型，5范围，6描述
wlog(__file__, 'out/debug.log', '开始构建卡牌(gamecards)。')
gamecards = {}
i = 1
while i < ga_data.nrows:
    data = ga_data.row_values(i)
    gamecard_data = {}

    gamecard_id = data[0]
    gamecard_data['name'] = data[1]
    gamecard_data['description'] = data[6]

    gamecard_data['category'] = data[2]
    if gamecard_data['category'] == 'equipment':
        gamecard_data['equipment_category'] = data[4]
        if (gamecard_data['equipment_category']
                == 'weapon') or (gamecard_data['equipment_category'][4:]
                                 == 'horse'):
            gamecard_data['range'] = int(data[5])
    elif gamecard_data['category'] == 'trick':
        if data[3]:
            gamecard_data['delay'] = True
        else:
            gamecard_data['delay'] = False
    i += 1
    gamecards[gamecard_id] = gamecard_data

wlog(__file__, 'out/debug.log', '构建卡牌(gamecards)已结束。')
with open('data/gamecards.json', 'w', encoding='utf-8') as file:
    json.dump(gamecards, file, ensure_ascii=False)
    wlog(__file__, 'out/debug.log', '"gamecards.json"已成功保存。')

# de_data行值：0id，1颜色，2花色，3点数，4卡id，5显示名称，6额外值
wlog(__file__, 'out/debug.log', '开始构建牌堆(gamecard_decks)。')
gamecard_decks = {}
i = 1
while i < de_data.nrows:
    data = de_data.row_values(i)
    card_info = {}

    card_deck_id = int(data[0])
    card_info['color'] = data[1]
    card_info['suit'] = data[2]
    card_info['id'] = data[4]
    card_info['show_name'] = data[5]

    if data[6]: card_info['extra_value'] = data[6]

    if isinstance(data[3], float):
        card_info['point'] = str(int(data[3]))
    else:
        card_info['point'] = data[3]

    i += 1
    gamecard_decks[card_deck_id] = card_info

wlog(__file__, 'out/debug.log', '构建牌堆(gamecard_decks)已结束。')
with open('data/gamecard_decks.json', 'w', encoding='utf-8') as file:
    json.dump(gamecard_decks, file, ensure_ascii=False)
    wlog(__file__, 'out/debug.log', '"gamecard_decks.json"已成功保存。')

# sk_data行值：0id，1名称，2源角色，3描述
wlog(__file__, 'out/debug.log', '开始构建技能(skills)。')
skills = {}
skill_list = []
i = 1
while i < sk_data.nrows:
    data = sk_data.row_values(i)
    skill_data = {}

    skill_id = data[0]
    skill_data['name'] = data[1]
    skill_data['character'] = data[2]
    skill_data['description'] = data[3]

    i += 1
    skills[skill_id] = skill_data
    skill_list.append({
        'name': skill_data['name'],
        'id': skill_id,
        'character': skill_data['character']
    })

wlog(__file__, 'out/debug.log', '构建技能(skills)已结束。')
with open('data/skills.json', 'w', encoding='utf-8') as file:
    json.dump(skills, file, ensure_ascii=False)
    wlog(__file__, 'out/debug.log', '"skills.json"已成功保存。')

# ch_data行值：0id，1称号，2名称，3性别，4元素，5国家，6星级
# 7完成状态，8技能设计师，9初始体力值，10最大体力值，11初始护甲值，12+技能名称
wlog(__file__, 'out/debug.log', '开始构建角色信息(characters)。')
characters = []
for i in range(1, ch_data.nrows):
    data = ch_data.row_values(i)
    character_data = {
        'id': data[0],
        'title': data[1],
        'name': data[2],
        'sex': data[3],
        'element': data[4],
        'country': data[5],
        'level': int(data[6]),
        'design_info': data[7],
        'designer': data[8],
        'health_point': int(data[9]),
        'max_health_point': int(data[10]),
        'armor_point': int(data[11])
    }

    character_data['skills'] = []
    j = 12
    character_skills = []
    try:
        while data[j] != '':
            for k in skill_list:
                if k['name'] == data[j]:
                    if k['character'] == data[0]:
                        character_data['skills'].append({
                            'name':
                            k['name'],
                            'id':
                            k['id'],
                            'description':
                            skills[k['id']]['description'],
                            'origin':
                            True
                        })
                        character_skills.append(k['id'])
                        break
            j += 1
    except:
        pass

    for k in skill_list:
        if k['character'] == data[0]:
            if k['id'] not in character_skills:
                character_data['skills'].append({
                    'name':
                    k['name'],
                    'id':
                    k['id'],
                    'description':
                    skills[k['id']]['description'],
                    'origin':
                    False
                })

    characters.append(character_data)
    wlog(__file__, 'out/debug.log', '已成功构建角色 ' + character_data['id'] + ' 的全部信息。')

wlog(__file__, 'out/debug.log', '构建角色信息(characters)已结束。')
with open('data/data.json', 'w', encoding='utf-8') as file:
    output = {
        'character_data': characters,
        'verions': 'Beta-0318'
    }
    json.dump(output, file, ensure_ascii=False)
    wlog(__file__, 'out/debug.log', '"data.json"已成功保存。')

wlog(__file__, 'out/debug.log', 'json 构建结束。\n')