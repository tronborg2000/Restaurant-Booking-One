from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    guests = db.Column(db.Integer, nullable=False)

def save_booking(name, email, phone, date, time, guests):
    new_booking = Booking(name=name, email=email, phone=phone, date=date, time=time, guests=guests)
    db.session.add(new_booking)
    db.session.commit()

def is_available(date, time):
    existing_bookings = Booking.query.filter_by(date=date, time=time).all()
    return len(existing_bookings) == 0

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/submit-booking', methods=['POST'])
def submit_booking():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']

    try:
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        time = datetime.strptime(request.form['time'], '%H:%M').time()
    except ValueError:
        return render_template('booking.html', error="Invalid date or time format. Please try again.")

    guests = int(request.form['guests'])

    if is_available(date, time):
        save_booking(name, email, phone, date, time, guests)
        return redirect(url_for('booking'))
    else:
        return render_template('booking.html', error="The selected date and time are not available.")

if __name__ == '__main__':
    app.run(debug=True)

