from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, static_url_path='/assets', static_folder='assets')
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

        if is_available(date, time):
            save_booking(name, email, phone, date, time, guests)
            success = "Thank you for your booking!"
        else:
            error = "The selected date and time are not available."

        print("Success:", success, "Error:", error)  # Add this line

    return render_template('booking.html', success=success, error=error)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
