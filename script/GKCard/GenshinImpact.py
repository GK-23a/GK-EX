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
            setattr(self, f'skill{i}', dict(
                name=sdata.get('name', ''),
                description=sdata.get('description', ''),
                visible=bool(sdata.get('visible', 0))))

    def to_number(self, origin_key) -> int | None:
        """将属性字符串转换为数字"""
        if origin_key == 'country':
            country_numbers = {
                "Mondstadt": 0,
                "Liyue": 1,
                "Inazuma": 2,
                "Sumeru": 3,
                "Fontaine": 4,
                "Natlan": 5,
                "Snezhnaya": 6,
                "Khaenri'ah": 7,
                'others': 9
            }
            return country_numbers.get(self.country, 9)
        elif origin_key == 'element':
            element_numbers = {
                'pyro': 0,
                'hydro': 1,
                'anemo': 2,
                'electro': 3,
                'dendro': 4,
                'cryo': 5,
                'geo': 6,
                'others': 9
            }
            return element_numbers.get(self.element, 9)
        elif origin_key == 'sex':
            sex_numbers = {
                'male': 0,
                'female': 1,
                'others': 9
            }
            return sex_numbers.get(self.sex, 9)
        else:
            return None

    @staticmethod
    def number_to(value, origin_key) -> str | None:
        """将属性数字转换为字符串"""
        if origin_key == 'country':
            country_numbers = {
                0: "Mondstadt",
                1: "Liyue",
                2: "Inazuma",
                3: "Sumeru",
                4: "Fontaine",
                5: "Natlan",
                6: "Snezhnaya",
                7: "Khaenri'ah",
                9: 'others'
            }
            return country_numbers.get(value, 'others')
        elif origin_key == 'element':
            element_numbers = {
                0: 'pyro',
                1: 'hydro',
                2: 'anemo',
                3: 'electro',
                4: 'dendro',
                5: 'cryo',
                6: 'geo',
                9: 'others'
            }
            return element_numbers.get(value, 'others')
        elif origin_key == 'sex':
            sex_numbers = {
                0: 'male',
                1: 'female',
                9: 'others'
            }
            return sex_numbers.get(value, 'others')
        else:
            return None

    def add_skill(self, skill_name):
        """新增角色技能"""
        setattr(self, f'skill{self.skill_num}', dict(name=skill_name, description='', visible=False))
        self.skill_num += 1
