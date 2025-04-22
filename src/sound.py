import enum
import numpy as np


class Phoneme:
    """音素类

    属性：
        - name: 音素名称
        - duration: 持续时间(世界时间单位)
        - strength: 强度 1-10
        - difficulty: 发音难度 1-10
        - clarity: 清晰度 1-10"""

    def __init__(self,
                 name: str,
                 duration: float = 0.5,
                 strength: float = 2.,
                 difficulty: float = 1,
                 clarity: float = 5):
        """初始化音素类"""
        self.name = name
        self.duration = duration  # 持续时间(世界时间单位)
        self.strength = strength  # 强度 1-10
        self.difficulty = difficulty  # 发音难度 1-10
        self.clarity = clarity  # 清晰度 1-10


class Vowel(Phoneme):
    """元音类

    属性：
        - name: 元音名称"""

    def __init__(self,
                 name: str,
                 duration: float = 0.5,
                 strength: float = 5.,
                 difficulty: float = 5,
                 clarity: float = 5):
        """初始化元音类"""
        super().__init__(name, duration, strength, difficulty, clarity)
        self.is_vowel = True  # 是否为元音


class Consonant(Phoneme):
    """辅音类

    属性：
        - name: 辅音名称"""

    def __init__(self,
                 name: str,
                 duration: float = 0.5,
                 strength: float = 3.,
                 difficulty: float = 7,
                 clarity: float = 3):
        """初始化辅音类"""
        super().__init__(name, duration, strength, difficulty, clarity)
        self.is_consonant = True  # 是否为辅音


class Tone(enum.Enum):
    """音调枚举类

    属性：
        - FIRST: 第一声
        - SECOND: 第二声
        - THIRD: 第三声
        - FOURTH: 第四声"""
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4


class Sound:
    """音节类

    属性：
        - vowel: 元音
        - consonant: 辅音
        - tone: 音调
        - time: 持续时间(拍)"""

    def __init__(self,
                 Phoneme: list[Phoneme],
                 strength: float = 1.0,
                 tone: Tone = Tone.FIRST):
        """初始化音节类"""
        self.name = "".join([phoneme.name for phoneme in Phoneme])
        self.is_sound = True  # 是否为音节
        self.tone = tone

        self.duration = np.sum([phoneme.duration
                                for phoneme in Phoneme]) * strength
        self.strength = np.sum([phoneme.strength
                                for phoneme in Phoneme]) * strength
        self.difficulty = np.sum([phoneme.difficulty for phoneme in Phoneme])

    def __repr__(self):
        return f"({self.name})"


# 常用的元音
dict_vowels = {
    'a': Vowel("a", 0.45, 1., 1.),
    'o': Vowel("o", 0.45, 1., 1.),
    'e': Vowel("e", 0.45, 1., 1.),
    'i': Vowel("i", 0.45, 1., 1.),
    'u': Vowel("u", 0.45, 1., 1.),
    'ü': Vowel("ü", 0.5, 1., 2., 8),
}

# 常用的辅音
dict_consonants = {
    "b": Consonant("b"),
    "p": Consonant("p"),
    "m": Consonant("m"),
    "f": Consonant("f"),
    "d": Consonant("d"),
}

monster_roar = Sound(
    [dict_consonants["b"], dict_vowels["a"], dict_consonants["m"]],
    strength=5.0,
    tone=Tone.FOURTH,
)
