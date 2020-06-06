#!/usr/bin/python3

import tools
import pygame as pg

from os import path, chdir

from var import *
from cursors import *
from classes import Cell, Palette, Toolbar, Camera

pg.init()

class Engine:

    def __init__(self):
        self.running = True
        self.screen = pg.display.set_mode(WINDOW_SIZE)
        self.clock = pg.time.Clock()
        self.elapsed_time = 0.0

        self.canvas_size = DISPLAY_SIZE
        self.cell_size = CELL_SIZE

        self.grid = True
        self.working_data = False

        self.canvas = []
        self.canvas_area = Cell(0, 0)

        self.toolbar = None

        self.left_color = 0
        self.right_color = 0

        self.rotation = 0

        self.clipboard = {}
        self.root_dir = path.dirname(__file__)
        self.data_dir = None
        self.img_dir = None
        self.res_dir = None

        self.click_buffer = []
        self.cursor = cursor_norm

        self.last_save_dir = ''

    def save(self, save_dir):
        import pickle
        for c in self.canvas:
            c.image = None
            c.rect = None
        
        data = {'canvas' : self.canvas, 'palette' : self.toolbar.palette}

        with open(path.join(self.data_dir, "{}.bmd".format(save_dir)), 'wb') as f:
            pickle.dump(data, f)
            f.close()

        for c in self.canvas:
            c.set(CELL_SIZE, CELL_SIZE)
            c.update()
        self.working_data = False

    def load(self, load_dir):
        import pickle

        try:
            with open(path.join(self.data_dir, "{}.bmd".format(load_dir)), 'rb') as f:
                data = pickle.load(f)
                f.close()

            self.canvas = data['canvas']
            self.toolbar.palette = data['palette']
        except FileNotFoundError:
            pass

        for c in self.canvas:
            c.set(CELL_SIZE, CELL_SIZE)
            c.update()
            self.screen.blit(c.image, c)
        self.working_data = False

    def port(self, img_file, mode):
        try:
            w = int(list(self.canvas_size)[0]/self.cell_size)
            h = int(list(self.canvas_size)[1]/self.cell_size)
            if mode == 0:
                img = pg.Surface((w, h))
                img.convert_alpha()
                for x in range(w):
                    for y in range(h):
                        v = int((y * w) + x)
                        try:
                            c = self.canvas[v].color
                            img.set_at((x, y), c)
                        except IndexError:
                            pass
                pg.image.save(img, path.join(self.img_dir, img_file))

            if mode == 1:
                img = pg.image.load(path.join(self.img_dir, img_file))
                img.convert_alpha()
                for x in range(w):
                    for y in range(h):
                        v = int((y * w) + x)
                        try:
                            c = img.get_at((x, y))
                            self.canvas[v].color = c
                        except IndexError:
                            pass
                for c in self.canvas:
                    c.set(CELL_SIZE, CELL_SIZE)
                    c.update()
                    self.screen.blit(c.image, c)
                pg.display.update(self.canvas_area)
        except:
            print("Failed to port image.")
        self.working_data = False

    def install(self):
        # Handle Directories
        from os import mkdir
        if self.data_dir == None:
            try:
                mkdir(path.join(self.root_dir, 'data'))
            except FileExistsError:
                pass
        self.data_dir = path.join(self.root_dir, 'data')

        if self.img_dir == None:
            try:
                mkdir(path.join(self.data_dir, 'img'))
            except FileExistsError:
                pass
        self.img_dir = path.join(self.data_dir, 'img')

        if self.res_dir == None:
            try:
                mkdir(path.join(self.data_dir, 'res'))
            except FileExistsError:
                pass
        self.res_dir = path.join(self.data_dir, 'res')
    
    def start(self):
        self.install()
        # Handle Settings
        pg.display.set_caption(PROJECT_NAME)
        pg.key.set_repeat(50, 100)

        ds = list(DISPLAY_SIZE)
        X = int(ds[0] / CELL_SIZE)
        Y = int(ds[1] / CELL_SIZE)

        # Generate Canvas
        for y in range(X):
            for x in range(Y):
                c = Cell(x*CELL_SIZE, y*CELL_SIZE)
                c.set(CELL_SIZE, CELL_SIZE)
                self.canvas.append(c)
                c.update()
                self.screen.blit(c.image, c)

        self.canvas_area.set(ds[0], ds[1])
        pg.display.update(self.canvas_area)

        # Generate Toolbar
        self.toolbar = Toolbar(ds[0], 0)

        PALETTE = PALETTE_256
        for p in PALETTE:
            for c in range(PALETTE[p][3], PALETTE[p][4], PALETTE[p][5]):
                self.toolbar.palette.add_color(int(c*PALETTE[p][0]), int(c*PALETTE[p][1]), int(c*PALETTE[p][2]), 0)

        self.toolbar.color_l.color = self.toolbar.palette.colors[self.left_color]
        self.toolbar.color_r.color = self.toolbar.palette.colors[self.right_color]

        self.toolbar.set_palette()
        self.toolbar.set(CELL_SIZE)
        self.toolbar.update()
        self.toolbar.update_palette()

        for s in self.toolbar.cells:
            self.screen.blit(s.image, s)
        for b in self.toolbar.buttons:
            self.screen.blit(b.image, b)
        for t in self.toolbar.tools:
            self.screen.blit(t.image, t)
        pg.display.update(self.toolbar.palette_area)
        pg.display.update(self.toolbar.area)

        cursor = pg.cursors.compile(self.cursor, black='X', white='.', xor='o')
        pg.mouse.set_cursor((16, 16), (0, 0), *cursor)

        self.run()

    def run(self):
        while self.running:
            dt = self.clock.tick(30) / 1000
            self.event()
            self.update()
            self.elapsed_time += dt

    def draw_grid(self):
        if len(self.click_buffer) <= 1:
            ds = list(self.canvas_size)
            for x in range(0, ds[0], CELL_SIZE):
                pg.draw.line(self.screen, (255, 255, 255, 128), (x, 0), (x, ds[1]))
            for y in range(0, ds[1], CELL_SIZE):
                pg.draw.line(self.screen, (255, 255, 255, 128), (0, y), (ds[0], y))
            pg.display.update(self.canvas_area)

    def update(self):
        self.event()
        self.toolbar.update()
        end = len(self.click_buffer)-1
        if len(self.click_buffer) > 1:
            xstart = int(self.click_buffer[0][0]/self.cell_size)
            ystart = int(self.click_buffer[0][1]/self.cell_size)
            xstop = int(self.click_buffer[end][0]/self.cell_size)
            ystop = int(self.click_buffer[end][1]/self.cell_size)

            sel = Cell(xstart*self.cell_size, ystart*self.cell_size, r=255, g=255, b=255, a=128)
            sel.set(xstop*self.cell_size, ystop*self.cell_size)
            sel.image.convert_alpha()
            self.screen.blit(sel.image, sel)
            pg.display.update(self.canvas_area)
        else:
            if self.grid:
                self.draw_grid()

    def event(self):
        mp = list(pg.mouse.get_pos())
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
            ### SCROLLING ###
                if event.button == 4:
                    try:
                        if self.left_color < len(self.toolbar.cells)-1:
                            self.left_color += 1
                            self.toolbar.color_l.color = self.toolbar.palette.colors[self.left_color]
                            self.toolbar.update()
                            self.screen.blit(self.toolbar.color_l.image, self.toolbar.color_l)
                            pg.display.update(self.toolbar.area)
                    except TypeError:
                        pass
                if event.button == 5:
                    try:
                        if self.left_color > 0:
                            self.right_color -= 1
                            self.toolbar.color_l.color = self.toolbar.palette.colors[self.left_color]
                            self.toolbar.update()
                            self.screen.blit(self.toolbar.color_l.image, self.toolbar.color_l)
                            pg.display.update(self.toolbar.area)
                    except TypeError:
                        pass
            if event.type == pg.MOUSEMOTION or event.type == pg.MOUSEBUTTONDOWN:
            ### TOOLBAR ###
                # Data
                if self.toolbar.area.rect.collidepoint(mp[0], mp[1]):
                    if pg.mouse.get_pressed() == (1, 0, 0):
                        if self.toolbar.button_save.rect.collidepoint(mp[0], mp[1]):
                            if not self.working_data:
                                print("Enter name to save")
                                name = input(": ")
                                self.working_data = True
                            self.save(name)
                        if self.toolbar.button_load.rect.collidepoint(mp[0], mp[1]):
                            print("Enter name to load")
                            name = input(": ")
                            self.working_data = True
                            self.load(name)
                        if self.toolbar.button_export.rect.collidepoint(mp[0], mp[1]):
                            if not self.working_data:
                                print("Enter name to save")
                                name = input(": ")
                                self.last_save_dir = name
                                self.working_data = True
                                self.port(name, 0)
                        if self.toolbar.button_import.rect.collidepoint(mp[0], mp[1]):
                            print("Enter name to load")
                            name = input(": ")
                            self.last_save_dir = name
                            self.working_data = True
                            self.port(name, 1)
                    # Set Tool
                        for t in self.toolbar.tools:
                            if t.rect.collidepoint(mp[0], mp[1]):
                                if t.cursor != None:
                                    self.cursor = t.cursor
                                    cursor = pg.cursors.compile(self.cursor, black='X', white='.', xor='o')
                                    pg.mouse.set_cursor((16, 16), (0, 0), *cursor)
                    # Change Color
                    if self.toolbar.palette_area.rect.collidepoint(mp[0], mp[1]):
                        if pg.mouse.get_pressed() == (1, 0, 0):
                            for i, c in enumerate(self.toolbar.cells):
                                if c.rect.collidepoint(mp[0], mp[1]):
                                    self.left_color = i
                                    self.toolbar.color_l.color = self.toolbar.palette.colors[self.left_color]
                                    self.toolbar.update()
                                    self.screen.blit(self.toolbar.color_l.image, self.toolbar.color_l)
                                    pg.display.update(self.toolbar.area)
                        if pg.mouse.get_pressed() == (0, 0, 1):
                            for i, c in enumerate(self.toolbar.cells):
                                if c.rect.collidepoint(mp[0], mp[1]):
                                    self.right_color = i
                                    self.toolbar.color_r.color = self.toolbar.palette.colors[self.right_color]
                                    self.toolbar.update()
                                    self.screen.blit(self.toolbar.color_r.image, self.toolbar.color_r)
                                    pg.display.update(self.toolbar.area)
            ### CANVAS ###
                # Apply Tool
                if self.canvas_area.rect.collidepoint(mp[0], mp[1]):
                    if pg.mouse.get_pressed() == (1, 0, 0):
                        if self.cursor == cursor_norm:
                            tools.select(self, mp)
                        if self.cursor == cursor_draw:
                            tools.draw(self, mp, self.left_color)
                            pg.display.update(self.canvas_area)
                        if self.cursor == cursor_rect:
                            if not self.working_data:
                                self.working_data = True
                                tools.rect_f(self, mp, self.left_color)
                                pg.display.update(self.canvas_area)
                        if self.cursor == cursor_rcte:
                            if not self.working_data:
                                self.working_data = True
                                tools.rect_e(self, mp, self.left_color)
                                pg.display.update(self.canvas_area)
                        if self.cursor == cursor_oval:
                            if not self.working_data:
                                self.working_data = True
                                tools.oval_f(self, mp, self.left_color)
                                pg.display.update(self.canvas_area)
                        if self.cursor == cursor_ovle:
                            if not self.working_data:
                                self.working_data = True
                                tools.oval_e(self, mp, self.left_color)
                                pg.display.update(self.canvas_area)
                        if self.cursor == cursor_fill:
                            if not self.working_data:
                                self.working_data = True
                                tools.flood_fill(self, mp, self.left_color)
                                pg.display.update(self.canvas_area)
                        if self.cursor == cursor_pick:
                            self.left_color = tools.dropper(self, mp)
                            self.toolbar.color_l.color = tools.dropper(self, mp)
                            self.screen.blit(self.toolbar.color_l.image, self.toolbar.color_l)
                            pg.display.update(self.toolbar.area)
                    if pg.mouse.get_pressed() == (0, 0, 1):
                        if self.cursor == cursor_draw:
                            tools.draw(self, mp, self.right_color)
                            pg.display.update(self.canvas_area)
                        if self.cursor == cursor_rect:
                            if not self.working_data:
                                self.working_data = True
                                tools.rect_f(self, mp, self.right_color)
                                pg.display.update(self.canvas_area)
                        if self.cursor == cursor_rcte:
                            if not self.working_data:
                                self.working_data = True
                                tools.rect_e(self, mp, self.right_color)
                                pg.display.update(self.canvas_area)
                        if self.cursor == cursor_oval:
                            if not self.working_data:
                                self.working_data = True
                                tools.oval_f(self, mp, self.right_color)
                                pg.display.update(self.canvas_area)
                        if self.cursor == cursor_ovle:
                            if not self.working_data:
                                self.working_data = True
                                tools.oval_e(self, mp, self.right_color)
                                pg.display.update(self.canvas_area)
                        if self.cursor == cursor_fill:
                            if not self.working_data:
                                self.working_data = True
                                tools.flood_fill(self, mp, self.right_color)
                                pg.display.update(self.canvas_area)
                        if self.cursor == cursor_pick:
                            self.right_color = tools.dropper(self, mp)
                            self.toolbar.color_r.color = tools.dropper(self, mp)
                            self.screen.blit(self.toolbar.color_r.image, self.toolbar.color_r)
                            pg.display.update(self.toolbar.area)
            # Commit Selection
            if event.type == pg.MOUSEBUTTONUP:
                if self.canvas_area.rect.collidepoint(mp[0], mp[1]):
                    if self.cursor == cursor_norm:
                        if not self.working_data:
                            self.working_data = True
                            tools.set_select(self, mp)
        ### KEYS ###
            if event.type == pg.KEYDOWN:
                # Rotation
                if event.key == pg.K_KP2:
                    self.rotation = 270
                if event.key == pg.K_KP4:
                    self.rotation = 180
                if event.key == pg.K_KP8:
                    self.rotation = 90
                if event.key == pg.K_KP6:
                    self.rotation = 0
                # Blur
                if event.key == pg.K_b:
                    if not self.working_data:
                        tools.blur(self)
                        pg.display.update(self.canvas_area)
                # Quick Save
                if (event.mod == pg.KMOD_LCTRL or event.mod == pg.KMOD_RCTRL) and event.key == pg.K_s:
                    if self.last_save_dir != '':
                        self.working_data = True
                        self.port(self.last_save_dir, 0)
                # Grid
                if (event.mod == pg.KMOD_LCTRL or event.mod == pg.KMOD_RCTRL) and event.key == pg.K_g:
                    self.grid = False
                    for c in self.canvas:
                        self.screen.blit(c.image, c)
                    pg.display.update(self.canvas_area)
                    made_changes = True
                if (event.mod == pg.KMOD_LSHIFT or event.mod == pg.KMOD_RSHIFT) and event.key == pg.K_g:
                    self.grid = True
                # Pasting
                if (event.mod == pg.KMOD_LCTRL or event.mod == pg.KMOD_RCTRL) and event.key == pg.K_v:
                    tools.paste(self, mp)
                    pg.display.update(self.canvas_area)
                if (event.mod == pg.KMOD_LSHIFT or event.mod == pg.KMOD_RSHIFT) and event.key == pg.K_v:
                    tools.paste(self, mp, mode=1)
                    pg.display.update(self.canvas_area)
                # Undo
                if (event.mod == pg.KMOD_LCTRL or event.mod == pg.KMOD_RCTRL) and event.key == pg.K_z:
                    print("I really needa learn how to do that..")
                # Exiting
                if event.key == pg.K_ESCAPE:
                    self.running = False
                # Change Mouse Position
                if mp[1] > 0 and mp[1] < list(self.canvas_size)[1] and mp[0] > 0 and mp[0] < list(self.canvas_size)[0]:
                    if event.key == pg.K_UP:
                        for c in self.canvas:
                            if c.rect.collidepoint(mp[0], mp[1]):
                                pg.mouse.set_pos([c.posx+(CELL_SIZE/2), c.posy+(CELL_SIZE/2)-CELL_SIZE])
                    if event.key == pg.K_DOWN:
                        for c in self.canvas:
                            if c.rect.collidepoint(mp[0], mp[1]):
                                pg.mouse.set_pos([c.posx+(CELL_SIZE/2), c.posy+(CELL_SIZE/2)+CELL_SIZE])
                    if event.key == pg.K_LEFT:
                        for c in self.canvas:
                            if c.rect.collidepoint(mp[0], mp[1]):
                                pg.mouse.set_pos([c.posx+(CELL_SIZE/2)-CELL_SIZE, c.posy+(CELL_SIZE/2)])
                    if event.key == pg.K_RIGHT:
                        for c in self.canvas:
                            if c.rect.collidepoint(mp[0], mp[1]):
                                pg.mouse.set_pos([c.posx+(CELL_SIZE/2)+CELL_SIZE, c.posy+(CELL_SIZE/2)])

E = Engine()
E.start()
