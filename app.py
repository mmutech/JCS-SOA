from flask import Flask, render_template, send_file, request, after_this_request, abort
from sqlalchemy import desc
from datetime import datetime
from database import db, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models import Bill
import pandas as pd
import os
import uuid

app = Flask(__name__)

# Set config from database.py
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

# Initialize DB
db.init_app(app)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/export-soa")
def export_soa():
    account_no = request.args.get('account_no')
    # start_date = request.args.get('start_date')
    # end_date = request.args.get('end_date')

    query = Bill.query.order_by(desc(Bill.billing_id))

    if account_no:
        query = query.filter(Bill.customeraccountno == account_no)

    # if start_date:
    #     try:
    #         start = datetime.strptime(start_date, "%Y-%m-%d").date()
    #         query = query.filter(Bill.billing_id >= start)
    #     except ValueError:
    #         return "Invalid start_date format. Use YYYY-MM-DD", 400

    # if end_date:
    #     try:
    #         end = datetime.strptime(end_date, "%Y-%m-%d").date()
    #         query = query.filter(Bill.billing_id <= end)
    #     except ValueError:
    #         return "Invalid end_date format. Use YYYY-MM-DD", 400

    bills = query.all()

    if not bills:
        return "No data found for the specified filters.", 404

    bill_data = [{
        "Billing ID": b.billing_id,
        "Month/Year": b.monthyear,
        "Customer Account No": b.customeraccountno,
        "Reference Number": b.referencenumber,
        "Customer Name": b.customerfirstname,
        "Customer Address": b.customeraddress,
        "Phone Number": b.phonenumber,
        "Region": b.region,
        "33KV Feeder": b.feeder33kv,
        "11KV Feeder": b.feeder11kv,
        "Transformer Number": b.transformernumber,
        "DT Name": b.dtname,
        "Tariff Code": b.tariffcode,
        "Tariff Rate": b.tariffrate,
        "Status Code": b.statuscode,
        "Billing Type": b.billingtype,
        "Meter Number": b.meternumber,
        "Present Reading": b.presentreading,
        "Previous Reading": b.previousreading,
        "Meter Status": b.meterstatus,
        "Opening Balance": b.openingbalance,
        "Adjustment": b.adjustment,
        "Total Payment": b.totalpayment,
        "Last Payment Date": b.lastpaymentdate,
        "Last Payment Amount": b.lastpaymentamount,
        "Net Arrears": b.netarrears,
        "Energy (kWh)": b.energykwh,
        "Current VAT Amount": b.currentvatamount,
        "Total Amount Billed": b.totalamountbilled,
        "Closing Balance": b.closingbalance
    } for b in bills]

    # Generate unique file path
    account_part = account_no if account_no else "all"
    unique_id = uuid.uuid4().hex[:8]
    file_path = f"soa_export_{account_part}_{unique_id}.xlsx"

    # Save DataFrame to Excel
    df = pd.DataFrame(bill_data)
    df.to_excel(file_path, index=False)

    @after_this_request
    def cleanup(response):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Failed to delete temp file: {e}")
        return response

    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
