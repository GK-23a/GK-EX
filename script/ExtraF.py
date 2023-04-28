sex_list = {'male': 0, 'female': 1}


def sex(body: str) -> int:
    try:
        return sex_list[body]
    except:
        return 2


country_list = {
    'mondstadt': 0,
    'liyue': 1,
    'inazuma': 2,
    'sumeru': 3,
    'snezhnaya': 7,
    'others': 9
}


def country(body: str) -> int:
    return country_list[body]


element_list = {
    'pyro': 0,
    'hydro': 1,
    'anemo': 2,
    'electro': 3,
    'dendro': 4,
    'cryo': 5,
    'geo': 6,
    'others': 7,
    'none': 7
}


def element(body: str) -> int:
    return element_list[body]


element_color_list = {
    'pyro': '#e2311d',
    'hydro': '#1c72fd',
    'anemo': '#33cc83',
    'electro': '#d376f0',
    'dendro': '#78842d',
    'cryo': '#98c8e8',
    'geo': '#cfa726',
    'others': '#000000',
    'none': '#000000',
}


def color(body: str) -> str:
    return element_color_list[body]


dlcs_list = {'genshin-standard': 0, 'genshin-god': 1, 'genshin-designer': 2, 'others':3}


def dlcs(body: str) -> int:
    return dlcs_list[body]


def star(star_level: int) -> int:
    if star_level == 5:
        return 0
    else:
        return 1


def get_fliter_list(dict_body: dict,
                    type: str | None,
                    item: str | None = None,
                    return_body: str = 'id') -> list:
    flitered = []
    for data in dict_body:
        if type != None:
            if data[type] == item:
                flitered.append(data[return_body])
        else:
            flitered.append(data[return_body])
    return flitered