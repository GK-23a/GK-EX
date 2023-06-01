from os import path
from time import asctime, localtime, time


def get_time(left=0, right=0):
    return asctime(localtime(time()))[4 + left:19 + right]


def wlog(filename, logfile, log_body, level='Info'):
    # 日志结构：[时间戳] 消息级别: <文件名> 消息内容
    now_time = '[' + get_time() + ']'
    with open(logfile, 'a', encoding='UTF-8') as log:
        log.write(now_time + ' ' + level + ': <' + path.basename(filename) + '> ' + log_body + '\n')


sex_dict = {'male': 0, 'female': 1, 'both': 2}

country_dict = {
    'mondstadt': 0,
    'liyue': 1,
    'inazuma': 2,
    'sumeru': 3,
    'snezhnaya': 6,
    'others': 8
}

element_dict = {
    'pyro': 0,
    'hydro': 1,
    'anemo': 2,
    'electro': 3,
    'dendro': 4,
    'cryo': 5,
    'geo': 6,
    'others': 7,
}

element_color_dict = {
    'pyro': '#e2311d',
    'hydro': '#1c72fd',
    'anemo': '#33cc83',
    'electro': '#d376f0',
    'dendro': '#78842d',
    'cryo': '#98c8e8',
    'geo': '#cfa726',
    'others': '#000000',
}
dlc_dict = {
    'genshin-standard': 0,
    'genshin-god': 1,
    'genshin-designer': 2,
    'others': 3
}


def country(body: str) -> int:
    return country_dict[body]


def country_back(num: int) -> str:
    for key, value in country_dict.items():
        if value == num:
            return key
    return ''


def sex(body: str) -> int:
    return sex_dict[body]


def sex_back(num: int) -> str:
    for key, value in sex_dict.items():
        if value == num:
            return key
    return ''


def element(body: str) -> int:
    return element_dict[body]


def element_back(num: int) -> str:
    for key, value in element_dict.items():
        if value == num:
            return key
    return ''


def color(body: str) -> str:
    return element_color_dict[body]


def color_back(body: str) -> str:
    for key, value in element_color_dict.items():
        if value == body:
            return key
    return ''


def dlcs(body: str) -> int:
    return dlc_dict[body]


def dlcs_back(num: int) -> str:
    for key, value in dlc_dict.items():
        if value == num:
            return key
    return ''


def star(star_level: int) -> int:
    if star_level == 5:
        return 0
    else:
        return 1


def star_back(num: int) -> int:
    if num == 0:
        return 5
    else:
        return 4
