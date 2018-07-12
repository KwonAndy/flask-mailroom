import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


# function that takes Donor and Donation information and adds it to the db
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        
        donor_name = request.form['donor']
        donation = int(request.form['amount'])
        # donation = float({0:.2f}.format(request.form['amount'])

        # if database does not contain the added donor, saves the new donor
        # if donor_name not in Donor.name:
        #     Donor(name = donor_name).save()

        try:
            donor = Donor.get(Donor.name == donor_name)
        except: 
            donor = Donor(name = donor_name)
            donor.save()

        Donation(donor = donor, value = donation).save()

        return redirect(url_for('home'))
    
    else:
        return render_template('add.jinja2')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port, debug=True)

