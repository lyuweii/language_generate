import agent.agent as agt

class BaseEnvironment:
    def __init__(self,num_agents=10):
        self.state = None
        self.action_space = None
        self.observation_space = None
        self.agents= []
        for i in range(num_agents):
            self.agents.append(agt.Agent(self,i,name=f"Agent_{i}"))
        self.current_step = 0


    def reset(self):
        """Reset the environment to an initial state."""
        pass

    def step(self, action):
        """Take an action in the environment and return the next state, reward, done, and info."""
        pass

    def render(self):
        """Render the environment."""
        pass

    def close(self):
        """Close the environment."""
        pass