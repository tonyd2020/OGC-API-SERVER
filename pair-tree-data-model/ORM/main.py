import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import backref

URI = "postgres://team6:ITC303@localhost:5430/pairtree"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    cmd_id = db.Column(db.Integer)
    sites = db.relationship('Site', backref='site_owner')
    devices = db.relationship('Device', backref='device_owner')
    samples = db.relationship('Sample', backref='owner')

class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    todo_geo_fence = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id',
                                                   onupdate='RESTRICT',
                                                   ondelete='RESTRICT'))
    sub_sites = db.relationship('SubSite', backref='main_site')


class OemDevice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    num_sensors = db.Column(db.Integer)
    devices = db.relationship('Device', backref='oem_device')
    sensors = db.relationship('OemSensor', backref='oem_device')


class Sample(db.Model):
    oem_sensor_id = db.Column(db.Integer, db.ForeignKey('oem_sensor.id',
                                                        onupdate='RESTRICT',
                                                        ondelete='RESTRICT'), primary_key=True)
    sub_site_id = db.Column(db.Integer, db.ForeignKey('sub_site.id',
                                                      onupdate='RESTRICT',
                                                      ondelete='RESTRICT'), primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id',
                                                   onupdate='RESTRICT',
                                                   ondelete='RESTRICT'), primary_key=True)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.TIMESTAMP)
    value = db.Column(db.Float)
    metric = db.Column(db.String(50))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    height = db.Column(db.Float)
    sensor = db.relationship('OemSensor', back_populates='locations')
    location = db.relationship('SubSite', back_populates='sensors')


class OemSensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    oem_device_id = db.Column(db.Integer, db.ForeignKey('oem_device.id',
                                                        onupdate='RESTRICT',
                                                        ondelete='RESTRICT'))
    oem_sensor_decode = db.relationship('OemSensorDecode', backref='oem_sensor', uselist=False)
    # sub_sites= db.relationship('SubSite', secondary='sample')
    locations = db.relationship('Sample', back_populates='sensor')


class SubSite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    todo_geo_fence = db.Column(db.Integer)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id',
                                                  onupdate='RESTRICT',
                                                  ondelete='RESTRICT'))
    devices = db.relationship('Device', backref='sub_site')
    # samples = db.relationship('Sample', back_populates='sub_site')
    sensors = db.relationship('Sample', back_populates='location')


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_eui = db.Column(db.String(40))
    network_eui = db.Column(db.String(40))
    comments = db.Column(db.TEXT)
    installed = db.Column(db.TIMESTAMP)
    decomm = db.Column(db.TIMESTAMP)
    active = db.Column(db.Boolean)
    location_name = db.Column(db.String(50))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    subsite_id = db.Column(db.Integer, db.ForeignKey('sub_site.id',
                                                     onupdate='RESTRICT',
                                                     ondelete='RESTRICT'))
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id',
                                                   onupdate='RESTRICT',
                                                   ondelete='RESTRICT'))
    oem_device_id = db.Column(db.Integer, db.ForeignKey('oem_device.id',
                                                        onupdate='RESTRICT',
                                                        ondelete='RESTRICT'))


class OemSensorDecode(db.Model):
    oem_sensor_id = db.Column(db.Integer, db.ForeignKey('oem_sensor.id',
                                                        onupdate='RESTRICT',
                                                        ondelete='RESTRICT'), primary_key=True)
    metric = db.Column(db.String(50))
    packet_ind = db.Column(db.String(100))
    packet_ind_mask = db.Column(db.String(100))
    field = db.Column(db.String(100))
    label = db.Column(db.String(100))
    unit = db.Column(db.String(100))
    packet = db.Column(db.Integer)
    byte_start = db.Column(db.Integer)
    byte_end = db.Column(db.Integer)
    type = db.Column(db.String(100))
    offset = db.Column(db.Float)
    multiplier = db.Column(db.Float)


# Create the Database
db.create_all()

# Add an owner
tony = Owner(name="Tony", cmd_id=1)
brad = Owner(name="Brad", cmd_id=10)
frank = Owner(name="Frank", cmd_id=100)
db.session.add(tony)
db.session.add(brad)
db.session.add(frank)
db.session.commit()

# Add a Site
# owner = Owner.query.filter_by(id=1).first()
# print(owner.name)
my_farm = Site(name="Tony's Farm", owner_id=1, todo_geo_fence=123456)
db.session.add(my_farm)
db.session.commit()

# Add a Sub site
my_farm = Site.query.filter_by(id=1).first()
print(my_farm.name)
my_farm_sub_site = SubSite(name="West side of Tony's Farm", site_id=1, todo_geo_fence=123460)
db.session.add(my_farm_sub_site)
db.session.commit()

# # Add an OEM Device
jaycar_therm = OemDevice(name="Jaycar Temperature Sensor", num_sensors=1)
db.session.add(jaycar_therm)
db.session.commit()

# Add a Device
dev = Device(comments="West side Temperature sensor",
             device_eui="aaaa.bbbb.cccc.1234",
             network_eui="10.1.0.123",
             installed=datetime.datetime.now(),
             active=True,
             location_name="Greenhouse",
             subsite_id=1,
             owner_id=1,
             oem_device_id=1)
db.session.add(dev)
db.session.commit()

# Add an OEM Sensor
jaycar_therm_sensor = OemSensor(name="NE corner temp sensor", oem_device_id=1)
db.session.add(jaycar_therm_sensor)
db.session.commit()


db_engine = create_engine(URI)
result = db_engine.execute("""
CREATE OR REPLACE FUNCTION notify_sample_changes()
RETURNS trigger AS $$
BEGIN
  PERFORM pg_notify(
    'sample_changed',
    json_build_object(
      'operation', TG_OP,
      'record', row_to_json(NEW)
    )::text
  );

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER sample_changed
AFTER INSERT OR UPDATE
ON public.sample
FOR EACH ROW
EXECUTE PROCEDURE notify_sample_changes();
""")

sample1 = Sample(
    time=datetime.datetime.now(),
    value=283.56,
    metric="Indoor Temperature",
    longitude=-100.456,
    latitude=123.345,
    height=45.04,
    oem_sensor_id=1,
    sub_site_id=1,
    owner_id=1
)

db.session.add(sample1)
db.session.commit()

