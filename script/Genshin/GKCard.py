number_dict = {
    'country': [
        'mondstadt',
        'liyue',
        'inazuma',
        'sumeru',
        'fontaine',
        'natlan',
        'snezhnaya',
        "khaenri'ah"
    ],
    'element': ['pyro', 'hydro', 'anemo', 'electro', 'dendro', 'cryo', 'geo'],
    'sex': ['male', 'female']
}


class GKCharacterCard:

    def __init__(self, cid):
        self.id: str = cid
        self.title: str = '称号'
        self.name: str = '新角色'
        self.sex: str = 'male'
        self.element: str = 'others'
        self.country: str = 'others'
        self.level: int = 5
        self.designer: str = 'None'
        self.design_state: bool = False
        self.artist: str = 'None'
        self.health_point: int = 3
        self.max_health_point: int = 3
        self.armor_point: int = 0
        self.dlc: str = 'others'
        self.skill_num: int = 1
        self.skill1: dict = dict(name='', description='', visible=False)

    def pack(self) -> dict:
        """将角色信息合成为字典"""
        datas = {
            'id': self.id,
            'title': self.title,
            'name': self.name,
            'sex': self.sex,
            'element': self.element,
            'country': self.country,
            'level': self.level,
            'designer': self.designer,
            'design_state': self.design_state,
            'artist': self.artist,
            'health_point': self.health_point,
            'max_health_point': self.max_health_point,
            'armor_point': self.armor_point,
            'dlc': self.dlc,
            'skills': []
        }
        for i in range(1, self.skill_num + 1):
            skill = f'skill{i}'
            if getattr(self, skill).get('name', None):
                datas['skills'].append(getattr(self, skill))
        return datas

    def unpack(self, pack: dict):
        """解包标准格式字典"""
        self.id = pack.get('id', 'None')
        self.title = pack.get('title', '称号')
        self.name = pack.get('name', '新角色')
        self.sex = pack.get('sex', 'male')
        self.element = pack.get('element', 'others')
        self.country = pack.get('country', 'others')
        self.level = int(pack.get('level', 5))
        self.designer = pack.get('designer', 'None')
        self.design_state = bool(pack.get('design_state', 0))
        self.artist = pack.get('artist', 'None')
        self.health_point = int(pack.get('health_point', 3))
        self.max_health_point = int(pack.get('max_health_point', 3))
        self.armor_point = int(pack.get('armor_point', 0))
        self.dlc = pack.get('dlc', 'others')
        self.skill_num = len(pack.get('skills'))
        for i, sdata in enumerate(pack.get('skills')):
            setattr(self, f'skill{i+1}', dict(
                name=sdata.get('name', ''),
                description=sdata.get('description', ''),
                visible=bool(sdata.get('visible', 0))))

    def to_number(self, origin_key) -> int | None:
        """将属性字符串转换为数字"""
        if origin_key in list(number_dict.keys()):
            numbers = {country: i for i, country in enumerate(number_dict.get(origin_key))}
            number = numbers.get(getattr(self, origin_key), len(number_dict.get(origin_key)))
            return number
        else:
            return None

    @staticmethod
    def number_to(value, origin_key) -> str | None:
        """将属性数字转换为字符串"""
        if origin_key in list(number_dict.keys()):
            numbers = {i: country for i, country in enumerate(number_dict.get(origin_key))}
            number = numbers.get(value, 'others')
            return number
        else:
            return None

    def add_skill(self, skill_name, description='', visible=False):
        """新增角色技能"""
        self.skill_num += 1
        setattr(self, f'skill{self.skill_num}', dict(name=skill_name, description=description, visible=visible))
