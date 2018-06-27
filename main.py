import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)
app.secret_key = b"q[8m\x17\xafn\xacw'\xe6;\xbbF2\xc1\xb9,\x9b\x04\xc7\xa0\x1f\x0e"


@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/add', methods=['GET', 'POST'])
def add():
    # session[donation]
    if 'donation' not in session:
        session['donation'] = [0]
    if request.method == 'POST':
        donation = (request.form['amount'])

    return render_template('create.jinja2', session=session)


@app.route('/submit', methods=['POST'])
def submit():
    donor_name = request.form['name']
    donor_amount = request.form['amount']
    print(donor_amount)
    print(donor_name)
    # Attempt to look up an existing matching donor, if one is found, you'll nave a 'Donor' object.
    # if not, create a new one
    try:
        donor = Donor.get(Donor.name == donor_name)
        print("Found saved donor: " + str(donor))
    except Donor.DoesNotExist:
        donor = Donor(name=donor_name)
        donor.save()

    code = base64.b32encode(os.urandom(8)).decode().strip("=")
    saved_donation = Donation(value=donor_amount, donor=donor, code=code)
    saved_donation.save()

    return render_template('submit.jinja2', code=code)


@app.route('/retrieve')
def retrieve():
    code = request.args.get('code', None)

    if code is None:
        return render_template('retrieve.jinja2')
    else:
        try:
            saved_donation = Donation.get(Donation.code == code)
        except Donation.DoesNotExist:
            return render_template(retrieve.jinja2, error="Code not found.")

        session['donation'] = saved_donation.value

        return redirect(url_for('submit'))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
