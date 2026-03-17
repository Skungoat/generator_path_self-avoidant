from position import Position
from random import shuffle

class Reseau:
    def __init__(self, n: int):
        
        self.len = n
        self.reset_tab()
    
    def reset_tab(self):
       
        self.tab = [[-1 for _ in range(self.len)] for _ in range(self.len)]
    
    def get_pos_tab(self, i: int, j: int):
        return self.tab[i][j]

    def set_pos(self, val: int, i: int, j: int):
        self.tab[i][j] = val

    def move_smart(self, i: int, j: int, start_pos: tuple, nb_pas: int):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        shuffle(directions)
        
        if nb_pas > 2: 
            for di, dj in directions:
                if (i + di, j + dj) == start_pos:
                    return i + di, j + dj, "BOUCLE" 
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.len and 0 <= nj < self.len:
                if self.get_pos_tab(ni, nj) == -1:
                    self.set_pos(0, ni, nj)
                    return ni, nj, "AVANCE"
        
        return i, j, "BLOQUÉ"