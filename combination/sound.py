import enum
import random
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
        self.is_consonant = False


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
        self.is_vowel = False


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


class YunMu:
    """韵母类

    属性：
        - name: 韵母名称
        - duration: 持续时间(世界时间单位)
        - strength: 强度 1-10
        - difficulty: 发音难度 1-10
        - clarity: 清晰度 1-10"""

    def __init__(self, strength: float = 1.0, *args: list[Phoneme]):
        # 排序 args，将元音放在最前面
        sorted_args = sorted(args, key=lambda x: x.is_vowel, reverse=True)
        self.name = "".join([phoneme.name for phoneme in sorted_args])
        self.is_yunmu = True
        self.strength = (np.sum([phoneme.strength
                                 for phoneme in sorted_args])) * strength
        self.duration = (np.sum([phoneme.duration
                                 for phoneme in sorted_args])) * strength
        self.difficulty = np.sum(
            [phoneme.difficulty for phoneme in sorted_args])

    def __repr__(self):
        return f"{self.name}"

    @staticmethod
    def random_yunmu():
        """随机生成一个韵母"""
        v_length = np.random.randint(1, 3)
        c_length = np.random.randint(0, 1 if v_length >= 2 else 3)
        vowels = [
            dict_vowels[random.choice("aeiouü")] for i in range(v_length)
        ]
        consonants = [
            dict_consonants[random.choice("bpmfd")] for i in range(c_length)
        ]
        return YunMu(1.0, *vowels, *consonants)


class ShengMu:
    """声母类

    属性：
        - name: 声母名称
        - duration: 持续时间(世界时间单位)
        - strength: 强度 1-10
        - difficulty: 发音难度 1-10
        - clarity: 清晰度 1-10"""

    def __init__(self, strength: float = 1.0, *args: list[Consonant]):
        # 排序 args，将辅音放在最前面，最多两个辅音
        sorted_args = sorted(args, key=lambda x: x.is_consonant)[:2]
        self.name = "".join([phoneme.name for phoneme in sorted_args])
        self.is_shengmu = True
        self.strength = (np.sum([phoneme.strength
                                 for phoneme in sorted_args])) * strength
        self.duration = (np.sum([phoneme.duration
                                 for phoneme in sorted_args])) * strength
        self.difficulty = np.sum(
            [phoneme.difficulty for phoneme in sorted_args])

    def __repr__(self):
        return f"{self.name}"

    @staticmethod
    def random_shengmu():
        """随机生成一个声母"""
        c_length = np.random.randint(1, 2)
        consonants = [
            dict_consonants[random.choice("bpmfd")] for i in range(c_length)
        ]
        return ShengMu(1.0, *consonants)


class Syllable:
    """音节类

    属性：
        - name: 音节名称
        - duration: 持续时间(世界时间单位)
        - strength: 强度 1-10
        - difficulty: 发音难度 1-10
        - clarity: 清晰度 1-10"""

    def __init__(
        self,
        yunmu: YunMu,
        shengmu: ShengMu = None,
        strength: float = 1.0,
    ):
        """初始化音节类"""
        self.name = shengmu.name + yunmu.name if shengmu and yunmu else ""
        self.is_syllable = True
        self.shengmu = shengmu
        self.yunmu = yunmu
        self.strength = (shengmu.strength +
                         yunmu.strength) * strength if shengmu and yunmu else 0
        self.duration = (shengmu.duration +
                         yunmu.duration) * strength if shengmu and yunmu else 0
        self.difficulty = (shengmu.difficulty +
                           yunmu.difficulty) if shengmu and yunmu else 0

    def __repr__(self):
        return f"{self.name}"

    @staticmethod
    def random_syllable():
        """随机生成一个音节"""
        yunmu = YunMu.random_yunmu()
        shengmu = ShengMu.random_shengmu() if random.random() > 0.5 else None
        return Syllable(yunmu, shengmu, 1.0)


class Word:

    def __init__(self, verb=False, *args: list[Syllable]):
        self.name = "".join([syllable.name for syllable in args])
        self.is_word = True
        self.is_verb = verb
        self.duration = np.sum([syllable.duration for syllable in args])
        self.strength = np.sum([syllable.strength for syllable in args])
        self.difficulty = np.sum([syllable.difficulty for syllable in args])

    def __repr__(self):
        return f"{self.name}"


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
