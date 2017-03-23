from engine.misc.util import Util
from engine.globs.eventDispatcher import EventDispatcher
from engine.globs.renderer import Renderer
from pygame import Surface, font
from pygame.sprite import Sprite


class FadingScreen(Sprite):
    active = True
    a, t, x = 0, 255, 0

    def __init__(self):
        super().__init__()
        self.image = Surface((640, 480))
        self.rect = self.image.get_rect()
        text = 'Game Over'
        fuente = font.SysFont('verdana', 50)
        self.msg = fuente.render(text, 1, [255, 0, 0])
        self.m_r = self.msg.get_rect(center=self.rect.center)
        self.image.blit(self.msg, self.m_r)

    def update(self):
        self.a += 1
        if self.a <= 255:
            self.image.set_alpha(self.a)
        elif self.a > 600:
            Util.salir('gameover')


def gameover(evento):
    if evento.data['obj'].nombre == 'heroe':
        Renderer.add_overlay(FadingScreen(), 50)

EventDispatcher.register(gameover, "MobDeath")
