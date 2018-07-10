from app import db

# db.reflect()
#

class Measurement(db.Model):
    __tablename__ = 'measurement'


class Station(db.Model):
    __tablename__ = 'station'
