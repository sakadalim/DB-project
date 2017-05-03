import pymysql.cursors
from flask import Flask, render_template, request, session, url_for, redirect
import random
app =Flask(__name__)

conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='DBProject',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

app.secret_key = 'you will never guess what this is'

@app.route('/')
def hello():
    return render_template('welcomePage.html')

@app.route('/guestSearch')
def guestSearch():
    return render_template('guestSearch.html')

@app.route('/guestSearchGetInfo', methods=['POST'])
def guestSearchGetInfo():
    input_type = request.form['input_type']
    source = request.form['source_city']
    dest = request.form['dest_city']
    date_entered = request.form['date_entered']
    cursor = conn.cursor()
    if input_type == "city":
        query = 'SELECT * from flight WHERE flight.departure_airport in (SELECT airport_name FROM airport WHERE airport_city = %s) AND flight.arrival_airport in (SELECT airport_name FROM airport WHERE airport_city = %s) AND flight.departure_time = %s'
    if input_type =="airport":
        query = 'SELECT * FROM flight WHERE departure_airport = %s AND arrival_airport = %s AND departure_time = %s'
    cursor.execute(query, (source,dest,date_entered))
    data = cursor.fetchall()
    cursor.close()

    if (data):
        error = None
        return render_template('searchResultGuest.html', result = data)
    else:
        error = 'no results found'
        return render_template('guestSearch.html', error = error)

@app.route('/flightStat')
def flightStat():
    return render_template('flightStat.html')

@app.route('/guestFlightStat', methods = ['POST'])
def guestFlightStat():
    flight_num = request.form['flight_num']
    date_entered = request.form['date_entered']
    cursor = conn.cursor()
    query = 'SELECT * FROM flight WHERE flight.flight_num = %s AND (flight.departure_time = %s OR flight.arrival_time = %s )'
    cursor.execute(query,(flight_num,date_entered,date_entered))
    data = cursor.fetchall()
    cursor.close()

    if (data):
        error = None
        return render_template('flightStatResult.html', result = data)
    else:
        error = 'no results found'
        return render_template('flightStat.html', error = error)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/customerRegistration')
def customerRegistration():
    return render_template('customerRegistrationPage.html')

@app.route('/addNewCustomer', methods = ['POST'])
def addNewCustomer():
    email = request.form['email']
    name = request.form['name']
    password =  request.form['password']
    building_number = request.form['building_number']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    phone_number = request.form['phone_number']
    passport_number = request.form['passport_number']
    passport_expiration = request.form['passport_expiration']
    passport_country = request.form['passport_expiration']
    dob = request.form['date_of_birth']

    cursor = conn.cursor()
    query = 'INSERT INTO customer VALUES ( %s, %s, md5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(query,(email, name, password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, dob))
    conn.commit()
    cursor.close()
    return render_template('registrationSuccess.html')

@app.route('/bookingAgentRegistration')
def bookingAgentRegistration():
    return render_template('bookingAgentRegistrationPage.html')

@app.route('/addNewBookingAgent', methods = ['POST'])
def addNewBookingAgent():
    email = request.form['email']
    password = request.form['password']
    booking_agent_id = request.form['booking_agent_id']

    cursor = conn.cursor()
    query = 'INSERT INTO booking_agent VALUES (%s, md5(%s), %s)'
    cursor.execute(query,(email, password, booking_agent_id))
    conn.commit()
    cursor.close()
    return render_template('registrationSuccess.html')

@app.route('/airlineStaffRegistration')
def airlineStaffRegistration():
    return render_template('airlineStaffRegistrationPage.html')

@app.route('/addNewAirlineStaff', methods = ['POST'])
def addNewAirlineStaff():
    username = request.form['username']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    dob = request.form['dob']
    airline_name = request.form['airline_name']

    cursor = conn.cursor()
    query = 'INSERT INTO airline_staff VALUES (%s, md5(%s), %s, %s, %s, %s)'
    cursor.execute(query, (username, password, first_name, last_name, dob, airline_name))
    conn.commit()
    cursor.close()
    return render_template('registrationSuccess.html')

@app.route('/login')
def login():
    return render_template('loginPage.html')

@app.route('/loginAuth', methods=['POST'])
def loginAuth():
    user_type = request.form['user_type']
    username = request.form['username']
    password = request.form['password']

    if user_type == "customer":
        cursor = conn.cursor()
        query = 'SELECT * FROM customer WHERE email = %s and password = md5(%s)'
        cursor.execute(query, (username, password))
        data = cursor.fetchone()
        cursor.close()
        error = None
        if(data):
            session['username'] = username
            return redirect(url_for('customerPage'))
        else:
            error = 'Invalid login or username'
            return render_template('loginPage.html', error=error)

    elif user_type=="booking_agent":
        cursor= conn.cursor()
        query= 'SELECT * FROM booking_agent WHERE email = %s and password = md5(%s)'
        cursor.execute(query, (username, password))
        data= cursor.fetchone()
        cursor.close()
        error=None
        if (data):
            session['username']=username
            return redirect(url_for('bookingAgentPage'))
        else:
            error= 'Invalid login or username'
            return render_template('loginPage.html', error=error)

    elif user_type == "airline_staff":
        cursor= conn.cursor()
        query='SELECT * FROM airline_staff Where username = %s and password = md5(%s)'
        cursor.execute(query, (username, password))
        data= cursor.fetchone()
        cursor.close()
        error=None
        if (data):
            session['username']=username
            return redirect(url_for('airlineStaffPage'))
        else:
            error= 'Invalid login or username'
            return render_template('loginPage.html', error=error)

    else:
        error = 'error for now'
        return render_template('loginPage.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username')
    return render_template('successfullLogout.html')

@app.route('/customerPage')
def customerPage():
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT customer.name,flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price,flight.status, flight.airplane_id FROM flight, ticket, purchases, customer WHERE customer.email = purchases.customer_email AND purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND customer.email = %s'
    cursor.execute(query, (username))
    data = cursor.fetchall()
    cursor.close()
    return render_template('customerPage.html', username=username, posts = data)

@app.route('/customerSearchFlight')
def customerSearchFlight():
    username = session['username']
    return render_template('customerSearchFlight.html', username=username)

@app.route('/customerSearchFlightGetInfo', methods = ['POST'])
def customerSearchFlightGetInfo():
    username = session['username']
    input_type = request.form['input_type']
    source = request.form['source_city']
    dest = request.form['dest_city']
    date_entered = request.form['date_entered']
    cursor = conn.cursor()
    if input_type == "city":
        query = 'SELECT * from flight WHERE flight.departure_airport in (SELECT airport_name FROM airport WHERE airport_city = %s) AND flight.arrival_airport in (SELECT airport_name FROM airport WHERE airport_city = %s) AND flight.departure_time = %s AND flight.status = %s'
    if input_type == "airport":
        query = 'SELECT * FROM flight WHERE departure_airport = %s AND arrival_airport = %s AND departure_time = %s AND flight.status = %s'
    cursor.execute(query, (source,dest,date_entered,'upcoming'))
    data = cursor.fetchall()
    cursor.close()
    if (data):
        error = None
        return render_template('customerSearchFlightResult.html', result = data, username = username)
    else:
        error = 'No upcoming flights for your chosen date'
        return render_template('customerSearchFlight.html', username = username, error = error)

@app.route('/customerPurchaseFlight', methods = ['POST'])
def customerPurchaseFlight():
    username = session['username']
    airline_name = request.form['airline_name']
    flight_num = request.form['flight_num']
    date_entered = request.form['date_entered']
    cursor = conn.cursor()
    query = 'SELECT * FROM purchases WHERE ticket_id = %s'
    ticket_id = random.randint(0,9999999)
    while ( (cursor.execute(query,ticket_id)) == None):
        ticket_id = random.randint(0,9999999)
    query = 'INSERT INTO ticket VALUES (%s,%s,%s)'
    cursor.execute(query,(ticket_id,airline_name,flight_num))
    conn.commit()
    query = 'INSERT INTO `purchases` (`ticket_id`, `customer_email`, `booking_agent_id`, `purchase_date`) VALUES (%s, %s, NULL,CURRENT_DATE)'
    cursor.execute(query,(ticket_id,username,))
    conn.commit()
    cursor.close()
    return redirect(url_for('customerPage'))

@app.route('/bookingAgentPage')
def bookingAgentPage():
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT booking_agent.booking_agent_id,flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price,flight.status, flight.airplane_id FROM flight, ticket, purchases, booking_agent WHERE booking_agent.booking_agent_id = purchases.booking_agent_id AND purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND booking_agent.email = %s'
    cursor.execute(query, (username))
    data = cursor.fetchall()
    cursor.close()
    return render_template('bookingAgentPage.html', username=username, posts=data)

@app.route('/bookingAgentSearchFlight')
def bookingAgentSearchFlight():
    username = session['username']
    return render_template('bookingAgentSearchFlight.html', username=username)

@app.route('/bookingAgentSearchFlightGetInfo', methods = ['POST'])
def bookingAgentSearchFlightGetInfo():
    username = session['username']
    input_type = request.form['input_type']
    source = request.form['source_city']
    dest = request.form['dest_city']
    date_entered = request.form['date_entered']
    cursor = conn.cursor()
    if input_type == "city":
        query = 'SELECT * from flight WHERE flight.departure_airport in (SELECT airport_name FROM airport WHERE airport_city = %s) AND flight.arrival_airport in (SELECT airport_name FROM airport WHERE airport_city = %s) AND flight.departure_time = %s AND flight.status = %s'
    if input_type =="airport":
        query = 'SELECT * FROM flight WHERE departure_airport = %s AND arrival_airport = %s AND departure_time = %s AND flight.status = %s'
    cursor.execute(query, (source,dest,date_entered,'upcoming'))
    data = cursor.fetchall()
    cursor.close()
    if (data):
        error = None
        return render_template('bookingAgentSearchFlightResult.html', username = username, result = data)
    else:
        error = 'No upcoming flights for your chosen date'
        return render_template('bookingAgentSearchFlight.html', username = username, error = error)

#This does not include the date aspect, simply a total commission thus far.
@app.route('/bookingAgentCommission', methods = ['GET', 'POST'])
def bookingAgentCommission():
    username=session['username']
    if request.method == 'GET':
        return render_template('bookingAgentCommission.html', username=username)
    else:
        input_type = request.form['input_type']
        if input_type == 'past_month':
            cursor = conn.cursor()
            query= 'SELECT booking_agent.booking_agent_id, SUM(price)*.10 as commission FROM Flight,Ticket,Purchases,booking_agent WHERE Flight.flight_num=Ticket.flight_num and Ticket.ticket_id=Purchases.ticket_id and Purchases.booking_agent_id=booking_agent.booking_agent_id and booking_agent.email=%s and flight.departure_time >= CURRENT_DATE AND flight.arrival_time <= DATE_ADD(CURRENT_DATE,INTERVAL 30 DAY)'
            cursor.execute(query,(username))
            data= cursor.fetchall()
            cursor.close()
            return render_template('bookingAgentCommission.html', username=username, data=data)
        elif input_type == 'date_range':
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            cursor = conn.cursor()
            query= 'SELECT booking_agent.booking_agent_id, SUM(price)*.10 as commission FROM Flight,Ticket,Purchases,booking_agent WHERE Flight.flight_num=Ticket.flight_num and Ticket.ticket_id=Purchases.ticket_id and Purchases.booking_agent_id=booking_agent.booking_agent_id and booking_agent.email=%s and flight.departure_time >= %s AND flight.arrival_time <= %s'
            cursor.execute(query,(username,start_date,end_date))
            data= cursor.fetchall()
            cursor.close()
            return render_template('bookingAgentCommission.html', username=username, data=data)


@app.route('/airlineStaffPage')
def airlineStaffPage():
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT airline_staff.first_name, airline_staff.last_name FROM airline_staff WHERE airline_staff.username = %s'
    cursor.execute(query,username)
    data = cursor.fetchone()
    cursor.close()
    return render_template('airlineStaffPage.html', username = username, data = data)

@app.route('/viewMyFlights', methods = ['GET', 'POST'])
def viewMyFlights():
    username = session['username']
    if request.method == 'GET':
        cursor = conn.cursor()
        query = 'SELECT flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id FROM flight, airline_staff WHERE airline_staff.username = %s AND flight.airline_name = airline_staff.airline_name AND flight.departure_time >= CURRENT_DATE AND flight.arrival_time <= DATE_ADD(CURRENT_DATE,INTERVAL 30 DAY)'
        cursor.execute(query, username)
        data = cursor.fetchall()
        cursor.close()
        return render_template('viewMyFlights.html', username = username, data = data)

    else:
        search_type = request.form['search_type']
        if search_type == 'date':
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            cursor = conn.cursor()
            query = 'SELECT flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id FROM flight, airline_staff WHERE airline_staff.username = %s AND flight.airline_name = airline_staff.airline_name AND flight.departure_time >= %s AND flight.arrival_time <= %s'
            cursor.execute(query, (username,start_date,end_date))
            data = cursor.fetchall()
            cursor.close()
            if data:
                return render_template('viewMyFlights.html', username = username, data = data)
            else:
                error = 'No result for this date range!'
                return render_template('viewMyFlights.html', username = username, error = error)

        elif search_type == 'airport':
            source = request.form['source']
            dest = request.form['dest']
            cursor = conn.cursor()
            query = 'SELECT flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id FROM flight, airline_staff WHERE airline_staff.username = %s AND flight.airline_name = airline_staff.airline_name AND flight.departure_time >= CURRENT_DATE AND flight.arrival_time <= DATE_ADD(CURRENT_DATE,INTERVAL 30 DAY) AND flight.departure_airport = %s AND flight.arrival_airport = %s'
            cursor.execute(query,(username,source,dest))
            data = cursor.fetchall()
            cursor.close()
            if data:
                return render_template('viewMyFlights.html', username = username, data = data)
            else:
                error = 'No result for the entered airports!'
                return render_template('viewMyFlights.html', username = username, error = error)
        elif search_type == 'city':
            source = request.form['source']
            dest = request.form['dest']
            cursor = conn.cursor()
            query = 'SELECT flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id FROM flight, airline_staff WHERE airline_staff.username = %s AND flight.airline_name = airline_staff.airline_name AND flight.departure_time >= CURRENT_DATE AND flight.arrival_time <= DATE_ADD(CURRENT_DATE,INTERVAL 30 DAY) AND flight.departure_airport in (SELECT airport_name FROM airport WHERE airport_city = %s) AND flight.arrival_airport in (SELECT airport_name FROM airport WHERE airport_city = %s)'
            cursor.execute(query,(username,source,dest))
            data = cursor.fetchall()
            cursor.close()
            if data:
                return render_template('viewMyFlights.html', username = username, data = data)
            else:
                error = 'No result for the entered cities!'
                return render_template('viewMyFlights.html', username = username, error = error)

@app.route('/createNewFlight', methods = ['GET', 'POST'])
def createNewFlight():
    username = session['username']
    if request.method  == 'GET':
        return render_template('createNewFlight.html', username = username)
    else:
        flight_num = request.form['flight_num']
        cursor = conn.cursor()
        query = 'SELECT flight.flight_num FROM flight WHERE flight.flight_num = %s'
        cursor.execute(query,flight_num)
        data = cursor.fetchone()
        cursor.close()
        if data:
            error = 'This flight number already exist, please choose a new one'
            return render_template('createNewFlight.html', username = username, error = error)
        else:
            airline_name = request.form['airline_name']
            cursor = conn.cursor()
            query = 'SELECT airline_name FROM airline WHERE airline_name = %s'
            cursor.execute(query,airline_name)
            data = cursor.fetchone()
            cursor.close()
            if data == None:
                error = 'Airline does not exist, please try again!'
                return render_template('createNewFlight.html', username = username, error = error)
            else:
                departure_airport = request.form['departure_airport']
                cursor = conn.cursor()
                query = 'SELECT airport_name FROM airport WHERE airport_name = %s'
                cursor.execute(query,departure_airport)
                data = cursor.fetchone()
                cursor.close()
                if data == None:
                    error = 'Departur airport does not exist, please try again!'
                    return render_template('createNewFlight.html', username = username, error = error)
                else:
                    arrival_airport = request.form['arrival_airport']
                    cursor = conn.cursor()
                    query = 'SELECT airport_name FROM airport WHERE airport_name = %s'
                    cursor.execute(query,departure_airport)
                    data = cursor.fetchone()
                    cursor.close()
                    if data == None:
                        error = 'Arrival airport does not exist, please try again!'
                        return render_template('createNewFlight.html', username = username, error = error)
                    else:
                        airplane_id = request.form['airplane_id']
                        cursor = conn.cursor()
                        query = 'SELECT airplane_id FROM airplane WHERE airline_name = %s AND airplane_id = %s'
                        cursor.execute(query,(airline_name,airplane_id))
                        data = cursor.fetchone()
                        cursor.close()
                        if data == None:
                            error = 'Airplane ID does not exist, please try again!'
                            return render_template('createNewFlight.html', username = username, error = error)
                        else:
                            departure_time = request.form['departure_time']
                            arrival_time = request.form['arrival_time']
                            price = request.form['price']
                            status = request.form['status']
                            cursor = conn.cursor()
                            query = 'INSERT INTO `flight` (`airline_name`, `flight_num`, `departure_airport`, `departure_time`, `arrival_airport`, `arrival_time`, `price`, `status`, `airplane_id`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                            cursor.execute(query,(airline_name,flight_num,departure_airport,departure_time,arrival_airport,arrival_time,price,status,airplane_id))
                            conn.commit()
                            cursor.close()
                            message = "Flight has been added!"
                            error = None
                            return render_template('createNewFlight.html', username =username, message = message)

@app.route('/airlineStaffChangeFlightStatus')
def airlineStaffChangeFlightStatus():
    username = session['username']
    return render_template('airlineStaffChangeFlightStatus.html', username=username)

@app.route('/airlineStaffChangeFlightStatusAction',methods = ['POST'])
def airlineStaffChangeFlightStatusAction():
    username=session['username']
    airline_name=request.form['airline_name']
    cursor = conn.cursor()
    query= 'SELECT airline_name FROM airline WHERE airline_name =%s'
    cursor.execute(query, airline_name)
    data = cursor.fetchone()
    cursor.close()
    if data == None:
        error= 'Error: The Flight status was not updated. Airline does not exist!'
        return render_template('airlineStaffChangeFlightStatus.html', username=username, error=error)
    else:
        flight_number= request.form['flight_number']
        cursor = conn.cursor()
        query= 'SELECT flight_num FROM flight WHERE flight_num =%s'
        cursor.execute(query, flight_number)
        data = cursor.fetchone()
        cursor.close()
        if data == None:
            error= 'Error: The Flight status was not updated. flight number does not exist!'
            return render_template('airlineStaffChangeFlightStatus.html', username=username, error=error)
        else:
            flight_status= request.form['flight_status']
            cursor = conn.cursor()
            query= 'UPDATE `flight` SET `status` = %s WHERE `flight`.`airline_name` = %s AND `flight`.`flight_num` = %s'
            cursor.execute(query,(flight_status, airline_name,flight_number))
            conn.commit()
            cursor.close()
            error= 'The Flight status has been updated'
            return render_template('airlineStaffChangeFlightStatus.html', username=username, error=error)


@app.route('/airlineStaffAddAirplane')
def airlineStaffAddAirplane():
    username= session['username']
    return render_template('airlineStaffAddAirplane.html',username=username)

@app.route('/airlineStaffAddAirplaneAction', methods =['POST'])
def airlineStaffAddAirplaneAction():
    username= session['username']
    airline_name=request.form['airline_name']
    cursor=conn.cursor()
    query= 'SELECT airline_name FROM Airplane WHERE airline_name= %s'
    cursor.execute(query,airline_name)
    data=cursor.fetchone()
    cursor.close()
    if data == None :
        error= 'Airline does not exist, please input a different one'
        return render_template('airlineStaffAddAirplane.html',username=username, error=error)
    else:
        airplane_id=request.form['airplane_id']
        cursor=conn.cursor()
        query= 'SELECT airplane_id FROM airplane WHERE airplane_id= %s'
        cursor.execute(query,airplane_id)
        data=cursor.fetchone()
        cursor.close()
        if (data):
            error= 'Airplane ID already exist, please input a different one'
            return render_template('airlineStaffAddAirplane.html', username=username, error=error)
        else:
            numSeats= request.form['seats']
            cursor=conn.cursor()
            query= 'INSERT into Airplane VALUES(%s,%s,%s)'
            cursor.execute(query,(airline_name,airplane_id,numSeats))
            conn.commit()
            cursor.close()
            error= 'Airplane has been SUCCESSFULLY added'
            return render_template('airlineStaffAddAirplane.html',username=username, error=error)


@app.route('/airlineStaffAddAirport')
def airlineStaffAddAirport():
    username=session['username']
    return render_template('airlineStaffAddAirport.html', username=username)

@app.route('/airlineStaffAddAirportAction', methods=['POST'])
def airlineStaffAddAirportAction():
    username=session['username']
    airport_name=request.form['airport_name']
    cursor = conn.cursor()
    query = 'SELECT airport_name FROM airport WHERE airport_name= %s'
    cursor.execute(query,airport_name)
    data= cursor.fetchall()
    cursor.close()
    if(data):
        error= 'The airport you are trying to enter already exists'
        return render_template('airlineStaffAddAirport.html', username=username, error=error)
    airport_city=request.form['city']
    cursor=conn.cursor()
    query= 'INSERT into airport VALUES(%s,%s)'
    cursor.execute(query,(airport_name, airport_city))
    conn.commit()
    cursor.close()
    error= 'Airport has been SUCCESSFULY added'
    return render_template('airlineStaffAddAirport.html', username=username, error=error)

@app.route('/viewReport', methods = ['GET','POST'] )
def viewReport():
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT airline_name FROM airline_staff WHERE username = %s'
    cursor.execute(query, username)
    airline_name = cursor.fetchone()['airline_name']
    cursor.close()
    if request.method == 'GET':
        return render_template('viewReport.html', username = username, airline_name = airline_name)
    else:
        input_type = request.form['input_type']
        if input_type == 'date_entered':
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            cursor = conn.cursor()
            query = 'SELECT count(*) as ticket_sales FROM (purchases NATURAL JOIN ticket) WHERE airline_name = %s and purchase_date >= %s AND purchase_date <= %s'
            cursor.execute(query,(airline_name,start_date,end_date))
            date_data = cursor.fetchone();
            cursor.close()
            if  date_data== None:
                error = 'Error: No results found for the date entered.'
                return render_template('viewReport.html', username= username,airline_name= airline_name, error = error)
            else:
                return render_template('viewReport.html', username = username, airline_name = airline_name,date_data = date_data)
        elif input_type == 'past_month':
            cursor = conn.cursor()
            query = 'SELECT count(*) AS ticket_sales FROM (purchases NATURAL JOIN ticket) WHERE airline_name = %s AND YEAR(purchase_date) = YEAR(CURDATE()) AND MONTH(purchase_date) = MONTH(CURDATE() - INTERVAL 1 MONTH)'
            cursor.execute(query,airline_name)
            month_count = cursor.fetchone();
            cursor.close()
            if month_count == None:
                error = 'Error: No result for the past month!'
                return render_template('viewReport.html', username = username, airline_name = airline_name, error = error)
            else:
                return render_template('viewReport.html', username= username, airline_name = airline_name, month_count = month_count)
        elif input_type == 'past_year':
            cursor = conn.cursor()
            query = 'SELECT count(*) AS ticket_sales FROM (purchases NATURAL JOIN ticket) WHERE airline_name = %s AND purchases.purchase_date <= CURRENT_DATE AND purchases.purchase_date >= DATE_SUB(CURRENT_DATE, INTERVAL 1 YEAR)'
            cursor.execute(query,airline_name)
            year_total = cursor.fetchone();
            cursor.close()
            cursor = conn.cursor()
            query = 'SELECT MONTH(purchase_date) as Month, count(*) AS ticket_sales FROM (purchases NATURAL JOIN ticket) WHERE airline_name = %s AND YEAR(purchase_date) = YEAR(CURDATE()) GROUP BY MONTH(purchase_date)'
            cursor.execute(query,airline_name)
            year_data = cursor.fetchall();
            cursor.close()
            if year_data == None:
                error = 'Error: No result for the past year.'
                return render_template('viewReport.html', username = username, airline_name = airline_name, error= error)
            else:
                return render_template('viewReport.html', username = username, airline_name = airline_name, year_data = year_data, year_total = year_total)





@app.route('/airlineStaffBookingAgentLookup')
def airlineStaffBookingAgentLookup():
    username=session['username']
    cursor = conn.cursor()
    query='SELECT booking_agent_id, count(booking_agent_id) as ticket_sales from purchases  where MONTH(purchase_date) = MONTH(CURDATE() - INTERVAL 1 MONTH) group by booking_agent_id order by count(booking_agent_id) desc limit 5'
    cursor.execute(query)
    data =cursor.fetchall()
    cursor.close()
    return render_template('airlineStaffBookingAgentLookup.html', username=username, data = data)

@app.route('/airlineStaffBookingAgentLookupAction', methods=['POST'])
def airlineStaffBookingAgentLookupAction():
    username=session['username']
    timeLine=request.form['Time Frame']
    if (timeLine == "month"):
        cursor = conn.cursor()
        query='SELECT booking_agent_id, count(booking_agent_id) as ticket_sales from purchases  where MONTH(purchase_date) = MONTH(CURDATE() - INTERVAL 1 MONTH) group by booking_agent_id order by count(booking_agent_id) desc limit 5'
        cursor.execute(query)
        data =cursor.fetchall()
        cursor.close()
        return render_template('airlineStaffBookingAgentLookup.html', username=username, data = data)
    elif timeLine == 'year':
        cursor = conn.cursor()
        query='SELECT booking_agent_id, count(booking_agent_id) as ticket_sales from purchases where purchase_date >= DATE_SUB(CURRENT_DATE,INTERVAL 1 YEAR) AND purchase_date <= CURRENT_DATE group by booking_agent_id order by count(booking_agent_id) desc limit 5'
        cursor.execute(query)
        data =cursor.fetchall()
        cursor.close()
        return render_template('airlineStaffBookingAgentLookup.html', username=username, data = data)

@app.route('/airlineStaffBookingAgentLookupCommission')
def airlineStaffBookingAgentLookupCommission():
    username=session['username']
    cursor=conn.cursor()
    query= 'SELECT airline_name from airline_staff where username = %s'
    cursor.execute (query,(username))
    airlineName= cursor.fetchone()['airline_name']
    cursor.close()
    cursor = conn.cursor()
    query='SELECT booking_agent_id, sum(price * 0.10) as commission from (flight natural join ticket natural join purchases) where purchase_date >= DATE_SUB(CURRENT_DATE,INTERVAL 1 YEAR) AND purchase_date <= CURRENT_DATE AND flight.airline_name = %s group by booking_agent_id order by commission desc limit 5'
    cursor.execute(query,airlineName)
    data =cursor.fetchall()
    cursor.close()
    return render_template('airlineStaffBookingAgentLookupCommission.html', username=username, data = data)



@app.route('/airlineStaffTopCustomer')
def airlineStaffTopCustomer():
    username=session['username']
    cursor=conn.cursor()
    query= 'SELECT airline_name from airline_staff where username = %s'
    cursor.execute (query,(username))
    airlineName= cursor.fetchone()['airline_name']
    cursor.close()
    cursor=conn.cursor()
    query= 'SELECT customer.name, customer.email, count(customer.email) as tickets_bought from (customer natural join purchases natural join ticket) where airline_name = %s and purchase_date >= DATE_SUB(CURRENT_DATE,INTERVAL 1 YEAR) AND purchase_date <= CURRENT_DATE group by customer.email order by count(customer.email) DESC limit 1'
    cursor.execute(query, (airlineName))
    data = cursor.fetchall()
    cursor.close()
    return render_template('airlineStaffTopCustomer.html', username=username, data = data)

@app.route('/airlineStaffTopCustomerFlights')
def airlineStaffTopCustomerFlights():
    username=session['username']
    cursor=conn.cursor()
    query= 'SELECT airline_name from airline_staff where username = %s'
    cursor.execute (query,(username))
    airlineName= cursor.fetchone()['airline_name']
    cursor.close()
    cursor=conn.cursor()
    query= 'SELECT customer.name from (customer natural join purchases natural join ticket) where airline_name = %s and purchase_date >= DATE_SUB(CURRENT_DATE,INTERVAL 1 YEAR) AND purchase_date <= CURRENT_DATE group by customer.email order by count(customer.email) DESC limit 1'
    cursor.execute(query, (airlineName))
    customerName = cursor.fetchone()['name']
    cursor.close()
    cursor=conn.cursor()
    query= 'SELECT DISTINCT customer.name, ticket.flight_num from (flight natural join ticket natural join purchases natural join customer) where airline_name = %s and customer.name = %s'
    cursor.execute(query, (airlineName,customerName))
    data=cursor.fetchall()
    cursor.close()
    return render_template('airlineStaffTopCustomerFlights.html', username=username, data = data)







if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
