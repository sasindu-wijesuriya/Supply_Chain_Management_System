import mysql.connector
import hashlib


def addRecordsToATable(db_details, table_name, records_details_list):
    """
    HOW TO CALL THE FUNCTION (Example)
    records_data_list = [('end', 0.0, 1), ('ret', 0.2, 100), ('whole', 0.3, 6)]
    utils.addRecordsToATable(db_details, "customer_type", records_data_list)
    """
    print("Adding records to the table " + table_name + ":\n" + str(records_details_list))
    query_entering_sample_data = "INSERT INTO " + table_name + " VALUES ("
    for i in range(len(records_details_list[0]) - 1):
        query_entering_sample_data += "%s,"
    query_entering_sample_data += "%s);"
    database_instance = mysql.connector.connect(**db_details)
    my_cursor_add_records_to_a_table = database_instance.cursor()
    try:
        my_cursor_add_records_to_a_table.executemany(query_entering_sample_data, records_details_list)
        database_instance.commit()
        print("\nEntering Record(s) Successful")
    except Exception as e:
        print("Exception Occurred")
        print(e)
    my_cursor_add_records_to_a_table.close()
    database_instance.close()


def callProcedure(db_details, procedure_name, parameters_list):
    """
    :param db_details:
    :param procedure_name:
    :param parameters_list as a tuple:
    :return:
    """

    query_calling_procedure = "CALL " + db_details['database'] + '.' + procedure_name + str(parameters_list) + ';'
    print(query_calling_procedure)
    database_instance = mysql.connector.connect(**db_details)
    my_cursor_call_procedure = database_instance.cursor()
    try:
        my_cursor_call_procedure.execute(query_calling_procedure)
        database_instance.commit()
        print("\nCalling procedure " + procedure_name + " Successful")
    except Exception as e:
        print("Exception Occurred")
        print(e)
    my_cursor_call_procedure.close()
    database_instance.close()


def hashPassword(password):
    """returns the hashed password as a string of 32 bits"""
    salt = "DBGroupProject"
    database_password = password + salt
    hashed = hashlib.md5(database_password.encode())
    return hashed.hexdigest()
