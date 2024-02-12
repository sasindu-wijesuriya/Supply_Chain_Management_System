import mysql.connector
from flask import redirect, url_for, render_template
from res.PythonScripts import utils


def registrationFunction(request, database_instance, super_password_okay=False):
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and \
            'repeatPassword' in request.form and 'email' in request.form and 'mode' in request.form:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        RePassword = request.form['repeatPassword']
        mode = request.form['mode']
        cursor = database_instance.cursor()
        cursor.execute('SELECT * FROM Users WHERE user_name = %s', (email,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        else:
            if password == RePassword:
                hashedPassword = utils.hashPassword(password)
                cursor.callproc('RegisterUser', (name, email, hashedPassword, mode))
                database_instance.commit()
                msg = 'You have successfully registered !'
            else:
                msg = 'passwords do not match!'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


def loginFunction(request, session, database_instance):
    my_cursor = database_instance.cursor()
    msg = ''

    if session["loggedin"]:
        if "customer_id" in session:
            return redirect(url_for('home'))

        elif "main_manager_id" in session:
            return redirect(url_for('mainmanager'))

        elif "store_manager_id" in session:
            my_cursor3 = database_instance.cursor()
            my_cursor3.execute("select manager_id, store, user_name from store_manager where manager_id = %s ", (session["store_manager_id"],))
            user = my_cursor3.fetchone()

            # getting stores list to check the validity of the store
            cursor4 = database_instance.cursor()
            cursor4.execute('SELECT store_name FROM store')
            stores_list = cursor4.fetchall()

            store_manager_id = user[0]
            store_manager_store = user[1]
            store_manager_name = user[2]

            url = 'storemanager'
            if store_manager_store is None:
                return render_template('manager/form_store_manager_fill_store.html', url=url,
                                       store_manager_id=store_manager_id, store_manager_name=store_manager_name,
                                       stores_list=stores_list)
            else:
                session['store_manager_store'] = store_manager_store
                return redirect(url_for('storemanager'))
                # return render_template('storemanager_index.html', store=store_manager_store)


    elif (request.method == "POST" and 'username' in request.form and 'password' in request.form and \
            'mode' in request.form):
        user_details = request.form
        username = user_details['username']
        password = user_details['password']
        hashed_password = utils.hashPassword(password)
        mode = user_details['mode']
        my_cursor.execute('SELECT * FROM users WHERE user_name = %s AND password = %s AND mode = %s',
                          (username, hashed_password, mode,))
        account = my_cursor.fetchone()
        print("Account :", account)
        if account:
            session['loggedin'] = True
            session['mode'] = mode

            if mode == "customer":
                my_cursor1 = database_instance.cursor()
                my_cursor1.execute("select customer_id from customer where user_name = %s ", (username,))
                user = my_cursor1.fetchone()
                session['customer_id'] = user[0]
                # msg = 'Logged in successfully !'
                print('Customer :', user[0], 'logged in.')
                return redirect(url_for('home'))

            elif mode == 'Main_manager':
                my_cursor2 = database_instance.cursor()
                my_cursor2.execute("select manager_id from main_manager where user_name = %s ", (username,))
                user = my_cursor2.fetchone()
                session['main_manager_id'] = user[0]
                print('Main manager :', user[0], 'logged in.')
                return redirect(url_for('mainmanager'))

            elif mode == 'Store_manager':
                my_cursor3 = database_instance.cursor()
                my_cursor3.execute("select manager_id, store from store_manager where user_name = %s ", (username,))
                user = my_cursor3.fetchone()

                # getting stores list to check the validity of the store
                cursor4 = database_instance.cursor()
                cursor4.execute('SELECT store_name FROM store')
                stores_list = cursor4.fetchall()

                store_manager_id = user[0]
                store_manager_store = user[1]
                store_manager_name = username

                print('Store manager :', user[0], 'logged in.')
                url = 'storemanager'
                session['store_manager_id'] = store_manager_id

                if store_manager_store is None:
                    return render_template('manager/form_store_manager_fill_store.html', url=url,
                                           store_manager_id=store_manager_id, store_manager_name=store_manager_name, stores_list=stores_list)
                else:
                    session['store_manager_store'] = store_manager_store
                    return redirect(url_for('storemanager'))
                    # return render_template('storemanager_index.html', store=store_manager_store)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


def logoutFunction(session):
    session.pop('customer_id', None)
    session.pop('loggedin', None)
    session.pop('mode', None)
    session.pop('main_manager_id', None)
    session.pop('store_manager_id', None)
    session.pop('store_manager_store', None)
    return redirect(url_for('home'))


def profileFunction(database_instance, session, request):
    login = False
    if 'customer_id' in session:
        login = True
    # database_instance = mysql.connector.connect(**db_details)
    msg = ""
    username = session['customer_id']
    if request.method == 'POST' and 'name' in request.form and 'address_number' in request.form and 'address_line_1' in \
            request.form and 'address_line_2' in request.form and 'contact_number' in request.form and 'customer_type' \
            in request.form:
        name = request.form['name']
        address_number = request.form['address_number']
        address_line_1 = request.form['address_line_1']
        address_line_2 = request.form['address_line_2']
        contact_number = request.form['contact_number']
        customer_type = request.form['customer_type']
        cursor = database_instance.cursor()
        cursor.execute("update customer set name = %s , address_number = %s , address_line_1 = %s , address_line_2 = %s"
                       " , contact_number = %s , customer_type = %s where  customer_id = %s ;",
                       (name, address_number, address_line_1, address_line_2, contact_number, customer_type, username,))
        database_instance.commit()
        msg = 'profile updated successfully !'

    my_cursor = database_instance.cursor()
    my_cursor.execute("SELECT * FROM customer where customer_id = %s ;", (username,))
    user_details = my_cursor.fetchone()
    return render_template('customer/Profile.html', userDetail=user_details, msg=msg, login=login)


def homepage(request, database_instance, session):
    login = False
    session['loggedin'] = False
    if 'customer_id' in session:
        login = True
        session['loggedin'] = True
    if 'store_manager_id' in session:
        login = True
        session['loggedin'] = True
    if 'main_manager_id' in session:
        login = True
        session['loggedin'] = True
    return render_template("customer/index.html", login=login)


def contactUs(request, database_instance, session):
    login = False
    session['loggedin'] = False
    if 'customer_id' in session:
        login = True
        session['loggedin'] = True
    if 'store_manager_id' in session:
        login = True
        session['loggedin'] = True
    if 'main_manager_id' in session:
        login = True
        session['loggedin'] = True
    return render_template("customer/contactUs.html", login=login)