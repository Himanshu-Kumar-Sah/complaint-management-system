cursor.execute("""Alter Table user_complaints_details
    #                MODIFY Column woker_phone_no char(10) default 'N/A' ;""")