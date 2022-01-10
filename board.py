import tkinter as tk
import numpy as np

class Tile:
    fg_colors = {0:"blue",1:"blue",2:"green",3:"red",4:"black",5:"yellow",6:"cyan",7:"green",8:"red"}

    def __init__(self, is_bomb:bool , tk_label , is_selected:bool):
        self.tk_label = tk_label # an object of type tk.Label 
        # tk_label is of central importance, when I modify it, the player sees something different too
        self.is_bomb = is_bomb # boolean variable, True if this tile is a bomb
        self.is_visible = False # True if this tile is visible to the player
        self.is_flagged = False # True if the player has flagged this tile, (flagged meaning they think it's a bomb)
        self.is_selected = is_selected  # True means that the cursor is on this tile, if the tile is selected the background color of that tile will appear differently, this is so that the player can tell which tile they are currently on
        self.touching_n = 0 # number of bombs this tile is touching, defaults to 0, gets modifed when `fill_neighbours` is called
        self.label = "" # this is the text that will be displayed when the tile is revealed (/'detonated')  
        self.bg_color = "grey90" # this is the background color of the tile
        self.fg_color = "blue" # this is the color of the self.label text to be displayed when the tile is detonated
        if self.is_bomb:
            self.fg_color = "black" # if the tile is a bomb, the foreground should be black
            self.label = "*" # and the label will be a *

    def __str__(self): # I used this for debugging purposes
        string_rep = "" + str(self.is_bomb) + " " + str(self.touching_n) + " " + self.label
        return string_rep 

    def fill_neighbours(self,neighbours): # fills the neighbourse attribute
        self.neighbours = neighbours # a list of Tile instances: the neighbouring tiles

        # if the tile is not a bomb, count how many of it's neighbours are bombs, and set it's label appropriately
        if not self.is_bomb:
            for t in neighbours:
                if t.is_bomb:
                    self.touching_n += 1
            self.fg_color = Tile.fg_colors[self.touching_n] 
            if self.touching_n == 0: 
                self.label = "" 
            else: 
                self.label = str(self.touching_n)

    # This is a helper method, once you update a tile's attributes, call this function and it will update the tk_label of the tile appropriately. Calling this function is what will change what the user sees
    def update_tk_label(self):
        # when a tile is selected, the background color is always white, this is how you know where your cursor is

        # if the tile is visible to the player, do this, doesn't matter if it's flagged 
        if self.is_visible:
            if self.is_selected and not self.is_bomb:
                self.tk_label["bg"] = "white"
            else:
                self.tk_label["bg"] = self.bg_color
            self.tk_label["fg"] = self.fg_color
            self.tk_label["text"] = self.label

        # if the tile is not visible to the player but it is flagged, display the flag and the light blue background
        elif self.is_flagged:
            if self.is_selected:
                self.tk_label["bg"] = "white"
            else:
                self.tk_label["bg"] = "light blue"
            self.tk_label["fg"] = "dark red"
            self.tk_label["text"] = "!"

        # if the tile is not visible to the player, and not flagged, don't show any text and make it grey (or white if selected)
        elif self.is_selected:
            self.tk_label["bg"] = "white"
            self.tk_label["text"] = "" 
        else: # not selected, not flagged, not visible
            self.tk_label["bg"] = "grey"
            self.tk_label["text"] = "" 

        return # this return statement is not necessary, it's just here for readability


    # when you hover over a tile you 'select' it
    def select(self):
        # when a tile is selected, i.e. when the cursor is hovering over it, update it's is_selected attribute by setting it to True, then call the update_tk_label() function so that this change will be displayed to the player
        self.is_selected = True
        self.update_tk_label() 
        return 

    # when you move on to another tile you need to unselect it
    def unselect(self):
        self.is_selected = False
        self.update_tk_label()
        return 

    def flag_toggle(self):
        if self.is_flagged == True: self.is_flagged = False
        else: self.is_flagged = True
        self.update_tk_label()
        # note: you can toggle flag even if something is already exposed, it won't do anything that the user can see becuase if a tile is visible (is_visible==True) then whether or not it's flagged is of little importance
        return 

    def detonate(self):
        if self.is_flagged and self.is_visible == False and self.is_selected:
            return False , -1 # the first arg returned tells you that it's not a bomb, the second argument is -1, this is kinda sloppy code, it's a patch to prevent the tile from being revealed in case the tile has alread been flagged, this ensures that if a tile is flagged you cannot detonate it and get a nasty surprise
       

        elif self.is_bomb:
            self.bg_color = "red"
        self.is_visible = True
        self.update_tk_label()
        
        return self.is_bomb , self.touching_n # return True if it is a bomb, also the number of neighbours touching

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

    # key press
    def flag_toggle(self):
        xc , yc = self.cursor
        self.tiles[xc][yc].flag_toggle()
        return 

    # key press
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




