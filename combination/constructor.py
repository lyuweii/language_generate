import random
import combination.combination as cc
from memory.base import BaseMemory
from sound import Word, Syllable, YunMu, ShengMu
from sound import dict_vowels, dict_consonants


class Constructor:
    """
    A class to represent a constructor for a combination of strings.
    """

    def __init__(self, memory: BaseMemory):
        self.data = memory
        # 自己相关的计为 subject
        self.s_node = self.data.match_node("_subject_")
        # 动作相关的计为 verb
        self.v_node = self.data.match_node("_verb_")
        # 其他相关的计为 object
        self.o_node = self.data.match_node("_object_")

        # 构造 vowels 和 consonants
        self.vowels = dict_vowels
        self.consonants = dict_consonants

    def _random_word(self):
        """
        生成一个随机的单词
        """
        pass

    def __call__(self, *args):
        """
        构造句子，传入的一定是 word,返回一个 combination 对象
        """
        for arg in args:
            # 查找节点
            node = self.data.match_node(arg)
            # 查找对应声音
            sound_node = self.data.max_weight_node(node, sound_eq=True)
            # 判断性质
            svo_node = self.data.which_adjacent(node, self.s_node, self.v_node,
                                                self.o_node)
            if not svo_node:
                self.match_edge(node, self.s_node)
