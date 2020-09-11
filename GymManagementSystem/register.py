from tkinter import *
from datetime import datetime
import pandas as pd
import sqlite3 as sl

con = sl.connect('user-data.db')
with con:
	con.execute("""
				CREATE TABLE IF NOT EXISTS user (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT NOT NULL,
				pin TEXT NOT NULL,
				last_payment_date TEXT,
				payment_due TEXT,
				last_login TEXT
				);
				""")
con.close()

def register_success():
	global register_success_screen
	register_success_screen = Toplevel(screen)
	register_success_screen.title("REGISTRER")
	register_success_screen.geometry("250x100")
	Label(register_success_screen, text = "User successfully registered", fg = "green", font = ("Calibri", 12)).pack()
	Label(register_success_screen, text = "").pack()
	Button(register_success_screen, text = "OK", width = 20, height = 2, command = delete_register_success_screen).pack()

def register_empty():
	global register_empty_screen
	register_empty_screen = Toplevel(screen)
	register_empty_screen.title("REGISTRER")
	register_empty_screen.geometry("250x100")
	Label(register_empty_screen, text = "Empty entry detected", fg = "red", font = ("Calibri", 12)).pack()
	Label(register_empty_screen, text = "").pack()
	Button(register_empty_screen, text = "OK", width = 20, height = 2, command = delete_register_empty_screen).pack()

def register_name_taken():
	global name_taken_screen
	name_taken_screen = Toplevel(screen)
	name_taken_screen.title("REGISTER")
	name_taken_screen.geometry("250x100")
	Label(name_taken_screen, text = "Name already in use", fg = "red", font = ("Calibri", 12)).pack()
	Label(name_taken_screen, text = "").pack()
	Button(name_taken_screen, text = "OK", width = 20, height = 2, command = delete_name_taken_screen).pack()

def register_failed():
	global register_failed_screen
	register_failed_screen = Toplevel(screen)
	register_failed_screen.title("REGISTRER")
	register_failed_screen.geometry("250x100")
	Label(register_failed_screen, text = "Registration failed: pin does not match", fg = "red", font = ("Calibri", 12)).pack()
	Label(register_failed_screen, text = "").pack()
	Button(register_failed_screen, text = "OK", width = 20, height = 2, command = delete_register_failed_screen).pack()

def failed_pin():
	global failed_pin_screen
	failed_pin_screen = Toplevel(screen)
	failed_pin_screen.title("Pin Error")
	failed_pin_screen.geometry("250x100")
	Label(failed_pin_screen, text = "PIN must be at least 4 digits", fg = "red", font = ("Calibri", 12)).pack()
	Button(failed_pin_screen, text = "OK", command = delete_failed_pin_screen).pack()

def register_user():
	global reg_label
	reg_label = Label(screen1, text = "")
	reg_label.pack()
	name_info = name.get()
	pin_info = pin.get()
	conf_pin_info = conf_pin.get()

	con = sl.connect('user-data.db')
	c = con.cursor()

	c.execute('SELECT * FROM user WHERE name = ?', (name_info,))
	exists = c.fetchall()
	if not exists:
		if name_info and pin_info and conf_pin_info and pin_info == conf_pin_info:
			if len(pin_info) > 3 or len(conf_pin_info) > 3:
				sql = 'INSERT INTO user (name, pin) values(?, ?)'
				data = (name_info, pin_info)
				with con:
					con.execute(sql, data)
					con.commit()
				register_success()
			else:
				failed_pin()
		if not name_info or not pin_info or not conf_pin_info:
			register_empty()
		if pin_info != conf_pin_info:
			register_failed()
	else:
		register_name_taken()

	name_entry.delete(0, END)
	pin_entry.delete(0, END)
	conf_pin_entry.delete(0, END)
	con.close()

# GUI register window
def register():
	global screen1
	screen1 = Toplevel(screen)
	screen1.title("REGISTER")
	screen1.geometry("300x250")

	global name, pin, conf_pin
	global name_entry, pin_entry, conf_pin_entry
	name = StringVar()
	pin = StringVar()
	conf_pin = StringVar()

	Label(screen1, text = "Please enter details below").pack()
	Label(screen1, text = "").pack()
	Label(screen1, text = "Name").pack()
	name_entry = Entry(screen1, textvariable = name)
	name_entry.pack()
	Label(screen1, text = "Pin").pack()
	pin_entry = Entry(screen1, textvariable = pin)
	pin_entry.pack()
	Label(screen1, text = "Confirm pin").pack()
	conf_pin_entry = Entry(screen1, textvariable = conf_pin)
	conf_pin_entry.pack()
	Label(screen1, text = "").pack()
	Button(screen1, text = "Register", width = 10, height = 1, command = register_user).pack()

# functions to delete various windows
def delete_login_failed_screen():
	login_failed_screen.destroy()

def delete_login_success_screen():
	login_success_screen.destroy()
	login_screen.destroy()

def delete_register_success_screen():
	register_success_screen.destroy()
	screen1.destroy()

def delete_name_taken_screen():
	name_taken_screen.destroy()

def delete_register_empty_screen():
	register_empty_screen.destroy()

def delete_register_failed_screen():
	register_failed_screen.destroy()

def delete_success_reset_screen():
	success_reset_screen.destroy()
	screen5.destroy()

def delete_failed_pin_screen():
	failed_pin_screen.destroy()

# displays successful login screen
def login_success():
	global login_success_screen
	login_success_screen = Toplevel(screen)
	login_success_screen.title("Login successful")
	login_success_screen.geometry("250x100")
	Label(login_success_screen, text = "Login successful", fg = "green", font = ("Calibri", 12)).pack()
	Button(login_success_screen, text = "OK", width = 20, height = 2, command = delete_login_success_screen).pack()

# displays failed login screen
def login_failed():
	global login_failed_screen
	login_failed_screen = Toplevel(screen)
	login_failed_screen.title("Login failed")
	login_failed_screen.geometry("250x100")
	Label(login_failed_screen, text = "Login failed", fg = "red", font = ("Calibri", 12)).pack()
	Button(login_failed_screen, text = "OK", width = 20, height = 2, command = delete_login_failed_screen).pack()

# verify login details
def login_verify():
	global name1, pin1, dt_string
	name1 = name_verify.get()
	pin1 = pin_verify.get()
	name_entry1.delete(0, END)
	pin_entry1.delete(0, END)
	con = sl.connect('user-data.db')

	# get date/time for user login
	now = datetime.now()
	dt_string = now.strftime("%m/%d/%Y %I:%M%p")

	with con:
		c = con.cursor()
		params = (name1, pin1)
		c.execute('SELECT * FROM user WHERE name = ? AND pin = ?', params)
		if c.fetchone() is not None:
			# update user last login in database
			params = (dt_string, name1)
			c.execute('UPDATE user SET last_login = ? WHERE name = ?', params)
			login_success()
		else:
			login_failed()
	con.close()

def failed_reset():
	global failed_reset_screen
	failed_reset_screen = Toplevel(screen)
	failed_reset_screen.title("PIN Error")
	failed_reset_screen.geometry("250x100")
	Label(failed_reset_screen, text = "PIN reset failed", fg = "red", font = ("Calibri", 12)).pack()
	Button(failed_reset_screen, text = "OK", width = 20, height = 2, command = delete_failed_reset_screen).pack()

def success_reset():
	global success_reset_screen
	success_reset_screen = Toplevel(screen)
	success_reset_screen.title("PIN Reset")
	success_reset_screen.geometry("250x100")
	Label(success_reset_screen, text = "PIN reset successful", fg = "greeb", font = ("Calibri", 12)).pack()
	Button(success_reset_screen, text = "OK", width = 20, height = 2, command = delete_success_reset_screen).pack()

# function call to update user PIN in database
def update_pin():
	con = sl.connect('user-data.db')
	c = con.cursor()
	r_pin = r_pin_entry.get()
	r_conf_pin = r_conf_pin_entry.get()
	pin_label = Label(screen5, text = "")
	pin_label.pack()

	if r_pin == r_conf_pin:
		sql = 'UPDATE user SET pin = ? WHERE name = ?'
		params = (r_pin, name1)
		c.execute(sql, params)
		con.commit()
		success_reset()
	else:
		failed_reset()
	con.close()

# allows user to reset pin
def reset_pin():
	global screen5
	global r_pin, r_conf_pin, r_pin_entry, r_conf_pin_entry
	r_pin = StringVar()
	r_conf_pin = StringVar()

	screen5 = Toplevel(screen)
	screen5.title("RESET PIN")
	screen5.geometry("250x200")
	Label(screen5, text = "RESET PIN").pack()
	Label(screen5, text = "PIN:").pack()
	r_pin_entry = Entry(screen5, textvariable = r_pin)
	r_pin_entry.pack()
	Label(screen5, text = "").pack()
	Label(screen5, text = "CONFIRM PIN:").pack()
	r_conf_pin_entry = Entry(screen5, textvariable = r_conf_pin)
	r_conf_pin_entry.pack()
	Label(screen5, text = "").pack()
	Button(screen5, text = "UPDATE", command = update_pin).pack()

def login():
	global login_screen
	login_screen = Toplevel(screen)
	login_screen.title("Login")
	login_screen.geometry("300x250")

	Label(login_screen, text = "Please enter details below to login").pack()
	Label(login_screen, text = "").pack()
	global name_verify, pin_verify, name_entry1, pin_entry1
	name_verify = StringVar()
	pin_verify = StringVar()

	Label(login_screen, text = "Name").pack()
	name_entry1 = Entry(login_screen, textvariable = name_verify)
	name_entry1.pack()
	Label(login_screen, text = "").pack()
	Label(login_screen, text = "Pin").pack()
	pin_entry1 = Entry(login_screen, textvariable = pin_verify)
	pin_entry1.pack()
	Label(login_screen, text = "").pack()
	Button(login_screen, text = "Login", width = 20, height = 1, command = login_verify).pack()
	Label(login_screen, text = "").pack()
	Button(login_screen, text = "Reset Pin", width = 20, height = 1, command = reset_pin).pack()


def main_screen():
	global screen, reg_label
	screen = Tk()
	screen.geometry("300x250")
	screen.title("Hanley's Gym")
	Label(text = "Hanley's Gym", bg = "grey", width = "300", height = "2", font = ("Calibri", 13)).pack()
	Label(text = "").pack()
	Button(text = "LOGIN", height = "2", width = "30", command = login).pack()
	Label(text = "").pack()
	Button(text = "REGISTER", height = "2", width = "30", command = register).pack()

	screen.mainloop()

main_screen()