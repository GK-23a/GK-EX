from customlog import wlog
import character_card
import json

wlog(__file__, 'out/debug.log', '角色图像构建开始。')

# json读取
with open('json/characters.json', encoding='UTF-8') as jsonfile:
    character_data = json.loads(jsonfile.read())
wlog(__file__, 'out/debug.log', '"characters.json"读取完成。')

# 循环图像生成
for ch_id in character_data:
    ch_img = character_card.cardbuild(ch_id, character_data)
    if ch_img:
        ch_img.save('out/character_img/'+ch_id+'.png')
        wlog(__file__, 'out/debug.log', character_data[ch_id]['name'] + ' (' + ch_id + ')已保存为 "' + ch_id + '.png" 。')

wlog(__file__, 'out/debug.log', '角色图像生成已完成全部构建与保存。\n')

