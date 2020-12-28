import sqlite3 as sl

con = sl.connect('user-data.db')
cur = con.cursor()

addColumn = 'UPDATE user SET l_name = LOWER(l_name)'
print('Last name updated')
cur.execute(addColumn)

con.close()