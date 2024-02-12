from flask import Flask, request, session
import mysql.connector
from res.PythonScripts import authenticationAndProfile, productsHandling, utils, reports, managersFunctions

app = Flask(__name__)
app.secret_key = 'your secret key'

# TODO : Get the db_details from the txt file
db_details = {'user': 'root', 'password': '', 'host': 'localhost', 'database': 'test3'}
# db_details = {'user': 'freedb_testuser2', 'password': '87fB*5ueP#E6yru', 'host': 'sql.freedb.tech', 'database': 'freedb_testdatabase2', 'port': 3306}
database_instance = mysql.connector.connect(**db_details)


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    return authenticationAndProfile.homepage(request, database_instance, session)


@app.route('/register', methods=['GET', 'POST'])
def register():
    return authenticationAndProfile.registrationFunction(request, database_instance, False)


@app.route('/login', methods=['GET', 'POST'])
def login():
    return authenticationAndProfile.loginFunction(request, session, database_instance)


@app.route('/logout')
def logout():
    return authenticationAndProfile.logoutFunction(session)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return authenticationAndProfile.profileFunction(database_instance, session, request)


@app.route('/product_list', methods=['GET', 'POST'])
def productList():
    return productsHandling.productListFunction(database_instance, session)


@app.route('/addtocart', methods=['GET', 'POST'])
def AddToCart():
    return productsHandling.AddToCartFunction(request, database_instance, session)


@app.route('/cart', methods=['GET', 'POST'])
def Cart():
    return productsHandling.CartFunction(request, db_details, database_instance, session)


@app.route('/contactUs', methods=['GET', 'POST'])
def contactUs():
    return authenticationAndProfile.contactUs(request, database_instance, session)


@app.route('/buyNow', methods=['GET', 'POST'])
def BuyNow():
    return productsHandling.BuyNowFunction(request, db_details, database_instance, session)


@app.route('/mainmanager', methods=['GET', 'POST'])
def mainmanager():
    return managersFunctions.mainManagerFunction(database_instance, session, request)


@app.route('/storemanager', methods=['GET', 'POST'])
def storemanager():
    return managersFunctions.storeManagerFunction(database_instance, session, request)


@app.route('/mmdashboard')
def MainManagerDashBoard():
    return managersFunctions.MainManagerDashBoardFunction()


@app.route('/smdashboard')
def StoreManagerDashBoard():
    return managersFunctions.StoreManagerDashBoardFunction()


@app.route('/trainschedule', methods=['GET', 'POST'])
def trainsched():
    return managersFunctions.trainSchedFunction(database_instance, session, request)


@app.route('/truckschedule')
def trucksched():
    return managersFunctions.truckSchedFunction()


@app.route('/humanresources', methods=['GET', 'POST'])
def humanres():
    return managersFunctions.humanResFunction(database_instance, session, request)


@app.route('/logistics', methods=['GET', 'POST'])
def logistics():
    return managersFunctions.logisticsFunction(database_instance, session, request)


# @app.route('/pendingorders')
# def pendingorders():
#     return managersFunctions.pendingOrdersFunction()


@app.route('/assets', methods=['GET', 'POST'])
def assets():
    return managersFunctions.assetsFunction()


@app.route('/addproducts', methods=['GET', 'POST'])
def addproducts():
    return managersFunctions.addProductsFunction(database_instance, session, request)


@app.route('/addtrucks', methods=['GET', 'POST'])
def addtrucks():
    return managersFunctions.addTrucksFunction(database_instance, session, request)


@app.route('/orders', methods=['GET', 'POST'])
def orders():
    return managersFunctions.ordersFunction(database_instance, session, request)


@app.route('/pendingorders', methods=['GET', 'POST'])
def pendingorders():
    return managersFunctions.pendingOrdersFunction(database_instance, session, request)


# @app.route('/formstoremanagerfillstore', methods=['GET','POST'])
# def formStoreManagerFillStore():
#     return managersFunctions.FormStoreManagerFillStoreFuntion(database_instance, session, request)


@app.route('/quarterlyreport', methods=['GET', 'POST'])
def QuarterlyReport():
    return reports.QuarterlyReportFunction(request, db_details, database_instance, session)


@app.route('/itemswithmostorders', methods=['GET', 'POST'])
def ItemsWithMostOrders():
    return reports.ItemsWithMostOrdersFunction(request, database_instance, session)


@app.route('/salesreportofstores')
def SalesReportOfStores():
    return reports.SalesReportOfStoresFunction(request, database_instance, session)


@app.route('/workinghoursofdrivers')
def WorkingHoursOfDrivers():
    return reports.GetWorkingHoursOfDriversFunction(request, database_instance, session)


@app.route('/workinghoursofdriverassistants')
def WorkingHoursOfDriverAssistants():
    return reports.GetWorkingHoursOfDriverAssistantsFunction(request, database_instance, session)


@app.route('/customerreport', methods=['GET', 'POST'])
def GenerateCustomerReport():
    return reports.GenerateCustomerReportFunction(request, database_instance, session)


@app.route('/trucksusedhours', methods=['GET', 'POST'])
def UsedHoursOfTrucks():
    return reports.UsedHoursOfTrucksFunction(request, database_instance, session)


# main function
if __name__ == '__main__':
    app.run(debug=True)
