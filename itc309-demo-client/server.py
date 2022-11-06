import requests
import pandas as pd
from flask import Flask, render_template, request, flash, url_for, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jgfgjor5ss35'
sta_schema = ['Things', 'Locations', 'Sensors', 'ObservedProperties', 'Datastreams', 'Observations',
              'FeaturesOfInterest']

FROST_URL = "https://frost-server.anthonydera.com/FROST-Server"
bearer = {'Authorization': 'Bearer ' + '456456'}


# @app.route("/")
# def home():
#     return render_template("index.html")


@app.route("/", methods=['GET', 'POST'])
def home():
    global server_url
    global username
    global password
    global url_set
    global url_option

    if request.method == 'POST':
        server_url = request.form['url']
        username = request.form['username']
        password = request.form['password']
        url_option = request.form['url_option']
        if not server_url:
            flash('URL is required!')
            server_url = FROST_URL
            url_set = False
        if not username:
            flash('Username is required!')
            url_set = False
        elif not password:
            flash('Password is required!')
            url_set = False
        else:
            url_set = True
            return redirect(url_for('get_main'))
    url_set = False
    return render_template("index.html", url_set=url_set)


@app.route("/main")
def get_main():
    table_rows = []
    try:
        for entity in sta_schema:
            url_path = f"{server_url}/v1.0/{entity}?$count=true&$select=@iot.count"
            frost_data = get_Data(url_path)
            entity_count = frost_data["@iot.count"]
            table_rows.append({entity: entity_count})
    except requests.HTTPError as err:
        print(err)
        return render_template("401.html")
    except requests.ConnectionError as err:
        print(err)
        return render_template("ConnectionError.html")
    return render_template("main.html", table_rows=table_rows, url_path=url_path)


@app.route("/Things")
def get_Things():
    url_path = f"{server_url}/v1.0/Things?$orderby=@iot.id&$select=@iot.id,name,description,properties"
    return render_template("things.html", data=get_Data(url_path)["value"], url_path=url_path)


@app.route("/Locations")
def get_Locations():
    url_path = f"{server_url}/v1.0/Locations?$select=@iot.id,name,description,location,properties"
    return render_template("locations.html", data=get_Data(url_path)["value"], url_path=url_path)


@app.route("/Location/<id>")
def get_LocationMap(id):
    url_path = f"{server_url}/v1.0/Locations({id})?$select=@iot.id,name,description,location,properties"
    data = get_Data(url_path)
    lat = data["location"]["coordinates"][0]
    lon = data["location"]["coordinates"][1]

    return render_template("location_Map.html", data=data, lat=lat, lon=lon, id=id, url_path=url_path)


@app.route("/Sensors")
def get_Sensors():
    url_path = f"{server_url}/v1.0/Sensors?$select=@iot.id,name,description,properties,Encodingtype,Metadata"
    return render_template("sensors.html", data=get_Data(url_path)["value"], url_path=url_path)


@app.route("/ObservedProperties")
def get_ObservedProperties():
    url_path = f"{server_url}/v1.0/ObservedProperties?$select=@iot.id,name,description,definition, properties"
    return render_template("observed_properties.html", data=get_Data(url_path)["value"], url_path=url_path)


@app.route("/Datastreams")
def get_Datastreams():
    url_path = f"{server_url}/v1.0/Datastreams?$orderby=@iot.id&$select=@iot.id,name,description,observationType,unitOfMeasurement"
    return render_template("datastreams.html", data=get_Data(url_path)["value"], url_path=url_path)


@app.route("/Datastream/<id>")
def get_Datastream(id):
    url_path = f"{server_url}/v1.0/Datastreams({id})?$orderby=@iot.id&$select=@iot.id,name,description,observationType,unitOfMeasurement"
    return render_template("datastreams.html", data=[get_Data(url_path)], url_path=url_path)


@app.route("/Observations/<id>")
def get_Observations(id):
    url_path = f"{server_url}/v1.0/Datastreams({id})/Observations?$orderby=@iot.id&$select=@iot.id,phenomenonTime,parameters,result"
    data = get_Data(url_path)["value"]
    try:
        df = pd.DataFrame(data)
        labels = df["phenomenonTime"].to_list()
        values = df["result"].to_list()
    except UnboundLocalError:
        print("result is empty")
        return render_template("error.html")
    except KeyError:
        return render_template("error.html")

    return render_template("observations.html", data=data, labels=labels, values=values, id=id, url_path=url_path)


@app.route("/FeaturesOfInterest")
def get_FeaturesOfInterest():
    url_path = f"{server_url}/v1.0/FeaturesOfInterest?$select=@iot.id,name,description,encodingType,feature.coordinates"
    return render_template("features.html", data=get_Data(url_path)["value"], url_path=url_path)


@app.route("/FeatureOfInterest/<id>")
def get_FeatureOfInterest(id):
    url_path = f"{server_url}/v1.0/Observations({id})/FeatureOfInterest?$select=@iot.id,name,description,encodingType,feature"
    return render_template("feature.html", data=get_Data(url_path), id=id, url_path=url_path)


@app.route("/Thing/<id>")
def get_things_related(id):
    url_path = f"{server_url}/v1.0/Things({id})/Locations?$orderby=@iot.id&$select=@iot.id,name"
    locations = get_Data(url_path)["value"]
    url_path = f"{server_url}/v1.0/Things({id})/Datastreams?$orderby=@iot.id&$select=@iot.id,name"
    datastreams = get_Data(url_path)["value"]
    return render_template("things_relations.html", id=id, datastreams=datastreams, locations=locations,
                           url_path=url_path)


def get_Data(url_path):
    if url_option == 'frost':
        frost_response = requests.get(url_path, auth=(username, password))
    else:
        frost_response = requests.get(url_path, headers=bearer)
    if frost_response.status_code == 401:
        frost_response.raise_for_status()
    if frost_response.status_code == 302:
        frost_response.raise_for_status()
    return frost_response.json()


@app.errorhandler(401)
def errorHandler(e):
    return render_template('302.html'), 401


if __name__ == "__main__":
    app.run(debug=True)
