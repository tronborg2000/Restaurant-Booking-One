from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, static_url_path='/assets', static_folder='assets')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

TOTAL_TABLES = 10  # Define the total number of tables available

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    tables = db.Column(db.Integer, nullable=False)  # Added field for the number of tables

def save_booking(name, email, phone, date, time, guests, tables):
    new_booking = Booking(name=name, email=email, phone=phone, date=date, time=time, guests=guests, tables=tables)
    db.session.add(new_booking)
    db.session.commit()

def is_available(date, time, tables):
    existing_bookings = Booking.query.filter_by(date=date, time=time).all()
    reserved_tables = sum([booking.tables for booking in existing_bookings])
    return (TOTAL_TABLES - reserved_tables) >= tables

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    success = request.args.get('success')
    error = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        try:
            date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
            time = datetime.strptime(request.form['time'], '%H:%M').time()
        except ValueError:
            return render_template('booking.html', error="Invalid date or time format. Please try again.")

        guests = int(request.form['guests'])
        tables = int(request.form['tables'])  # Get the number of tables from the form

        if is_available(date, time, tables):
            save_booking(name, email, phone, date, time, guests, tables)
            success = "Thank you for your booking!"
        else:
            error = "The selected date and time are not available or there aren't enough tables."

    return render_template('booking.html', success=success, error=error)

@app.route('/cancel_booking', methods=['GET', 'POST'])
def cancel_booking():
    success = request.args.get('success')
    error = None
    if request.method == 'POST':
        booking_id = request.form['booking_id']

        booking = Booking.query.get(booking_id)
        if booking:
            db.session.delete(booking)
            db.session.commit()
            success = "Your booking has been canceled."
        else:
            error = "No booking found with the provided ID."

    return render_template('cancel_booking.html', success=success, error=error)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

