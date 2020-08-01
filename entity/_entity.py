from abc import ABC, abstractmethod


class Entity(ABC):

    def __init__(self):
        self._clock = 0.0

    @property
    def clock(self):
        return self._clock

    @abstractmethod
    def tick(self, dt):
        self._clock += dt