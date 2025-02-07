import sqlite3
con_obj=sqlite3.connect(database='BankDetails.sqlite')  #CWD
cur_obj=con_obj.cursor()
try:
    cur_obj.execute('''create table users(
                    users_acno integer primary key autoincrement,
                    users_pass text,
                    users_name text,
                    users_mob text,
                    users_email text,
                    users_balance float,
                    users_adhar text,
                    users_opendate text)
                ''')


    cur_obj.execute('''create table txn(
                    txn_id integer primary key autoincrement,
                    txn_acno int,
                    txn_type text,
                    txn_date text,
                    txn_amt float,
                    txn_update_bal float)
                    ''')
    print('Tables created successfully')
except:
    pass
con_obj.close()
