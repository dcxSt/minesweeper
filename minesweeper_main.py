import tkinter as tk
from board import Tile,Board


window = tk.Tk() # Create a tkinter window
window.title("Minesweeper") 


frame_top = tk.Frame(master=window,relief=tk.RIDGE,border=5) # add a frame to the top
start_over_button = tk.Button(master=frame_top, text="Start\nOver", fg="black",bg="white") # initiate the start over button

instruct_label = tk.Label(master=frame_top, text="left: l\tright: h\tup: k\tdown: j\nflag: f\tdetonate: a", fg="black",bg="white") # this label tells the player what the commands are to move


# pack the start over button and the instruction label into the top frame "frame_top" from the left
start_over_button.pack(side=tk.LEFT)
instruct_label.pack(side=tk.LEFT)

frame_top.pack() # pack the top frame into the top of the tkinter window 


# here is where the board is initiated and displayed
frame_board = tk.Frame(master=window,relief=tk.RIDGE,border=10,bg="white") # initiate the frame for the board
board = Board(window , frame_board) # pass the board's frame and the main tkinter window as arguments to the class Board's __init__ method to instantiate a new instance of Board
board.frame_board.pack() # once the frame of the board has been setup, pack it 


# handle keypresses, this is for moving the cursor "lkjh", for adding / removing flags "f", and detonating tiles "a"
def handle_keypress(event):
    if event.char in "lkjh":
        board.move_cursor(event.char)
    elif event.char == "f":
        board.flag_toggle()
    elif event.char == "a":
        board.detonate_tile()
    else:
        print("Invalid keypress.")

# this is a method that is called when the user clicks the `start over` button
def handle_start_over(event):
    global board # this tells python that we are modifying the board variable which is in the global namespace
    board.frame_board.destroy() # destroy the tkinter frame for the board
    new_frame = tk.Frame(master=window,relief=tk.RIDGE,border=10,bg="black") # create a new tkinter frame to replace it 
    board = Board(window , new_frame) # initialize a new Board instance and get the variable board to point to it, instead of the last one
    board.frame_board.pack() # pack the new frame into the tkinter window 


window.bind("<Key>", handle_keypress) # handle keypresses
start_over_button.bind("<Button-1>",handle_start_over) # handle `start over` button clicks

window.mainloop() # tells python to run the tkinter *event loop* which listens for events (like keypresses and clicks)  



