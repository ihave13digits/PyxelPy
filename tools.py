def select(target, mp):
    target.click_buffer.append(mp)
    if len(target.click_buffer) > 2:
        target.click_buffer.pop(1)

def set_select(target, mp):
    target.click_buffer.append(mp)
    l = len(target.click_buffer)-1
    data = {'width' : 0, 'height' : 0, 'colors' : [], 'matrix' : []}

    if (
            int(target.click_buffer[0][0]/target.cell_size) < int(target.click_buffer[l][0]/target.cell_size)
                    ) and (
                        int(target.click_buffer[0][1]/target.cell_size) < int(target.click_buffer[l][1]/target.cell_size)):
        x1 = int(target.click_buffer[0][0]/target.cell_size)
        y1 = int(target.click_buffer[0][1]/target.cell_size)
        x2 = int(target.click_buffer[l][0]/target.cell_size)
        y2 = int(target.click_buffer[l][1]/target.cell_size)
        step = 1
    else:
        y1 = int(target.click_buffer[0][0]/target.cell_size)
        x1 = int(target.click_buffer[0][1]/target.cell_size)
        y2 = int(target.click_buffer[l][0]/target.cell_size)
        x2 = int(target.click_buffer[l][1]/target.cell_size)
        step = -1
    
    data['width'] = abs(x1 - x2)+1
    data['height'] = abs(y1 - y2)+1

    for x in range(x1, x2+1, step):
        for y in range(y1, y2+1, step):
            v = int(y * int(list(target.canvas_size)[0])/target.cell_size) + x
            data['colors'].append(target.canvas[v].color)
            data['matrix'].append(target.canvas[v])

    target.click_buffer.clear()
    target.clipboard = data
    target.working_data = False

def rect_e(target, mp, C):
    try:
        v1 = (int(mp[1]/target.cell_size) * int(list(target.canvas_size)[0]/target.cell_size)) + int(mp[0]/target.cell_size)
        for x in range(target.clipboard['width']):
            for y in range(target.clipboard['height']):
                if (x == 0 or x == target.clipboard['width']-1) or (y == 0 or y == target.clipboard['height']-1):
                    try:
                        v2 = (y * target.clipboard['width']) + x
                        v = v1 + ((y * int(list(target.canvas_size)[0]/target.cell_size)) + x)
                        if type(C) == int:
                            target.canvas[v].color = target.toolbar.palette.colors[C]
                        else:
                            target.canvas[v].color = C
                        target.canvas[v].update()
                        target.screen.blit(target.canvas[v].image, target.canvas[v])
                    except IndexError:
                        pass
    except KeyError:
        pass
    target.working_data = False

def rect_f(target, mp, C):
    try:
        v1 = (int(mp[1]/target.cell_size) * int(list(target.canvas_size)[0]/target.cell_size)) + int(mp[0]/target.cell_size)
        for x in range(target.clipboard['width']):
            for y in range(target.clipboard['height']):
                try:
                    v2 = (y * target.clipboard['width']) + x
                    v = v1 + ((y * int(list(target.canvas_size)[0]/target.cell_size)) + x)
                    if type(C) == int:
                        target.canvas[v].color = target.toolbar.palette.colors[C]
                    else:
                        target.canvas[v].color = C
                    target.canvas[v].update()
                    target.screen.blit(target.canvas[v].image, target.canvas[v])
                except IndexError:
                    pass
    except KeyError:
        pass
    target.working_data = False

def circle(target, mp, C, mode=1):
    mx = int(mp[0]/target.cell_size)
    my = int(mp[1]/target.cell_size)
    try:
        if target.clipboard['height'] >= target.clipboard['width']:
            r = int(target.clipboard['height']/2)
        if target.clipboard['width'] > target.clipboard['height']:
            r = int(target.clipboard['width']/2)
        
        if mode == 0:
            eps = r/3.14
        else:
            eps = r
        cx = mx + int(r/2)
        cy = my + int(r/2)
        v1 = (int(mp[1]/target.cell_size) * int(list(target.canvas_size)[0]/target.cell_size)) + int(mp[0]/target.cell_size)
        for x in range(mx, r+mx):
            for y in range(my, r+my):
                v = v1 + ((y * int(list(target.canvas_size)[0]/target.cell_size)) + x)
                if abs( (x-cx)**2 + (y-cy)**2 - r**2) < eps**2:
                    try:
                        if type(C) == int:
                            target.canvas[v].color = target.toolbar.palette.colors[C]
                            target.canvas[v].update()
                            target.screen.blit(target.canvas[v].image, target.canvas[v])
                        else:
                            target.canvas[v].color = C
                            target.canvas[v].update()
                            target.screen.blit(target.canvas[v].image, target.canvas[v])
                    except IndexError:
                        pass
    except KeyError:
        pass
    target.working_data = False

def oval_e(target, mp, C):
    try:
        w = int(target.clipboard['width']/2)
        h = int(target.clipboard['height']/2)
        cx = int(mp[0]/target.cell_size) + (int(target.clipboard['width']/2))
        cy = int(mp[1]/target.cell_size) + (int(target.clipboard['height']/2))
        v1 = (int(mp[1]/target.cell_size) * int(list(target.canvas_size)[0]/target.cell_size)) + int(mp[0]/target.cell_size)
        for x in range(int(mp[0]/target.cell_size), target.clipboard['width']+int(mp[0]/target.cell_size)):
            for y in range(int(mp[1]/target.cell_size), target.clipboard['height']+int(mp[1]/target.cell_size)):
                v = v1 + ((y * int(list(target.canvas_size)[0]/target.cell_size)) + x)
                try:
                    if abs( (((x-cx)**2) / w**2) + (((y-cy)**2) / h**2) ) <= 1:
                        try:
                            if type(C) == int:
                                target.canvas[v].color = target.toolbar.palette.colors[C]
                                target.canvas[v].update()
                                target.screen.blit(target.canvas[v].image, target.canvas[v])
                            else:
                                target.canvas[v].color = C
                                target.canvas[v].update()
                                target.screen.blit(target.canvas[v].image, target.canvas[v])
                        except IndexError:
                            pass
                except ZeroDivisionError:
                    pass
    except KeyError:
        pass
    target.working_data = False

def oval_f(target, mp, C):
    try:
        w = int(target.clipboard['width']/2)
        h = int(target.clipboard['height']/2)
        cx = int(mp[0]/target.cell_size) + (int(target.clipboard['width']/2))
        cy = int(mp[1]/target.cell_size) + (int(target.clipboard['height']/2))
        v1 = (int(mp[1]/target.cell_size) * int(list(target.canvas_size)[0]/target.cell_size)) + int(mp[0]/target.cell_size)
        for x in range(int(mp[0]/target.cell_size), target.clipboard['width']+int(mp[0]/target.cell_size)):
            for y in range(int(mp[1]/target.cell_size), target.clipboard['height']+int(mp[1]/target.cell_size)):
                v = v1 + ((y * int(list(target.canvas_size)[0]/target.cell_size)) + x)
                try:
                    if abs( (((x-cx)**2) / w**2) + (((y-cy)**2) / h**2) ) <= 1:
                        try:
                            if type(C) == int:
                                target.canvas[v].color = target.toolbar.palette.colors[C]
                                target.canvas[v].update()
                                target.screen.blit(target.canvas[v].image, target.canvas[v])
                            else:
                                target.canvas[v].color = C
                                target.canvas[v].update()
                                target.screen.blit(target.canvas[v].image, target.canvas[v])
                        except IndexError:
                            pass
                except ZeroDivisionError:
                    pass
    except KeyError:
        pass
    target.working_data = False

def paste(target, mp, mode=0):
    try:
        if target.rotation == 0:
            lx = [0, target.clipboard['width'], 1]
            ly = [0, target.clipboard['height'], 1]
        if target.rotation == 90:
            lx = [target.clipboard['width']-1, -1, -1]
            ly = [0, target.clipboard['height'], 1]
        if target.rotation == 180:
            lx = [target.clipboard['width']-1, -1, -1]
            ly = [target.clipboard['height']-1, -1, -1]
        if target.rotation == 270:
            lx = [0, target.clipboard['width'], 1]
            ly = [target.clipboard['height']-1, -1, -1]

        v1 = (int(mp[1]/target.cell_size) * int(list(target.canvas_size)[0]/target.cell_size)) + int(mp[0]/target.cell_size)
        for x in range(lx[0], lx[1], lx[2]):
            for y in range(ly[0], ly[1], ly[2]):
                try:
                    v2 = (y * target.clipboard['width']) + x
                    v = v1 + ((y * int(list(target.canvas_size)[0]/target.cell_size)) + x)
                    if mode == 0:
                        target.canvas[v].color = target.clipboard['colors'][v2]
                    if mode == 1:
                        target.canvas[v].color = target.clipboard['matrix'][v2].color
                    target.canvas[v].update()
                    target.screen.blit(target.canvas[v].image, target.canvas[v])
                except IndexError:
                    pass
    except KeyError:
        pass
    target.working_data = False

def blur(target, mode=0):
    w = int(list(target.canvas_size)[0]/target.cell_size)
    h = int(list(target.canvas_size)[1]/target.cell_size)
    for y in range(0, w):
        for x in range(0, h):
            v = int((y*w)+x)
            lr = []
            lg = []
            lb = []
            if v-w >= 0 and v-w < w*h:
                lr.append(target.canvas[v-w].color[0])
                lg.append(target.canvas[v-w].color[1])
                lb.append(target.canvas[v-w].color[2])
            if v+w >= 0 and v+w < w*h:
                lr.append(target.canvas[v+w].color[0])
                lg.append(target.canvas[v+w].color[1])
                lb.append(target.canvas[v+w].color[2])
            if v-1 >= 0 and v-1 < w*h:
                lr.append(target.canvas[v-1].color[0])
                lg.append(target.canvas[v-1].color[1])
                lb.append(target.canvas[v-1].color[2])
            if v+1 >= 0 and v+1 < w*h:
                lr.append(target.canvas[v+1].color[0])
                lg.append(target.canvas[v+1].color[1])
                lb.append(target.canvas[v+1].color[2])
            R, G, B = 0, 0, 0
            for r in lr:
                R += r
            for g in lg:
                G += g
            for b in lb:
                B += b
            blend = (int(R/len(lr)), int(G/len(lg)), int(B/len(lb)))
            target.canvas[v].color = blend
            target.canvas[v].update()
            target.screen.blit(target.canvas[v].image, target.canvas[v])
    target.working_data = False

def draw(target, mp, C):
    if type(C) == int:
        for c in target.canvas:
            if c.rect.collidepoint(mp[0], mp[1]):
                c.color = target.toolbar.palette.colors[C]
                c.update()
                target.screen.blit(c.image, c)
    else:
        for c in target.canvas:
            if c.rect.collidepoint(mp[0], mp[1]):
                c.color = C
                c.update()
                target.screen.blit(c.image, c)

def dropper(target, mp):
    for c in target.canvas:
        if c.rect.collidepoint(mp[0], mp[1]):
            return c.color

def flood_fill(target, mp, C):
    ds = list(target.canvas_size)
    width = int(list(target.canvas_size)[0]/target.cell_size)
    height = int(list(target.canvas_size)[1]/target.cell_size)
    
    v = int(mp[1] / target.cell_size) * width + int(mp[0]/target.cell_size)
    
    remove = target.canvas[v].color
    if type(C) == int:
        place = target.toolbar.palette.colors[C]
    else:
        place = C

    to_set = [v]
    been_set = []

    while len(to_set) > 0:
        if target.canvas[to_set[0]].color == remove:
            if target.canvas[to_set[0]].color == remove:
                target.canvas[to_set[0]].color = place
                target.canvas[to_set[0]].update()
                target.screen.blit(target.canvas[to_set[0]].image, target.canvas[to_set[0]])
            if to_set[0] not in been_set:
                    been_set.append(to_set[0])

        vn = to_set[0] - width
        vs = to_set[0] + width
        ve = to_set[0] + 1
        vw = to_set[0] - 1


        if vn < height*width and vn >= 0:
            if int(target.canvas[vn].posy/target.cell_size) >= 0:
                if target.canvas[vn].color == remove:
                    if vn not in been_set:
                        been_set.append(vn)
                        to_set.append(vn)
        if vs < height*width and vs >= 0:
            if int(target.canvas[vs].posy/target.cell_size) < height*width:
                if target.canvas[vs].color == remove:
                    if vs not in been_set:
                        been_set.append(vs)
                        to_set.append(vs)
        if ve < height*width and ve >= 0:
            if int(target.canvas[ve].posx/target.cell_size) < width-1:
                if target.canvas[ve].color == remove:
                    if ve not in been_set:
                        been_set.append(ve)
                        to_set.append(ve)
        if vw < height*width and vw >= 0:
            if int(target.canvas[vw].posx/target.cell_size) >= 0:
                if target.canvas[vw].color == remove:
                    if vw not in been_set:
                        been_set.append(vw)
                        to_set.append(vw)
        to_set.pop(0)
    target.working_data = False
