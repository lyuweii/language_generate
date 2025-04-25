import os
import numpy as np
from memory.base import BaseMemory


class BaseAgent:
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
        self.reward = 10
        self.alpha = 0.2  # 学习率
        self.gamma = 0.9  # 折扣因子
        self.epsilon = 0.1  # 探索率
        self.beta = 0.95  # 记忆使用率
        self.memory = BaseMemory()  # 记忆图

    def associate(self, data1, data2):
        """建立联系，如果已经存在则加倍权重"""
        node1 = self.memory.match_node(data1)
        node2 = self.memory.match_node(data2)
        edge, is_connected = self.memory.match_edge(node1, node2)
        if is_connected:
            edge['weight'] *= 2
        return edge

    def get_associatian(self, data_name: str, **kwarg):
        """在记忆中寻找与 data 相关的节点，如果不满足返回 None。"""
        data_node = self.memory.match_node(data_name)
        associated_nodes = self.memory.incident_nodes(data_node).select(
            **kwarg)
        if not associated_nodes:
            return None
        return associated_nodes

    def update_memory(self,
                      state,
                      action,
                      next_action=None,
                      reward: float = np.random.rand()):
        """Markov chain 机制更新记忆，认为 state/action 保持不变"""
        data1_node = self.memory.match_node(state)
        data2_node = self.memory.match_node(action)
        edge, _ = self.memory.match_edge(data1_node, data2_node)

        value = edge['weight']
        if not next_action:
            next_value = value
        else:
            next_action_node = self.memory.match_node(next_action)
            next_action_max_node = self.memory.max_weight_node(
                next_action_node)
            next_value = 0 if not next_action_max_node else next_action_max_node[
                'weight']
        # 认为 state 保持不变
        edge['weight'] = (
                1 -
                self.beta) * value + self.beta * reward + self.gamma * next_value

    def show_memory(self, num: int, names=None):
        self.memory.plot(num, names=names)

    def save_memory(self):
        dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        file_path = os.path.join(dir_path, "/result/", f"{self.name}.net")
        self.memory.save(file_path)

    def load_memory(self):
        dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        file_path = os.path.join(dir_path, "/result/", f"{self.name}.net")
        if os.path.exists(file_path):
            self.memory.load(file_path)
        else:
            raise FileNotFoundError(f"Memory file {file_path} not found.")
        

