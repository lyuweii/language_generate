import random
from matplotlib import pyplot as plt
import numpy as np
import sound as sd
import igraph as ig
from memory import Memory
from types import SimpleNamespace


class Agent:
    """代理
    属性：
        - name: 名称
        - env: 环境
        - position: 位置
        - tx_range: 发送范围
        - rx_range: 接收范围
        - sounds: 接收到的声音列表
        - reward: 奖励值
        - vowels: 元音列表
        - consonants: 辅音列表
        - alpha: 学习率
        - gamma: 折扣因子
        - epsilon: 探索率
        - beta: 记忆使用率"""

    def __init__(self, env, id: int, name: str = "Agent"):
        """初始化人类"""
        self.id = id
        self.name = name
        self.env = env
        self.position = np.random.rand(2) * env.size
        self.tx_range = 100
        self.rx_range = 100
        self.sounds = []
        self.reward = 50
        self.vowels = sd.dict_vowels
        self.consonants = sd.dict_consonants
        self.alpha = 0.1  # 学习率
        self.gamma = 0.9  # 折扣因子
        self.epsilon = 0.1  # 探索率
        self.beta = 0.9  # 记忆使用率
        self.memory = Memory()  # 记忆图

    def receive_sound(self, sound: sd.Sound):
        """接收信号"""
        # 更新记忆
        self.memory.match_node(sound.name, sound, sound=True)

    def send_sound(self, sound: sd.Sound):
        """发送信号"""
        from environment import Signal
        signal = Signal(self, self.position, self.tx_range, sound)
        self.env.broadcast(signal)

    @staticmethod
    def wrap_data(data, name, **kwargs):
        return SimpleNamespace(name=name, data=data, kwargs=kwargs)

    def make_rand_sound(self):
        constant = self.consonants[random.choice("bpmfd")]
        vowel = self.vowels[random.choice("aeiouü")]
        sound = sd.Sound([constant, vowel])
        return SimpleNamespace(name=sound.name, data=sound)

    def make_rand_good(self):
        good = random.choice(self.env.goods)
        return SimpleNamespace(name=f"{good}", data=good)

    def associate(self, data1, data2):
        """建立联系"""
        node1 = self.memory.match_node(data1.name, data1.data, **data1.kwargs)
        node2 = self.memory.match_node(data2.name, data2.data, **data2.kwargs)
        conneted = False
        if self.memory.data.are_connected(node1, node2):
            # 如果已经连接，则不需要重新连接
            conneted=True
        edge = self.memory.match_edge(node1, node2)
        if conneted:
            # 权重提高
            edge['weight'] *= 2
        return edge

    def get_associatian(self, data_name: str, **kwarg):
        """在记忆中寻找与 data 相关的节点"""
        data_node = self.memory.match_node(data_name)
        associated_nodes = self.memory.incident_nodes(data_node).select(
            **kwarg)
        if not associated_nodes:
            return None
        return associated_nodes

    def choose_correspond(self,
                          data_name: str,
                          data,
                          callback: callable,
                          param_map: dict = None,
                          **kwargs):
        default_map = {
            'data': ['good'],
            'other': ['sound'],
        }
        param_map = param_map or default_map

        data_args = {k: kwargs[k] for k in param_map['data'] if k in kwargs}
        other_args = {k: kwargs[k] for k in param_map['other'] if k in kwargs}

        data_node = self.memory.match_node(data_name, data, **data_args)
        if np.random.uniform(0, 1) < self.epsilon or np.random.uniform(
                0,
                1) > self.beta or not self.memory.select_nodes(**other_args):
            other = callback()
            other_node = self.memory.match_node(other.name, other.data,
                                                **other_args)
            other = other.data
        else:
            other_node = self.memory.max_weight_node(data_node)
            if not other_node:
                other_nodes = self.memory.select_nodes(**other_args)
                other_node = random.choice(other_nodes)
            other = other_node['data']
        return other

    def choose_sound(self, good: int):
        """选择声音"""
        data_node = self.memory.match_node(f"{good}", good, good=True)
        if np.random.uniform(0, 1) < self.epsilon or np.random.uniform(
                0, 1) > self.beta or not self.memory.select_nodes(sound=True):
            other = self.make_rand_sound()
            other_node = self.memory.match_node(other.name,
                                                other.data,
                                                sound=True)
            other = other.data
        else:
            other_node = self.memory.max_weight_node(data_node)
            if not other_node:
                other_nodes = self.memory.select_nodes(sound=True)
                other_node = random.choice(other_nodes)
            other = other_node['data']
        return other

    def choose_good(self, sound: sd.Sound):
        """选择物体"""
        data_node = self.memory.match_node(sound.name, sound, sound=True)
        if np.random.uniform(0, 1) < self.epsilon or np.random.uniform(
                0, 1) > self.beta or not self.memory.select_nodes(good=True):
            other = self.make_rand_good()
            other_node = self.memory.match_node(other.name,
                                                other.data,
                                                good=True)
            other = other.data
        else:
            other_node = self.memory.max_weight_node(data_node)
            if not other_node:
                other_nodes = self.memory.select_nodes(good=True)
                other_node = random.choice(other_nodes)
            other = other_node['data']
        return other

    def update_qlearning(self, good: int, sound: sd.Sound, next_good: int,
                         reward: float):
        # 先认识一下 good 和 sound
        good_node = self.memory.match_node(f"{good}", good, good=True)
        sound_node = self.memory.match_node(sound.name, sound, sound=True)

        # 判断一下两个 node 是否连接
        edge = self.memory.match_edge(good_node, sound_node)
        old_value = edge['weight']

        next_good_node = self.memory.match_node(f"{next_good}",
                                                next_good,
                                                good=True)
        # 联系下一个物体
        self.memory.match_edge(next_good_node, sound_node)
        next_max_weight_edge = self.memory.max_weight_edge(next_good_node)
        next_max = 0 if not next_max_weight_edge else next_max_weight_edge[
            'weight']

        new_value = (1 - self.alpha) * old_value + self.alpha * (
            reward + self.gamma * next_max)

        # 更新边的权重
        edge['weight'] = new_value

    def show_memory(self, n: int = 5):
        """展示记忆"""
        self.memory.plot(n, [f"{good}" for good in self.env.goods])
