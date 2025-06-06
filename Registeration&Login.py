import mysql.connector
data = None
def connection():
    global data
    try:
        data = mysql.connector.connect(host='localhost',username='root',password='HKSahSe@79',database='user_database')
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
        query = """Create Table If Not Exists user_registeration_details(
            user_first_name varchar(50) NOT NULL ,
            user_last_name varchar (50),
            user_email_id varchar(50) UNIQUE ,
            user_phone_no char(10) PRIMARY KEY,
            check (user_phone_no REGEXP '^[1-9][0-9]{9}$'),
            user_gender ENUM('M','F','O'),
            user_password varchar(255) NOT NULL
            );"""
        my_cursor.execute(query)

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
        else:
            print("wrong username or password")
    else:
        print("No database connection available.")      
        

def main():
    connection()
    print("Register(R) OR Login(L)")
    User_input = input("Enter (R/L)")
    if User_input == 'R':
        registeration()
    elif User_input == 'L':
        login()
    else:
        print("wrong Input")
    
    
if __name__ == "__main__":
    main()
