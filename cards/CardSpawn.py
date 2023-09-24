import json
import os
import logging
from datetime import datetime
from typing import Literal

from PIL import Image
from PySide6.QtWidgets import QProgressBar, QLabel

try:
    from .CardBuild import character_card_build
except ImportError:
    from CardBuild import character_card_build

### 生成默认配置文件

# spawn_a4_print_image: bool / 是否生成A4尺寸的打印版图片
build_a4_print = False

# all_character: bool / 是否生成全部角色卡；若为True，忽略character_list
all_character = True

# character_list: list | None / 生成角色卡的列表
character_list = [
]


### 生成函数
log_folder = os.path.join('output', 'log')
if not os.path.exists(log_folder):
    os.makedirs(log_folder)
logging.basicConfig(
    filename=os.path.join('output', 'log', 'CardSpawn.gkcl'),
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='[%Y/%m/%d %H:%M:%S]')


def spawn_card(
        build_a4_image: bool = False,
        build_all_character: bool = False,
        selected_character_ids: list | None = None,
        progress_bar: QProgressBar | None = None
) -> None:
    # 读取json
    with open(os.path.join('assets', 'card_data.json'), encoding='UTF-8') as file:
        gk_data = json.loads(file.read())
    character_datas = gk_data['character_data']
    version_data = gk_data['character_data_versions']
    original_datas = [d for d in character_datas if d['design_state']]
    original_filtered_datas = [d for d in character_datas if not d['design_state']]
    logging.warning('有部分角色未进行构建，这些角色未勾选「设计完成」。')
    logging.warning(f'未构建的角色： {str([i["id"] for i in original_filtered_datas])[1:-1]}')
    if build_all_character:
        datas = original_datas
    else:
        datas = [d for d in original_datas if d['id'] in selected_character_ids]
        filtered_datas = [d for d in original_datas if d['id'] not in selected_character_ids]
        if filtered_datas:
            logging.info('有部分角色未进行构建，这些角色被指定构建，但设计完成了。')
            logging.info(f'未构建的角色： {str([i["id"] for i in original_filtered_datas])[1:-1]}')
    logging.info(f'即将构建的角色： {str([i["id"] for i in datas])[1:-1]}')

    being_build_a4_image_list = spawn_card_image(
        datas,
        version_data,
        progress_bar=progress_bar
    )
    if build_a4_image:
        spawn_a4_image(being_build_a4_image_list)


# 角色卡生成
def spawn_card_image(
        character_datas: list,
        version_data: str,
        definition: Literal['high', 'low'] = 'high',
        progress_bar: QProgressBar | list[QProgressBar | QLabel] | None = None,
        all_progress_bar: list[QProgressBar | QLabel | bool] | None = None
) -> list:
    def progress_run(value, text):
        if all_progress_bar:
            all_progress_bar[0].setValue(value)
            all_progress_bar[1].setText(text)
            return value

    max_value = 100
    if len(all_progress_bar) == 3:
        if all_progress_bar[2]:
            max_value = 70
    add_value = max_value / (len(character_datas) + 1)
    now_value = progress_run(0, '准备导出') + add_value
    # 创建存储文件夹
    formatted_time = str(datetime.now().strftime("%Y%m%d-%H%M%S"))[:]
    folder_dir = os.path.join('output', 'character_image', formatted_time)
    if not os.path.exists(folder_dir):
        os.makedirs(folder_dir)

    # 创建列表
    character_images = list()

    # 迭代生成
    for i, data in enumerate(character_datas):
        now_value = progress_run(now_value, f'导出角色 {data["name"]} 图片({i+1} / {len(character_datas)})') + add_value
        try:
            ch_img = character_card_build(data, version_data, progress_bar=progress_bar)
        except Exception:
            logging.error(f'{data.get("id")}构建失败了！具体错误信息见下：')
            logging.error(Exception)
            logging.error('--------------------')
            raise
        else:
            save_file = os.path.join('output', 'character_image', formatted_time, data['id'] + '.png')
            character_images.append(ch_img)
            if definition == 'low':
                ch_img = ch_img.resize(620, 960)
            ch_img.save(save_file)
            logging.info(f'{data.get("id")}构建完成，预计保存到{str(save_file)}')
    progress_run(max_value, '生成了所有的角色图像')
    return character_images


# 生成适用于A4打印的图像
def spawn_a4_image(
        character_images: list,
        all_progress_bar: list[QProgressBar | QLabel] = None
) -> None:
    def progress_run(value, text):
        if all_progress_bar:
            all_progress_bar[0].setValue(value)
            all_progress_bar[1].setText(text)
            return value
    now_value = progress_run(72, '正在生成打印版图片')
    formatted_time = str(datetime.now().strftime("%Y%m%d-%H%M%S"))[:]
    folder_dir = os.path.join('output', 'print_image', formatted_time)
    if not os.path.exists(folder_dir):
        os.makedirs(folder_dir)

    card_group = [character_images[i:i + 9] for i in range(0, len(character_images), 9)]
    i = 1
    for j, nine_cards_list in enumerate(card_group):
        now_value = progress_run(now_value, f'正在生成打印版图片({j+1} / {len(card_group)})') + 30 / len(card_group)
        logging.info(f'打印张生成开始: 第 {j+1} 张')
        card_size_point = (2560, 3520)
        card_point = []
        for y in range(3):
            for x in range(3):
                card_point.append((x * card_size_point[0], y * card_size_point[1]))
        a4page = Image.new('RGBA', (8168, 11552), (256, 256, 256, 256))
        try:
            i = 0
            while i < 9:
                character_image = Image.new('RGBA', (card_size_point[0], card_size_point[1]), (0, 0, 0, 256))
                character_image.paste(nine_cards_list[i], (20, 20))
                a4page.paste(character_image, card_point[i])
                i += 1
                logging.info(f'打印张生成: 第 {j+1} 张，第 {i} / 9 个')
        except IndexError:
            pass
        a4page.save(os.path.join('output', 'print_image', formatted_time, f'a4page-{str(j+1)}.png'))
        i += 1
    logging.info('打印张生成结束')
    progress_run(100, '完成打印张生成')


if __name__ == "__main__":
    spawn_card(build_a4_print, all_character, character_list)
