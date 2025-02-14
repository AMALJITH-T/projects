from flask import Flask, render_template, redirect, url_for, request, session, flash
from database import init_db, db_session
from models import User, Room, Reservation
from datetime import datetime, timedelta
import secrets
from sqlalchemy.orm import joinedload
from flask import request

app = Flask(__name__)
secret_key = secrets.token_hex(16)
app.secret_key = secret_key
app.config['SIMULATED_CURRENT_TIME'] = None

# Initialize the database
init_db()

# Example data
example_rooms = [
    {"room_number": "101", "room_type": "Standard", "price": 100},
    {"room_number": "102", "room_type": "Deluxe", "price": 150},
    {"room_number": "103", "room_type": "Suite", "price": 200},
]

# Populate example rooms
for room_data in example_rooms:
    room_number = room_data["room_number"]
    existing_room = Room.query.filter_by(room_number=room_number).first()

    if not existing_room:
        room = Room(**room_data)
        db_session.add(room)

db_session.commit()

def is_admin(user_id):
    user = User.query.get(user_id)
    return user and user.is_admin
    

# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Replace the following with your actual user authentication logic
        if username == 'Amal123' and password == 'Amal@123':
            user_id = '1'
            session['user_id'] = user_id  # Set the user_id for the session
            flash('Login successful!', 'success')
            return redirect(url_for('book_room'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

# Remove the registration route
# (You can keep the logout route if needed)

# Note: Ensure that you update the navigation links in your templates accordingly.




@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/book_room', methods=['GET', 'POST'])
def book_room():
    if 'user_id' not in session:
        flash('Please log in to book a room.', 'error')
        return redirect(url_for('login'))
    
    current_time = app.config['SIMULATED_CURRENT_TIME'] or datetime.now()

    if request.method == 'POST':
        room_id = int(request.form.get('room'))
        check_in_date = datetime.strptime(request.form.get('check_in_date'), '%Y-%m-%d')
        check_out_date = datetime.strptime(request.form.get('check_out_date'), '%Y-%m-%d')

        user_id = session['user_id']

        # Check if the room is available for the selected dates
        room = Room.query.filter_by(id=room_id).options(joinedload(Room.reservations)).first()
        if not room or not room.is_available(check_in_date, check_out_date):
            return render_template('book_room.html', rooms=Room.query.all(), error="Room not available for selected dates")

        user = User.query.get(user_id)

        # Check if the user has overlapping reservations
        if user.has_overlapping_reservation(room_id, check_in_date, check_out_date):
            return render_template('book_room.html', rooms=Room.query.all(), error="Room booked by the user for overlapping dates")

        # Add the reservation to the booking history
        reservation = Reservation(user_id=user_id, room_id=room_id, check_in_date=check_in_date, check_out_date=check_out_date)
        db_session.add(reservation)
        db_session.commit()

        booking_details = {
            'booking_id': reservation.id,
            'room_number': room.room_number,
            'check_in_date': check_in_date.strftime('%Y-%m-%d'),
            'check_out_date': check_out_date.strftime('%Y-%m-%d')
        }

        return render_template('proof_of_booking.html', **booking_details)

    rooms = Room.query.all()
    return render_template('book_room.html', rooms=rooms)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        return redirect(url_for('proof_of_booking'))

    return render_template('payment.html')

@app.route('/proof_of_booking')
def proof_of_booking():
    booking_id = request.args.get('booking_id')
    booking_details = get_booking_details(booking_id)
    return render_template('proof_of_booking.html', **booking_details)

@app.route('/set_simulated_time', methods=['POST'])
def set_simulated_time():
    simulated_time_str = request.form.get('simulated_time')
    
    if simulated_time_str:
        # Parse the submitted time string
        simulated_time = datetime.strptime(simulated_time_str, '%Y-%m-%dT%H:%M')
        
        # Set the simulated current time in the app config
        app.config['SIMULATED_CURRENT_TIME'] = simulated_time

    return redirect(url_for('book_room'))

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if not user or not user.is_admin:
        return redirect(url_for('index'))

    reservations = Reservation.query.all()
    return render_template('admin_dashboard.html', reservations=reservations)

if __name__ == '__main__':
    app.run(debug=True)
