#[Balanced Payments](http://balancedpayments.com) Example
**Flask & Bootstrap 3 Starter Project to Process Credit Cards**

This is a fully working Flask & Bootstrap 3 Implementation of Balanced Payments Credit Card processing. It uses Balanced.js to securely handle payment details. 

Use this example as a starting point for your own project, or copy and paste code for your existing project. 

##Set up locally
####Without virtual environment:

	git clone git@github.com:NickWoodhams/Balanced-Payments-Flask-Starter.git
	cd Balanced-Payments-Flask-Starter
	pip install -r requirements.txt

####With virtual environment:

	git clone git@github.com:NickWoodhams/Balanced-Payments-Flask-Starter.git
	cd Balanced-Payments-Flask-Starter
	virtualenv venv
	source venv/bin/activate
	pip install -r requirements.txt

##Create Development Database
Create a Postgres or MySQL database locally, and use your database credentials in the next step. The database tables will be created the first time the code is executed. 

##Update config.py

Update your Database settings, secret key, and [http://balancedpayments.com](Balanced Payments) credentials.

Copy your Marketplace Credentials from your Balanced Payments Dashboard. Debug mode is set to True, but should always be set to False when live.

##Start the Webserver

Simply run `python app.py`

The project should be accessable at [http://localhost:9030](http://localhost:9030)
