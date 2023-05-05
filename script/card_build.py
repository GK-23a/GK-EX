from ExtraF import wlog
import character_card
import json

# Setting: 是否生成打印张
printbuild = False

wlog(__file__, 'out/debug.log', '卡面构建开始。')

# 打印张生成准备
cards = []

wlog(__file__, 'out/debug.log', '角色图像构建开始。')

# json读取
with open('data/data.json', encoding='UTF-8') as jsonfile:
    filedict = json.loads(jsonfile.read())
    character_data = filedict['character_data']
wlog(__file__, 'out/debug.log', '"data.json"读取完成。')

# 循环图像生成
for ch in character_data:
    ch_img = character_card.cardbuild(ch, filedict['verions'])
    if ch_img:
        ch_img.save('out/character_img/' + ch['id'] + '.png')
        wlog(
            __file__, 'out/debug.log', ch['name'] + ' (' + ch['id'] + ')已保存为 "' + ch['id'] + '.png" 。')
        cards.append(ch_img)

wlog(__file__, 'out/debug.log', '角色图像生成已完成全部构建与保存。\n')

# 打印张生成
if printbuild:
    wlog(__file__, 'out/debug.log', '打印张生成开始。')
    cardss = [cards[i:i + 9] for i in range(0, len(cards), 9)]
    i = 1
    for cards_ in cardss:
        character_card.print_build(cards_).save('out/print/page-' + str(i) + '.png')
        wlog(__file__, 'out/debug.log', '打印张' + str(i) + '生成、保存完成。')
        i += 1
    wlog(__file__, 'out/debug.log', '打印张生成结束。')

wlog(__file__, 'out/debug.log', '卡面构建结束。\n')