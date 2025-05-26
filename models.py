from database import db
from datetime import date

class Bill(db.Model):
    __tablename__ = 'billing_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Surrogate PK
    billing_id = db.Column(db.Date)
    monthyear = db.Column(db.String(20))
    customeraccountno = db.Column(db.String(50))
    referencenumber = db.Column(db.String(50))
    customerfirstname = db.Column(db.String(100))
    customeraddress = db.Column(db.String(200))
    phonenumber = db.Column(db.String(20))
    region = db.Column(db.String(50))
    feeder33kv = db.Column(db.String(50))
    feeder11kv = db.Column(db.String(50))
    transformernumber = db.Column(db.String(50))
    dtname = db.Column(db.String(100))
    tariffcode = db.Column(db.String(50))
    tariffrate = db.Column(db.String(20))
    statuscode = db.Column(db.String(20))
    billingtype = db.Column(db.String(50))
    meternumber = db.Column(db.String(50))
    presentreading = db.Column(db.String(20))
    previousreading = db.Column(db.String(20))
    meterstatus = db.Column(db.String(50))
    openingbalance = db.Column(db.String(20))
    adjustment = db.Column(db.String(20))
    totalpayment = db.Column(db.String(20))
    lastpaymentdate = db.Column(db.Date)
    lastpaymentamount = db.Column(db.String(20))
    netarrears = db.Column(db.String(20))
    energykwh = db.Column(db.String(20))
    currentvatamount = db.Column(db.String(20))
    totalamountbilled = db.Column(db.String(20))
    closingbalance = db.Column(db.String(20))

    def __repr__(self):
        return f"<Bill {self.customeraccountno} - {self.monthyear}>"
