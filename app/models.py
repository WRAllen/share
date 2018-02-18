from . import db

class BaseTable(db.Model): 
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(64),unique=True)

tab_relation = lambda tname, col1, fk1, col2, fk2:db.Table(tname,
    db.Column(col1,db.Integer,db.ForeignKey(fk1)),
    db.Column(col2,db.Integer,db.ForeignKey(fk2)))

