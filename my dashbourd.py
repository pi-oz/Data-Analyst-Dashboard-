import tkinter as tk
from tkinter import filedialog,messagebox,ttk
import matplotlib.pyplot as plt
import pandas as pd
import io
import numpy as np
import seaborn as sns
# Backend
df=None
def show_in_bar():
    global df
    buffer=io.StringIO()
    df.info(buf=buffer)
    infoo=buffer.getvalue()
    return infoo
def open_file_print():
    global df
    try:
        file_path=filedialog.askopenfilename(filetypes=[("CSV File","*.csv")])
        df=pd.read_csv(file_path)
    except():
        messagebox.showinfo("File is not loaded!")

    if df is None:
        messagebox.showinfo("Failed","Data is not loaded!")
    else:
        column_menu['values']=list(df.columns)
        column_menu2['values']=list(df.columns)
        x_axis['values']=list(df.columns)
        y_axis['values']=list(df.columns)
        messagebox.showinfo("Succesfull","Data is loaded Succesfully!")
        show_data=f"""This is the first 5 row from your data:\n{df.head().to_string()}\n\nOther Information about data\n{show_in_bar()}"""
        output.delete("1.0","end")
        output.insert(tk.END,show_data)

# get line
def get_line(a=0):
    if a==0:
        line=column_menu.get()
        return line
    else:
        line=column_menu2.get()
        return line
def get_line_for_scatter():
    line1=x_axis.get()
    line2=y_axis.get()
    return line1,line2
# Line graph
def line():
    try:
        line=get_line()
        if df[line].dtype in ['int64','float64']:
            plt.figure(figsize=(10,10))
            plt.title(f"{line} Line chart")
            plt.xlabel("Index")
            plt.ylabel(line)
            df[line].plot()
            plt.show()
        else:
            messagebox.showinfo("Failed","The Given Column data in String")
    except Exception as e:
        messagebox.showinfo("Failed","select column")

def pie():
    line=get_line()
    try:
        if df[line].dtype in ['int64','float64']:
            df[line].plot.pie(autopct="%1.1f%%")
            plt.title(f"{line} Pie Chart",fontsize=14)
            plt.show()
        else:
            messagebox.showinfo("Failed","The given column in String")
    except Exception as e:
        messagebox.showinfo("Failed","Select column")

def hist():
    try:
        line=get_line()
        if df[line].dtype in ['int64','float64']:
            df[line].hist(bins=40)
            plt.title(f"{line} Histogram Chart")
            plt.show()
        else:
            messagebox.showinfo("Failed","The Given column in String")
    except Exception as e:
        messagebox.showinfo("Failed","Select column")

def bar():
    try:
        line=get_line()
        if df[line].dtype in ['int64','float64']:
            df[line].plot.bar()
            plt.title(f"{line} Bar Chart")
            plt.show()
        else:
            messagebox.showinfo("Failed","The Given column in String")
    except Exception as e:
        messagebox.showinfo("Failed","Select column")
    
def statics():
    try:
        line=get_line(4)
        if df[line].dtype in ['int64','float64']:
            text_box2=f"Mean:{df[line].mean()}\nMinimum:{df[line].min()}\nMax:{df[line].max()}\nSum:{df[line].sum()}\nVarience:{df[line].var()}\nStandard derivation:{df[line].std()}\n"
            text_box3=f"\nAdditional Information\nTotal Number of rows:{df[line].count()}\ndata type:{df[line].dtype}"
            output2.delete("1.0","end")
            output2.insert(tk.END,text_box2)
            output2.insert(tk.END,text_box3)
        else:
            messagebox.showinfo("Failed","The Given column  data in String")
    except Exception as e:
         messagebox.showinfo("Failed","Select column")

def scatter():
    line1,line2=get_line_for_scatter()
    try: 
        plt.figure(figsize=(10,6))
        plt.scatter(df[line1],df[line2],alpha=0.5)
        plt.title(f"Scatter plot- {line1} vs {line2}")
        plt.xlabel(line1)
        plt.ylabel(line2)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showinfo("Failed","Please select both axis values")

def coorelation():
    numeric_column=df.select_dtypes(include=[np.number])
    if len(numeric_column)<2:
        messagebox.showinfo("Failed","The given data have only one numeric column")
    else:
        plt.figure(figsize=(10,10))
        correlation=numeric_column.corr()
        sns.heatmap(correlation,annot=True,cmap="viridis")
        plt.show()

# --------------------------------------------------Front--------------------------------------------------
# ---------------------------------------------------------------------------------------------------------
root=tk.Tk()
root.title("My Dashboard")
root.geometry("1366x768")

# Theme
style = ttk.Style()
style.theme_use("alt")

# For Big Label
style.configure("Big.TLabel", font=("Arial", 40))

# Customize button
style.configure("TButton",
                background="red",
                foreground="yellow",
                padding=10)
# on hover of button
style.map("TButton",
          background=[("active", "darkgreen")])

notebook=ttk.Notebook(root)
notebook.pack(expand=True,fill="both")

# each frame is new tab
tab1=ttk.Frame(notebook)
tab2=ttk.Frame(notebook)
tab3=ttk.Frame(notebook)
#create tab
notebook.add(tab1,text="Data Loading")
notebook.add(tab2,text="Graph generater")
notebook.add(tab3,text="Statics")

# -------------------------Tab1-------------------------
# Introduction of Frame work on tab1
introduction=ttk.Label(tab1,text="Welcome to My Data Analyst Dashboard",style="Big.TLabel",padding=20)
introduction.pack(side='top',pady=20)

# frame
frame1=tk.Frame(tab1,bg="lightgrey",height=800,width=1348)
frame1.place(x=10,y=145)

# LabelFrame
lableframe0=ttk.LabelFrame(tab1,text="Data view")
lableframe0.place(x=7,y=210,height=500,width=1346)
# Buttons
load_csv=ttk.Button(tab1,text="Load CSV File",command=open_file_print).place(x=50,y=160)

# output widget
output=tk.Text(tab1,height=28,width=146, font=("Consolas", 12),wrap=tk.NONE)
output.place(x=10,y=230)

# scroll bar
scroll_y = tk.Scrollbar(tab1, orient='vertical', command=output.yview)
scroll_x = tk.Scrollbar(tab1, orient='horizontal', command=output.xview)
output.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
scroll_y.place(x=1322, y=231, height=444)
scroll_x.place(x=12, y=650, width=1336)

# --------------------------tab2-------------------------
introduction2=ttk.Label(tab2,text="Let's generate the Graphs",style="Big.TLabel",padding=15)
# Lableframe
lableframe1=ttk.LabelFrame(tab2,text="Single Column Visualization")
lableframe1.place(x=10,y=100,height=75,width=1346)
introduction2.grid(padx=30,pady=20)
column_var=tk.StringVar()
column_menu=ttk.Combobox(tab2,textvariable=column_var)
column_menu.set("Select anyone")
column_menu.place(x=50,y=130)

#different graph
line_graph=ttk.Button(tab2,text="Line Graph",command=line).place(x=214,y=120)
pie_chart=ttk.Button(tab2,text="Pie Chart",command=pie).place(x=320,y=120)
Histograph=ttk.Button(tab2,text="Histogram",command=hist).place(x=429,y=120)
Bar_graph=ttk.Button(tab2,text="Bar Graph",command=bar).place(x=535,y=120)

# lableframe
lableframe2=ttk.LabelFrame(tab2,text="Two column Visualization")
lableframe2.place(x=10,y=190,height=80,width=1346)
# combobox
x_side=tk.StringVar()
y_side=tk.StringVar()
x_axis=ttk.Combobox(tab2,textvariable=x_side)
y_axis=ttk.Combobox(tab2,textvariable=y_side)
x_axis.set("Select Anyone")
y_axis.set("Select Anyone")
x_axis.place(x=50,y=220)
y_axis.place(x=200,y=220)
scatter=ttk.Button(tab2,text="Scatter plot",command=scatter).place(x=350,y=210)
x_lable=ttk.Label(tab2,text="X Axis").place(x=100,y=245)
y_lable=ttk.Label(tab2,text="Y Axis").place(x=250,y=245)
# -------------------------tab3-------------------------
lableframe3=ttk.LabelFrame(tab3,text="Statistic & Co-relation")
lableframe3.place(x=10,y=10,height=75,width=1346)
labelframe_for_text=ttk.LabelFrame(tab3,text="Quick Summary")
labelframe_for_text.place(x=7,y=110,height=560,width=1346)
column_var2=tk.StringVar()
column_menu2=ttk.Combobox(tab3,textvariable=column_var2)
column_menu2.set("Select anyone")
column_menu2.place(x=30,y=40)
output2=tk.Text(tab3,height=33,width=167)
output2.place(x=10,y=130)
statics=ttk.Button(tab3,text="Get Statics",command=statics).place(x=180,y=29)
corr_button=ttk.Button(tab3,text="Co-relation",command=coorelation).place(x=300,y=29)

# looping the window
root.mainloop()
