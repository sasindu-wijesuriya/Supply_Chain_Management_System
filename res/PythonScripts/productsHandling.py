import datetime

from flask import redirect, url_for, render_template


def productListFunction(database_instance, session):
    login = False
    if 'customer_id' in session:
        login = True
    myCursor = database_instance.cursor()
    myCursor.execute("select * from items")
    products = myCursor.fetchall()
    return render_template('customer/product_list.html', products=products, login=login)


def AddToCartFunction(request, database_instance, session):
    item_id = request.form['item_id']
    print(item_id)

    if 'customer_id' in session:
        login = True
        myCursor = database_instance.cursor()
        myCursor.execute("select * from items where item_id = %s ", (request.form['item_id'],))
        item = myCursor.fetchone()
        return render_template('customer/addToCart.html', item=item, login=login)

    else:
        return redirect(url_for('login'))


def CartFunction(request, db_details, database_instance, session):
    if 'customer_id' in session:
        customerID = session['customer_id']
        print(customerID)
        login = True
        if request.method == 'POST' and 'quantity' in request.form and 'item_id' in request.form:
            quantity = request.form['quantity']
            item_id = request.form['item_id']
            customer_id = session['customer_id']

            myCursor1 = database_instance.cursor()
            myCursor1.callproc('AddToCart',(customerID,item_id, quantity))
            #myCursor1.execute("insert into cart values (%s , %s, %s )", (customerID,item_id, quantity))
            database_instance.commit();

        myCursor1 = database_instance.cursor()
        myCursor1.execute("select * from cart_items where customer_id = %s ", (customerID,))
        item = myCursor1.fetchall()
        print(item)

        myCursor2 = database_instance.cursor()
        myCursor2.execute("select * from cart_details where customer_id = %s ", (customerID,))
        detail = myCursor2.fetchone()
        print(detail)

        return render_template('customer/Cart.html', login=login, items=item, details=detail)

    else:
        return redirect('login')


def BuyNowFunction(request, db_details, database_instance,  session):
    if 'customer_id' in session:
        customerID = session['customer_id']
        login = True

        if request.method == 'POST' and 'routeID' in request.form and 'addressNo' in request.form and 'addressLine1' in request.form and 'addressLine2' in request.form and 'deliveryDate' in request.form:

            todayDate = datetime.date.today()
            deliveryDate = datetime.datetime.strptime(request.form['deliveryDate'], "%Y-%m-%d").date()
            days_to_deliver = deliveryDate - todayDate
            print("Difference is " + str(days_to_deliver.days) + " days")
            if days_to_deliver.days < 7:
                msg = "Sorry, the items cannot be delivered before " + str(todayDate + datetime.timedelta(days=7))
                url = "buyNow"
                return render_template('popupMsg.html', msg=msg, url=url)

            myCursor = database_instance.cursor()
            myCursor.callproc('BuyCart', (customerID, request.form['routeID'], request.form['addressNo'], request.form['addressLine1'], request.form['addressLine2'], request.form['deliveryDate']))
            database_instance.commit()
            msg = "success"
            url = "home"
            return render_template('popupMsg.html', msg=msg, url=url)

        myCursor = database_instance.cursor()
        myCursor.execute("select IsItemCountMatch( %s );", (customerID,))
        result = myCursor.fetchall()
        if result[0][0] == 1:
            return render_template('customer/buyNow.html')
        elif result[0][0] == 0:
            msg = "item count is not enough"
            url = "cart"
            return render_template('popupMsg.html',msg=msg , url=url)
        elif result[0][0] == 4:
            msg ="please fill the profile details"
            url ="profile"
            return render_template('popupMsg.html', msg=msg, url=url)





