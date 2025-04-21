import random
import numpy as np
import sound as sd
import igraph as ig


class Agent:
    """人类类
    属性：
        - name: 人类名称
        - env: 环境
        - position: 位置
        - tx_range: 发送范围
        - rx_range: 接收范围
        - sounds: 接收到的声音列表
        - reward: 奖励值
        - vowels: 元音列表
        - consonants: 辅音列表
        - q_table: Q-learning表
        - alpha: 学习率
        - gamma: 折扣因子
        - epsilon: 探索率"""

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
        self.memory = ig.Graph()  # 记忆图

    def receive_sound(self, sound: sd.Sound):
        """接收信号"""
        self.sounds.append(sound)
        # 更新记忆
        self.memory.add_vertex(name=sound.name, data=sound)
        #print(f"{self.name} Received sound: {sound.name}")

    def send_sound(self, sound: sd.Sound):
        """发送信号"""
        from environment import Signal
        signal = Signal(self, self.position, self.tx_range, sound)
        self.env.broadcast(signal)

    def match_memory(self, other, name):
        if len(self.memory.vs) == 0 or not self.memory.vs.select(name_eq=name):
            node = self.memory.add_vertex(name=name, data=other)
        else:
            node = self.memory.vs.select(name_eq=name)[0]
        return node

    def max_edge_weight(self, node: ig.Vertex):
        # 获取所有邻接边的权重
        edges = self.memory.incident(node)
        if not edges:
            return 0
        max_weight = max([self.memory.es[e]['weight'] for e in edges])
        return max_weight

    def incident_memory(self, node: ig.Vertex):
        neighbors = node.neighbors()
        if not neighbors:
            return None
        max_weight = self.max_edge_weight(node)
            # 获取所有邻接边的权重
        edges = self.memory.incident(node)
        weights = [self.memory.es[e]['weight'] for e in edges]
        # 找到最大权重对应的邻接节点
        max_weight = max(weights)
        max_nodes = [
            neighbors[i] for i, w in enumerate(weights) if w == max_weight
        ]
        return random.choice(max_nodes)

    def add_rand_sound_memory(self, node):
        constant = self.consonants[random.choice("bpmfd")]
        vowel = self.vowels[random.choice("aeiouü")]
        sound = sd.Sound([constant, vowel])
        # 接 sound 和 good 在记忆中挂钩
        sound_node = self.match_memory(sound, sound.name)
        self.memory.add_edge(node, sound_node, weight=np.random.rand())
        return sound

    def add_rand_good_memory(self, node):
        good = random.choice(self.env.goods)
        good_node = self.match_memory(good, f"{good}")
        self.memory.add_edge(node, good_node, weight=np.random.rand())
        return good

    def choose_sound(self, good: int):
        # 判断记忆中有没有 good
        node = self.match_memory(good, f"{good}")
        # 根据探索率来确认返回
        if np.random.uniform(0, 1) < self.epsilon:
            sound = self.add_rand_sound_memory(node)
        else:
            sound_node = self.incident_memory(node)
            if not sound_node:
                sound = self.add_rand_sound_memory(node)
            else:
                sound = sound_node['data']
        return sound

    def choose_good(self, sound: sd.Sound):
        # 判断记忆中有没有 sound
        node = self.match_memory(sound, sound.name)
        # 根据探索率来确认返回
        if np.random.uniform(0, 1) < self.epsilon:
            good = self.add_rand_good_memory(node)
        else:
            good_node = self.incident_memory(node)
            if not good_node:
                good = self.add_rand_good_memory(node)
            else:
                good = good_node['data']
        return good

    def update_qlearning(self, good: int, sound: sd.Sound, next_good: int,
                         reward: float):
        # 先认识一下 good 和 sound
        good_node = self.match_memory(good, f"{good}")
        sound_node = self.match_memory(sound, sound.name)
        
        # 判断一下两个 node 是否连接
        if not self.memory.are_connected(good_node.index, sound_node.index):
            self.memory.add_edge(good_node, sound_node, weight=np.random.rand())
            
        edge_id = self.memory.get_eid(good_node.index,sound_node.index)

        old_value = self.memory.es[edge_id]['weight']

        next_good_node = self.match_memory(next_good, f"{next_good}")
        next_max = self.max_edge_weight(next_good_node)

        new_value = (1 - self.alpha) * old_value + self.alpha * (
            reward + self.gamma * next_max)
        
        # 更新边的权重
        self.memory.es[edge_id]['weight'] = new_value
