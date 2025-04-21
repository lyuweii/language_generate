import random
import numpy as np
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

    def train(self, episodes: int =500):
        """训练Q-learning表"""
        rewards = []
        steps = []
        epsilon=0.1

        for ep in range(episodes):
            # 随机选一个物品
            good = random.choice(self.goods)
            agent = random.choice(self.agents)
            total_average_reward = 0
            step = 0
            done = False
            # 设置探索率
            for agent in self.agents:
                agent.epsilon = epsilon
            while not done:
                sound = agent.choose_sound(good)
                agent.send_sound(sound)
                # 检查
                next_good, next_agent, done, average_reward,goods= self.judge(
                    agent, good, sound)

                agent = next_agent
                good = next_good
                step += 1
                total_average_reward += average_reward

                if done:
                    break
            rewards.append(total_average_reward)
            steps.append(step)
            # 动态调整探索率
            epsilon = max(0.01, 0.1 - ep / 500)

            if ep % 50 == 0:
                print(
                    f"Episode {ep}: Steps={step}, Reward={total_average_reward:.1f}"
                )
        return rewards, steps

    
    def judge(self,agent:Agent,good:int,sound: sd.Sound):
        next_agent = random.choice([a for a in self.agents if a is not agent])
        next_good = random.choice([g for g in self.goods if g is not good])
        flag=True
        average_reward = 0
        goods=[]
        for rv in self.agents:
            if rv is agent:
                continue
            rv_good = rv.choose_good(sound)
            if rv_good == good:
                reward = 10
            else:
                reward = -1
                flag=False
            goods.append(rv_good)
            average_reward+=reward
            rv.update_qlearning(good, sound, next_good, reward)
        average_reward /= len(self.agents)
        return next_good, next_agent, flag, average_reward,goods
            

    def run(self):
        """运行环境"""
        for i in range(50):
            self.add_agent(Agent(self, i,f"H-{i}"))
        
        self.train()

        #self.agents[0].send_sound(sd.monster_roar)
