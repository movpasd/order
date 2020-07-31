from abc import ABC, abstractmethod


class RenderManager:

    def __init__(self, screen, renderables=None):

        self._screen = screen
        if renderables is None:
            renderables = []
        self.renderables = renderables

    @property
    def screen(self):
        return self._screen

    def update(self):

        for renderable in self.renderables:
            renderable.draw(self.screen)


class Renderable(ABC):

    @abstractmethod
    def draw(self, screen): pass
