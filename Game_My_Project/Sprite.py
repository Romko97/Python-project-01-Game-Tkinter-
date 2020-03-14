class Sprite:
    """ Батьківський клас елементів гри"""
    def __init__(self, game):
        self.game = game
        self.endgame = False   # позначає кінець ігри
        self.coordinates = None
    
    def move(self):
        pass

    def coords(self):
        """ повертає змінну обєкта coordinates"""
        return self.coordinates