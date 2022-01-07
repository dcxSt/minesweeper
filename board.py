import tkinter as tk
import numpy as np

class Tile:
    fg_colors = {0:"blue",1:"blue",2:"green",3:"red",4:"black",5:"yellow",6:"cyan",7:"green",8:"red"}

    def __init__(self, is_bomb:bool , tk_label , is_selected:bool):
        self.tk_label = tk_label # an object of type tk_label
        self.is_bomb = is_bomb
        self.is_visible = False
        self.is_flagged = False
        self.is_selected = is_selected
        self.touching_n = 0 # number of bombs this tile is touching
        self.label = ""
        self.bg_color = "grey90"
        self.fg_color = "blue"
        if self.is_bomb:
            self.bg_color = "grey90"
            self.fg_color = "black"
            self.label = "*"

    def __str__(self):
        string_rep = "" + str(self.is_bomb) + " " + str(self.touching_n) + " " + self.label
        return string_rep

    def fill_neighbours(self,neighbours): # fills the neighbourse attribute
        self.neighbours = neighbours # a list of tile objects, the neighbouring tiles
        if not self.is_bomb:
            for t in neighbours:
                if t.is_bomb:
                    self.touching_n += 1
            self.fg_color = Tile.fg_colors[self.touching_n]
            if self.touching_n == 0:
                self.label = ""
            else: 
                self.label = str(self.touching_n)

    def update_tk_label(self):
        if self.is_visible:
            if self.is_selected and not self.is_bomb:
                self.tk_label["bg"] = "white"
            else:
                self.tk_label["bg"] = self.bg_color
            self.tk_label["fg"] = self.fg_color
            self.tk_label["text"] = self.label
        elif self.is_flagged:
            if self.is_selected:
                self.tk_label["bg"] = "white"
            else:
                self.tk_label["bg"] = "light blue"
            self.tk_label["fg"] = "dark red"
            self.tk_label["text"] = "!"
        elif self.is_selected:
            self.tk_label["bg"] = "white"
            self.tk_label["text"] = "" 
        else: # not selected, not flagged, not visible
            self.tk_label["bg"] = "grey"
            self.tk_label["text"] = "" 

        return 


    # when you hover over a tile you 'select' it
    def select(self):
        self.is_selected = True
        self.update_tk_label() 
        return 

    # when you move on to another tile you need to unselect it
    def unselect(self):
        # if self.is_selected == False: 
        #     raise Exception("Logic error")
        self.is_selected = False
        self.update_tk_label()
        return 

    def flag_toggle(self):
        if self.is_flagged == True: self.is_flagged = False
        else: self.is_flagged = True
        self.update_tk_label()
        # note: you can toggle flag even if something is already exposed, it won't do anything
        return 

    def detonate(self):
        if self.is_flagged and self.is_visible == False and self.is_selected:
            print("yay") # debug
            return False , -1
        

        elif self.is_bomb:
            self.bg_color = "red"
        self.is_visible = True
        self.update_tk_label()
        
        return self.is_bomb , self.touching_n # return True if it is a bomb, also the n of neighbours touching

    def reveal(self): # this method is called on every tile if a bomb is detonated
        self.is_visible = True
        self.update_tk_label() 
        return 




        

class Board:
    def __init__(self, window, frame_board, x=70, y=29, n_bombs=326):
        print("initializing a board with {} columns and {} rows".format(x,y)) # Trace

        ############

        self.x , self.y = x , y # dimensions of the grid
        self.n_bombs = n_bombs
        self.cursor = [0,0]
        self.idxs = np.array([(i % x, i // x) for i in range(y*x)])
        self.bomb_places = np.random.choice(len(self.idxs), size=n_bombs, replace=False)
        self.bomb_idxs = self.idxs[self.bomb_places] 
        
        # generate the tiles
        self.tiles = [["" for i in range(y)] for j in range(x)]

        self.frame_board = frame_board # tk.Frame(master=window,relief=tk.RIDGE,border=10,bg="white")

        for place_idx, (xc,yc) in enumerate(self.idxs):
            frame = tk.Frame(
                master=self.frame_board,
                relief=tk.RIDGE,
                border=1
            )
            frame.grid(row=yc,column=xc)

            is_selected = False 
            if xc == 0 and yc == 0:
                is_selected = True
                label = tk.Label(master=frame, text="",width=1,height=1, fg="white",bg="white")
            else:
                label = tk.Label(master=frame, text="", width=1,height=1,fg="white", bg="grey")
            label.pack() # add the label to the tk frame

            if place_idx in self.bomb_places:
                self.tiles[xc][yc] = Tile(is_bomb = True , tk_label = label , is_selected = is_selected)
            else:
                self.tiles[xc][yc] = Tile(is_bomb = False , tk_label = label , is_selected = is_selected)



        ############

        # loop through once more to fill neighbour information
        for xc, col in enumerate(self.tiles):
            for yc, tile in enumerate(col):
                neigh_minx = max(0,xc - 1)
                neigh_maxx = min(x,xc + 2)
                neigh_miny = max(0,yc - 1)
                neigh_maxy = min(y,yc + 2)

                neighbours = []
                for xn in range(neigh_minx , neigh_maxx):
                    for yn in range(neigh_miny , neigh_maxy):
                        if xn != xc or yn != yc:
                            neighbours.append(self.tiles[xn][yn])
                tile.fill_neighbours(neighbours)


        return 

        # Board.display_board()
        # self.debug_display_board()
        # self.debug()

    # key presses
    def move_cursor(self,key_pressed):
        if key_pressed not in "awdsilkjh" or len(key_pressed)!=1: raise Exception("key press not valid, logic error")
        if key_pressed in "wk" and self.cursor[1] > 0:
            xc,yc = self.cursor
            self.tiles[xc][yc].unselect()
            self.cursor[1] -= 1
            xc,yc = self.cursor
            self.tiles[xc][yc].select()
        elif key_pressed in "sj" and self.cursor[1] < self.y - 1:
            xc,yc = self.cursor
            self.tiles[xc][yc].unselect()
            self.cursor[1] += 1
            xc,yc = self.cursor
            self.tiles[xc][yc].select()
        elif key_pressed in "dl" and self.cursor[0] < self.x - 1:
            xc,yc = self.cursor
            self.tiles[xc][yc].unselect()
            self.cursor[0] += 1
            xc,yc = self.cursor
            self.tiles[xc][yc].select()
        elif key_pressed in "ah" and self.cursor[0] > 0:
            xc,yc = self.cursor
            self.tiles[xc][yc].unselect()
            self.cursor[0] -= 1
            xc,yc = self.cursor
            self.tiles[xc][yc].select()

        return 

    def flag_toggle(self):
        xc , yc = self.cursor
        self.tiles[xc][yc].flag_toggle()
        return 

    def detonate_tile(self , tile = None):
        if tile == None:
            xc,yc = self.cursor
            tile = self.tiles[xc][yc] 
        is_bomb , touching_n = tile.detonate() 

        if is_bomb:
            # game over, reveal all the tiles
            for col in self.tiles:
                for tile in col:
                    tile.reveal()

        elif touching_n == 0:
            # if none of the neighbours are bombs
            # recursive call, be weary!
            for neighbour in tile.neighbours:
                if not neighbour.is_visible:
                    self.detonate_tile(neighbour)
        return 



if __name__ == "__main__":
    board = Board() # test init




