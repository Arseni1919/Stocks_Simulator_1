from globals import *


class MetaEnv(ABC):
    def __init__(self):
        self.name = 'MetaEnv'
        self.action_space = []

    @abstractmethod
    def reset(self):
        """
        :return: observation, info
        """
        pass

    @abstractmethod
    def sample_action(self):
        pass

    @abstractmethod
    def step(self, action):
        """
        :return: observation, reward, terminated, truncated, info
        """
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def render(self, info=None):
        pass
