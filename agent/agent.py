import numpy as np
import src.sound as sd
from base import BaseAgent
from combination.construct import Constructor

class Agent(BaseAgent):
    def __init__(self, env, id: int, name: str = "Agent"):
        """初始化"""
        super().__init__(env, id, name)
        self.position = np.random.rand(2) * env.size
        self.vowels = sd.dict_vowels
        self.consonants = sd.dict_consonants
        self.mood = 0  # 情绪
        self.actions = ["cry", "laugh"]
        self.constructor = Constructor()

    def cry(self):
        self.mood = -1

    def laugh(self):
        self.mood = 1

    def reset_mood(self):
        self.mood = 0

    def generate_word(self):
        """生成一个随机的单词"""
        vowel = np.random.choice(self.vowels)
        constant = np.random.choice(self.consonants)
        return sd.Sound([vowel, constant])
        
    def construct_sentence(self,*args):
        syllables =[]
        for arg in args:
            node = self.memory.match_node(arg)
            sound_node = self.memory.max_weight_node(node,sound_eq=True)
            if not sound_node:
                syllable = self.generate_word()
                sound_node = self.memory.match_node(syllable, sound=True)
            sound = sound_node['data']
            syllables.append(sound)
        return self.constructor.construct(syllables)
        
        
