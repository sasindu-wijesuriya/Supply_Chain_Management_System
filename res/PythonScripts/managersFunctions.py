from datetime import date

from flask import redirect, url_for, render_template


def storeManagerFunction(database_instance, session, request):
    if 'mode' not in session:
        return redirect(url_for('home'))


    elif session['mode'] != 'Store_manager':
        return redirect(url_for('logout'))


    elif request.method == 'POST' and 'store_manager_store' in request.form:
        store_manager_store = request.form['store_manager_store']
        store_manager_id = session['store_manager_id']

        # getting stores list to check the validity of the store
        cursor1 = database_instance.cursor()
        cursor1.execute('SELECT store_name FROM store')
        stores_list = cursor1.fetchall()
        for store_tuple in stores_list:
            if store_manager_store in store_tuple:
                break
        else:
            return render_template('login.html', error="Invalid Store Entered!!! Please login again.")

        session['store_manager_store'] = store_manager_store
        print("Store Manager Store :", store_manager_store)
        cursor = database_instance.cursor()
        cursor.execute('UPDATE store_manager set store= %s WHERE store_manager.manager_id = %s', (store_manager_store, store_manager_id))
        database_instance.commit()
        return render_template('manager/storemanager_index.html', store=store_manager_store, store_manager_id=store_manager_id)


    elif 'store_manager_store' in session:
        store_manager_id = session['store_manager_id']
        store_manager_store = session['store_manager_store']
        return render_template('manager/storemanager_index.html', store=store_manager_store, store_manager_id=store_manager_id)

    else:
        return redirect(url_for('logout'))


def mainManagerFunction(database_instance, session, request):
    if 'main_manager_id' in session:
        main_manager_id = session['main_manager_id']
        return render_template('manager/manager_index.html', main_manager_id=main_manager_id)
    else:
        return redirect(url_for('logout'))






def MainManagerDashBoardFunction():
    return render_template('manager/main_manager_dashboard.html')


def StoreManagerDashBoardFunction():
    return render_template('manager/store_manager_dashboard.html')


def trainSchedFunction(database_instance, session, request):
    if request.method == 'POST' and 'trainid' in request.form and 'departuretime' in request.form and 'departuredate' in request.form and 'availablecapacity' in request.form:
        cursor = database_instance.cursor()
        trainID = request.form['trainid']
        departureTime = request.form['departuretime']
        departureDate = request.form['departuredate']
        availableCapacity = request.form['availablecapacity']
        arrivalStation = request.form['arrivalstation']
        cursor.callproc('Add_Train_Schedule', [trainID, departureTime, departureDate, availableCapacity, arrivalStation])
        database_instance.commit()
        cursor.close()
        return redirect(url_for('trainsched'))
    cursor = database_instance.cursor()
    cursor.execute("SELECT * from train_schedule natural join arrival_station ")
    trains_in_schedule = cursor.fetchall()
    cursor.close()
    return render_template('manager/scheduletrain.html', trains_in_schedule=trains_in_schedule)


def truckSchedFunction():
    return 'schedule truck here'


def humanResFunction(database_instance, session, request):
    if request.method == 'POST' and 'drivername' in request.form and 'nic' in request.form and 'addressline1' in request.form and 'addressline2' in request.form:

        drivername = request.form['drivername']
        nic = request.form['nic']
        addressline1 = request.form['addressline1']
        addressline2 = request.form['addressline2']
        cursor = database_instance.cursor()
        cursor.callproc('Add_Driver', [drivername, nic, addressline1, addressline2])
        database_instance.commit()
        cursor.close()
        return redirect(url_for('humanres'))
    elif request.method == 'POST' and 'DELETE' in request.form:
        deletedrow = request.form['identifier']
        cursor = database_instance.cursor()
        cursor.execute('DELETE FROM driver WHERE driver_id = %s', (deletedrow,))
        cursor.close()
        return redirect(url_for('humanres'))
    if request.method == 'POST' and 'driverassistantname' in request.form and 'danic' in request.form and 'daaddressline1' in request.form and 'daaddressline2' in request.form:

        driverassistantname = request.form['driverassistantname']
        danic = request.form['danic']
        daaddressline1 = request.form['daaddressline1']
        daaddressline2 = request.form['daaddressline2']
        cursor = database_instance.cursor()
        cursor.callproc('Add_Driver_assistant', [driverassistantname, danic, daaddressline1, daaddressline2])
        database_instance.commit()
        cursor.close()
        return redirect(url_for('humanres'))
    elif request.method == 'POST' and 'DELETE2' in request.form:
        deletedrow = request.form['identifier']
        cursor = database_instance.cursor()
        cursor.execute('DELETE FROM driver_assistant WHERE driver_assistant_id = %s', (deletedrow,))
        cursor.close()
        return redirect(url_for('humanres'))
    cursor = database_instance.cursor()
    cursor.execute('SELECT * FROM driver')
    drivers = cursor.fetchall()
    cursor.close()
    cursor = database_instance.cursor()
    cursor.execute('SELECT * FROM driver_assistant')
    driversassistant = cursor.fetchall()
    cursor.close()
    return render_template('manager/humanres.html', drivers=drivers, driverassistant=driversassistant)


def logisticsFunction(database_instance, session, request):
    if request.method == 'POST' and 'driverid' in request.form and 'driverassid' in request.form and 'truckid' in request.form and 'routeid' in request.form and 'departuredate' in request.form and 'departuretime' in request.form:
        driverid = request.form['driverid']
        driverassid = request.form['driverassid']
        routeid = request.form['routeid']
        departuredate = request.form['departuredate']
        departuretime = request.form['departuretime']
        truckid = request.form['truckid']

        cursor = database_instance.cursor()
        print(driverid, departuredate)
        try:
            cursor.callproc('AddTruckSession', [int(truckid), int(driverid), int(driverassid), int(routeid), departuredate, departuretime])
            database_instance.commit()
        except Exception as e:
            msg=e
            url="logistics"
            return render_template('popupMsg.html', msg=msg, url=url)

        return redirect(url_for('logistics'))

    cursor = database_instance.cursor()
    cursor.execute("SELECT * from truck_schedule order by truck_session_id")
    schedules = cursor.fetchall()
    cursor.close()

    cursor1 = database_instance.cursor()
    cursor1.execute("SELECT * from truck where store_name = %s", (session["store_manager_store"],))
    availabletruck = cursor1.fetchall()
    cursor1.close()

    cursor2 = database_instance.cursor()
    cursor2.execute("SELECT * from driver where store_name = %s", (session["store_manager_store"],))
    availabledrivers = cursor2.fetchall()
    cursor2.close()

    cursor3 = database_instance.cursor()
    cursor3.execute("SELECT * from driver_assistant where store_name = %s", (session["store_manager_store"],))
    availabledriverassistants = cursor3.fetchall()
    cursor3.close()

    cursor4 = database_instance.cursor()
    cursor4.execute("SELECT * from route where store_name = %s", (session["store_manager_store"],))
    route_list = cursor4.fetchall()
    cursor4.close()

    return render_template('manager/logistics.html', schedules=schedules, availabletruck=availabletruck, availabledriver=availabledrivers, availabledriverassistant=availabledriverassistants, route_list=route_list)


# def pendingOrdersFunction():
#     return render_template('logistics.html')


def assetsFunction():
    return render_template('manager/assets.html')


def addProductsFunction(database_instance, session, request):
    if request.method == 'POST' and 'itemid' in request.form and 'itemname' in request.form and 'capacity' in request.form and 'price' in request.form and 'description' in request.form:
        itemid = request.form['itemid']
        itemname = request.form['itemname']
        capacity = request.form['capacity']
        price = request.form['price']
        description = request.form['description']
        cursor = database_instance.cursor()
        cursor.callproc('AddProduct', [int(itemid), itemname, float(capacity), float(price), description])
        database_instance.commit()
        cursor.close()
        return redirect(url_for('addproducts'))
    elif request.method == 'POST' and 'DELETE' in request.form:
        deletedrow = request.form['identifier']
        print(deletedrow)
        cursor = database_instance.cursor()
        cursor.execute('DELETE FROM items WHERE item_id = %s', (deletedrow,))
    cursor = database_instance.cursor()
    cursor.execute("SELECT * from items")
    items = cursor.fetchall()
    cursor.close()
    return render_template('manager/addproducts.html', items=items)


def addTrucksFunction(database_instance, session, request):
    if request.method == 'POST' and 'truckcapacity' in request.form and 'usedhours' in request.form and 'truckid' in request.form:
        truckcapacity = request.form['truckcapacity']
        truckid = request.form['truckid']
        usedhours = request.form['usedhours']
        store = request.form['store']
        cursor = database_instance.cursor()
        cursor.callproc('AddTruck', [float(truckcapacity), float(usedhours), str(store)])
        database_instance.commit()
        cursor.close()
        return redirect(url_for('addtrucks'))
    elif request.method == 'POST' and 'DELETE' in request.form:
        deletedrow = request.form['identifier']
        print(deletedrow)
        cursor = database_instance.cursor()
        cursor.execute('DELETE FROM truck WHERE truck_id = %s', (deletedrow,))
    cursor = database_instance.cursor()
    cursor.execute('SELECT * from truck')
    trucks = cursor.fetchall()
    return render_template('manager/addtrucks.html', trucks=trucks)


def ordersFunction(database_instance, session, request):
    if request.method == 'POST' and 'orderid' in request.form and 'trainschedule' in request.form:
        trainschedule = request.form['trainschedule']
        orderid = request.form['orderid']
        cursor = database_instance.cursor()

        try:
            cursor.callproc('OrderAssignToTrain', [int(orderid), int(trainschedule.split()[0])])
            database_instance.commit()
        except Exception as e:
            msg=e
            url="orders"
            return render_template('popupMsg.html', msg=msg, url=url)

        return redirect(url_for('orders'))
    cursor = database_instance.cursor()
    cursor.execute('SELECT * FROM manager_order_view')
    ordersview = cursor.fetchall()
    cursor.close()
    cursor = database_instance.cursor()
    cursor.execute('SELECT train_session_id,departure_date FROM train_schedule where departure_date > NOW()')
    traindropdown = cursor.fetchall()
    cursor.close()
    return render_template('manager/orders.html', ordersview=ordersview, traindropdown=traindropdown)


def pendingOrdersFunction(database_instance, session, request):
    if request.method == 'POST' and 'trucksessionid' in request.form and 'orderid' in request.form:
        trucksessionid = request.form['trucksessionid']
        orderid = request.form['orderid']
        cursor = database_instance.cursor()

        try:
            cursor.callproc("OrderAssignToTruck", [int(orderid), int(trucksessionid)])
        except Exception as e:
            msg=e
            url="pendingorders"
            return render_template('popupMsg.html', msg=msg, url=url)

        database_instance.commit()
        return redirect(url_for('pendingorders'))

    cursor = database_instance.cursor()
    cursor.execute("SELECT order_table.* FROM order_table NATURAL JOIN route WHERE store_name = %s",
                   (session['store_manager_store'],))
    pending_orders = cursor.fetchall()
    cursor.close()
    cursor = database_instance.cursor()
    today_date = date.today()
    cursor.execute("SELECT * FROM truck_schedule WHERE departure_date > %s", (today_date,))
    availabletruck = cursor.fetchall()
    cursor.close()
    return render_template('manager/pendingorders.html', pending_orders=pending_orders, availabletruck=availabletruck)

