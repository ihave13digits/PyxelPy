from pygame import sprite, Surface, Rect

from var import DISPLAY_SIZE, CELL_SIZE, COLOR_BG
from cursors import *

BG = list(COLOR_BG)

class Cell(sprite.Sprite):

    def __init__(self, x, y, r=BG[0], g=BG[1], b=BG[2]):
        sprite.Sprite.__init__(self)

        self.posx = x
        self.posy = y
        self.color = (r, g, b)
        self.image = None
        self.rect = None

    def set(self, w, h):
        self.image = Surface([w, h])
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.posx, self.posy)

    def fill(self, r, g, b, color=(-1, -1, -1)):
        if color != (-1, -1, -1):
            self.color = (r, g, b)
        else:
            self.color = color

    def update(self):
        self.image.fill(self.color)

class Palette:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.colors = []

    def add_color(self, r, g, b):
        c = (r, g, b)
        self.colors.append(c)

    def insert_color(self, r, g, b, index):
        self.colors.insert(index, (r, g, b))

    def remove_color(self, index):
        self.colors.pop(index)

    def remove_by_color(self, color, rng):
        for r in range(-rng, rng):
            clr = (c[0]+r, c[1], c[2])
            self.colors.remove(clr)
        for g in range(-rng, rng):
            clr = (c[0], c[1]+g, c[2])
            self.colors.remove(clr)
        for b in range(-rng, rng):
            clr = (c[0], c[1], c[2]+b)
        self.colors.remove(clr)

class Button(sprite.Sprite):

    def __init__(self, x, y, img, cursor=None):
        import pygame as pg
        from os import path, chdir
        sprite.Sprite.__init__(self)

        self.posx = x
        self.posy = y
        r = path.dirname(__file__)
        chdir(path.join(r, 'data'))
        self.img = pg.image.load(path.join('res', img))
        chdir(r)
        self.image = None
        self.rect = None
        self.cursor = cursor

    def set(self, w, h):
        self.image = Surface([w, h])
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.posx, self.posy)

    def update(self):
        self.image.blit(self.img, (0, 0))

class Toolbar:

    def __init__(self, x, y):
        self.area = Cell(x, y)
        self.palette_area = Cell(x, y+(CELL_SIZE*16))
        
        self.button_save = Button(x+CELL_SIZE*0, y, 'save.png')
        self.button_load = Button(x+CELL_SIZE*2, y, 'load.png')
        self.button_export = Button(x+CELL_SIZE*4, y, 'export.png')
        self.button_import = Button(x+CELL_SIZE*6, y, 'import.png')

        self.color_l = Cell(x, y+CELL_SIZE*4, r=65, g=65, b=65)
        self.color_r = Cell(x+CELL_SIZE*4, y+CELL_SIZE*4, r=65, g=65, b=65)
        
        self.tool_1 = Button(x+CELL_SIZE*0, y+CELL_SIZE*8, 'norm.png', cursor_norm)
        self.tool_2 = Button(x+CELL_SIZE*2, y+CELL_SIZE*8, 'draw.png', cursor_draw)
        self.tool_3 = Button(x+CELL_SIZE*4, y+CELL_SIZE*8, 'line.png', cursor_line)
        self.tool_4 = Button(x+CELL_SIZE*6, y+CELL_SIZE*8, 'fill.png', cursor_fill)

        self.tool_5 = Button(x+CELL_SIZE*0, y+CELL_SIZE*10, 'pick.png', cursor_pick)
        self.tool_6 = Button(x+CELL_SIZE*2, y+CELL_SIZE*10, 'tool.png', cursor_)
        self.tool_7 = Button(x+CELL_SIZE*4, y+CELL_SIZE*10, 'tool.png', cursor_)
        self.tool_8 = Button(x+CELL_SIZE*6, y+CELL_SIZE*10, 'tool.png', cursor_)

        self.tool_9 = Button(x+CELL_SIZE*0, y+CELL_SIZE*12, 'rect.png', cursor_rect)
        self.tool_10 = Button(x+CELL_SIZE*2, y+CELL_SIZE*12, 'rcte.png', cursor_rcte)
        self.tool_11 = Button(x+CELL_SIZE*4, y+CELL_SIZE*12, 'oval.png', cursor_oval)
        self.tool_12 = Button(x+CELL_SIZE*6, y+CELL_SIZE*12, 'ovle.png', cursor_ovle)

        self.tool_13 = Button(x+CELL_SIZE*0, y+CELL_SIZE*14, 'tool.png', cursor_)
        self.tool_14 = Button(x+CELL_SIZE*2, y+CELL_SIZE*14, 'tool.png', cursor_)
        self.tool_15 = Button(x+CELL_SIZE*4, y+CELL_SIZE*14, 'tool.png', cursor_)
        self.tool_16 = Button(x+CELL_SIZE*6, y+CELL_SIZE*14, 'tool.png', cursor_)
        
        self.palette = Palette(16, 32)
        self.buttons = []
        self.tools = []
        self.cells = []

    def set(self, size):
        self.area.set(size*16, size*32)
        self.palette_area.set(size*16, size*32)
        self.buttons = [
            self.button_save, self.button_load,
            self.button_export, self.button_import
            ]
        self.tools = [
                self.tool_1, self.tool_2, self.tool_3, self.tool_4,
                self.tool_5, self.tool_6, self.tool_7, self.tool_8,
                self.tool_9, self.tool_10, self.tool_11, self.tool_12,
                self.tool_13, self.tool_14, self.tool_15, self.tool_16
                ]
        self.color_l.set(size*4, size*4)
        self.color_r.set(size*4, size*4)
        for button in self.buttons:
            button.set(size*2, size*2)
        for tool in self.tools:
            tool.set(size*2, size*2)
        for swatch in self.cells:
            swatch.set(int(size/2), int(size/2))

    def set_palette(self):
        ds = list(DISPLAY_SIZE)
        X = ds[0]
        Y = ds[1]/2
        x = 0
        y = 0
        for i, c in enumerate(self.palette.colors):
            s = Cell(x*(int(CELL_SIZE/2))+X, y*(int(CELL_SIZE/2))+Y)
            s.color = c
            s.set(CELL_SIZE, CELL_SIZE)
            self.cells.append(s)
            x += 1
            if x >= self.palette.width:
                y += 1
                x = 0

    def update(self):
        self.button_save.update()
        self.button_load.update()
        self.button_export.update()
        self.button_import.update()

        self.tool_1.update()
        self.tool_2.update()
        self.tool_3.update()
        self.tool_4.update()
        self.tool_5.update()
        self.tool_6.update()
        self.tool_7.update()
        self.tool_8.update()
        self.tool_9.update()
        self.tool_10.update()
        self.tool_11.update()
        self.tool_12.update()
        self.tool_13.update()
        self.tool_14.update()
        self.tool_15.update()
        self.tool_16.update()
        
        self.color_l.update()
        self.color_r.update()
    
    def update_palette(self):
        for c in self.cells:
            c.update()

class Camera:

    def __init__(self, width, height):
        self.camera = Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.width - HEIGHT), y)
        self.camera = Rect(x, y, self.width, self.height)
