from tkinter import Tk
from window2 import *
from db_operation import *

if __name__ == "__main__":
    database = Database()
    database.create_table()
    root = Tk()
    mainWindow = center_frame_window(root, database)
    root.mainloop()
