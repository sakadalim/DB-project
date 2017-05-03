Use Cases

Database Project Part C

John Buckley 
Sakada Lim 

-- Searches for flights based on city 
SELECT * from flight WHERE flight.departure_airport in (SELECT airport_name FROM airport WHERE airport_city = %s) AND flight.arrival_airport in (SELECT airport_name FROM airport WHERE airport_city = %s) AND flight.departure_time = %s
-- Searchs for flights based on Airport 
SELECT * FROM flight WHERE departure_airport = %s AND arrival_airport = %s AND departure_time = %s
-- Gets Flight statists 
SELECT * FROM flight WHERE departure_airport = %s AND arrival_airport = %s AND departure_time = %s'
-- Adds new Customer to Database (email, name, password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, dob)
INSERT INTO customer VALUES ( %s, %s, md5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s)
--Adds New booking Agent to database (email, password, booking_agent_id)
INSERT INTO booking_agent VALUES (%s, md5(%s), %s)
--Adds Airline Staff to database (username, password, first_name, last_name, dob, airline_name)
INSERT INTO airline_staff VALUES (%s, md5(%s), %s, %s, %s, %s)

--Check to see if customer can login 
SELECT * FROM customer WHERE email = %s and password = md5(%s)
--Check to see if booking Agent can log in 
SELECT * FROM booking_agent WHERE email = %s and password = md5(%s)
--Check to see if Airline Staff can login 
SELECT * FROM airline_staff Where username = %s and password = md5(%s)
--Get all flight information for customer 
SELECT customer.name,flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price,flight.status, flight.airplane_id FROM flight, ticket, purchases, customer WHERE customer.email = purchases.customer_email AND purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND customer.email = %s
--Search customer flight information based on city 
SELECT * from flight WHERE flight.departure_airport in (SELECT airport_name FROM airport WHERE airport_city = %s) AND flight.arrival_airport in (SELECT airport_name FROM airport WHERE airport_city = %s) AND flight.departure_time = %s AND flight.status = %s
--Search customer flight infirmation based on Airport 
SELECT * FROM flight WHERE departure_airport = %s AND arrival_airport = %s AND departure_time = %s AND flight.status = %s
--Select flight with the following ID 
SELECT * FROM purchases WHERE ticket_id = %s
--Add ticket to Database after it has been purchased 
INSERT INTO ticket VALUES (%s,%s,%s)
--Add additional Ticket information into the database after it has been purchased 
INSERT INTO `purchases` (`ticket_id`, `customer_email`, `booking_agent_id`, `purchase_date`) VALUES (%s, %s, NULL,CURRENT_DATE)


--Get booking agent's flights and information 
SELECT booking_agent.booking_agent_id,flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price,flight.status, flight.airplane_id FROM flight, ticket, purchases, booking_agent WHERE booking_agent.booking_agent_id = purchases.booking_agent_id AND purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND booking_agent.email = %s
--Select flight based off of City 
SELECT * from flight WHERE flight.departure_airport in (SELECT airport_name FROM airport WHERE airport_city = %s) AND flight.arrival_airport in (SELECT airport_name FROM airport WHERE airport_city = %s) AND flight.departure_time = %s AND flight.status = %s'
--Select flight based off of airport 
SELECT * FROM flight WHERE departure_airport = %s AND arrival_airport = %s AND departure_time = %s AND flight.status = %s
--Get booking Agent commission for the past 30 days 
SELECT booking_agent.booking_agent_id, SUM(price)*.10 as commission FROM Flight,Ticket,Purchases,booking_agent WHERE Flight.flight_num=Ticket.flight_num and Ticket.ticket_id=Purchases.ticket_id and Purchases.booking_agent_id=booking_agent.booking_agent_id and booking_agent.email=%s and flight.departure_time >= CURRENT_DATE AND flight.arrival_time <= DATE_ADD(CURRENT_DATE,INTERVAL 30 DAY)


--Get Airline staff information 
SELECT airline_staff.first_name, airline_staff.last_name FROM airline_staff WHERE airline_staff.username = %s
--Airline staff View my flights 
SELECT flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id FROM flight, airline_staff WHERE airline_staff.username = %s AND flight.airline_name = airline_staff.airline_name AND flight.departure_time >= CURRENT_DATE AND flight.arrival_time <= DATE_ADD(CURRENT_DATE,INTERVAL 30 DAY)
--My flights based off of date 
SELECT flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id FROM flight, airline_staff WHERE airline_staff.username = %s AND flight.airline_name = airline_staff.airline_name AND flight.departure_time >= %s AND flight.arrival_time <= %s'
--My flights based off of airport 
SELECT flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id FROM flight, airline_staff WHERE airline_staff.username = %s AND flight.airline_name = airline_staff.airline_name AND flight.departure_time >= CURRENT_DATE AND flight.arrival_time <= DATE_ADD(CURRENT_DATE,INTERVAL 30 DAY) AND flight.departure_airport = %s AND flight.arrival_airport = %s
--My flights based off of destination 
SELECT flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id FROM flight, airline_staff WHERE airline_staff.username = %s AND flight.airline_name = airline_staff.airline_name AND flight.departure_time >= CURRENT_DATE AND flight.arrival_time <= DATE_ADD(CURRENT_DATE,INTERVAL 30 DAY) AND flight.departure_airport in (SELECT airport_name FROM airport WHERE airport_city = %s) AND flight.arrival_airport in (SELECT airport_name FROM airport WHERE airport_city = %s)
--Check to see if flight being created already exists 
SELECT flight.flight_num FROM flight WHERE flight.flight_num = %s
--check to see if airline exists 
SELECT airline_name FROM airline WHERE airline_name = %s
-- Check to see if departure airport exists 
SELECT airport_name FROM airport WHERE airport_name = %s
--Check to see if arrival airport exists 
SELECT airport_name FROM airport WHERE airport_name = %s
--check to see if airline id already exists 
SELECT airplane_id FROM airplane WHERE airline_name = %s AND airplane_id = %s
--Insert new airplane into Database (airline_name,flight_num,departure_airport,departure_time,arrival_airport,arrival_time,price,status,airplane_id)
INSERT INTO `flight` (`airline_name`, `flight_num`, `departure_airport`, `departure_time`, `arrival_airport`, `arrival_time`, `price`, `status`, `airplane_id`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
--Change flight status 
UPDATE `flight` SET `status` = %s WHERE `flight`.`airline_name` = %s AND `flight`.`flight_num` = %s
--Add airplane to Database 
INSERT into Airplane VALUES(%s,%s,%s)

--View all tickets purchased in a time frame 
SELECT count(*) as ticket_sales FROM (purchases NATURAL JOIN ticket) WHERE airline_name = %s and purchase_date >= %s AND purchase_date <= %s
--select all tickets purchased in a recent time frame 
SELECT count(*) AS ticket_sales FROM (purchases NATURAL JOIN ticket) WHERE airline_name = %s AND YEAR(purchase_date) = YEAR(CURDATE()) AND MONTH(purchase_date) = MONTH(CURDATE() - INTERVAL 1 MONTH)
-- get top 5 booking agents from a select airline (past month)  
SELECT booking_agent_id, count(booking_agent_id) as ticket_sales from purchases  where MONTH(purchase_date) = MONTH(CURDATE() - INTERVAL 1 MONTH) group by booking_agent_id order by count(booking_agent_id) desc limit 5'
-- Get top 5 booking Agents from a select airline (past year) 
SELECT booking_agent_id, count(booking_agent_id) as ticket_sales from purchases where purchase_date >= DATE_SUB(CURRENT_DATE,INTERVAL 1 YEAR) AND purchase_date <= CURRENT_DATE group by booking_agent_id order by count(booking_agent_id) desc limit 5
-- Get commission of top 5 booking agents 
SELECT booking_agent_id, sum(price * 0.10) as commission from (flight natural join ticket natural join purchases) where purchase_date >= DATE_SUB(CURRENT_DATE,INTERVAL 1 YEAR) AND purchase_date <= CURRENT_DATE AND flight.airline_name = %s group by booking_agent_id order by commission desc limit 5
-- Get top customer total flights
SELECT customer.name, customer.email, count(customer.email) as tickets_bought from (customer natural join purchases natural join ticket) where airline_name = %s and purchase_date >= DATE_SUB(CURRENT_DATE,INTERVAL 1 YEAR) AND purchase_date <= CURRENT_DATE group by customer.email order by count(customer.email) DESC limit 1
-- Get list of all flights taken by top customer 
SELECT DISTINCT customer.name, ticket.flight_num from (flight natural join ticket natural join purchases natural join customer) where airline_name = %s and customer.name = %s


