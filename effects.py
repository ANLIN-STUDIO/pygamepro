from typing import Union
import pygame
import pygamepro.parameter



# pygamepro.effects.Gradients(screen, surface_p, surface_c, [0, 0], 1).run()
class Gradients:
    def __init__(self,
                 screen: pygame.Surface,
                 parent: pygame.Surface,
                 child: pygame.Surface,
                 parent_pos: Union[list, tuple],
                 delay: Union[int, float],
                 child_pos: Union[list, tuple] = None):
        self.screen = screen
        self.parent_surface = self.ps = parent
        self.child_surface = self.cs = child
        self.parent_pos = self.pp = parent_pos
        if child_pos is None:
            self.child_pos = self.cp = parent_pos
        else:
            self.child_pos = self.cp = child_pos
        self.delay = delay

    def run(self):
        child_alpha = ca = 0
        s = self.screen
        while ca <= 255:
            self.screen.fill(pygamepro.colors.White)
            self.ps.set_alpha(255 - ca)
            self.screen.blit(self.ps, self.pp)
            self.cs.set_alpha(ca)
            self.screen.blit(self.cs, self.cp)
            pygame.display.flip()
            pygame.time.delay(self.delay)
            ca += 1


# pygamepro.effects.Fade_out(screen, surface_p, surface_c, [0, 0], colors.Black, 1).run()
class Fade_out:
    def __init__(self,
                 screen: pygame.Surface,
                 parent: pygame.Surface,
                 child: pygame.Surface,
                 parent_pos: Union[list, tuple],
                 background: Union[list, tuple],
                 delay: int,
                 child_pos: Union[list, tuple] = None):
        self.screen = screen
        self.parent_surface = self.ps = parent
        self.child_surface = self.cs = child
        self.parent_pos = self.pp = parent_pos
        if child_pos is None:
            self.child_pos = self.cp = parent_pos
        else:
            self.child_pos = self.cp = child_pos
        self.delay = delay
        self.background = background

    def run(self):
        parent_alpha = pa = 255
        child_alpha = ca = 0
        s = self.screen
        while pa >= 0:
            self.screen.fill(self.background)
            self.ps.set_alpha(pa)
            self.screen.blit(self.ps, self.pp)
            pygame.display.flip()
            pygame.time.delay(self.delay)
            pa -= 1
        while ca <= 255:
            self.screen.fill(self.background)
            self.cs.set_alpha(ca)
            self.screen.blit(self.cs, self.cp)
            pygame.display.flip()
            pygame.time.delay(self.delay)
            ca += 1


# pygamepro.effects.Diffusion(screen, surface_p, surface_c, [0, 0], pygame.mouse.get_pos(), 0.2).run()
class Diffusion:
    def __init__(self,
                 screen: pygame.Surface,
                 parent: pygame.Surface,
                 child: pygame.Surface,
                 parent_pos: Union[list, tuple],
                 start_point: Union[list, tuple],
                 speed: Union[int, float],
                 child_pos: Union[list, tuple] = None):
        self.screen = screen
        self.parent_surface = self.ps = parent
        self.child_surface = self.cs = child
        self.parent_pos = self.pp = parent_pos
        if child_pos is None:
            self.child_pos = self.cp = parent_pos
        else:
            self.child_pos = self.cp = child_pos
        self.start_point = self.sp = start_point
        self.speed = speed

    def run(self):
        self.screen.blit(self.ps, self.pp)
        pygame.display.flip()
        self.screen.blit(self.cs, self.cp)
        xr = yr = 0
        wr = hr = 0
        sp = self.sp
        size = [0, 0]
        rect = [0, 0, 0, 0]
        while xr+wr<=self.cs.get_width()*2:
            size = [size[0]+self.speed, size[1]+self.speed]
            rect = [sp[0] - xr, sp[1] - yr, size[0] + wr, size[1] + hr]
            pygame.display.update(rect)
            xr += self.speed
            yr += self.speed
            wr += self.speed
            hr += self.speed


# pygamepro.effects.Move(screen, surface_p, surface_c, [0, 0], 0.2).run()
class Move:
    def __init__(self,
                 screen: pygame.Surface,
                 parent: pygame.Surface,
                 child: pygame.Surface,
                 parent_pos: Union[list, tuple],
                 speed: Union[int, float],
                 direction: int = pygamepro.parameter.Right,
                 child_pos: Union[list, tuple] = None):
        self.screen = screen
        self.parent_surface = self.ps = parent
        self.child_surface = self.cs = child
        self.parent_pos = self.pp = parent_pos
        if child_pos is None:
            self.child_pos = self.cp = parent_pos
        else:
            self.child_pos = self.cp = child_pos
        self.direction = direction
        self.speed = speed

    def run(self):
        speed = self.speed
        pp = self.pp
        cp = [self.cp[0]-self.cs.get_width(), self.cp[1]]
        rel = 0
        while rel <= self.cs.get_width():
            if self.direction == pygamepro.parameter.Right:
                pp[0] += speed
                cp[0] += speed
            elif self.direction == pygamepro.parameter.Left:
                pp[0] -= speed
                cp[0] -= speed
            elif self.direction == pygamepro.parameter.Top:
                pp[1] -= speed
                cp[1] -= speed
            elif self.direction == pygamepro.parameter.Bottom:
                pp[0] += speed
                cp[0] += speed
            rel += speed
            self.screen.blit(self.ps, pp)
            self.screen.blit(self.cs, cp)
            pygame.display.flip()
