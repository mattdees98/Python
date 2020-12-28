import sqlite3 as sl

con = sl.connect('user-data.db')
cur = con.cursor()

addColumn = 'UPDATE user SET l_name = LOWER(l_name);'

cur.execute('UPDATE user SET l_name = LOWER(l_name) WHERE LOWER(l_name) != l_name COLLATE Latin1_General_CS_AS')
print('executing')

con.close()