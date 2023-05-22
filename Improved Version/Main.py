import tkinter as tk
from tkinter import *
from tkinter import ttk
from ctypes import windll
import tkinter.messagebox as mb
import pandas as pd
import Algorithms as Alg
import LineInformation as Li

class MainWindow:

    def __init__(self, master):
        self.master = master
        self.master.title("London Underground Navigation System")
        self.master.geometry("630x550")
        self.frame = Frame(self.master, bg='grey69')
        self.frame.pack()


        self.label_title = Label(self.frame, text="London Underground Navigation System", bg="azure", width="350",
                                 relief="ridge", height="5", bd=5, font=("Helvetica", 13, "bold")).pack(pady=20)        

        # Loads excel document data
        self.data = pd.read_excel("London Underground Data.xlsx", header=None)
        self.df = pd.DataFrame(self.data)
        
        # Separation here of Lines, Stations and Time
        columns_needed = [1, 2, 3, 0]
        self.fil_df = self.df[self.df[3] > 0] # data frame with source, destination, weight
        self.n_df = self.df[self.df.isna().any(axis=1)] # data frame with only nodes (stations)
        self.edges = []
        self.sped_up_edge = []
        self.weight = {}
        for index, row in self.fil_df.iterrows(): # Convert edges to array format
            self.edges.append([row[column] for column in columns_needed])
            self.weight[(row[1], row[2])] = row[3]
            self.weight[(row[2], row[1])] = row[3]

        self.sped_up_edge = self.edges.copy()
        for node in self.sped_up_edge:
            if node[3] == "Bakerloo":
                node[2] = node[2]/2

        
        self.allNodes = sorted(set([node for node in self.n_df[1]]))

        self.label_start = Label(self.frame, text="Starting Station").pack()
        self.input_start = ttk.Combobox(self.frame, values=self.allNodes, width="30",
                                        state="readonly")
        self.input_start.pack(pady=10)
        self.label_finish = Label(self.frame, text="Target Station").pack()
        self.input_finish = ttk.Combobox(self.frame, values=self.allNodes, width="30",
                                         state="readonly")
        self.input_finish.pack(pady=10)

        # Declare input variables for time.
        self.time_hour = StringVar()
        self.time_hour.set(0)
        self.time_min = StringVar()
        self.time_min.set(0)
        # Time (hours and minutes) label and entry boxes.
        self.label_hour = Label(self.frame, text="Time (Hours: 00-24)").pack()
        self.text_hour = Entry(self.frame, textvariable=self.time_hour, width="15", bd=5)
        self.text_hour.pack(padx=10, pady=10)
        self.label_min = Label(self.frame, text="Time (Minutes: 00-60)").pack()
        self.text_min = Entry(self.frame, textvariable=self.time_min, width="15", bd=5)
        self.text_min.pack(padx=10, pady=10)

        # Continue and Exit button on the front page.
        self.process_button = Button(self.frame, text="Get Directions", height="2", width="15", bd=3, bg="grey",
                                     font=("Helvetica", 12, "bold"), command=self.entry_verification).pack(pady=10)
        self.exit_button = Button(self.frame, text="EXIT", height="2", width="10", bd=3, bg="grey",
                                  font=("Helvetica", 10, "bold"), command=self.exit_window).pack()
        
    def entry_verification(self):
        speed_up = False
        # Checks whether the input for the hour and minutes are valid.
        if str.isnumeric(self.text_hour.get()) and str.isnumeric(self.text_min.get()):
            if 0 <= int(self.text_hour.get()) <= 24 and 0 <= int(self.text_min.get()) <= 60:
                if 9 <= int(self.text_hour.get()) < 16 or 19 <= int(self.text_hour.get()) < 24:
                    # To use the graph with the updated bakerloo line speed
                    speed_up = True
                if len(self.input_start.get()) == 0 or len(self.input_finish.get()) == 0:
                    mb.showinfo("Missing Arguments", "Please ensure that all entries are filled and entered correctly.")
                elif self.input_start.get() == self.input_finish.get():
                    mb.showinfo("Error?", "The entries for the starting and finishing stations are both the same. "
                                "You're already there!")
                else:
                    if self.input_start.get() and self.input_finish.get() in self.allNodes:
                        if speed_up:
                            self.initialise_results(self.sped_up_edge)
                        else:
                            self.initialise_results(self.edges)
            else:
                mb.showerror("Error!", "Invalid time parameters.")
        else:
            mb.showerror("Error!", "Time MUST contain postivie numberic numbers only withing the specified region.")



    # Calls the Dijkstra's path finding function, stores the values and parses it into the results table.
    def initialise_results(self, graph_edges):
        # Initialising the graph in advanced for Dijkstra's algorithm to traverse.
        graph = Alg.Graph(graph_edges, self.n_df, self.weight)
        shortest_path, maxTime, distance = graph.dijkstraPath(self.input_start.get(),
                                                              self.input_finish.get())
        self.master.destroy()
        distance.append("")
        Results(Tk(), shortest_path, maxTime, distance)

    # Method that opens a confirmation box and then terminates the program if yes.
    def exit_window(self):
        exit_ = mb.askyesno("Exit Warning!", "Are you sure you want to quit?")
        if exit_:
            self.master.destroy()

class Results:
    def __init__(self, master, shortest_path, maxTime, distance):
        self.master = master
        self.master.title("Navigation System Results")
        self.master.geometry("900x500")
        self.master.config(bg='grey69')
        self.frame = Frame(self.master, bg='grey69')
        self.frame.pack()

        # Creates a Treeview/Table that can display the Stations, Train Lines, Travel Time Between Stations and the
        # Total Time (Including the Idle time for passenger (dis)embarking).
        tl_cols1 = ("Station", "Train Line", "Travel Time Between Station", "Total Time (Idle Time Included)")
        self.box = ttk.Treeview(self.frame, columns=tl_cols1, show="headings")
        for col in tl_cols1:
            self.box.heading(col, text=col)
            self.box.column(col, anchor=CENTER)
            self.box.pack(fill=BOTH)
        
        for i in range(len(shortest_path)):
            self.box.insert('', 'end', values=(shortest_path[i][0], shortest_path[i][1], 
                                                distance[i], shortest_path[i][2]))

        # Journey summary label.
        self.summary_label = Label(self.frame, text="Journey Summary - Scroll down if the list is incomplete.").pack()
        self.summary1 = Text(self.frame, height=10, width=90)
        self.summary1.pack()

        # Stopping point for the line change
        shortest_path.append([' ', ' ', 0])

        # Output journey Summary here
        start, end = 0, 0
        while start < len(shortest_path)-1:
            end += 1
            if shortest_path[end-1][1] != shortest_path[end][1]:
                self.summary1.insert(END, shortest_path[start][1] + ': ' + shortest_path[start][0] + ' to ' + shortest_path[end-1][0])
                start = end
                if end != len(shortest_path)-1:
                    self.summary1.insert(END, '\n\n-- From station: ' + shortest_path[end-1][0] + ', change to the ' + shortest_path[end][1] + ' line --\n\n')
        self.summary1.insert(END, '\n\nYou have made it to your destination *' + shortest_path[end-1][0] + '*')
        self.summary1.config(state=DISABLED)

        # Displays the final distance at the bottom of the window.
        self.label_distance = Label(self.frame, text="Total Journey Time: " + str(maxTime) + " Minutes").pack()

        # Buttons to exit or return to the main window.
        self.back = Button(self.frame, text="Back", height="2", width="5", bd=2, font=("Helvetica", 8, "bold"),
                           bg='grey', command=self.back_main).pack(side=LEFT, fill=X, anchor=W, expand=YES)
        self.exit = Button(self.frame, text="Exit", height="2", width="5", bd=2, font=("Helvetica", 8, "bold"),
                           bg="grey", command=self.exit_window).pack(side=LEFT, fill=X, anchor=W, expand=YES)
    
    # Method to initialise the main window and destroy the current results table.
    def back_main(self):
        self.master.destroy()
        MainWindow(Tk())

    # Method that opens a confirmation box and then terminates the program if yes.
    def exit_window(self):
        exit_ = mb.askyesno("Exit Warning!", "Are you sure you want to quit?")
        if exit_:
            self.master.destroy()

class Information:
    def __init__(self, master):
        pass

if __name__ == '__main__':
    root = Tk()
    MainWindow(root)
    root.mainloop()
