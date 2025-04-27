import agent._agent as agt
import combination.sound as sd
import numpy as np
import env.environment as env
import random


def train_action(environment, episodes: int):
    rewards = []
    steps = []
    epsilon = 0.1
    # 首先是将状态更新到记忆
    for agent in environment.agents:
        add_action_memory(agent)

    for ep in range(episodes):
        # 随机选择一个代理
        agent = random.choice(environment.agents)
        action = random.choice(agent.actions)

        total_average_reward = 0
        step = 0
        done = False
        # 设置探索率
        for a in environment.agents:
            a.epsilon = epsilon
        while True:
            sound = agent.choose_sound(action, action, action=True)
            done = False
            # 检查
            filtered_agents = [a for a in environment.agents if a is not agent]

            agent.reward = 5
            average_reward = 0
            for a in filtered_agents:
                a.choose_action(sound)
                if a.mood == agent.mood:
                    a.reward = 5
                    agent.reward += 1
                else:
                    done = True
                    a.reward = -5
                    agent.reward -= 1
                average_reward += a.reward

            average_reward /= len(filtered_agents)
            total_average_reward += average_reward

            for a in environment.agents:
                next_action = random.choice(a.actions)
                a.update_qlearning(action,
                                   sound,
                                   next_action,
                                   agent.reward,
                                   action=True)
            # # 重置 mood
            for a in environment.agents:
                a.mood = 0
            agent = random.choice(filtered_agents)
            action = agent.choose_action()
            step += 1

            if not done:
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


def add_action_memory(agent: agt.Agent):
    """将位置添加到记忆中"""
    for a in agent.actions:
        agent.memory.match_node(a, data=a, action=True)
