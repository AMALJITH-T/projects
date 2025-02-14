from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_required, UserMixin, login_user, current_user
import random
import secrets

app = Flask(__name__)

MAX_FLIGHTS = 10

class Flight:
    def __init__(self):
        self.flightNumber = ""
        self.source = ""
        self.destination = ""
        self.availableSeats = []  # should be a list
        self.fare = 0.0

def initializeFlights():
    airport_names = [
        "Thiruvananthapuram International Airport",
        "Cochin International Airport",
        "Kannur International Airport",
        "Calicut International Airport",
        "Singapore Changi Airport",
        "Dubai International Airport",
        "Hong Kong International Airport",
        "Incheon International Airport",
        "Haneda Airport",
        "Hamad International Airport"
    ]

    flights = [Flight() for _ in range(MAX_FLIGHTS * len(airport_names) ** 2)]

    for i in range(MAX_FLIGHTS * len(airport_names) ** 2):
        flights[i].flightNumber = f"AL00{i + 1}"
        flights[i].source = random.choice(airport_names)
        flights[i].destination = random.choice(airport_names)
        flights[i].availableSeats = [f"{i}{j}" for j in range(1, random.randint(50, 200) + 1)]
        flights[i].fare = round(random.uniform(200.0, 800.0), 2)

    return flights

flights = initializeFlights()

users = {'AMAL2003': {'password': 'HUNTERJR25'}}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

app.secret_key = secrets.token_hex(16)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
@login_required
def index():
    return render_template('location.html', flights=flights, username=current_user.id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Replace this with your actual user authentication logic
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.HTML', error='Invalid credentials')

    return render_template('login.HTML')

@app.route('/search_flights', methods=['POST'])
def search_flights():
    departure_place = request.form.get('departure')
    destination_place = request.form.get('destination')

    print(f"Departure Place: {departure_place}")
    print(f"Destination Place: {destination_place}")

    for flight in flights:
        print(f"Flight: {flight.flightNumber}, Source: {flight.source}, Destination: {flight.destination}")

    filtered_flights = [
        flight for flight in flights
        if flight.source == departure_place and flight.destination == destination_place
    ]

    print(f"Filtered Flights: {filtered_flights}")

    return render_template('available flights.html', flights=filtered_flights)

@app.route('/seat_selection/<flightNumber>', methods=['GET', 'POST'])
def seat_selection(flightNumber):
    selected_flight = next((flight for flight in flights if flight.flightNumber == flightNumber), None)
    print("Processing seat selection...")

    if request.method == 'POST':
        selected_seats = request.form.getlist('seat[]')

        if not selected_seats:
            return render_template('seat_selection.html', flight=selected_flight, error="Please select at least one seat.")

        for seat in selected_seats:
            if seat.isdigit():  # Check if the seat is an integer
                seat = str(seat)  # Convert it to a string

            if seat not in selected_flight.availableSeats:
                return render_template('seat_selection.html', flight=selected_flight, error=f"Seat {seat} is not available.")

        for seat in selected_seats:
            selected_flight.availableSeats.remove(seat)

        print("Seats selected:", selected_seats)
        return redirect(url_for('payment', flightNumber=flightNumber, selected_seats=selected_seats))

    return render_template('seat_selection.html', flight=selected_flight)

@app.route('/payment/<flightNumber>/<selected_seat>', methods=['GET', 'POST'])
def payment(flightNumber, selected_seat):
    if request.method == 'POST':
        return "Payment successful! Your seat is booked."
    else:
        return render_template('payment.html', flightNumber=flightNumber, selected_seat=selected_seat)



@app.route('/book/<flightNumber>', methods=['GET', 'POST'])
def book(flightNumber):
    if request.method == 'POST':
        numPassengers = int(request.form['num_passengers'])
        return "Booking successful!"
    else:
        return render_template('book.html', flightNumber=flightNumber)

if __name__ == '__main__':
    app.run(debug=True)
