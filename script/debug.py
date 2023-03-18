from customlog import wlog
import character_card
import json
import os

wlog(__file__, 'out/debug_.log', '角色图像的debug构建开始。', 'Debug')

# debug是否重建json
rebuild_json = False
if rebuild_json:
    os.system('{} {}'.format('python', 'script/json_build.py'))
    wlog(__file__, 'out/debug_.log', 'json数据文件已成功生成。', 'Debug')

# json读取
with open('json/characters.json', encoding='UTF-8') as jsonfile:
    character_data = json.loads(jsonfile.read())
wlog(__file__, 'out/debug_.log', '"characters.json"读取完成。', 'Debug')

# debug单独获取
debug_character_id = [
    'nilou'
    ]
debug_character_data = {}
for id in debug_character_id:
    debug_character_data[id] = character_data[id]
    

# 循环图像生成
for ch_id in debug_character_data:
    ch_img = character_card.cardbuild(ch_id, debug_character_data)
    if ch_img:
        ch_img.save('out/character_img/'+ch_id+'.png')
        wlog(__file__, 'out/debug_.log', debug_character_data[ch_id]['name'] + ' (' + ch_id + ')已保存为 "' + ch_id + '.png" 。', 'Debug')
        ch_img.show()

wlog(__file__, 'out/debug_.log', '角色图像的debug生成已完成全部构建与保存。\n', 'Debug')

