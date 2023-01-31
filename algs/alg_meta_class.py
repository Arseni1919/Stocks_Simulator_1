from globals import *


class MetaAlg(ABC):

    def __init__(self):
        self.name = 'Alg'

    @abstractmethod
    def return_action(self, observation):
        """
        :param observation:
        :return: action
        """
        pass

    @abstractmethod
    def update(self, observation, action, reward, next_observation, terminated, truncated):
        pass

    @abstractmethod
    def render(self, info):
        pass
