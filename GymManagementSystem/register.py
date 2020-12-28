# import statements
import sys, os
from tkinter import *
from datetime import datetime
import sqlite3 as sl
import tkinter as tk

def resource_path(relative_path):
     if hasattr(sys, '_MEIPASS'):
         return os.path.join(sys._MEIPASS, relative_path)
     return os.path.join(os.path.abspath("."), relative_path)

# initialize connection and database
con = sl.connect('user-data.db')
with con:
	con.execute("""
				CREATE TABLE IF NOT EXISTS user (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				l_name TEXT NOT NULL,
				f_name TEXT NOT NULL,
				name TEXT NOT NULL,
				pin TEXT NOT NULL,
				address TEXT,
				phone TEXT,
				last_payment_date TEXT,
				payment_due TEXT,
				last_login TEXT,
				date_reg TEXT
				);
				""")
con.close()

def calendar():
	top = tk.Toplevel(screen)
	cal = DateEntry(top, width = 12, background = 'darkblue')

# display a success screen when payment information is updated
def payment_update_successful():
	global payment_update_success_screen
	payment_update_success_screen = Toplevel(screen)
	payment_update_success_screen.title("Update Success")
	payment_update_success_screen.geometry("250x100")
	payment_update_success_screen.iconphoto(False, photo)
	Label(payment_update_success_screen, text = "Payment successfully updated", fg = "green", font = ("Calibri", 12)).pack()
	Label(payment_update_success_screen, text = "").pack()
	Button(payment_update_success_screen, text = "OK", width = 20, height = 2, command = delete_payment_success_screen).pack()

# delete successful payment screen on button click
def delete_payment_success_screen():
	payment_update_success_screen.destroy()

# add a month to user payment information
def add_month():
	now = datetime.now()
	dt_string = now.strftime("%m/%d/%Y")
	dt_month = now.strftime("%m")
	dt_day = now.strftime("%d")
	dt_year = now.strftime("%Y")
	dt_month = int(dt_month) + 1

	if dt_month == 13:
		dt_month = 1
		dt_year = int(dt_year) + 1
	else:
		dt_month = str(dt_month)
		next_payment_date = str(dt_month + '/' + dt_day + '/' + dt_year)

	con = sl.connect('user-data.db')
	c = con.cursor()

	dt_string = str(dt_string)
	c.execute('UPDATE user SET last_payment_date = ? WHERE f_name = ? AND l_name = ?', (dt_string, f_name, l_name))
	c.execute('UPDATE user SET payment_due = ? WHERE f_name = ? AND l_name = ?', (next_payment_date, f_name, l_name))
	con.commit()
	con.close()
	payment_update_successful()

# GUI to add a custom amount of months to user payment information
def add_custom():
	global custom_window, months, month_entry
	months = StringVar()
	custom_window = Toplevel(screen)
	custom_window.title("Entry")
	custom_window.geometry("250x120")
	custom_window.iconphoto(False, photo)

	custom_window.grid_columnconfigure(0, weight = 1)
	custom_window.grid_columnconfigure(1, weight = 1)

	Label(custom_window, text = "Enter the amount of months", padx = 5, pady = 5, font = ("Calibri", 12)).grid(row = 0, columnspan = 2, sticky = NSEW)
	month_entry = Entry(custom_window, textvariable = months)
	month_entry.grid(row = 1, columnspan = 2, sticky = NSEW)
	Label(custom_window, text = "").grid(row = 3)
	Button(custom_window, text = "ENTER", width = 20, height = 2, command = add_custom_eq).grid(row = 4, columnspan = 3, sticky = NSEW)

# math equations for adding a custom amount of months to user payment information
def add_custom_eq():
	months = month_entry.get()
	print(months)
	custom_window.destroy()

	now = datetime.now()
	dt_string = now.strftime("%m/%d/%Y")
	dt_month = now.strftime("%m")
	dt_day = now.strftime("%d")
	dt_year = now.strftime("%Y")
	print(dt_month)
	dt_month = int(dt_month)
	i = 0
	while i <= int(months):
		if dt_month == 12:
			dt_month = 1
			dt_year = int(dt_year) + 1
			print(dt_month)
		else:
			dt_month = dt_month + 1
			print(dt_month)
		i += 1

	dt_month = str(dt_month)
	dt_string = str(dt_string)
	dt_year = str(dt_year)
	next_payment_date = str(dt_month + '/' + dt_day + '/' + dt_year)

	con = sl.connect('user-data.db')
	c = con.cursor()
	c.execute('UPDATE user SET last_payment_date = ? WHERE f_name = ? AND l_name = ?', (dt_string, f_name, l_name))
	c.execute('UPDATE user SET payment_due = ? WHERE f_name = ? AND l_name = ?', (next_payment_date, f_name, l_name))
	con.commit()
	con.close()
	payment_update_successful()

# admin panel GUI to update payment information
def update_payment_info_screen():
	global payment_info_screen, first_name, last_name, payment_due

	payment_info_screen = Toplevel(screen)
	payment_info_screen.title("Update Payment Info")
	payment_info_screen.geometry("400x100")
	payment_info_screen.iconphoto(False, photo)

	payment_info_screen.grid_columnconfigure(0, weight = 1)
	payment_info_screen.grid_columnconfigure(1, weight = 1)
	payment_info_screen.grid_rowconfigure(1, weight = 1)

	Label(payment_info_screen, text = "Update Payment Info", font = ("Calibri", 16)).grid(row = 0, columnspan = 2, sticky = NSEW)
	Button(payment_info_screen, text = "ADD A MONTH", command = add_month).grid(row = 1, column = 0, rowspan = 2, sticky = NSEW)
	Button(payment_info_screen, text = "CUSTOM", command = add_custom).grid(row = 1, column = 1, rowspan = 2, sticky = NSEW)

def verify_admin():
	global verify_window, admin_pin, admin_pin_entry
	verify_window = Toplevel(screen)
	verify_window.geometry("250x130")
	verify_window.title("Admin Panel")
	verify_window.iconphoto(False, photo)
	admin_pin = StringVar()

	verify_window.grid_columnconfigure(0, weight = 1)

	Label(verify_window, text = "ENTER PIN: ", font = ("Calibri", 16)).grid(row = 0, columnspan = 3, sticky = NSEW)
	admin_pin = Entry(verify_window, textvariable = admin_pin)
	admin_pin.grid(row = 2, columnspan = 2)
	Label(verify_window, text = "").grid(row = 3)
	Button(verify_window, text = "LOG IN", width = 20, height = 2, command = admin_login).grid(row = 4, columnspan = 3)

def admin_login():
	global pin1
	pin1 = admin_pin.get()

	# initialize database connection
	con = sl.connect('user-data.db')

	# execute SQL statements
	with con:
		c = con.cursor()
		pin = c.execute('SELECT pin FROM user WHERE name = "admin"')
		pin = str(c.fetchone()).strip("'',[]()")

		if pin1 == pin:
			admin_panel1()
		else:
			login_failed()

	con.close()
# GUI for the admin panel
def admin_panel1():
	# admin panel gui
	global admin_panel, search_f_name, search_l_name
	verify_window.destroy()
	search_f_name = StringVar()
	search_l_name = StringVar()
	login_screen.destroy()
	admin_panel = Toplevel(screen)
	admin_panel.geometry("800x250")
	admin_panel.title("Admin Panel")
	admin_panel.iconphoto(False, photo)

	admin_panel.grid_columnconfigure(0, weight = 1)
	admin_panel.grid_columnconfigure(1, weight = 1)
	admin_panel.grid_columnconfigure(2, weight = 1)
	admin_panel.grid_columnconfigure(3, weight = 1)
	admin_panel.grid_rowconfigure(5, weight = 1)

	Label(admin_panel, text = "ADMIN PANEL", font = ("Calibri", 16)).grid(row = 0, columnspan = 3, sticky = NSEW)
	Label(admin_panel, text = "Search for user: ", font = ("Calibri", 14)).grid(row = 1, columnspan = 3, sticky = NSEW)
	Label(admin_panel, text = "First name: ", padx = 5, pady = 5, font = ("Calibri", 14)).grid(row = 2, column = 0, sticky = W)
	search_f_name = Entry(admin_panel, textvariable = search_f_name)
	search_f_name.grid(row = 2, column = 1, columnspan = 2, sticky = NSEW)
	Label(admin_panel, text = "Last name: ", padx = 5, pady = 5, font = ("Calibri", 14)).grid(row = 3, column = 0, sticky = W)
	search_l_name = Entry(admin_panel, textvariable = search_l_name)
	search_l_name.grid(row = 3, column = 1, columnspan = 2, sticky = NSEW)
	Label(admin_panel, text = "").grid(row = 4)
	Button(admin_panel, text = "SEARCH", width = 20, height = 2, command = display_data).grid(row = 5, columnspan = 3, sticky = NSEW)

# error message for a user not ofund
def entry_not_found():
	global entry_not_found_screen
	entry_not_found_screen = Toplevel(screen)
	entry_not_found_screen.title("Entry Error")
	entry_not_found_screen.geometry("250x120")
	entry_not_found_screen.iconphoto(False, photo)
	Label(entry_not_found_screen, text = "User not found in database", fg = "red", font = ("Calibri", 12)).pack()
	Button(entry_not_found_screen, text = "OK", width = 20, height = 2, command = delete_entry_screen).pack()

# display user based on search criteria
def display_data():	
	# search for user
	global first_name, last_name, payment_due, f_name, l_name, address, phone, name, pin
	f_name = search_f_name.get()
	l_name = search_l_name.get()

	# set name entries to lowercase and strip whitespace
	f_name = f_name.lower().strip()
	l_name = l_name.lower().strip()
	print(f_name)
	print(l_name)

	# initialize database connection and execute SQL search statements
	con = sl.connect('user-data.db')
	c = con.cursor()

	c.execute('SELECT name FROM user WHERE f_name = ? and l_name = ?', (f_name, l_name))
	name = c.fetchone()
	c.execute('SELECT pin FROM user WHERE f_name = ? and l_name = ?', (f_name, l_name))
	pin = c.fetchone()
	c.execute('SELECT payment_due FROM user WHERE f_name = ? and l_name = ?', (f_name, l_name))
	payment_due = c.fetchone()
	c.execute('SELECT f_name FROM user WHERE f_name = ? and l_name = ?', (f_name, l_name))
	first_name = c.fetchone()
	c.execute('SELECT l_name FROM user WHERE f_name = ? and l_name = ?', (f_name, l_name))
	last_name = c.fetchone()
	c.execute('SELECT address FROM user WHERE f_name = ? and l_name = ?', (f_name, l_name))
	address = str(c.fetchone()).strip("'',[](){}")
	c.execute('SELECT phone FROM user WHERE f_name = ? and l_name = ?', (f_name, l_name))
	phone = c.fetchone()

	# display user data
	Label(admin_panel, text = "First Name", padx = 5, pady = 5, font = ("Calibri", 14)).grid(row = 2, column = 3, sticky = NSEW)
	Label(admin_panel, text = "Last Name", padx = 5, pady = 5, font = ("Calibri", 14)).grid(row = 2, column = 4, sticky = NSEW)
	Label(admin_panel, text = "Payment Due", padx = 5, pady = 5, font = ("Calibri", 14)).grid(row = 2, column = 5, sticky = NSEW)
	Label(admin_panel, text = "Phone", padx = 5, pady = 5, font = ("Calibri", 14)).grid(row = 2, column = 6, sticky = NSEW)
	Label(admin_panel, text = "Address", padx = 5, pady = 5, font = ("Calibri", 14)).grid(row = 2, column = 7, sticky = NSEW)
	
	# display user info depending on if it contains current payment information
	if first_name is not None and last_name is not None:
		Label(admin_panel, text = first_name, padx = 5, pady = 5, font = ("Calibri", 12)).grid(row = 3, column = 3, sticky = NSEW)
		Label(admin_panel, text = last_name, padx = 5, pady = 5, font = ("Calibri", 12)).grid(row = 3, column = 4, sticky = NSEW)
	else:
		Label(admin_panel, text = "", padx = 5, pady = 5, font = ("Calibri", 12)).grid(row = 3, column = 3, sticky = NSEW)
		Label(admin_panel, text = "", padx = 5, pady = 5, font = ("Calibri", 12)).grid(row = 3, column = 4, sticky = NSEW)
		entry_not_found()
	if payment_due is not None:
		Label(admin_panel, text = payment_due, padx = 5, pady = 5, font = ("Calibri", 12)).grid(row = 3, column = 5, sticky = NSEW)
	else:
		Label(admin_panel, text = "", padx = 5, pady = 5, font = ("Calibri", 12)).grid(row = 3, column = 5, sticky = NSEW)
	if phone is not None:
		Label(admin_panel, text = phone, padx = 5, pady = 5, font = ("Calibri", 12)).grid(row = 3, column = 6, sticky = NSEW)
	else:
		Label(admin_panel, text = "", padx = 5, pady = 5, font = ("Calibri", 12)).grid(row = 3, column = 6, sticky = NSEW)
	if address is not None:
		Label(admin_panel, text = address, padx = 5, pady = 5, font = ("Calibri", 12)).grid(row = 3, column = 7, sticky = NSEW)
	else:
		Label(admin_panel, text = "", padx = 5, pady = 5, font = ("Calibri", 12)).grid(row = 3, column = 7, sticky = NSEW)
	# update payment info
	Button(admin_panel, text = "UPDATE PAYMENT INFO", width = 20, height = 2, command = update_payment_info_screen).grid(row = 5, column = 3, columnspan = 3, rowspan = 2, sticky = NSEW)
	Button(admin_panel, text = "UPDATE USER", width = 20, height = 2, command = update_user).grid(row = 5, column = 6, columnspan = 3, rowspan = 2, sticky = NSEW)
	con.close()

# screen for successfully registered user
def register_success():
	global register_success_screen
	register_success_screen = Toplevel(screen)
	register_success_screen.title("Register Successful")
	register_success_screen.geometry("250x100")
	register_success_screen.iconphoto(False, photo)
	Label(register_success_screen, text = "User successfully registered", fg = "green", font = ("Calibri", 12)).pack()
	Label(register_success_screen, text = "").pack()
	Button(register_success_screen, text = "OK", width = 20, height = 2, command = delete_register_success_screen).pack()

def update_user():
	global update_user_screen
	update_user_screen = Toplevel(screen)
	update_user_screen.geometry("400x350")
	update_user_screen.title("Admin Panel")
	update_user_screen.iconphoto(False, photo)

	global name1, pin1, conf_pin1, f_name1, l_name1, date_reg1, date_due1
	global f_name_entry1, l_name_entry1, name_entry1, pin_entry1, conf_pin_entry1, date_reg_entry1, date_due_entry1, phone1, phone_entry1, address1, address_entry1
	name1 = StringVar()
	l_name1 = StringVar()
	f_name1 = StringVar()
	pin1 = StringVar()
	conf_pin1 = StringVar()
	date_reg1 = StringVar()
	date_due1 = StringVar()
	phone1 = StringVar()
	address1 = StringVar()

	update_user_screen.grid_columnconfigure(0, weight = 1)
	update_user_screen.grid_columnconfigure(1, weight = 1)
	update_user_screen.grid_columnconfigure(2, weight = 1)
	update_user_screen.grid_rowconfigure(10, weight = 1)

	Label(update_user_screen, text = "Please enter details below", font = ("Calibri", 16)).grid(row = 0, columnspan = 3, sticky = NSEW)
	Label(update_user_screen, text = "First name: ", font = ("Calibri", 12)).grid(row = 1, column = 0, sticky = W)
	f_name_entry1 = Entry(update_user_screen, textvariable = f_name1)
	f_name_entry1.insert(0, first_name)
	f_name_entry1.grid(row = 1, column = 1, columnspan = 2, sticky = NSEW)

	Label(update_user_screen, text = "Last name: ", font = ("Calibri", 12)).grid(row = 2, column = 0, sticky = W)
	l_name_entry1 = Entry(update_user_screen, textvariable = l_name1)
	l_name_entry1.insert(0, last_name)
	l_name_entry1.grid(row = 2, column = 1, columnspan = 2, sticky = NSEW)

	Label(update_user_screen, text = "Username: ", font = ("Calibri", 12)).grid(row = 3, column = 0, sticky = W)
	name_entry1 = Entry(update_user_screen, textvariable = name1)
	name_entry1.insert(0, name)
	name_entry1.grid(row = 3, column = 1, columnspan = 2, sticky = NSEW)

	Label(update_user_screen, text = "PIN: ", font = ("Calibri", 12)).grid(row = 4, column = 0, sticky = W)
	pin_entry1 = Entry(update_user_screen, textvariable = pin1)
	pin_entry1.insert(0, pin)
	pin_entry1.grid(row = 4, column = 1, columnspan = 2, sticky = NSEW)

	Label(update_user_screen, text = "Phone Number: ", font = ("Calibri", 12)).grid(row = 6, column = 0, sticky = W)
	phone_entry1 = Entry(update_user_screen, textvariable = phone1)
	phone_entry1.insert(0, phone)
	phone_entry1.grid(row = 6, column = 1, columnspan = 2, sticky = NSEW)

	Label(update_user_screen, text = "Address: ", font = ("Calibri", 12)).grid(row = 7, column = 0, sticky = W)
	address_entry1 = Entry(update_user_screen, textvariable = address1)
	address_entry1.insert(0, address)
	address_entry1.grid(row = 7, column = 1, columnspan = 2, sticky = NSEW)

	Label(update_user_screen, text = "Date Due: ", font = ("Calibri", 12)).grid(row = 8, column = 0, sticky = W)
	date_due_entry1 = Entry(update_user_screen, textvariable = date_due1)
	date_due_entry1.insert(0, payment_due)
	date_due_entry1.grid(row = 8, column = 1, columnspan = 2, sticky = NSEW)

	Label(update_user_screen, text = "").grid(row = 9)
	Button(update_user_screen, text = "UPDATE", width = 20, height = 2, command = update_user_db).grid(row = 10, columnspan = 3, rowspan = 2, sticky = NSEW)

def success_update():
	global success_update_screen
	success_update_screen = Toplevel(screen)
	success_update_screen.title("Admin Panel")
	success_update_screen.geometry("250x100")
	success_update_screen.iconphoto(False, photo)
	Label(success_update_screen, text = "User successfully updated", fg = "green", font = ("Calibri", 12)).pack()
	Label(success_update_screen, text = "").pack()
	Button(success_update_screen, text = "OK", width = 20, height = 2, command = delete_success_update_screen).pack()

def unsuccess_update():
	global unsuccess_update_screen
	unsuccess_update_screen = Toplevel(screen)
	unsuccess_update_screen.title("Admin Panel")
	unsuccess_update_screen.geometry("250x100")
	unsuccess_update_screen.iconphoto(False, photo)
	Label(unsuccess_update_screen, text = "User successfully updated", fg = "green", font = ("Calibri", 12)).pack()
	Label(unsuccess_update_screen, text = "").pack()
	Button(unsuccess_update_screen, text = "OK", width = 20, height = 2, command = delete_unsuccess_update_screen).pack()

def update_user_db():
	con = sl.connect('user-data.db')
	c = con.cursor()

	name_info = name1.get()
	f_name_info = f_name1.get()
	l_name_info = l_name1.get()
	pin_info = pin1.get()
	payment_due_info = date_due1.get()
	phone_info = phone1.get()
	address_info = address1.get()

	# convert strings to lowercase and strip leading/ending whitespace
	name_info = name_info.strip()
	f_name_info = f_name_info.strip().lower()
	l_name_info = l_name_info.strip().lower()
	pin_info = pin_info.strip()
	phone_info = phone_info.strip()
	address_info = address_info.strip()

	if name_info and f_name_info and l_name_info and pin_info and payment_due_info and phone_info and address_info:
		params = (name_info, f_name_info, l_name_info, pin_info, payment_due_info, phone_info, address_info, f_name, l_name)
		c.execute('UPDATE user SET name = ?, f_name = ?, l_name = ?, pin = ?, payment_due = ?, phone = ?, address = ? WHERE f_name = ? AND l_name = ?', params)
		con.commit()
		success_update()
	else: 
		unsuccess_update()

	con.close()
# delete the successful registery screen
def delete_register_success_screen():
	register_success_screen.destroy()
	screen1.destroy()

# error message for an empty register entry
def register_empty():
	global register_empty_screen
	register_empty_screen = Toplevel(screen)
	register_empty_screen.title("Register Error")
	register_empty_screen.geometry("250x100")
	register_empty_screen.iconphoto(False, photo)
	Label(register_empty_screen, text = "Empty entry detected", fg = "red", font = ("Calibri", 12)).pack()
	Label(register_empty_screen, text = "").pack()
	Button(register_empty_screen, text = "OK", width = 20, height = 2, command = delete_register_empty_screen).pack()

# error message for a registery name already taken, usernames are unique
def register_name_taken():
	global name_taken_screen
	name_taken_screen = Toplevel(screen)
	name_taken_screen.title("Register Error")
	name_taken_screen.geometry("250x100")
	name_taken_screen.iconphoto(False, photo)
	Label(name_taken_screen, text = "Name already in use", fg = "red", font = ("Calibri", 12)).pack()
	Label(name_taken_screen, text = "").pack()
	Button(name_taken_screen, text = "OK", width = 20, height = 2, command = delete_name_taken_screen).pack()

# error screen for failed registration
def register_failed():
	global register_failed_screen
	register_failed_screen = Toplevel(screen)
	register_failed_screen.title("Register")
	register_failed_screen.geometry("250x100")
	register_failed_screen.iconphoto(False, photo)
	Label(register_failed_screen, text = "Registration failed: pin does not match", fg = "red", font = ("Calibri", 12)).pack()
	Label(register_failed_screen, text = "").pack()
	Button(register_failed_screen, text = "OK", width = 20, height = 2, command = delete_register_failed_screen).pack()

# error screen for an invalid pin
def failed_pin():
	global failed_pin_screen
	failed_pin_screen = Toplevel(screen)
	failed_pin_screen.title("PIN Error")
	failed_pin_screen.geometry("250x120")
	failed_pin_screen.iconphoto(False, photo)
	Label(failed_pin_screen, text = "PIN must be at least 4 digits", fg = "red", font = ("Calibri", 12)).pack()
	Button(failed_pin_screen, text = "OK", width = 20, height = 2, command = delete_failed_pin_screen).pack()

# register user and insert into database
def register_user():
	# pull information from user entry
	global reg_label, f_name_info, name_info, l_name_info, pin_info, conf_pin_info, date_reg_info, payment_due_info, phone_info, address_info
	reg_label = Label(screen1, text = "")
	reg_label.grid(row = 0, column = 0)
	name_info = name.get()
	f_name_info = f_name.get()
	l_name_info = l_name.get()
	pin_info = pin.get()
	conf_pin_info = conf_pin.get()
	date_reg_info = date_reg.get()
	payment_due_info = date_due.get()
	phone_info = phone.get()
	address_info = address.get()

	# convert strings to lowercase and strip leading/ending whitespace
	name_info = name_info.strip()
	f_name_info = f_name_info.strip().lower()
	l_name_info = l_name_info.strip().lower()
	pin_info = pin_info.strip()
	conf_pin_info = conf_pin_info.strip()
	phone_info = phone_info.strip()
	address_info = address_info.strip()

	# initialize database connection
	con = sl.connect('user-data.db')
	c = con.cursor()

	# execute SQL statements
	c.execute('SELECT * FROM user WHERE name = ?', (name_info,))
	exists = c.fetchall()
	if not exists:

		if name_info and f_name_info and l_name_info and pin_info and conf_pin_info and date_reg and date_due and phone_info and address_info and pin_info == conf_pin_info:
			if len(pin_info) > 3 or len(conf_pin_info) > 3:
				sql = 'INSERT INTO user (name, l_name, f_name, pin, phone, address, date_reg, payment_due) values(?, ?, ?, ?, ?, ?, ?, ?)'
				data = (name_info, l_name_info, f_name_info, pin_info, phone_info, address_info, date_reg_info, payment_due_info)
				with con:
					con.execute(sql, data)
					con.commit()
				register_success()
			else:
				failed_pin()
		if name_info and f_name_info and l_name_info and pin_info and not date_reg and not date_due and conf_pin_info and pin_info == conf_pin_info:
			if len(pin_info) > 3 or len(conf_pin_info) > 3:
					sql = 'INSERT INTO user (name, l_name, f_name, pin) values(?, ?, ?, ?)'
					data = (name_info, l_name_info, f_name_info, pin_info)
					with con:
						con.execute(sql, data)
						con.commit()
					register_success()
			else:
				failed_pin()

		if not name_info or not f_name_info or not l_name_info or not pin_info or not conf_pin_info:
			register_empty()
		if pin_info != conf_pin_info:
			register_failed()
	else:
		register_name_taken()

	# remove input from entries and close database connection
	name_entry.delete(0, END)
	pin_entry.delete(0, END)
	conf_pin_entry.delete(0, END)
	con.close()

# GUI register window
def register():
	global screen1
	screen1 = Toplevel(screen)
	screen1.title("REGISTER")
	screen1.geometry("400x350")
	screen1.iconphoto(False, photo)

	global name, pin, conf_pin, f_name, l_name, date_reg, date_due
	global f_name_entry, l_name_entry, name_entry, pin_entry, conf_pin_entry, date_reg_entry, date_due_entry, phone, phone_entry, address, address_entry
	name = StringVar()
	l_name = StringVar()
	f_name = StringVar()
	pin = StringVar()
	conf_pin = StringVar()
	date_reg = StringVar()
	date_due = StringVar()
	phone = StringVar()
	address = StringVar()

	screen1.grid_columnconfigure(0, weight = 1)
	screen1.grid_columnconfigure(1, weight = 1)
	screen1.grid_columnconfigure(2, weight = 1)
	screen1.grid_rowconfigure(10, weight = 1)

	Label(screen1, text = "Please enter details below", font = ("Calibri", 16)).grid(row = 0, columnspan = 3, sticky = NSEW)
	Label(screen1, text = "First name: ", font = ("Calibri", 12)).grid(row = 1, column = 0, sticky = W)
	f_name_entry = Entry(screen1, textvariable = f_name)
	f_name_entry.grid(row = 1, column = 1, columnspan = 2, sticky = NSEW)

	Label(screen1, text = "Last name: ", font = ("Calibri", 12)).grid(row = 2, column = 0, sticky = W)
	l_name_entry = Entry(screen1, textvariable = l_name)
	l_name_entry.grid(row = 2, column = 1, columnspan = 2, sticky = NSEW)

	Label(screen1, text = "Username: ", font = ("Calibri", 12)).grid(row = 3, column = 0, sticky = W)
	name_entry = Entry(screen1, textvariable = name)
	name_entry.grid(row = 3, column = 1, columnspan = 2, sticky = NSEW)

	Label(screen1, text = "PIN: ", font = ("Calibri", 12)).grid(row = 4, column = 0, sticky = W)
	pin_entry = Entry(screen1, textvariable = pin)
	pin_entry.grid(row = 4, column = 1, columnspan = 2, sticky = NSEW)

	Label(screen1, text = "Confirm PIN: ", font = ("Calibri", 12)).grid(row = 5, column = 0, sticky = W)
	conf_pin_entry = Entry(screen1, textvariable = conf_pin)
	conf_pin_entry.grid(row = 5, column = 1, columnspan = 2, sticky = NSEW)

	Label(screen1, text = "Phone Number: ", font = ("Calibri", 12)).grid(row = 6, column = 0, sticky = W)
	phone_entry = Entry(screen1, textvariable = phone)
	phone_entry.grid(row = 6, column = 1, columnspan = 2, sticky = NSEW)

	Label(screen1, text = "Address: ", font = ("Calibri", 12)).grid(row = 7, column = 0, sticky = W)
	address_entry = Entry(screen1, textvariable = address)
	address_entry.grid(row = 7, column = 1, columnspan = 2, sticky = NSEW)

	Label(screen1, text = "Date Registered: ", font = ("Calibri", 12)).grid(row = 8, column = 0, sticky = W)
	date_reg_entry = Entry(screen1, textvariable = date_reg)
	date_reg_entry.grid(row = 8, column = 1, columnspan = 2, sticky = NSEW)

	Label(screen1, text = "Date Due: ", font = ("Calibri", 12)).grid(row = 9, column = 0, sticky = W)
	date_due_entry = Entry(screen1, textvariable = date_due)
	date_due_entry.grid(row = 9, column = 1, columnspan = 2, sticky = NSEW)

	Label(screen1, text = "").grid(row = 10)
	Button(screen1, text = "REGISTER", width = 20, height = 2, command = register_user).grid(row = 10, columnspan = 3, rowspan = 2, sticky = NSEW)
# functions to delete various windows

def delete_success_update_screen():
	success_update_screen.destroy()
	update_user_screen.destroy()

def delete_unsuccess_update_screen():
	unsuccess_update_screen.destroy()

# deletes failed login screen
def delete_login_failed_screen():
	login_failed_screen.destroy()

# deletes successful login screen
def delete_login_success_screen():
	user_screen.destroy()

# deletes username taken screen
def delete_name_taken_screen():
	name_taken_screen.destroy()

# deletes empty registery screen
def delete_register_empty_screen():
	register_empty_screen.destroy()

# deletes failed registery screen
def delete_register_failed_screen():
	register_failed_screen.destroy()

# deletes entry not found screen
def delete_entry_screen():
	entry_not_found_screen.destroy()

# displays successful login screen
def login_success():
	global user_screen
	login_screen.destroy()
	user_screen = Toplevel(screen)
	user_screen.title("User Panel")
	user_screen.geometry("400x200")
	user_screen.iconphoto(False, photo)

	user_screen.grid_columnconfigure(0, weight = 1)
	user_screen.grid_columnconfigure(1, weight = 1)
	user_screen.grid_rowconfigure(3, weight = 1)

	con = sl.connect('user-data.db')
	c = con.cursor()
	c.execute('SELECT payment_due FROM user WHERE name = ?', (name1,))
	payment_due = c.fetchall()
	payment_due = str(payment_due).strip("'',[]()")


	Label(user_screen, text = "Welcome, " + name1, bg = "grey", padx = 5, pady = 5, font = ("Calibri", 16)).grid(row = 0, column = 0, columnspan = 2, sticky = NSEW)
	Label(user_screen, text = "Last login: " + dt_string, font = ("Calibri", 14)).grid(row = 1, column = 0, columnspan = 2, sticky = NSEW)
	Label(user_screen, text = "Next payment due: " + payment_due, font = ("Calibri", 14)).grid(row = 2, column = 0, columnspan = 2, sticky = NSEW)
	Button(user_screen, text = "LOG OUT", width = 20, height = 2, pady = 20, command = delete_login_success_screen).grid(row = 3, column = 0, columnspan = 2, rowspan = 2, sticky = NSEW)

	con.close()

# displays failed login screen
def login_failed():
	global login_failed_screen
	login_failed_screen = Toplevel(screen)
	login_failed_screen.title("Login failed")
	login_failed_screen.geometry("250x100")
	login_failed_screen.iconphoto(False, photo)
	Label(login_failed_screen, text = "Login failed", fg = "red", font = ("Calibri", 12)).pack()
	Button(login_failed_screen, text = "OK", width = 20, height = 2, command = delete_login_failed_screen).pack()

# verify login details
def login_verify():
	# pull user entries for login and delete text entries
	global name1, dt_string
	name1 = name_verify.get()
	name_entry1.delete(0, END)

	# set entries to lowercase/strip whitespace
	name1.strip()

	# initialize database connection
	con = sl.connect('user-data.db')

	# get date/time for user login
	now = datetime.now()
	dt_string = now.strftime("%m/%d/%Y %I:%M %p")

	# execute SQL statements
	with con:
		c = con.cursor()
		c.execute('SELECT * FROM user WHERE name = ?', (name1,))
		if c.fetchone() is not None:
			# update user last login in database
			params = (dt_string, name1)
			c.execute('UPDATE user SET last_login = ? WHERE name = ?', params)


			if name1 == 'admin':
				verify_admin()
			else:
				login_success()
		else:
			login_failed()
	con.close()

# message for failed pin reset
def failed_reset():
	global failed_reset_screen
	failed_reset_screen = Toplevel(screen)
	failed_reset_screen.title("PIN Error")
	failed_reset_screen.geometry("250x100")
	failed_reset_screen.iconphoto(False, photo)
	Label(failed_reset_screen, text = "PIN reset failed", fg = "red", font = ("Calibri", 12)).pack()
	Button(failed_reset_screen, text = "OK", width = 20, height = 2, command = delete_failed_reset_screen).pack()

# message for successful pin reset
def success_reset():
	global success_reset_screen
	success_reset_screen = Toplevel(screen)
	success_reset_screen.title("PIN Reset")
	success_reset_screen.geometry("250x100")
	success_reset_screen.iconphoto(False, photo)
	Label(success_reset_screen, text = "PIN reset successful", fg = "green", font = ("Calibri", 12)).pack()
	Button(success_reset_screen, text = "OK", width = 20, height = 2, command = delete_success_reset_screen).pack()

# deletes successful reset screen
def delete_success_reset_screen():
	success_reset_screen.destroy()
	screen5.destroy()

# deletes failed pin reset screen
def delete_failed_reset_screen():
	failed_reset_screen.destroy()

def delete_failed_pin_screen():
	failed_pin_screen.destroy()
# function call to update user PIN in database
def update_pin():
	con = sl.connect('user-data.db')
	c = con.cursor()
	r_pin = r_pin_entry.get()
	r_conf_pin = r_conf_pin_entry.get()
	pin_label = Label(screen5, text = "")
	pin_label.grid(row = 0, column = 0)

	r_pin.strip()
	r_conf_pin.strip()

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
	screen5.title("PIN Reset")
	screen5.geometry("250x200")
	screen5.iconphoto(False, photo)

	screen5.grid_columnconfigure(0, weight = 1)
	screen5.grid_columnconfigure(1, weight = 1)
	screen5.grid_columnconfigure(2, weight = 1)
	screen5.grid_rowconfigure(5, weight = 1)

	Label(screen5, text = "RESET PIN", font = ("Calibri", 16)).grid(row = 0, columnspan = 3, sticky = NSEW)
	Label(screen5, text = "PIN:", padx = 5, pady = 5, font = ("Calibri", 12)).grid(row = 1, column = 0, sticky = W)
	r_pin_entry = Entry(screen5, textvariable = r_pin)
	r_pin_entry.grid(row = 1, column = 1, columnspan = 2, sticky = NSEW)
	Label(screen5, text = "CONFIRM PIN:", padx = 5, pady = 5, font = ("Calibri", 12)).grid(row = 2, column = 0, sticky = W)
	r_conf_pin_entry = Entry(screen5, textvariable = r_conf_pin)
	r_conf_pin_entry.grid(row = 2, column = 1, columnspan = 2, sticky = NSEW)
	Label(screen5, text = "").grid(row = 3)
	Button(screen5, text = "UPDATE", command = update_pin).grid(row = 4, columnspan = 3, rowspan = 2, sticky = NSEW)

# GUI for user login screen
def login():
	global login_screen
	login_screen = Toplevel(screen)
	login_screen.title("Login")
	login_screen.geometry("450x250")
	login_screen.iconphoto(False, photo)

	Label(login_screen, padx = 5, pady = 5,text = "Please enter details below to login", font = ("Calibri", 14)).grid(row = 0, columnspan = 3, sticky = NSEW)
	global name_verify, name_entry1
	name_verify = StringVar()

	login_screen.grid_columnconfigure(0, weight = 1)
	login_screen.grid_columnconfigure(1, weight = 1)
	login_screen.grid_columnconfigure(2, weight = 1)
	login_screen.grid_rowconfigure(6, weight = 1)
	login_screen.grid_rowconfigure(8, weight = 1)

	Label(login_screen, text = "Username: ", padx = 5, pady = 5, font = ("Calibri", 12)).grid(row = 1, column = 0, sticky = W)
	name_entry1 = Entry(login_screen, textvariable = name_verify)
	name_entry1.grid(row = 1, column = 1, columnspan = 2, sticky = NSEW)
	Label(login_screen, text = "").grid(row = 3)
	Button(login_screen, text = "Login", width = 20, height = 1, padx = 5, pady = 5, command = login_verify).grid(row = 6, rowspan = 2, columnspan = 3, sticky = NSEW)
	Button(login_screen, text = "Reset Pin", width = 20, padx = 5, pady = 5, height = 1, command = reset_pin).grid(row = 8, rowspan = 2, columnspan = 3, sticky = NSEW)

# main GUI page
def main_screen():
	global screen, reg_label, photo
	screen = Tk()
	screen.geometry("1200x700")
	screen.title("Hanley's Gym")
	photo = PhotoImage(file = "icon.png")
	screen.iconphoto(False, photo)

	screen.grid_columnconfigure(0, weight = 1)
	screen.grid_rowconfigure(0, weight = 1)
	screen.grid_rowconfigure(1, weight = 1)
	screen.grid_rowconfigure(2, weight = 1)
	title = Label(text = "HANLEY'S GYM", bg = "grey", width = "300", height = "2", font = ("Calibri", 40)).grid(row = 0, column = 0, columnspan = 2, sticky = NSEW)
	Button(text = "LOGIN", height = "3", width = "30", padx = 5, pady = 5, font = ("Calibri", 25), command = login).grid(row = 1, column = 0, columnspan = 2, sticky = NSEW)
	Button(text = "REGISTER", height = "3", width = "30", padx = 5, pady = 5, font = ("Calibri", 25), command = register).grid(row = 2, column = 0, columnspan = 2, sticky = NSEW)

	screen.mainloop()

main_screen()