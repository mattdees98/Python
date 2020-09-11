# simple calculator app
# Matthew Dees
# March 19, 2020
# Last updated July 20, 2020

# import statements
import tkinter as tk
from tkinter import font as tkFont
import math as m

# create tkinter object
root = tk.Tk()
root.title("MD - Simple Calculator")
root.geometry("400x400")
root.minsize(350, 400)

# define font
font = tkFont.Font(family = 'Helvetica', size = 20, weight = 'bold')

# create entry row
e = tk.Entry(root, width = 60, borderwidth = 5, font = font)
e.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 10, sticky = tk.E + tk.W + tk.N + tk.S)

# button clicks to add numbers
def button_click(number):
	current = e.get()
	e.delete(0, tk.END)
	e.insert(0, str(current) + str(number))

# clear button
def button_clear():
	e.delete(0, tk.END)

# add button
def button_add():
	# pull first number
	num1 = e.get()
	global n1
	global math
	math = "addition"
	n1 = int(num1)
	e.delete(0, tk.END)

# subtract button
def button_sub():
	# pull first number
	num1 = e.get()
	global n1
	global math
	math = "subtraction"
	n1 = int(num1)
	e.delete(0, tk.END)

# multiply button
def button_mult():
	# pull first number
	num1 = e.get()
	global n1
	global math
	math = "multiplication"
	n1 = int(num1)
	e.delete(0, tk.END)

# division button
def button_div():
	# pull first number
	num1 = e.get()
	global n1
	global math
	math = "division"
	n1 = int(num1)
	e.delete(0, tk.END)

def button_square():
	num1 = e.get()
	global n1
	global math
	math = "square"
	n1 = int(num1)
	e.delete(0, tk.END)

def button_sqrt():
	num1 = e.get()
	global n1
	global math
	math = "sqrt"
	n1 = int(num1)
	sqrt_num = m.sqrt(n1)
	e.delete(0, tk.END)
	e.insert(0, float(sqrt_num))

#add the numbers together
def button_equal():
	num2 = e.get()
	e.delete(0, tk.END)

	# if else statement for which type of math is being done
	if math == "addition":
		e.insert(0, n1 + int(num2))

	if math == "subtraction":
		e.insert(0, n1 - int(num2))

	if math == "multiplication":
		e.insert(0, n1 * int(num2))

	if math == "division":
		e.insert(0, float(n1) / float(num2))

	if math == "square":
		sq_num = n1 ** int(num2)
		e.insert(0, int(sq_num))


# add number buttons
button_1 = tk.Button(root, text = "1", font = font, padx = 5, pady = 5, command = lambda: button_click(1))
button_2 = tk.Button(root, text = "2", font = font, padx = 5, pady = 5, command = lambda: button_click(2))
button_3 = tk.Button(root, text = "3", font = font, padx = 5, pady = 5, command = lambda: button_click(3))
button_4 = tk.Button(root, text = "4", font = font, padx = 5, pady = 5, command = lambda: button_click(4))
button_5 = tk.Button(root, text = "5", font = font, padx = 5, pady = 5, command = lambda: button_click(5))
button_6 = tk.Button(root, text = "6", font = font, padx = 5, pady = 5, command = lambda: button_click(6))
button_7 = tk.Button(root, text = "7", font = font, padx = 5, pady = 5, command = lambda: button_click(7))
button_8 = tk.Button(root, text = "8", font = font, padx = 5, pady = 5, command = lambda: button_click(8))
button_9 = tk.Button(root, text = "9", font = font, padx = 5, pady = 5, command = lambda: button_click(9))
button_0 = tk.Button(root, text = "0", font = font, padx = 5, pady = 5, command = lambda: button_click(0))

# add function buttons
button_add = tk.Button(root, text = "+", font = font, padx = 5, pady = 5, command = button_add)
button_sub = tk.Button(root, text = "-", font = font, padx = 5, pady = 5, command = button_sub)
button_mult = tk.Button(root, text = "*", font = font, padx = 5, pady = 5, command = button_mult)
button_div = tk.Button(root, text = "/", font = font, padx = 5, pady = 5, command = button_div)
button_equal = tk.Button(root, text = "=", font = font, padx = 5, pady = 5, command = button_equal)
button_clear = tk.Button(root, text = "CLEAR", font = font, padx = 5, pady = 5, command = button_clear)
button_square = tk.Button(root, text = "x^", font = font, padx = 5, pady = 5, command = button_square)
button_sqrt = tk.Button(root, text = "√", font = font, padx = 5, pady = 5, command = button_sqrt)

# put buttons on screen
button_1.grid(row = 1, column = 0, sticky = tk.E + tk.W + tk.N + tk.S)
button_2.grid(row = 1, column = 1, sticky = tk.E + tk.W + tk.N + tk.S)
button_3.grid(row = 1, column = 2, sticky = tk.E + tk.W + tk.N + tk.S)
button_4.grid(row = 2, column = 0, sticky = tk.E + tk.W + tk.N + tk.S)
button_5.grid(row = 2, column = 1, sticky = tk.E + tk.W + tk.N + tk.S)
button_6.grid(row = 2, column = 2, sticky = tk.E + tk.W + tk.N + tk.S)
button_7.grid(row = 3, column = 0, sticky = tk.E + tk.W + tk.N + tk.S)
button_8.grid(row = 3, column = 1, sticky = tk.E + tk.W + tk.N + tk.S)
button_9.grid(row = 3, column = 2, sticky = tk.E + tk.W + tk.N + tk.S)
button_0.grid(row = 4, column = 0, sticky = tk.E + tk.W + tk.N + tk.S)

# add weights to columns/rows for grid
root.grid_columnconfigure(0, weight = 1)
root.grid_columnconfigure(1, weight = 1)
root.grid_columnconfigure(2, weight = 1)
root.grid_rowconfigure(0, weight = 1)
root.grid_rowconfigure(1, weight = 1)
root.grid_rowconfigure(2, weight = 1)
root.grid_rowconfigure(3, weight = 1)
root.grid_rowconfigure(4, weight = 1)
root.grid_rowconfigure(5, weight = 1)
root.grid_rowconfigure(6, weight = 1)
root.grid_rowconfigure(7, weight = 1)

# align buttons in grid
button_clear.grid(row = 4, column = 1, columnspan = 2, sticky = tk.E + tk.W + tk.N + tk.S)
button_add.grid(row = 5, column = 0, sticky = tk.E + tk.W + tk.N + tk.S)
button_equal.grid(row = 7, column = 0, columnspan = 3, rowspan = 2, sticky = tk.E + tk.W + tk.N + tk.S)
button_sub.grid(row = 5, column = 1, sticky = tk.E + tk.W + tk.N + tk.S)
button_mult.grid(row = 5, column = 2, sticky = tk.E + tk.W + tk.N + tk.S)
button_div.grid(row = 6, column = 0, sticky = tk.E + tk.W + tk.N + tk.S)
button_square.grid(row = 6, column = 1, sticky = tk.E + tk.W + tk.N + tk.S)
button_sqrt.grid(row = 6, column = 2, sticky = tk.E + tk.W + tk.N + tk.S)

root.mainloop()