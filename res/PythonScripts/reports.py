from flask import redirect, url_for, render_template


def QuarterlyReportFunction(request, db_details, database_instance, session):
    if ('mode' not in session) or (session['mode'] != 'Main_manager'):
        msg = "You need to be a Main manager to see this report"
        url = 'login'
        return render_template('popupMsg.html', msg=msg, url=url)
    else:
        login = True
        myCursor1 = database_instance.cursor()
        if request.method == 'POST' and 'required_year' in request.form:
            yearOfReport = request.form['required_year']
        else:
            yearOfReport = 2023
        args = (yearOfReport, 0, 0, 0, 0)
        revenues = myCursor1.callproc('GetRevenueOfEachQuarterGivenYear', args)
        print("revenues : ", revenues)
        return render_template('reports/quarterly_report_for_year.html', login=login, revenues=revenues[1:], yearOfReport=yearOfReport)


def ItemsWithMostOrdersFunction(request, database_instance, session):
    if ('mode' not in session) or (session['mode'] != 'Main_manager'):
        msg = "You need to be a Main manager to see this report"
        url = 'login'
        return render_template('popupMsg.html', msg=msg, url=url)
    else:
        login = True
        myCursor1 = database_instance.cursor()
        myCursor1.execute("select * from items_with_most_orders ")
        items = myCursor1.fetchall()
        print(items)
        return render_template('reports/items_with_most_orders.html', login=login, items=items)


def SalesReportOfStoresFunction(request, database_instance, session):
    if 'store_manager_store' not in session:
        return redirect(url_for('logout'))
    store_name = session['store_manager_store']
    cursor1 = database_instance.cursor()
    cursor1.execute('SELECT route_id, revenue_of_route FROM route_revenue_view WHERE store_name= %s',(store_name,))
    route_revenue_data_list = cursor1.fetchall()
    return render_template('reports/sales_report_of_stores.html', route_revenue_data_list=route_revenue_data_list, store_name=store_name)


def UsedHoursOfTrucksFunction(request, database_instance, session):
    if 'store_manager_store' not in session:
        return redirect(url_for('logout'))
    store_name = session['store_manager_store']
    cursor1 = database_instance.cursor()
    cursor1.execute('SELECT truck_id, used_hours FROM trucks_used_hours WHERE store_name= %s',(store_name,))
    truck_used_hours_data_list = cursor1.fetchall()
    return render_template('reports/trucks_used_hours.html', truck_used_hours_data_list=truck_used_hours_data_list, store_name=store_name)


def GetWorkingHoursOfDriversFunction(request, database_instance, session):
    store_name = session['store_manager_store']
    cursor1 = database_instance.cursor()
    cursor1.execute('SELECT driver_id, driver_name, sum(working_hours) FROM driver_working_hours natural join driver where store_name= %s group by driver_id', (store_name,))
    working_hours_data_list = cursor1.fetchall()
    return render_template('reports/working_hours_of_drivers.html', working_hours_data_list=working_hours_data_list, store_name=store_name)


def GetWorkingHoursOfDriverAssistantsFunction(request, database_instance, session):
    store_name = session['store_manager_store']
    cursor1 = database_instance.cursor()
    cursor1.execute('SELECT driver_assistant_id, driver_assistant_name, sum(working_hours) FROM driver_assistant_working_hours natural join driver_assistant where store_name= %s group by driver_assistant_id', (store_name,))
    working_hours_data_list = cursor1.fetchall()
    return render_template('reports/working_hours_of_driver_assistants.html', working_hours_data_list=working_hours_data_list, store_name=store_name)


def GenerateCustomerReportFunction(request, database_instance, session):
    if request.method == 'POST' and 'required_customer_id' in request.form:
        required_customer_id = request.form['required_customer_id']
        cursor1 = database_instance.cursor()
        args = (required_customer_id, '', '', '', 0, 0, 0, 0)
        customer_report_data = cursor1.callproc('CustomerOrderReport', args)
        return render_template('reports/customer_report_generator.html', customer_report_data=customer_report_data)
    else:
        return render_template('reports/customer_report_generator.html', customer_report_data=('N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'))