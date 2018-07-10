from climate_app.__init__ import db

# db.reflect()


class Measurement(db.Model):
    __tablename__ = 'measurement'


class Station(db.Model):
    __tablename__ = 'station'
