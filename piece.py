from enum import Enum
from collections import deque
from random import *

import pygame
from pygame.locals import *

visible_next_count = 1

class PieceShape(Enum):
    O = 0
    I = 1
    S = 2
    Z = 3
    L = 4
    J = 5
    T = 6

    def rects(self) -> list[tuple[int, int, int, int]]:
        match self:
            case PieceShape.O: return [(0, 0, 2, 2)]
            case PieceShape.I: return [(0, 0, 1, 4)]
            case PieceShape.S: return [(1, 0, 2, 1), (0, 1, 2, 1)]
            case PieceShape.Z: return [(0, 0, 2, 1), (1, 1, 2, 1)]
            case PieceShape.L: return [(1, 2, 1, 1), (0, 0, 1, 3)]
            case PieceShape.J: return [(0, 2, 1, 1), (1, 0, 1, 3)]
            case PieceShape.T: return [(0, 0, 3, 1), (1, 1, 1, 1)]

    def size(self) -> tuple[int, int]:
        match self:
            case PieceShape.O: return (2, 2)
            case PieceShape.I: return (1, 4)
            case PieceShape.S: return (3, 2)
            case PieceShape.Z: return (3, 2)
            case PieceShape.L: return (2, 3)
            case PieceShape.J: return (2, 3)
            case PieceShape.T: return (3, 2)

    def fill(self, surface: pygame.Surface, color: tuple[int, int, int], pivot: tuple[float, float, float, float]):
        for rect in self.rects():
            surface.fill(color, pygame.Rect(pivot[0] + pivot[2] * rect[0], pivot[1] + pivot[3] * rect[1], pivot[2] * rect[2], pivot[3] * rect[3]))

class Piece:
    def __init__(self, x: int, y: int, shape: PieceShape, rotation: int):
        self.x = x
        self.y = y
        self.shape = shape
        self.rotation = rotation

    def rects(self) -> list[tuple[int, int, int, int]]:
        return map(lambda rect: self._transform_rect_(rect), self.shape.rects())

    def size(self) -> tuple[int, int]:
        if self.rotation == 1 or self.rotation == 3:
            shape_size = self.shape.size()
            return ([shape_size[1], shape_size[0]])
        else:
            return self.shape.size()

    def fill(self, surface: pygame.Surface, color: tuple[int, int, int], pivot: tuple[float, float, float, float]):
        for rect in self.rects():
            surface.fill(color, pygame.Rect(pivot[0] + pivot[2] * rect[0], pivot[1] + pivot[3] * rect[1], pivot[2] * rect[2], pivot[3] * rect[3]))

    def right(self) -> int:
        size = self.size()
        return self.x - round(size[0] / 2 - 0.49) + size[0]
    def left(self) -> int:
        size = self.size()
        return self.x - round(size[0] / 2 - 0.49)
    def top(self) -> int:
        size = self.size()
        return self.y - round(size[1] / 2 - 0.49)
    def bottom(self) -> int:
        size = self.size()
        return self.y - round(size[1] / 2 - 0.49) + size[1]

    def _transform_rect_(self, rect: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
        x = self.left()
        y = self.top()
        match self.rotation:
            case 0: return (x + rect[0], y + rect[1], rect[2], rect[3])
            case 1: return (x + self.shape.size()[1] - rect[1] - rect[3], y + rect[0], rect[3], rect[2])
            case 2: return (x + self.shape.size()[0] - rect[0] - rect[2], y + self.shape.size()[1] - rect[1] - rect[3], rect[2], rect[3])
            case 3: return (x + rect[1], y + self.shape.size()[0] - rect[0] - rect[2], rect[3], rect[2])

class PieceQueue:
    def __init__(self):
        self.queue = deque()
        self.rand = Random()
        for _ in range(visible_next_count):
            self.queue.append(PieceShape(self.rand.randrange(0, 7)))
    
    def next(self) -> PieceShape:
        self.queue.append(PieceShape(self.rand.randrange(0, 7)))
        return self.queue.popleft()