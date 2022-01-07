import tkinter as tk
from board import Tile,Board

window = tk.Tk()
window.title("Minesweeper")


frame_top = tk.Frame(master=window,relief=tk.RIDGE,border=5)
start_over_button = tk.Button(master=frame_top, text="Start\nOver", fg="black",bg="white")

instruct_label = tk.Label(master=frame_top, text="left: l\tright: h\tup: k\tdown: j\nflag: f\tdetonate: a", fg="black",bg="white")


start_over_button.pack(side=tk.LEFT)
instruct_label.pack(side=tk.LEFT)

frame_top.pack()


frame_board = tk.Frame(master=window,relief=tk.RIDGE,border=10,bg="white")
board = Board(window , frame_board)
board.frame_board.pack() # self.frame_board.pack()


def handle_keypress(event):
    if event.char in "lkjh":
        board.move_cursor(event.char)
    elif event.char == "f":
        board.flag_toggle()
    elif event.char == "a":
        board.detonate_tile()

def handle_start_over(event):
    global board 
    board.frame_board.destroy()
    new_frame = tk.Frame(master=window,relief=tk.RIDGE,border=10,bg="black")
    board = Board(window , new_frame)
    board.frame_board.pack()

# def handle_return(event):
#     all_labels[coords[0]][coords[1]]["bg"] = "black"
#     
# 
# window.bind('<Return>', handle_return)
window.bind("<Key>", handle_keypress)
start_over_button.bind("<Button-1>",handle_start_over)


window.mainloop()
