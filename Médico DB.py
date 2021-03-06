from tkinter import *				# Library for Graphic
from tkinter import messagebox		# Library for Menus and emergent windows
import sqlite3						# Library for DDBB
import xlsxwriter					# Library for generate and export to Excel (It is necessary to have the XlsxWriter module installed)
#import re

root=Tk()
root.title("Médico DB")
root.geometry("1000x600") # window size
root.iconbitmap("imagen.ico")

myframe=Frame(root) 
myframe.pack()

data0=StringVar()	# DATE
data1=StringVar()	# ID
data2=StringVar()	# NAME
data3=StringVar()	# LASTNAME
data4=StringVar()	# DATE OF BIRTH
data5=StringVar()	# AGE
data6=StringVar()	# TELEPHONE
data7=StringVar()	# ADRESS
data8=StringVar()	# TYPE STUDY AND OBSERVATIONS



#________________________________________________________________________________________________________________________________________________
# Decorator function for conection DDBB
def assistant_funtion(parameter_funtion):
	def int_funtion(*args, **kwargs):
		global Conection
		global Cursor
		try: 		# this "try" is in case the user forgets to connect to the DB.
			Conection=sqlite3.connect("db_Médico")
			Cursor=Conection.cursor()
			parameter_funtion(*args, **kwargs) 
			Conection.commit()
			Conection.close()
		except: messagebox.showinfo("ERROR", "'CONECT TO DB' FIRTS!!!!!.")	
	return int_funtion
			
	
#________________________________________________________________________________________________________________________________________________

#____CONNECT DDBB_________________________________________________________
def emergent_ddbb_success():
	messagebox.showinfo("SUCCESS", "The ddbb was CONNEC successfully..")

@assistant_funtion	#we call the decorator function to connect with the DDBB
def conect_ddbb():
	try:
		Cursor.execute("CREATE TABLE RRHH(DATEE INTEGER(20), ID INTEGER (20), NAME VARCHAR(20), LASTNAME VARCHAR(20), DATE_OF_BIRTH VARCHAR(20), AGE INTEGER(30), TELEPHONE INTEGER(30), ADRESS VARCHAR(100),COMMENTS VARCHAR(100))")
		emergent_ddbb_success() # we call the funtion who show the message "success" when the ddbb was created
	except: messagebox.showinfo("WARNING", "The ddbb was CONECT previusly..")
	

#____CREATE PATIENT IN DDBB______________________________________________________________________
	
@assistant_funtion	# we call the decorator function to connect with the DDBB
def create_ddbb():
	if data0.get()!="" and data1.get()!="" and data2.get()!="" and data3.get()!="" and data4.get()!="" and data5.get()!="" and data6.get()!="" and data7.get()!="":
		# List with variables entered in boxes
		fields=[(data0.get(), data1.get(), data2.get(), data3.get(), data4.get(), data5.get(), data6.get(), data7.get(), box_comments.get('1.0','end'))] # box_comments.get('1.0','end') it´s a command to get all text with that box
		Cursor.executemany("INSERT INTO RRHH VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", fields)
		messagebox.showinfo("SUCCESS", "The Patient ID was CREATED successfully..")
		data0.set("")
		data1.set("")
		data2.set("")
		data3.set("")
		data4.set("")
		data5.set("")
		data6.set("")
		data7.set("")
		box_comments.delete('1.0', END)
	else: messagebox.showinfo("ERROR", "All fields must be completed.")

#____READ Patient DDBB_________________________________________________________________________
@assistant_funtion	# we call the decorator function to connect with the DDBB
def read_ddbb():
	Cursor.execute("SELECT * FROM RRHH")
	selection=Cursor.fetchall()
	flag=""
	try:
		for index, tuple in enumerate(selection):	# is a comand to read the first element of the tuple of the list (I mind the ID).
			if tuple[1] == int(data1.get()) and flag == "":
				box_comments.delete('1.0', END) # Remove remaining comments before a new reading
				data0.set(tuple[0])
				data1.set(tuple[1])
				data2.set(tuple[2])
				data3.set(tuple[3])
				data4.set(tuple[4])
				data5.set(tuple[5])
				data6.set(tuple[6])
				data7.set(tuple[7])
				box_comments.insert('end', tuple[8]) # box_comments.insert('end','xxxxx') it´s a command to set all information in that box
				flag = "done"
		if flag != "done": messagebox.showinfo("ERROR", "The Patient ID was not exist..") 
	except: messagebox.showinfo("ERROR", "The Patient ID was not exist..")


#____UPDATE Patient DDBB_______________________________________________________________________
@assistant_funtion	# we call the decorator function to connect with the DDBB
def update_ddbb():
	if data1.get() != "":
		# with this comand, first the variable we want to modify/update, then the ID selected.
		Cursor.execute("UPDATE RRHH SET DATEE=? WHERE ID=?", (data0.get(), data1.get()))
		Cursor.execute("UPDATE RRHH SET NAME=? WHERE ID=?", (data2.get(), data1.get()))
		Cursor.execute("UPDATE RRHH SET LASTNAME=? WHERE ID=?", (data3.get(), data1.get()))
		Cursor.execute("UPDATE RRHH SET DATE_OF_BIRTH=? WHERE ID=?", (data4.get(), data1.get()))
		Cursor.execute("UPDATE RRHH SET AGE=? WHERE ID=?", (data5.get(), data1.get()))
		Cursor.execute("UPDATE RRHH SET TELEPHONE=? WHERE ID=?", (data6.get(), data1.get()))
		Cursor.execute("UPDATE RRHH SET ADRESS=? WHERE ID=?", (data7.get(), data1.get()))
		Cursor.execute("UPDATE RRHH SET COMMENTS=? WHERE ID=?", (box_comments.get('1.0','end'), data1.get())) 
		messagebox.showinfo("SUCCESS", "The Patient ID was UPdate..")
		data0.set("")
		data1.set("")
		data2.set("")
		data3.set("")
		data4.set("")
		data5.set("")
		data6.set("")
		data7.set("")
		box_comments.delete('1.0', END)
	else: messagebox.showinfo("WARNING", "Please, read an Patient ID first..")
	
#____DELETE PATIENT IN DDBB_______________________________________________________________________
@assistant_funtion	# we call the decorator function to connect with the DDBB
def delete_ddbb():
	if data1.get() != "":
		Cursor.execute("DELETE FROM RRHH WHERE ID = %s" % (data1.get()))  	# The "%s" token allows me to insert (and potentially format) a string. Notice that the %s token is replaced by whatever I pass to the string after the % symbol.
		messagebox.showinfo("SUCCESS", "The Patient ID in DB was DELETE..")
		data0.set("")
		data1.set("")
		data2.set("")
		data3.set("")
		data4.set("")
		data5.set("")
		data6.set("")
		data7.set("")
		box_comments.delete('1.0', END)
	else: messagebox.showinfo("WARNING", "Please, read an Patient ID first..")

# ____CLEAR FIELDS_____________________________________________________________________
def clear_fields():
	data0.set("")
	data1.set("")
	data2.set("")
	data3.set("")
	data4.set("")
	data5.set("")
	data6.set("")
	data7.set("")
	box_comments.delete('1.0', END)
	
#____EXIT___________________________________________________________________
def exit():
	valor_exit=messagebox.askokcancel("WARNING", "Are you shure do you want to EXIT?")
	if valor_exit==True:
		root.destroy()

#___HELP - About DDBB________________________________________________________
def about_ddbb():
	messagebox.showinfo("MEDICO_DB", "DDBB ÉXITO TROPICAL \n Registered with Ing. Flavio Monti \n Copyright # 1988 - 2021..")

#___HELP - License________________________________________________________
def license_ddbb():
	messagebox.showinfo("License", "Free license under the rights of Ing. Flavio Monti \n Since 2021..")

#________________________________________________________________________________________________________________________________________________
#------------------------------------------------------------------------------------------------------------------------------------------------

#--------MENU---------
bar_menu=Menu(root) 	# Declare "bar_menu" is the name of menu
root.config(menu=bar_menu) #, width="200", height="300"

#______BAR MENU___________________________________________________________________________________
ddbb_menu=Menu(bar_menu, tearoff=0)
bar_menu.add_cascade(label="DDBB", menu=ddbb_menu)
ddbb_menu.add_command(label="Conect DB", command=conect_ddbb)
ddbb_menu.add_command(label="Exit", command=exit)

delete_menu=Menu(bar_menu, tearoff=0)
bar_menu.add_cascade(label="Options", menu=delete_menu)
delete_menu.add_command(label="Clear fields", command=clear_fields)

crud_menu=Menu(bar_menu, tearoff=0)
bar_menu.add_cascade(label="CRUD", menu=crud_menu)
crud_menu.add_command(label="Create", command=create_ddbb)
crud_menu.add_command(label="Read", command=read_ddbb)
crud_menu.add_command(label="Update", command=update_ddbb)
crud_menu.add_command(label="Delete Patient", command=delete_ddbb)

help_menu=Menu(bar_menu, tearoff=0)
bar_menu.add_cascade(label="HELP", menu=help_menu)
help_menu.add_command(label="License", command=license_ddbb)
help_menu.add_command(label="Abaut DDBB", command=about_ddbb)

#________________________________________________________________________________________________________________________________________________
#------------------------------------------------------------------------------------------------------------------------------------------------

#___ HELLOW USER!
label_ID=Label(myframe, fg="red", text="WELCOME TO MEDICO_DB", font=("trajan", 22))
label_ID.grid(row=0, column=0, padx="3", pady="3")

#___DATE
label_ID=Label(myframe, text="DATE (dd/mm/aaaa)", font=("arial", 12))
label_ID.grid(row=2, column=0, padx="3", pady="3")
box_ID=Entry(myframe, width=40, textvariable=data0)
box_ID.grid(row=2, column=1, padx="3", pady="3")

#___ID
label_ID=Label(myframe, text="ID (DNI)", font=("arial", 12))
label_ID.grid(row=3, column=0, padx="3", pady="3")
box_ID=Entry(myframe, width=40, textvariable=data1)
box_ID.grid(row=3, column=1, padx="3", pady="3")

#___NAME
label_name=Label(myframe, text="Patient Name", font=("arial", 12))
label_name.grid(row=4, column=0, padx="3", pady="3")
box_name=Entry(myframe, width=40, textvariable=data2)
box_name.grid(row=4, column=1, padx="3", pady="3")

#___LAST NAME
label_lastname=Label(myframe, text="Patient Last Name", font=("arial", 12))
label_lastname.grid(row=5, column=0, padx="3", pady="3")
box_lastname=Entry(myframe, width=40, textvariable=data3)
box_lastname.grid(row=5, column=1, padx="3", pady="3")

#___DATE OF BIRTH
label_email=Label(myframe, text="Patient Date of Birth (dd/mm/aaaa)", font=("arial", 12))
label_email.grid(row=6, column=0, padx="3", pady="3")
box_email=Entry(myframe, width=40, textvariable=data4)
box_email.grid(row=6, column=1, padx="3", pady="3")

#___AGE
label_password=Label(myframe, text="Patient Age", font=("arial", 12))
label_password.grid(row=7, column=0, padx="3", pady="3")
box_password=Entry(myframe, width=40, textvariable=data5)
box_password.grid(row=7, column=1, padx="3", pady="3")

#___TELEPHONE
label_password=Label(myframe, text="Patient Tell/Cell", font=("arial", 12))
label_password.grid(row=8, column=0, padx="3", pady="3")
box_password=Entry(myframe, width=40, textvariable=data6)
box_password.grid(row=8, column=1, padx="3", pady="3")

#___ADRESS
label_password=Label(myframe, text="Patient Adress", font=("arial", 12))
label_password.grid(row=9, column=0, padx="3", pady="3")
box_password=Entry(myframe, width=40, textvariable=data7)
box_password.grid(row=9, column=1, padx="3", pady="3")

#___TYPE OF STUDY
label_comments=Label(myframe, text="Type of Study (Obs)", font=("arial", 12))
label_comments.grid(row=10, column=0, padx="8", pady="8")
box_comments=Text(myframe, width="50", height="5", fg="brown")
box_comments.grid(row=10, column=1, padx="8", pady="8")
scroll=Scrollbar(myframe, command=box_comments.yview)	# Generate scroll bar
scroll.grid(row=10, column=2, sticky="nsew") 	# sticky generate the lengh of the bar in all cardinal points (all height row)
box_comments.config(yscrollcommand=scroll.set)	# yscrollcommand hace que la barra te ubique en la pocision en la que estas del texto

#________________________________________________________________________________________________________________________________________________
#------------------------------------------------------------------------------------------------------------------------------------------------
#___BUTTON CONNECT
button_ddbb=Button(myframe, text="CONNECT to DB", bg="yellow", command=conect_ddbb, height="2", font = "bold")
button_ddbb.grid(row=1, column=4, padx="0", pady="3")

#___BUTTON CREATE
button_ddbb=Button(myframe, text="CREATE PATIENT", bg="light blue", command=create_ddbb)
button_ddbb.grid(row=11, column=0, padx="3", pady="3")

#___BUTTON CLEAR
button_delete=Button(myframe, text="CLEAR FILELDS", bg="light blue", command=clear_fields)
button_delete.grid(row=11, column=1, sticky="w", padx="3", pady="3")

#___BUTTON READ
button_CRUD=Button(myframe, text="READ 'ID' PATIENT", bg="light blue", command=read_ddbb)
button_CRUD.grid(row=11, column=1, padx="3", pady="3")

#___BUTTON UPDATE
button_HELP=Button(myframe, text="UPdate PATIENT", bg="light blue", command=update_ddbb)
button_HELP.grid(row=11, column=1, sticky="e", padx="3", pady="3")

#________________________________________________________________________________________________________________________________________________
#------------------------------------------------------------------------------------------------------------------------------------------------

#___CREATE A DB IN WORKBOOK AND ADD A WORKSHEET OF EXCEL.
@assistant_funtion	# we call the decorator function to connect with the DDBB
def bookexcel():
	workbook = xlsxwriter.Workbook("db_Médico.xlsx")	# Workbook
	worksheet = workbook.add_worksheet()				# Worksheet
	Cursor.execute("SELECT * FROM RRHH")
	selection=Cursor.fetchall()
	worksheet.write('B1', 'DATE OF STUDY')
	worksheet.write('C1', 'PATIENT ID')
	worksheet.write('D1', 'PATIENT NAME')
	worksheet.write('E1', 'PATIENT SURNAME')
	worksheet.write('F1', 'DATE OF BIRTH')
	worksheet.write('G1', 'PATIENT AGE')
	worksheet.write('H1', 'PATIENT TEL')
	worksheet.write('I1', 'PATIENT ADRESS')
	worksheet.write('J1', 'TYPE OF STUDY - OBS')
	row = 1
	col = 1
	for index, tuple in enumerate(selection):
		worksheet.write(row, col, tuple[0])
		worksheet.write(row, col+1, tuple[1])
		worksheet.write(row, col+2, tuple[2])
		worksheet.write(row, col+3, tuple[3])
		worksheet.write(row, col+4, tuple[4])
		worksheet.write(row, col+5, tuple[5])
		worksheet.write(row, col+6, tuple[6])
		worksheet.write(row, col+7, tuple[7])
		worksheet.write(row, col+8, tuple[8])
		row+=1
	workbook.close()


#___BUTTON GO TO DB in Excel.
button_ddbb=Button(myframe, text="Generate Excel DB", bg="light green", height="2", font = "bold", command= bookexcel) 
button_ddbb.grid(row=13, column=4, padx="0", pady="3")




root.mainloop()


			
		