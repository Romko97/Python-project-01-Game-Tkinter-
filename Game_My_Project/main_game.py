from tkinter import *
import random
import time
from Sprite import *
from Coords import *

class Game:
    """Головний контролюючий клас"""
    def __init__(self):
        self.tk = Tk()  
        self.tk.title("Romans game")
        self.tk.resizable(False,False) # Фіксуємо вікно 
        self.tk.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.tk, width = 500, height = 500, highlightthickness = 0)
        self.canvas.pack()
        self.tk.update()
        self.canvas_height = 500
        self.canvas_width = 500
        self.bg = PhotoImage(file = 'background3.gif') #  задній фон
        self.canvas.create_image(0,0, image = self.bg, anchor = 'nw')
        self.sprites = []
        self.running = True
        # текст який появиться коли ви закінчете гру
        self.game_over_text = self.canvas.create_text(250,250, text='ВІТАЄМО\n    ВАС\nЗ ПЕРЕМОГОЮ :)', state='hidden')
    
    def mainloop(self):
        while True:
            if self.running:
                for sprite in self.sprites:
                    sprite.move()
            else:
                time.sleep(1)
                # Щоб вивести текст під кінець ігри
                self.canvas.itemconfig(self.game_over_text, state = 'normal')
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)


class PlatformSprite(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x,y,image=self.photo_image,anchor="nw")
        self.coordinates = Coords(x,y,x+width,y+height)

class StickFigureSprite(Sprite):
    """ Клас обєкта чоловічка """
    def __init__(self, game):
        Sprite.__init__(self, game)
        # Малюнки бігаючого чоловічка
        self.images_left = [
            PhotoImage(file="figure-L1.gif"),
            PhotoImage(file="figure-L2.gif"),
            PhotoImage(file="figure-L3.gif")
        ]
        self.images_right = [
            PhotoImage(file="figure-R1.gif"),
            PhotoImage(file="figure-R2.gif"),
            PhotoImage(file="figure-R3.gif")
        ]
        self.image = game.canvas.create_image(200,470, image = self.images_left[0], anchor='nw')
        self.x = -2
        self.y = 0
        self.current_image = 0
        self.current_image_add = 1
        self.jump_count = 0
        self.last_time = time.time()
        self.coordinates = Coords()
        game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        game.canvas.bind_all('<KeyPress-Up>', self.jump)
        game.canvas.bind_all('<KeyPress-Down>', self.stop)
    
    def turn_left(self, evt):
        """ рух в ліву сторону"""
        if self.y == 0:
            self.x = -2
        
    def turn_right(self, evt):
        """ рух в праву сторону"""
        if self.y == 0:
            self.x = 2
        
    def jump(self, evt):
        """ стрибок """
        if self.y == 0:
            self.y = -4
            self.jump_count = 0
    
    def stop(self, evt):
        """зупинити рух"""
        if self.y == 0:
            self.x = 0
    
    def animate(self):
        if self.x!=0 and self.y==0:
            if time.time()-self.last_time>0.1:
                self.last_time = time.time()
                self.current_image += self.current_image_add
                if self.current_image>=2:
                    self.current_image_add=-1
                if self.current_image<=0:
                    self.current_image_add=1
        if self.x < 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, image = self.images_left[2])
            else:
                self.game.canvas.itemconfig(self.image, image = self.images_left[self.current_image])
        elif self.x > 0:
            if self.y!= 0:
                self.game.canvas.itemconfig(self.image, image =self.images_right[2]) # BAG
            else:
                self.game.canvas.itemconfig(self.image,image = self.images_right[self.current_image])
        
    def coords(self):
        """ Визначення позиції чоловічка"""
        xy=self.game.canvas.coords(self.image)
        self.coordinates.x1 = xy[0]
        self.coordinates.y1 = xy[1]
        self.coordinates.x2 = xy[0]+27
        self.coordinates.y2 = xy[1]+30
        return self.coordinates

    def move(self):
        self.animate()
        if self.y<0:
            self.jump_count += 1
            if self.jump_count > 20:
                self.y=4
        if self.y > 0:
            self.jump_count -= 10
        co = self.coords()
        left = True
        right = True
        top = True
        bottom = True
        falling = True
        # Перевірка чи вдарився чоловічок об нижню або верхню межу полотна.
        if self.y > 0 and co.y2 >= self.game.canvas_height:
            self.y = 0 #  Якщо так  то ми зупиняємо чоловічка по осі у
            bottom = False
        elif self.y < 0 and co.y1 <= 0:
            self.y = 0
            top = False
        if self.x > 0 and co.x2 >= self.game.canvas_width: # перевірка чи не стукнувся чоловічок в правий край вікна
            self.x = 0  #  Якщо так  то ми зупиняємо чоловічка по осі х 
            right = False
        elif self.x < 0 and co.x1 <=0: # перевірка чи не стукнувся чоловічок в лівик край вікна
            self.x = 0  #  Якщо так  то ми зупиняємо чоловічка по осі х 
            left = False
        for sprite in self.game.sprites:
            if sprite == self: #  Якщо спрайт це той самий обєк пропускаємо 1 ітерацію
                continue
            sprite_co = sprite.coords()
            if top and self.y < 0 and collided_top(co, sprite_co):
                self.y = -self.y
                top = False
            if bottom and self.y > 0 and collided_bottom(self.y, co, sprite_co):
                self.y = sprite_co.y1 - co.y2
                if self.y < 0:
                    self.y = 0
                bottom = False
                top = False
            if bottom and falling and self.y == 0 and co.y2 < self.game.canvas_height\
                        and collided_bottom(1, co, sprite_co):
                falling = False
            if left and self.x < 0 and collided_left(co, sprite_co):
                self.x = 0
                left = False
                if sprite.endgame:
                    self.end(sprite) # Чоловічок торкнувся дверей викликаємо функцію "кінець"
            if right and self.x > 0 and collided_right(co, sprite_co):
                self.x = 0
                right = False
                if sprite.endgame:
                    self.end(sprite) # Чоловічок торкнувся дверей викликаємо функцію "кінець"
        if falling and bottom and self.y == 0 and co.y2 < self.game.canvas_height:
            self.y = 4  # має бути 4 для падіння 
        self.game.canvas.move(self.image, self.x, self.y)

    def end (self, sprite):
        '''Коли чоловічок торкнувся дверей вони відкриваюся
        і чоловічок зникає і двері закриваються. гра закінчена'''
        self.game.running = False
        sprite.opendoor()
        time.sleep(1)
        self.game.canvas.itemconfig(self.image, state = 'hidden')
        sprite.closedoor() # Зачиняємо двері після зникнення в них чоловічка




class DoorSprite(Sprite):
    """Клас для створення дверей. персонаж добігши до виходу зупиняє ігру."""
    def __init__(self, game,x , y, width, height):
        Sprite.__init__(self, game)
        self.closed_door = PhotoImage(file = 'door1.gif')
        self.open_door = PhotoImage(file = 'door2.gif')
        #зберігаємо індетифікатор який повертає функція creat_image в змінну image
        self.image = game.canvas.create_image(x, y, image = self.closed_door, anchor='nw')
        # Координати дверей
        self.coordinates = Coords(x, y, x + (width/2), y + height)
        self.endgame = True # ця змінна є тру поки чоловічок не торкнеться спрайту дверей
    
    def opendoor(self):
        """ зображує відчинені двері """
        self.game.canvas.itemconfig(self.image, image = self.open_door)
        self.game.tk.update_idletasks() # примусово зображує малюнок

    def closedoor(self):
        """ зображує зачинені двері """
        self.game.canvas.itemconfig(self.image, image = self.closed_door)
        self.game.tk.update_idletasks()  # примусово зображує малюнок


g = Game()
platform1 = PlatformSprite(g, PhotoImage(file="platform1.gif"),0,480,100,10)
platform2 = PlatformSprite(g, PhotoImage(file="platform1.gif"),150,440,100,10)
platform3 = PlatformSprite(g, PhotoImage(file="platform1.gif"),300,400,100,10)
platform4 = PlatformSprite(g, PhotoImage(file="platform1.gif"),300,160,100,10)
platform5 = PlatformSprite(g, PhotoImage(file="platform2.gif"),175,350,66,10)
platform6 = PlatformSprite(g, PhotoImage(file="platform2.gif"),50,300,66,10)
platform7 = PlatformSprite(g, PhotoImage(file="platform2.gif"),170,120,66,10)
platform8 = PlatformSprite(g, PhotoImage(file="platform2.gif"),45,60,66,10)
platform9 = PlatformSprite(g, PhotoImage(file="platform3.gif"),170,250,32,10)
platform10 = PlatformSprite(g, PhotoImage(file="platform3.gif"),230,200,32,10)
g.sprites.append(platform1)
g.sprites.append(platform2)
g.sprites.append(platform3)
g.sprites.append(platform4)
g.sprites.append(platform5)
g.sprites.append(platform6)
g.sprites.append(platform7) 
g.sprites.append(platform8)
g.sprites.append(platform9)
g.sprites.append(platform10)
door = DoorSprite(g,45,30,40,35)
g.sprites.append(door)
sf = StickFigureSprite(g)
g.sprites.append(sf)

g.mainloop()