import random
import numpy as np
import networkx as nx
import sound as sd
from agent import Agent


class Signal:
    """信号类

    属性：
        - sound: 音节
        - sender: 发送者
        - position: 发送者位置
        - tx_range: 发送范围"""

    def __init__(self, sender: Agent, position: np.ndarray, tx_range: float,
                 sound: sd.Sound):
        """初始化信号类"""
        self.sound = sound
        self.sender = sender
        self.position = position
        self.tx_range = tx_range


class Environment:

    def __init__(self):
        self.size = 100
        self.agents = []
        self.goods = [0, 1, 2, 3, 4, 5]

    @staticmethod
    def calculate_distance(agent1: Agent, agent2: Agent):
        """计算两个人类之间的距离"""
        return np.linalg.norm(agent1.position - agent2.position)

    def add_agent(self, agent: Agent):
        self.agents.append(agent)

    def remove_agent(self, agent: Agent):
        if Agent in self.agents:
            self.agents.remove(agent)

    def broadcast(self, signal: Signal):
        """广播信号"""
        for receiver in self.agents:
            if receiver is signal.sender:
                continue
            distance = self.calculate_distance(signal, receiver)
            if distance < signal.tx_range and distance < receiver.rx_range:
                receiver.receive_sound(signal.sound)

    def choose_good(self):
        return random.choice(self.goods)

    def choose_agent(self):
        pass

    def judge_learn(self, good: int, action: int, sound: sd.Sound):
        pass

    def train(self, episodes: int = 500):
        """训练Q-learning表"""
        reward_list = []
        steps = []

        for ep in range(episodes):
            # 随机选一个物品
            good = random.choice(self.goods)
            agent = random.choice(self.agents)
            total_average_reward = 0
            step = 0
            done = False
            while not done:
                sound = agent.choose_sound(good)
                agent.send_sound(sound)
                self.judge(agent, sound, good)

                step+=1
                done = True
        print("ok")
    
    def judge(self,agent:Agent,sound: sd.Sound, good: int):
        reward = 0
        for rv in self.agents:
            if rv is agent:
                continue
            rv_good = rv.choose_good(sound)
            if rv_good == good:
                reward += 10
            else:
                reward -= 1
            

            


    def run(self):
        """运行环境"""
        for i in range(3):
            self.add_agent(Agent(self, i,f"H-{i}"))
        
        self.train()

        #self.agents[0].send_sound(sd.monster_roar)
