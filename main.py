from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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
    date = request.form['date']
    time = request.form['time']
    guests = request.form['guests']
    


    return redirect(url_for('booking'))

if __name__ == '__main__':
    app.run(debug=True)
