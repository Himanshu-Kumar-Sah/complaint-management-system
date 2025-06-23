import mysql.connector
import config
from datetime import datetime
from db_setup import create_tables  
from tabulate import tabulate
data = None
def connection():
    global data
    try:
        data = mysql.connector.connect(
        host=config.DB_HOST,
        username=config.DB_USER,
        password=config.DB_PASS,
        database=config.DB_NAME
        )
        print("Database connected successfully")
    except mysql.connector.Error as err:
        print("Error connecting to database:", err)
        data = None


def registeration():
    user_first_name = input("Enter Yours First Name :")
    user_last_name = input("Enter Yours Last Name: ")
    user_email_id = input("Enter Yours E-mail Id: ")
    user_phone_no = input("Enter Yours Phone No.: ")
    user_gender = input("Enter Yours Gender(M/F/O): ")
    user_password = input("Enter Yours Password: ")

    if data:
        my_cursor = data.cursor()
        insert_query = "INSERT INTO user_registeration_details (user_first_name, user_last_name, user_email_id, user_phone_no, user_gender, user_password) Values (%s,%s,%s,%s,%s,%s)"
        my_cursor.execute(insert_query,(user_first_name, user_last_name, user_email_id, user_phone_no, user_gender, user_password))
        data.commit()
        my_cursor.close()
        print("Registration successful.")
    else:
        print("No database connection available.")
    

def login():
    user_phone_no = input("Enter User Phone No. : ")
    user_password = input("Enter Yours Password: ")
    if data:
        my_cursor = data.cursor()
        query = """SELECT user_phone_no
        FROM user_registeration_details
        WHERE user_phone_no = %s AND user_password = %s;"""
        my_cursor.execute(query, (user_phone_no,user_password))
        result = my_cursor.fetchone()
        my_cursor.close()
        if result:
            print("welcome")
            return user_phone_no
        else:
            print("wrong username or password")
            return None
    else:
        print("No database connection available.")    
        return None  
        

def Add_Address(user_phone_no):
    house_no = int(input("Yours House No. : "))
    tower = input("Yours Tower No. : ")
    floor = int(input("Yours Floor No. "))
    locality = input("Locality : ")
    area = input("Area : ")
    city = input("City : ")
    state = input("State : ")
    pincode = int(input("Pincode : "))

    if data:
        my_cursor = data.cursor()
        insert_query = """INSERT INTO user_address_details (
            user_phone_no, user_house_no, user_tower_no, user_floor_no,
            user_locality, user_area, user_city, user_state, user_pincode
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        my_cursor.execute(insert_query,(user_phone_no, house_no, tower, floor, locality, area, city, state, pincode))
        data.commit()
        my_cursor.close()
        print("Address Added successful.")
    else:
        print("No database connection available.")


def Add_complain(user_phone_no):
    complain = input("Personal[P] or Community(all)[C]".upper())
    if complain == "P" or complain == "C":
        if complain == "P":
            if data:
                my_cursor = data.cursor()
                query = """Select user_phone_no FROM user_address_details where user_phone_no = %s"""
                my_cursor.execute(query, (user_phone_no,))
                result = my_cursor.fetchone()
                my_cursor.close()
                if not result:
                    print("Please add your address before submitting a personal complaint.")
                    Add_Address(user_phone_no)
                    my_cursor = data.cursor()
                    my_cursor.execute(query, (user_phone_no,))
                    result = my_cursor.fetchone()
                    my_cursor.close()
                    if not result:
                        print("Address not added. Complaint aborted.")
                        return 
        complain_type = input("Enter Complaint Type :")
        complain_description = input("Enter Complaint Description : ")
        complain_priority = input("Priority (Urgent/Normal) : ")
        complaint_datetime = datetime.now()
        complain_status = "Pending"
        if complain == "C":
            location = input("Enter Location: ")
        else:
            location = None

        if data:
            my_cursor = data.cursor()
            insert_query = """INSERT INTO user_complaints_details (
                    user_phone_no, complaint_type, complaint_desc, complaint_priority, complaint_datetime, status, complaint_scope, location, assigned_to
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

            my_cursor.execute(insert_query, (
                    user_phone_no, complain_type, complain_description, complain_priority, complaint_datetime,
                    complain_status, 'Personal' if complain == 'P' else 'Community', location, 'Not Assigned'
                ))

            data.commit()
            my_cursor.close()
            print("Complaint added successfully.")
        else:
            print("No database connection available.")
    else:
        print("Wrong input. Please enter P for Personal or C for Community.")


def view_complain(user_phone_no):
    if data:
        my_cursor = data.cursor()
        query = "Select * from user_complaints_details where user_phone_no = %s"
        my_cursor.execute(query,(user_phone_no,))
        results = my_cursor.fetchall()
        if results:
            print("\n--- Your Complaints ---\n")
            for row in results:
                print(f"Complaint ID    : {row[0]}")
                print(f"Phone Number    : {row[1]}")
                print(f"Type            : {row[2]}")
                print(f"Description     : {row[3]}")
                print(f"Priority        : {row[4]}")
                print(f"Date & Time     : {row[5]}")
                print(f"Status          : {row[6]}")
                print(f"Scope           : {row[7]}")
                print(f"Location        : {row[8] if row[8] else 'N/A'}")
                print(f"Assigned To     : {row[9]}")
                print(f"Worker Phone no.: {row[10] if row[10] else 'N/A'}")
                print("-" * 40)
            my_cursor.close()
        else:
            print("No complaints found.")

        my_cursor.close()
    else:
        print("No database connection.")

def give_feedback(user_phone_no):
    if data:
        my_cursor = data.cursor()
        query = """ SELECT complaint_id, complaint_desc FROM user_complaints_details
        WHERE user_phone_no = %s AND status = 'Resolved' AND feedback_rating IS NULL"""
        my_cursor.execute(query,(user_phone_no,))
        results = my_cursor.fetchall()
        if not results:
            print("No resolved complaints available for feedback.")
            my_cursor.close()
            return
        
        print("\n--- Resolved Complaints Pending Feedback ---\n")
        for row in results:
            print(f"Complaint ID    : {row[0]}")
            print(f"Description     : {row[1]}")
            print("-" * 40)

        complaint_id = int(input("Enter Complaint id for feedback : "))
        feedback_rating = int(input("Enter the Feedback in rating(1-5): "))
        if feedback_rating not in [1, 2, 3, 4, 5]:
            print("Invalid rating. Please enter a number between 1 and 5.")
            my_cursor.close()
            return
        feedback_text = input("Enter feedback on your complaint : ")

        update_query = """UPDATE user_complaints_details
                        SET feedback_rating = %s ,feedback_text = %s
                        WHERE complaint_id = %s AND user_phone_no = %s"""
        my_cursor.execute(update_query,(feedback_rating, feedback_text, complaint_id,user_phone_no))
        print("Thank you for your feedback.")
        data.commit()
        my_cursor.close()
    else:
        print("Database not connected.")    
        
        

def user_dashboard(user_phone_no):
    while True:
        print(f"\n--- User Dashboard ({user_phone_no}) ---")
        print("1. Add Address")
        print("2. Add Complaint")
        print("3. View Complaint Status")
        print("4. Give Feedback ")     
        print("5. Logout")
        choice = input("Choose an option (1-4): ")
        if choice == '1':
            Add_Address(user_phone_no)
        elif choice == '2':
            Add_complain(user_phone_no)
        elif choice == '3':
            view_complain(user_phone_no)
        elif choice == '4':
            give_feedback(user_phone_no)
        elif choice == '5':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")




def Admin_login():
    admin_username = input("Enter Admin Username : ")
    admin_password = input("Enter Admin Password: ")
    if data:
        my_cursor = data.cursor()
        query = """SELECT admin_username
        FROM admin_details
        WHERE admin_username = %s AND admin_password = %s;"""
        my_cursor.execute(query, (admin_username,admin_password))
        result = my_cursor.fetchone()
        my_cursor.close()
        if result:
            print("welcome")
            return admin_username
        else:
            print("wrong username or password")
            return None
    else:
        print("No database connection available.")    
        return None  
    

def view_all_complaints():
    if data:
        cursor = data.cursor()
        query = """Select complaint_id, user_phone_no, complaint_type, complaint_desc, 
                   complaint_priority, complaint_datetime, status, complaint_scope, 
                   location, assigned_to  from user_complaints_details"""
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        if result:
            headers = ["Complaint ID", "Phone No.", "Type", "Description", "Priority", "Date&Time", "Status", "Scope", "Location", "Assigned To"]
            print("\n--- All Complaints ---\n")
            print(tabulate(result, headers=headers, tablefmt="fancy_grid"))
            
        else:
            print("No complaints found.")
    else:
        print("Database not connected.")


def add_worker():
    if data:
        worker_name = input("Enter Worker Name:")
        worker_phone_no  = int(input("Enter Worker Phone No.:"))
        worker_password = input("Enter Worker Password:")
        specialization = input("Worker specialization: ")

        my_cursor = data.cursor()
        query = """INSERT INTO workers_details (worker_name, worker_phone_no, worker_password, specialization)
                   VALUES (%s, %s, %s, %s)"""
        my_cursor.execute(query,(worker_name, worker_phone_no, worker_password, specialization)) 
        data.commit()
        my_cursor.close()
        print("Worker added successfully.")
    else:
        print("No database connection available.")

def assign_complaint():
    if data:
        my_cursor = data.cursor()
        my_cursor.execute("SELECT complaint_id, complaint_type, complaint_scope, location FROM user_complaints_details WHERE assigned_to = 'Not Assigned'")
        complaints = my_cursor.fetchall()

        if not complaints:
            print("No unassigned complaints available.")
            return

        print(tabulate(complaints, headers=["ID", "Type", "Scope", "Location"], tablefmt="fancy_grid"))

        complaint_id = int(input("Enter Complaint id to be assign: "))

        my_cursor.execute("SELECT worker_id, worker_name, specialization FROM workers_details")
        workers = my_cursor.fetchall()
        print(tabulate(workers, headers=["Worker ID", "Name", "Specialization"], tablefmt="fancy_grid"))

        worker_id = int(input("Enter Worker ID to assign this complaint to: "))

        my_cursor.execute("Select worker_name, worker_phone_no From workers_details where worker_id = %s",(worker_id,))
        result = my_cursor.fetchone()
        if not result:
            print("Invalid worker ID.")
            return
        worker_name = result[0]
        worker_phone_no = result[1]

        update_query = """UPDATE user_complaints_details SET assigned_to = %s,worker_phone_no = %s , status = 'In Progress' Where complaint_id = %s"""
        my_cursor.execute(update_query,(worker_name,worker_phone_no,complaint_id))
        data.commit()
        print(f"Complaint ID {complaint_id} assigned to {worker_name}.")
        my_cursor.close()
    else:
        print("Database not connected.")

def update_complaint_status():
    if data:
        my_cursor = data.cursor()
        complaint_id = int(input("Enter Complaint id to Update: "))
        my_cursor.execute("Select complaint_id,status From user_complaints_details where complaint_id = %s",(complaint_id,))
        result = my_cursor.fetchone()
        if not result:
            print("Invalid Complaint ID.")
            return
        Current_Status = result[1]
        print(f"Current Status of {complaint_id} is : {Current_Status}. ")
        New_Status =  input("Enter new status [Pending/In Progress/Resolved]:").title()
        if New_Status not in ['Pending', 'In Progress', 'Resolved']:
            print("Invalid status. Please enter one of: Pending, In Progress, Resolved.")
            my_cursor.close()
            return
        update_query = """UPDATE user_complaints_details SET status = %s Where complaint_id = %s"""
        my_cursor.execute(update_query,(New_Status,complaint_id))
        data.commit()
        print("Complaint status updated.")
        my_cursor.close()
    else:
        print("Database not connected.")



def admin_dashboard(admin_username):
    while True:
        print(f"\n--- Admin Dashboard ({admin_username}) ---")
        print("1. View All Complaints")
        print("2. Assign Complaint to Workers")
        print("3. Update Complaint Status")
        print("4. Logout")
        print("5. Add Woker")
        
        choice = input("Choose an option (1-4): ")
        if choice == '1':
            view_all_complaints()
        elif choice == '2':
            assign_complaint()
        elif choice == '3':
            update_complaint_status()
        elif choice == '4':
            print("Logging out...")
            break
        elif choice == '5':
            add_worker()
        else:
            print("Invalid choice. Try again.")


def Worker_login():
    worker_phone_no = input("Enter Worker Phone no. : ")
    worker_password = input("Enter Worker Password: ")
    if data:
        my_cursor = data.cursor()
        query = """SELECT worker_phone_no
        FROM workers_details
        WHERE worker_phone_no = %s AND worker_password = %s;"""
        my_cursor.execute(query, (worker_phone_no ,worker_password))
        result = my_cursor.fetchone()
        my_cursor.close()
        if result:
            print("welcome")
            return worker_phone_no
        else:
            print("wrong username or password")
            return None
    else:
        print("No database connection available.")    
        return None  
    
def view_assigned_complaints(worker_phone_no):
    if data:
        my_cursor = data.cursor()
        query = """Select complaint_id, user_phone_no, complaint_type, complaint_desc, 
               complaint_priority, complaint_scope, location from user_complaints_details where worker_phone_no = %s"""
        my_cursor.execute(query, (worker_phone_no,))
        complaints = my_cursor.fetchall()
        if not complaints:
            print("No complaints assigned.")
            my_cursor.close()
            return
        print("\n--- Assigned Complaints ---\n")
        for complaint in complaints:
            complaint_id, phone_no, type_, desc, priority, scope, location = complaint
            print(f"Complaint ID   : {complaint_id}")
            print(f"Phone Number   : {phone_no}")
            print(f"Type           : {type_}")
            print(f"Description    : {desc}")
            print(f"Priority       : {priority}")
            print(f"Scope          : {scope}")
            print("-" * 40)
            if scope == 'Community':
                    print(f"Location       : {location if location else 'N/A'}")
            elif scope == 'Personal':
                addr_query = """
                    SELECT user_house_no, user_tower_no, user_floor_no, 
                           user_locality, user_area, user_city, user_state, user_pincode
                    FROM user_address_details
                    WHERE user_phone_no = %s"""
        my_cursor.execute(addr_query, (phone_no,))
        addr = my_cursor.fetchone()
        if addr:
                house_no, tower, floor, locality, area, city, state, pincode = addr
                print(f"Address        : House {house_no}, Tower {tower}, Floor {floor},")
                print(f"                 {locality}, {area}, {city}, {state} - {pincode}")
        else:
                print("Address        : [Not Available]")
                print("-" * 40)
        
        my_cursor.close()
    else:
        print("Database not connected.")


def update_assigned_complaint_status(worker_phone_no):
    if data:
        my_cursor = data.cursor()
        my_cursor.execute("SELECT complaint_id, complaint_type, complaint_scope FROM user_complaints_details WHERE worker_phone_no = %s",(worker_phone_no,))
        complaints = my_cursor.fetchall()

        if not complaints:
            print("No unassigned complaints available.")
            return

        print(tabulate(complaints, headers=["ID", "Type", "Scope"], tablefmt="fancy_grid"))

        complaint_id = int(input("Enter Complaint id to Update: "))
        my_cursor.execute("Select complaint_id,status From user_complaints_details where complaint_id = %s AND worker_phone_no = %s",(complaint_id ,worker_phone_no))
        result = my_cursor.fetchone()
        if not result:
            print("Invalid Complaint ID.")
            return
        Current_Status = result[1]
        print(f"Current Status of {complaint_id} is : {Current_Status}. ")
        New_Status =  input("Enter new status [Pending/In Progress/Resolved]:").title()
        if New_Status not in ['Pending', 'In Progress', 'Resolved']:
            print("Invalid status. Please enter one of: Pending, In Progress, Resolved.")
            my_cursor.close()
            return
        update_query = """UPDATE user_complaints_details SET status = %s Where complaint_id = %s"""
        my_cursor.execute(update_query,(New_Status,complaint_id))
        data.commit()
        print("Complaint status updated.")
        my_cursor.close()
    else:
        print("Database not connected.")

def worker_dashboard(worker_phone_no):
    while True:
        print(f"\n--- Worker Dashboard ({worker_phone_no}) ---")
        print("1. View Assigned Complaints")
        print("2. Update Complaint Status")
        print("3. Logout")
        
        choice = input("Choose an option (1-3): ")
        if choice == '1':
            view_assigned_complaints(worker_phone_no)
        elif choice == '2':
            update_assigned_complaint_status(worker_phone_no)
        elif choice == '3':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")


def main_menu():
    while True:
        print("\n--- Welcome to Complaint Management System ---")
        print("1. Register as User")
        print("2. Login as User")
        print("3. Login as Admin")
        print("4. Login as Worker")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")
        if choice == '1':
            registeration()
        elif choice == '2':
            phone_no = login()
            if phone_no:
                user_dashboard(phone_no)
        elif choice == '3':
            admin_username = Admin_login()
            if admin_username:
                admin_dashboard(admin_username) 
        elif choice == '4':
            worker_phone_no = Worker_login()
            if worker_phone_no:
                worker_dashboard(worker_phone_no)
        elif choice == '5':
            print("Exiting. Thank you!")
            break
        else:
            print("Invalid input. Try again.")

def main():
    connection()
    if data:
        create_tables(data)
        main_menu()

    
if __name__ == "__main__":
    main()
