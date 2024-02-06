#SET autocommit = 0;
#CONNECT()

import sqlite3 as sql
import random
import tkinter as tk
from tkinter import ttk


# CREATE a DATABASE IN RAM (testing)
con = sql.connect(':memory:')

# CREATE/OPEN a file called mydb.
#db = sql.connect('data/mydb')


######Create a database that contains relevant tables######

# con = sql.connect("myfilght.db")
cur = con.cursor()




#create aircraft table
cur.execute("CREATE TABLE aircraft(aircraft_id INTEGER PRIMARY KEY, aircraft_model TEXT)")

#create flight table
cur.execute("CREATE TABLE flight(flight_id TEXT PRIMARY KEY, aircraft_id INTEGER, pilot_id INTEGER, departure_time TIME, departure_date DATE, departure_airport TEXT, arrival_airport TEXT)")

#create pilot table
cur.execute("CREATE TABLE pilot(pilot_id INTEGER PRIMARY KEY, pilot_name TEXT)")

#check table exist#
res = cur.execute("SELECT name FROM sqlite_master")
res.fetchone()

####################################
#random.sample(range(0, 10000), 12)
#aircraft_id[425, 943, 300, 920, 219, 554, 274, 121, 610, 102]
#filght_id[77, 52, 16, 45, 75, 53, 7, 71, 26, 42, 82, 18, 3, 30, 15]
#pilot_id[3748, 1267, 2047, 3554, 8932, 7648, 8678, 4545, 8894, 7705, 9639, 3438]
####################################


######Insert data######
#aircraft_id, aircraft_model
aircraft_data = [
  (425, '777-300ER'),
  (943, 'B787-9'),
  (300, '777-300ER'),
  (920, 'A321-200'),
  (219, '777-300ER'),
  (554, 'A321-200'),
  (274, '777-300ER'),
  (121, 'B787-9'),
  (610, '777-300ER'),
  (102, 'A321-200')
]
cur.executemany("INSERT INTO aircraft VALUES(?, ?)", aircraft_data)
con.commit()  #Commit the CHANGE

#flight_id, aircraft_id, pilot_id, departure_time, departure_date, departure_airport, arrival_airport
flight_data = [
  ('BA77', 425, 3748, '01:20', '2023-11-12', 'LHR', 'EDI'),
  ('BA52', 300, 1267, '22:30', '2023-11-10', 'LHR', 'MAN'),
  ('BA16', 943, 2047, '16:40', '2023-11-15', 'LHR', 'EDI'),
  ('BA45', 920, 3554, '02:50', '2023-11-22', 'LGW', 'MAN'),
  ('BA75', 219, 8932, '13:00', '2023-12-01', 'LGW', 'GLA'),
  ('BA53', 554, 7648, '12:00', '2023-11-30', 'LGW', 'EDI'),
  ('BA07', 274, 8678, '16:20', '2023-12-05', 'EDI', 'BHX'),
  ('BA71', 121, 4545, '11:15', '2023-11-21', 'EDI', 'BRS'),
  ('BA26', 610, 8894, '09:10', '2023-11-27', 'EDI', 'LHR'),
  ('BA42', 102, 1267, '15:50', '2023-11-12', 'GLA', 'BRS'),
  ('BA82', 102, 7648, '08:10', '2023-11-22', 'GLA', 'LGW'),
  ('BA18', 219, 7705, '06:30', '2023-11-10', 'GLA', 'BHX'),
  ('BA03', 920, 3438, '06:30', '2023-12-01', 'LTN', 'MAN'),
  ('BA30', 300, 9639, '16:40', '2023-11-30', 'LTN', 'GLA'),
  ('BA15', 425, 7705, '13:00', '2023-12-05', 'BRS', 'EDI'),
]
cur.executemany("INSERT INTO flight VALUES(?, ?, ?, ?, ?, ?, ?)", flight_data)
con.commit() 

#pilot_id, pilot_name
pilot_data = [
  (3748, 'Kip Mendez'),
  (1267, 'Moises Hurst'),
  (2047, 'Haley Barron'),
  (3554,'Lucio Rowe'),
  (8932, 'Maryellen Burton'),
  (7648, 'Carlos Erickson'),
  (8678, 'Noe Villa'),
  (4545, 'Haywood Floyd'),
  (8894, 'Sammy House'),
  (7705, 'Leigh Farmer'),
  (9639, 'Tobias Donovan'),
  (3438, 'Christina Fritz'),
]
cur.executemany("INSERT INTO pilot VALUES(?, ?)", pilot_data)
con.commit() 


######Search specific data #######

for row in cur.execute("SELECT * FROM aircraft"):
  print(row)

for row1 in cur.execute("SELECT * FROM aircraft, flight WHERE aircraft.aircraft_id = flight.aircraft_id AND aircraft.aircraft_id = 425 "):
  print(row1)


for row2 in cur.execute("SELECT flight.flight_id,aircraft_model FROM flight LEFT JOIN aircraft ON aircraft.aircraft_id = flight.aircraft_id"):
  print(row2)

######Update data (update attribute values)######

###update one column###
cur.execute("UPDATE pilot SET pilot_name = 'Smith Floyd' WHERE pilot_id = 4545")

for update_pilot in cur.execute("SELECT pilot_id, pilot_name FROM pilot WHERE pilot_id = 4545"):
  print("The updated pilot information: ", update_pilot)

###update multiple columns###
cur.execute("UPDATE flight SET aircraft_id = 274, pilot_id = 4545, departure_time = '07:30' WHERE flight_id = 'BA18' ")

for update_filght in cur.execute("SELECT * FROM flight WHERE flight_id = 'BA18' "):
  print("The information of the updated flight: ", update_filght)




######To delete data and show remaining data after deletion######
cur.execute("DELETE FROM flight WHERE flight_id = 'BA30' ")


print("The remain flight table after deletion: ")
for remain_flight in cur.execute("SELECT * FROM flight"):
  print(remain_flight)


######Calculate and present summary statistics######

###the flights list and number for specific month###
print("The filght ID and departure time for flight in December: ")
for flight_december in cur.execute("SELECT flight_id, departure_date, departure_time FROM flight WHERE strftime('%m', departure_date) = '12' "):
  print(flight_december)

print('Total flight numbers in November: ')
for count_filght_november in cur.execute("SELECT count(*) FROM flight WHERE strftime('%m', departure_date) = '12' "):
  print(count_filght_november[0])

###the flights list and number for specific week###
print('Total flight numbers in the second week of November: ')
for count_filght_week in cur.execute("SELECT count(*) FROM flight WHERE departure_date BETWEEN '2023-11-06' AND '2023-11-12' "):
  print(count_filght_week[0])


###the number of a specific destination per month###
print('Total flight numbers to Edinburgh in November: ')
for count_des_nevember in cur.execute("SELECT count(*) FROM flight WHERE strftime('%m', departure_date) = '11' AND arrival_airport = 'EDI' "):
  print(count_des_nevember[0])


    

######Extra function######
def get_flight_from_model():
    cur.execute("SELECT flight.flight_id, aircraft_model FROM flight LEFT JOIN aircraft ON aircraft.aircraft_id = flight.aircraft_id")
    return cur.fetchall()


def search_my_flight(dep):
  cur.execute("SELECT departure_airport, arrival_airport, departure_date, departure_time FROM flight WHERE departure_airport = '%s'" % (dep,))
  return cur.fetchall()


def number_per_flight():
  cur.execute("SELECT count(*) FROM flight ORDER BY departure_airport")
  return cur.fetchall()


###test function###

print('The aircraft model of the flights: ')
print(get_flight_from_model())
print('\n')

print('Enter your departure airport: ')
# y = input()
print(search_my_flight('LHR'))
print('\n')

print('Number of flights per airport: ')
npf = number_per_flight()
print(npf[0][0])
print('\n')




  
###############################################################################

#GUI

###############################################################################
######function in tkinter######

#######aircraft#######
def add_aircraft():
    a_id = aircraft_entry1.get()
    a_model = aircraft_combobox1.get()
  
    print('Aircraft ID: ', a_id, 'Aircraft model: ', a_model)

    #add function#
    a_insert_query = '''INSERT INTO aircraft (aircraft_id, aircraft_model) VALUES(?, ?)'''
    a_insert_tuple = (a_id, a_model)
    cur.execute(a_insert_query, a_insert_tuple)
    con.commit()    


    #update function#
def update_aircraft():
    a_id = aircraft_entry1.get()
    a_model = aircraft_combobox1.get()
    print('Aircraft ID: ', a_id, 'Aircraft model: ', a_model)

    a_update_query = '''UPDATE aircraft SET aircraft_model= ? WHERE aircraft_id= ?'''
    a_update_tuple = (a_model, a_id)
    cur.execute(a_update_query, a_update_tuple)
    con.commit() 

    #search function#
def search_aircraft():
    a_id = aircraft_entry1.get()
    a_model = aircraft_combobox1.get()
    print('Aircraft ID: ', a_id)

    a_search_query = '''SELECT * FROM aircraft WHERE aircraft_id=?'''
    cur.execute(a_search_query, (a_id, ))
    con.commit()
    print(cur.fetchall())

    #delete function#
def delete_aircraft():
    a_id = aircraft_entry1.get()
    a_model = aircraft_combobox1.get()
    print('Aircraft ID: ', a_id, 'Aircraft model: ', a_model)

    a_delete_query = '''DELETE FROM aircraft WHERE aircraft_id=?'''
    cur.execute(a_delete_query, (a_id, ))
    con.commit()


    #view function#
def view_aircraft():
    for a_view in cur.execute("SELECT * FROM aircraft"):
      print(a_view)

#######flight#######
def add_flight():
    f_id = flight_entry1.get()
    f_a_id = flight_entry2.get()
    f_p_id = flight_entry3.get()
    f_d_time = flight_entry4.get()
    f_d_date = flight_entry5.get()
    f_d_airport = flight_combobox1.get()
    f_a_airport = flight_combobox2.get()

    print('Flight ID: ', f_id, 'Aircraft ID: ', f_a_id, 'Pilot ID: ', f_p_id, 'Departure time: ', f_d_time, 
    'Departure date: ', f_d_date, 'Departure airport: ', f_d_airport, 'Arrival airport: ', f_a_airport)

    #add function#
    f_insert_query = '''INSERT INTO flight (flight_id, aircraft_id, pilot_id, departure_time, departure_date, 
    departure_airport, arrival_airport) VALUES(?, ?, ?, ?, ?, ?, ?)'''
    f_insert_tuple = (f_id, f_a_id, f_p_id, f_d_time, f_d_date, f_d_airport, f_a_airport)
    cur.execute(f_insert_query, f_insert_tuple)
    con.commit()    

    #update function#
def update_flight():
    f_id = flight_entry1.get()
    f_a_id = flight_entry2.get()
    f_p_id = flight_entry3.get()
    f_d_time = flight_entry4.get()
    f_d_date = flight_entry5.get()
    f_d_airport = flight_combobox1.get()
    f_a_airport = flight_combobox2.get()
    print('Flight ID: ', f_id, 'Aircraft ID: ', f_a_id, 'Pilot ID: ', f_p_id, 'Departure time: ', f_d_time, 
    'Departure date: ', f_d_date, 'Departure airport: ', f_d_airport, 'Arrival airport: ', f_a_airport)

    f_update_query = '''UPDATE flight SET aircraft_id=?, pilot_id=?, departure_time=?, departure_date=?, departure_airport=?, arrival_airport=? WHERE flight_id= ?'''
    f_update_tuple = (f_a_id, f_p_id, f_d_time, f_d_date, f_d_airport, f_a_airport, f_id)
    cur.execute(f_update_query, f_update_tuple)
    con.commit() 

    #search function#
def search_flight():
    f_id = flight_entry1.get()
    f_a_id = flight_entry2.get()
    f_p_id = flight_entry3.get()
    f_d_time = flight_entry4.get()
    f_d_date = flight_entry5.get()
    f_d_airport = flight_combobox1.get()
    f_a_airport = flight_combobox2.get()
    print('Flight ID: ', f_id)

    f_search_query = '''SELECT * FROM flight WHERE flight_id=?'''
    cur.execute(f_search_query, (f_id, ))
    con.commit()
    print(cur.fetchall())



    #delete function#
def delete_flight():
    f_id = flight_entry1.get()
    f_a_id = flight_entry2.get()
    f_p_id = flight_entry3.get()
    f_d_time = flight_entry4.get()
    f_d_date = flight_entry5.get()
    f_d_airport = flight_combobox1.get()
    f_a_airport = flight_combobox2.get()
    print('Flight ID: ', f_id, 'Aircraft ID: ', f_a_id, 'Pilot ID: ', f_p_id, 'Departure time: ', f_d_time, 
    'Departure date: ', f_d_date, 'Departure airport: ', f_d_airport, 'Arrival airport: ', f_a_airport)

    f_delete_query = '''DELETE FROM flight WHERE flight_id=?'''
    cur.execute(f_delete_query, (f_id, ))
    con.commit()

    #view function#
def view_flight():
    for f_view in cur.execute("SELECT * FROM flight"):
      print(f_view)


########pliot#######
def add_pilot():
    p_id = pilot_entry1.get()
    p_name = pilot_entry2.get()
      
    print('Pilot ID: ', p_id, 'Pilot name: ', p_name)

    #add function#
    p_insert_query = '''INSERT INTO pilot (pilot_id, pilot_name) VALUES(?, ?)'''
    p_insert_tuple = (p_id, p_name)
    con.execute(p_insert_query, p_insert_tuple)
    con.commit()  

    #update function#
def update_pilot():
    p_id = pilot_entry1.get()
    p_name = pilot_entry2.get()
    print('Pilot ID: ', p_id, 'Pilot name: ', p_name)

    p_update_query = '''UPDATE pilot SET pilot_name= ? WHERE pilot_id= ?'''
    p_update_tuple = (p_name, p_id)
    cur.execute(p_update_query, p_update_tuple)
    con.commit() 

    #search function#
def search_pilot():
    p_id = pilot_entry1.get()
    p_name = pilot_entry2.get()
    print('Pilot ID: ', p_id)

    p_search_query = '''SELECT * FROM pilot WHERE pilot_id=?'''
    cur.execute(p_search_query, (p_id, ))
    con.commit()
    print(cur.fetchall())


    #delete function#
def delete_pilot():
    p_id = pilot_entry1.get()
    p_name = pilot_entry2.get()
    print('Pilot ID: ', p_id, 'Pilot name: ', p_name)

    p_delete_query = '''DELETE FROM pilot WHERE pilot_id=?'''
    cur.execute(p_delete_query, (p_id, ))
    con.commit()

    #view function#
def view_pilot():
    for p_view in cur.execute("SELECT * FROM pilot"):
      print(p_view)



######Calculate and present summary statistics######

###the flights list and number for specific month###
def f_number_month():
  f_no_month = extra_combobox1.get()
  extra_query1 = '''SELECT flight_id, departure_date, departure_time FROM flight WHERE strftime('%m', departure_date) = ?'''
  cur.execute(extra_query1, (f_no_month, ))
  con.commit()
  print('The filghts information of this month(' + f_no_month + '): ')
  print(cur.fetchall())
  extra_query2 = '''SELECT COUNT(*) FROM flight WHERE strftime('%m', departure_date) = ?'''
  cur.execute(extra_query2, (f_no_month, ))
  con.commit()
  e2 = cur.fetchall()
  print('Total flight numbers in this month(' + f_no_month + '): ')
  print(e2[0][0])



###the number of a specific destination per month###
def f_no_destination():
    # f_no_month = extra_combobox1.get()
    # f_no_dep = extra_combobox2.get()
    f_no_arr = extra_combobox3.get()
    extra_query3 = '''SELECT flight_id, departure_date, departure_time FROM flight WHERE arrival_airport = ?'''
    cur.execute(extra_query3, (f_no_arr, ))
    con.commit()
    print('The filghts information of ' + f_no_arr + ': ')
    print(cur.fetchall())
    extra_query4 = '''SELECT count(*) FROM flight WHERE arrival_airport = ?''' #strftime('%m', departure_date) = ? AND 
    cur.execute(extra_query4, (f_no_arr, ))
    con.commit() 
    e3 = cur.fetchall()
    print('Total flight numbers of '+ f_no_arr +' : ')
    print(e3[0][0])
  
###the number of a specific time###
def f_no_day():
    f_no_start = extra_entry1.get()
    # f_no_end = extra_entry2.get()
    extra_query5 = '''SELECT flight_id, departure_date, departure_time, departure_airport, arrival_airport FROM flight WHERE strftime('%Y-%m-%d', departure_date) = ?  ''' #AND strftime('%Y-%m-%d', departure_date) = ?
    cur.execute(extra_query5, (f_no_start, ))
    con.commit() 
    print('The filghts information of ' + f_no_start + ': ')
    print(cur.fetchall())
    extra_query6 = '''SELECT count(*) FROM flight WHERE strftime('%Y-%m-%d', departure_date) = ?'''
    cur.execute(extra_query6, (f_no_start, ))
    con.commit() 
    e6 = cur.fetchall()
    print('Total flight numbers of '+ f_no_start +' : ')
    print(e6[0][0])



####extra function####
def ef_flight_from_model():
    ef_f_from_model = ef_combobox1.get()
    ef_query1 = '''SELECT flight.flight_id, aircraft_model FROM flight LEFT JOIN aircraft ON aircraft.aircraft_id = flight.aircraft_id WHERE aircraft_model=? '''
    cur.execute(ef_query1, (ef_f_from_model, ))
    con.commit() 
    print(cur.fetchall())

def ef_pilot_from_flight():
  ef_p_from_f = ef_entry1.get()
  ef_query2 = '''SELECT flight.flight_id, pilot_name FROM flight LEFT JOIN pilot ON pilot.pilot_id = flight.pilot_id WHERE flight_id=? '''
  cur.execute(ef_query2, (ef_p_from_f, ))
  con.commit() 
  print(cur.fetchall())

#count the aircraft number by flight
def count_a_by_f():
  ef_count_a_by_f = ef_entry2.get()
  ef_query3 = '''SELECT aircraft_model FROM flight LEFT JOIN aircraft ON flight.aircraft_id = aircraft.aircraft_id WHERE flight_id=? '''
  cur.execute(ef_query3, (ef_count_a_by_f, ))
  con.commit() 
  ef3 = cur.fetchall()
  print(ef3[0][0])



'''
def ef_search_my_flight(dep):
  cur.execute("SELECT departure_airport, arrival_airport, departure_date, departure_time FROM flight WHERE departure_airport = '%s'" % (dep,))
  return cur.fetchall()
  '''


window = tk.Tk()
window.title('MyFlight')

frame = tk.Frame(window)
frame.pack()

scrollbar = tk.Scrollbar(window)         #add scrollbar
scrollbar.pack(side='right', fill='y')


#aircraft frame#
aircraft_info_frame = tk.LabelFrame(frame, text='Aircraft Input Data')
aircraft_info_frame.grid(row=0, column=0, sticky="news", padx=10, pady=2)

aircraft_label1 = tk.Label(aircraft_info_frame, text= 'Aircraft ID')
aircraft_label1.grid(row=0, column=0)
aircraft_label2 = tk.Label(aircraft_info_frame, text= 'Aircraft Model')
aircraft_label2.grid(row=0, column=1)

aircraft_entry1 = tk.Entry(aircraft_info_frame)
aircraft_combobox1 = ttk.Combobox(aircraft_info_frame, values=['777-300ER', 'B787-9', 'A321-200'])
aircraft_entry1.grid(row=1, column=0)
aircraft_combobox1.grid(row=1, column=1)

for widget in aircraft_info_frame.winfo_children():
  widget.grid_configure(padx=10, pady=2)

#flight frame#
flight_info_frame = tk.LabelFrame(frame, text='Flight Input Data')
flight_info_frame.grid(row= 3, column= 0, sticky="news", padx=10, pady=2)

flight_label1 = tk.Label(flight_info_frame, text= 'Flight ID')
flight_label1.grid(row= 0, column= 0)
flight_label2 = tk.Label(flight_info_frame, text= 'Aircraft ID')
flight_label2.grid(row= 0, column= 1)
flight_label3 = tk.Label(flight_info_frame, text= 'Pilot ID')
flight_label3.grid(row= 0, column= 2)
flight_label4 = tk.Label(flight_info_frame, text= 'Departure Time')
flight_label4.grid(row= 2, column= 0)
flight_label5 = tk.Label(flight_info_frame, text= 'Departure Date')
flight_label5.grid(row= 2, column= 1)
flight_label6 = tk.Label(flight_info_frame, text= 'Departure Airport')
flight_label6.grid(row= 4, column= 0)
flight_label7 = tk.Label(flight_info_frame, text= 'Arrival Airport')
flight_label7.grid(row= 4, column= 1)

flight_entry1 = tk.Entry(flight_info_frame)
flight_entry2 = tk.Entry(flight_info_frame)
flight_entry3 = tk.Entry(flight_info_frame)
flight_entry4 = tk.Entry(flight_info_frame)
flight_entry5 = tk.Entry(flight_info_frame)
flight_combobox1 = ttk.Combobox(flight_info_frame, values=['BRS', 'BHX', 'EDI', 'GLA', 'LHR', 'LGW', 'LTN', 'MAN'])
flight_combobox2 = ttk.Combobox(flight_info_frame, values=['BRS', 'BHX', 'EDI', 'GLA', 'LHR', 'LGW', 'LTN', 'MAN'])
flight_entry1.grid(row= 1, column= 0)
flight_entry2.grid(row= 1, column= 1)
flight_entry3.grid(row= 1, column= 2)
flight_entry4.grid(row= 3, column= 0)
flight_entry5.grid(row= 3, column= 1)
flight_combobox1.grid(row= 5, column= 0)
flight_combobox2.grid(row= 5, column= 1)

for widget in flight_info_frame.winfo_children():
  widget.grid_configure(padx=10, pady=2)

#pilot frame#
pilot_info_frame = tk.LabelFrame(frame, text='Pilot Input Data')
pilot_info_frame.grid(row= 5, column= 0, sticky="news", padx=10, pady=2)

pilot_label1 = tk.Label(pilot_info_frame, text= 'Pilot ID')
pilot_label1.grid(row= 0, column= 0)
pilot_label2 = tk.Label(pilot_info_frame, text= 'Pilot Name')
pilot_label2.grid(row= 0, column= 1)

pilot_entry1 = tk.Entry(pilot_info_frame)
pilot_entry2 = tk.Entry(pilot_info_frame)
pilot_entry1.grid(row= 1, column= 0)
pilot_entry2.grid(row= 1, column= 1)

for widget in pilot_info_frame.winfo_children():
  widget.grid_configure(padx=10, pady=2)

#stat frame#
extra_info_frame = tk.LabelFrame(frame, text='Total Number and List of Flights')
extra_info_frame.grid(row= 7, column= 0, sticky="news", padx=10, pady=2)

#moth#
extra_label1 = tk.Label(extra_info_frame, text= 'Month')
extra_label1.grid(row=0, column=0)
extra_combobox1 = ttk.Combobox(extra_info_frame, values=['11', '12'])
extra_combobox1.grid(row=0, column= 1)
button_extra1 = tk.Button(extra_info_frame, text='ENTER', activeforeground='#6fa8dc', command= f_number_month)
button_extra1.grid(row=0, column=3, padx=10, pady=2)

#destination#
extra_label2 = tk.Label(extra_info_frame, text= 'Destination')
extra_label2.grid(row=2, column=0)
# extra_combobox2 = ttk.Combobox(extra_info_frame, values=['BRS', 'BHX', 'EDI', 'GLA', 'LHR', 'LGW', 'LTN', 'MAN'])
extra_combobox3 = ttk.Combobox(extra_info_frame, values=['BRS', 'BHX', 'EDI', 'GLA', 'LHR', 'LGW', 'LTN', 'MAN'])
# extra_combobox2.grid(row= 1, column= 1)
extra_combobox3.grid(row= 2, column= 1)
button_extra2 = tk.Button(extra_info_frame, text='ENTER', activeforeground='#6fa8dc', command= f_no_destination)
button_extra2.grid(row=2, column=3, padx=10, pady=2)

#day#
extra_label3 = tk.Label(extra_info_frame, text= 'Day (YYYY-MM-DD)')
extra_label3.grid(row=1, column=0)
extra_entry1 = tk.Entry(extra_info_frame)
extra_entry1.grid(row= 1, column= 1)
# extra_entry2 = tk.Entry(extra_info_frame)
# extra_entry2.grid(row= 1, column= 2)
button_extra3 = tk.Button(extra_info_frame, text='ENTER', activeforeground='#6fa8dc', command= f_no_day)
button_extra3.grid(row=1, column=3, padx=10, pady=2)

for widget in extra_info_frame.winfo_children():
  widget.grid_configure(padx=10, pady=2)

#extra frame#
ef_info_frame = tk.LabelFrame(frame, text='More Information')
ef_info_frame.grid(row= 8, column= 0, sticky="news", padx=10, pady=2)

ef_label1 = tk.Label(ef_info_frame, text= 'Find flights by aircraft model: ')
ef_label1.grid(row=0, column=0)
ef_combobox1 = ttk.Combobox(ef_info_frame, values=['777-300ER', 'B787-9', 'A321-200'])
ef_combobox1.grid(row=0, column=1)
button_ef1 = tk.Button(ef_info_frame, text='ENTER', activeforeground='#6fa8dc', command= ef_flight_from_model)
button_ef1.grid(row=0, column=2, padx=10, pady=2)

ef_label3 = tk.Label(ef_info_frame, text= 'Find my aircraft model by flight ID: ')
ef_label3.grid(row=1, column=0)
ef_entry2 = tk.Entry(ef_info_frame)
ef_entry2.grid(row= 1, column= 1)
button_ef2 = tk.Button(ef_info_frame, text='ENTER', activeforeground='#6fa8dc', command= count_a_by_f)
button_ef2.grid(row=1, column=2, padx=10, pady=2)

ef_label2 = tk.Label(ef_info_frame, text= 'Find my pilot by flight ID: ')
ef_label2.grid(row=2, column=0)
ef_entry1 = tk.Entry(ef_info_frame)
ef_entry1.grid(row= 2, column= 1)
button_ef2 = tk.Button(ef_info_frame, text='ENTER', activeforeground='#6fa8dc', command= ef_pilot_from_flight)
button_ef2.grid(row=2, column=2, padx=10, pady=2)



####button###
#aircraft
aircraft_button_frame = tk.LabelFrame(frame, text = 'Aircraft Function')
aircraft_button_frame.grid(row= 2, column= 0, sticky="news", padx=10, pady=5)
button_add = tk.Button(aircraft_button_frame, text='ADD', activeforeground='#6fa8dc', command= add_aircraft)
button_add.grid(row=0, column=2, padx=10, pady=10)
button_update = tk.Button(aircraft_button_frame, text='UPDATE', activeforeground='#6fa8dc', command= update_aircraft)
button_update.grid(row=0, column=3, padx=10, pady=10)
button_search = tk.Button(aircraft_button_frame, text='SEARCH',activeforeground='#6fa8dc', command= search_aircraft)
button_search.grid(row=0, column=1, padx=10, pady=10)
button_delete = tk.Button(aircraft_button_frame, text='DELETE', activeforeground='#6fa8dc', command= delete_aircraft)
button_delete.grid(row=0, column=4, padx=10, pady=10)
button_view = tk.Button(aircraft_button_frame, text='VIEW', activeforeground='#6fa8dc', command= view_aircraft)
button_view.grid(row=0, column=0, padx=10, pady=10)

#flight
flight_button_frame = tk.LabelFrame(frame, text = 'Filght Function')
flight_button_frame.grid(row= 4, column= 0, sticky="news", padx=10, pady=5)
button_add1 = tk.Button(flight_button_frame, text='ADD', activeforeground='#6fa8dc', command= add_flight)
button_add1.grid(row=0, column=2, padx=10, pady=10)
button_update1 = tk.Button(flight_button_frame, text='UPDATE', activeforeground='#6fa8dc', command= update_flight)
button_update1.grid(row=0, column=3, padx=10, pady=10)
button_search1 = tk.Button(flight_button_frame, text='SEARCH',activeforeground='#6fa8dc', command= search_flight)
button_search1.grid(row=0, column=1, padx=10, pady=10)
button_delete1 = tk.Button(flight_button_frame, text='DELETE', activeforeground='#6fa8dc', command= delete_flight)
button_delete1.grid(row=0, column=4, padx=10, pady=10)
button_view1 = tk.Button(flight_button_frame, text='VIEW', activeforeground='#6fa8dc', command= view_flight)
button_view1.grid(row=0, column=0, padx=10, pady=10)

#pilot
pilot_button_frame = tk.LabelFrame(frame, text = 'Pliot Function')
pilot_button_frame.grid(row= 6, column= 0, sticky="news", padx=10, pady=5)
button_add2 = tk.Button(pilot_button_frame, text='ADD', activeforeground='#6fa8dc', command= add_pilot)
button_add2.grid(row=0, column=2, padx=10, pady=10)
button_update2 = tk.Button(pilot_button_frame, text='UPDATE', activeforeground='#6fa8dc', command= update_pilot)
button_update2.grid(row=0, column=3, padx=10, pady=10)
button_search2 = tk.Button(pilot_button_frame, text='SEARCH',activeforeground='#6fa8dc', command= search_pilot)
button_search2.grid(row=0, column=1, padx=10, pady=10)
button_delete2 = tk.Button(pilot_button_frame, text='DELETE', activeforeground='#6fa8dc', command= delete_pilot)
button_delete2.grid(row=0, column=4, padx=10, pady=10)
button_view2 = tk.Button(pilot_button_frame, text='VIEW', activeforeground='#6fa8dc', command= view_pilot)
button_view2.grid(row=0, column=0, padx=10, pady=10)







window.mainloop()



con.close()

