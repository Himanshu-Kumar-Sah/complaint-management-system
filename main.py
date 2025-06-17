import mysql.connector
import config
from datetime import datetime
from db_setup import create_tables
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
    complain = input("Personal[P] or Community(all)[C]".capitalize())
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
                print(f"Complaint ID   : {row[0]}")
                print(f"Phone Number   : {row[1]}")
                print(f"Type           : {row[2]}")
                print(f"Description    : {row[3]}")
                print(f"Priority       : {row[4]}")
                print(f"Date & Time    : {row[5]}")
                print(f"Status         : {row[6]}")
                print(f"Scope          : {row[7]}")
                print(f"Location       : {row[8] if row[8] else 'N/A'}")
                print(f"Assigned To    : {row[9]}")
                print("-" * 40)
        else:
            print("No complaints found.")

        my_cursor.close()
    else:
        print("No database connection.")


def user_dashboard(user_phone_no):
    while True:
        print(f"\n--- User Dashboard ({user_phone_no}) ---")
        print("1. Add Address")
        print("2. Add Complaint")
        print("3. View Complaint Status")
        print("4. Logout")
        choice = input("Choose an option (1-4): ")
        if choice == '1':
            Add_Address(user_phone_no)
        elif choice == '2':
            Add_complain(user_phone_no)
        elif choice == '3':
            view_complain(user_phone_no)
        elif choice == '4':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def main_menu():
    while True:
        print("\n--- Welcome to Complaint Management System ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")
        if choice == '1':
            registeration()
        elif choice == '2':
            phone_no = login()
            if phone_no:
                user_dashboard(phone_no)
        elif choice == '3':
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
