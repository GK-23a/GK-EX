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
        self.dlc: str = 'genshin-standard'
        self.skill_num: int = 1
        self.skill1: dict = dict(name='', description='', visible=False)

    def do_pack(self) -> dict:
        """将角色信息合成为一个字典，用于写入json文件。"""
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

    def add_skill(self):
        """新增角色技能"""
        setattr(self, f'skill{self.skill_num}', dict(name='', description='', visible=False))
        self.skill_num += 1
