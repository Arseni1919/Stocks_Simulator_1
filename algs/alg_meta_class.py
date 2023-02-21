from globals import *


class MetaAlg(ABC):
    # TODO: to transfer the main part of algs to this class
    # TODO: to make available multiple action calls
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
    def update_after_action(self, observation, action, reward, next_observation, terminated, truncated):
        pass

    @abstractmethod
    def render(self, info):
        pass
