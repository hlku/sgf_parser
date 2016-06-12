# -*- coding: UTF-8 -*-
import visual
import itertools

class Board(visual.vis.primitives.frame):
    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        
        visual.box(pos = (9, 9, -1),
                   size = (20, 20, 1),
                   color = (1, 0.75, 0),
                   material = visual.materials.wood,
                   frame = self)
        # lines
        params = dict(color = (.5, .5, .5), frame = self)
        for i in range(19):
            visual.curve(pos = [(0, i, 0), (18, i, 0)], radius = .05, **params)
        for i in range(19):
            visual.curve(pos=[(i, 0, 0), (i, 18, 0)], radius = .05, **params)
        
        self.stones, self.star = [], []
        for x in itertools.product((4, 10, 16), (4, 10, 16)): self.star.append(x[:])
        
    def setMap(self, board):        
        # clean the board
        for stone in self.stones: stone.visible = False
        self.stones = []
        
        for x in range(19):
            for y in range(19):
                if board[y + 1][x + 1] == 1:
                    stone = visual.cylinder(pos = (x, y, 0),
                                            axis = (0, 0, .1),
                                            radius = .4,
                                            color = visual.color.black,
                                            frame = self)
                elif board[y + 1][x + 1] == 2:
                    stone = visual.cylinder(pos = (x, y, 0),
                                            axis = (0, 0, .1),
                                            radius = .4,
                                            color = visual.color.white,
                                            frame = self)
                else: # 0
                    if(x + 1, y + 1) not in self.star:
                        stone = visual.cylinder(pos = (x, y, 0),
                                              axis = (0, 0, 0),
                                              radius = 0,
                                              color = visual.color.black,
                                              frame = self)
                    else:
                        stone = visual.cylinder(pos = (x, y, 0),
                                              axis = (0, 0, .01),
                                              radius = .2,
                                              color = (.5, .5, .5),
                                              frame = self)
                self.stones.append(stone)
