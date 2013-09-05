from flask import Flask, render_template, request, send_file, abort, redirect, make_response, url_for, jsonify, flash
from pprint import pprint
from modules.models import *
from modules.forms import *
from modules.custom_jinja_filters import *
import balanced


app = Flask(__name__)
app.config.from_pyfile('config.py', silent=False)
app.jinja_env.filters['format_currency'] = format_currency
balanced.configure(app.config['BALANCED_API_KEY'])


@app.route("/", methods=['GET', 'POST'])
def index():
    form = demoForm(csrf_enabled=False)
    if form.validate_on_submit():
        pprint(request.form)
        return redirect(url_for('order', username=form.merchant.data, item=form.item.data, price=form.amount.data))

    return render_template('index.html', form=form)


@app.route("/order/<username>/<item>/<float:price>", methods=['GET', 'POST'])
@app.route("/order/<username>/<item>/<int:price>", methods=['GET', 'POST'])
def order(username, item, price):
    form = orderDetailsForm()

    #populate the hidden fields in the form with information from the url
    form.username.data = username
    form.item.data = item
    form.price.data = price

    if form.validate_on_submit():
        #user entered all information sucessfully, save info to the database and send to payment page
        #save to database
        order = Order()
        form.populate_obj(order)
        db_session.add(order)
        db_session.commit()
        #redirect to the payment page
        return redirect(url_for('pay', order_id=order.id))

    return render_template('order.html', form=form, username=username, price=price)


@app.route("/pay/<int:order_id>", methods=['GET', 'POST'])
def pay(order_id):
    order = Order.query.get(order_id)
    if order.paid is True:
        return redirect(url_for('receipt', order_id=order.id))

    if request.method == 'POST':
        #charge the customer, mark the order as paid
        #need to create an account to attach the order to
        try:
            account = balanced.Marketplace.my_marketplace.create_buyer(
                email_address=None,
                card_uri=request.form['balancedCreditCardURI'],
                name=order.name,
            ).debit(
                amount=int(order.price)*100,
                description=order.item + " from " + order.username,
            )

            order.paid = True
            db_session.commit()
            return redirect(url_for('receipt', order_id=order.id))

        except balanced.exc.HTTPError as ex:
            flash('Transaction failed, %s' % ex.message, 'error')
            print ex

    return render_template('pay.html', order=order)


@app.route("/receipt/<int:order_id>")
def receipt(order_id):
    order = Order.query.get(order_id)
    if order.paid is not True:
        flash('Order is not yet paid', 'error')
        return redirect(url_for('pay', order_id=order.id))
    return render_template('receipt.html', order=order)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9030)
