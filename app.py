""" Import dependencies:
    - Flask framework API 
    - SQLAlchemy DB helper functions
    - psycopg2 PostgreSQL DB adapter """
    
from flask import Flask, render_template, json, jsonify, request, redirect, url_for
from flask_bootstrap import Bootstrap
from sqlalchemy.orm import load_only
from sqlalchemy import and_, or_
from database import db_session, POSTGRES, SQLALCHEMY_DATABASE_URI, cursor
from models.models import Articles
from forms.forms import FieldSelection, FieldSliders, text_fields, makeHTMLTable
from datetime import date, datetime
from math import floor, ceil
import psycopg2 as dbapi

# Initialize Flask
app = Flask(__name__)

# Config
app.config["SECRET_KEY"] = b"\xce\x8e\xc7\x8b\\\x1c\x07\xfa\xda\xe3\xa2\xcd\x05"
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

#globals
data = -1
formatted_source1 = -1
source1 = []
formatted_source2 = -1
source2 = []

# Query attribute/field names from the database
field_names = sorted([column.key for column in Articles.__table__.columns if not column.key in text_fields])
field_names = text_fields + field_names

Bootstrap(app)

def field_selector(fields):
    global field_names
    
    fields2 = set(fields)
    # Required for checkbox initialization
    field_tuples = [(x, x in fields2) for x in field_names[4:8]] + [(x, x in fields2) for x in field_names[8:]]  
    
    form = FieldSelection(field_tuples)
    
    return form
    
def range_filter_helper(fields, ranges):
    # Query by the relevant fields
    q = "SELECT "
    
    for field in fields:
        q += "%s, " % field
        
    # Filter by user input field ranges
    q = q.strip().strip(",")
    q += " FROM articles"
    
    # Execute the query
    cursor.execute(q)
    
    # Fetch all results of the query
    results = cursor.fetchall()
    
    #find min and max for each relevant field
    bounds = dict()
    for i in range(len(fields)):
        if not fields[i] in text_fields:
            currentField = [float(x[i]) for x in results]
            currentMin = floor(min(currentField))
            currentMax = ceil(max(currentField))
            bounds[fields[i]] = (currentMin, currentMax)
    
    today = date.today().strftime('%m/%d/%y')
    form2 = FieldSliders(fields, bounds, ranges)    
    
    return form2, today

def find_sources(source1, source2):
    global formatted_source1
    global formatted_source2
    
    #find all sources in data (only need to do once)
    if formatted_source1 == -1 or formatted_source2 == -1:   
        cursor.execute("SELECT DISTINCT source1 FROM articles")
        all_source1 = cursor.fetchall() #format: list of tuples
        formatted_source1 = [(x[0], True) for x in all_source1]
        
        cursor.execute("SELECT DISTINCT source2 FROM articles")
        all_source2 = cursor.fetchall() #format: list of tuples
        formatted_source2 = [(x[0], True) for x in all_source2]
    
    if len(source1) > 0:
        c = set(source1)
        formatted_source1 = [(x[0], x[0] in c) for x in formatted_source1]
    if len(source2) > 0:
        c = set(source2)
        formatted_source2 = [(x[0], x[0] in c) for x in formatted_source2]

    source1_form = FieldSelection(formatted_source1)
    source2_form = FieldSelection(formatted_source2)
    
    return source1_form, source2_form
    

def table_helper(data, fields, ranges, source1, source2):
    from_date, to_date = data[-1][1].split(" - ")

    # Convert dates from the daterange plugin's format to Year-Month-Day
    from_date = datetime.strptime(from_date, '%m/%d/%Y').strftime("%Y-%m-%d")
    to_date = datetime.strptime(to_date, '%m/%d/%Y').strftime("%Y-%m-%d")

    # Convert ranges from semicolon delimited strings to lists
    converted_ranges = []
    for r in ranges:
        converted_ranges.append(tuple(map(int, r.split(";"))))

    # Query by the relevant fields
    q = "SELECT "
    
    for field in fields:
        q += "%s, " % field

    q = q.strip().strip(",")
    q += " FROM articles WHERE "
        
    # Filter by user input field ranges    
    for i in range(len(fields)):
        if not fields[i] in text_fields:
            q += "CAST(%s AS float) >= %f and CAST(%s AS float) <= %f and " % \
                 (fields[i], converted_ranges[i][0], \
                    fields[i], converted_ranges[i][1])
    
    # Filter by date range
    q += "title1_date >= '%s' and title1_date" \
         "<= '%s'" % (from_date, to_date)
    
    # Filter by sources (using or statements only)
    if len(source1) + len(source2) > 0:
        q += " and ("
    
        for i in range(len(source1)):
            q += "source1 = '{}'".format(source1[i])
            q += " or "
        
        for i in range(len(source2)):
            q += "source2 = '{}'".format(source2[i])
            q += " or "
    
        q = q.strip().strip(" or")
        q += ")"
    
    
    # Execute the query
    cursor.execute(q)
    
    # Fetch all results of the query
    results = cursor.fetchall()
        
    # Make a dynamic HTML table to display the selected fields
    table = makeHTMLTable(fields, results)      
    return table
    
def build_site(data, source1, source2):
    fields, ranges = zip(*(data[:-1]))

    #Field Selection
    form = field_selector(fields)
    
    #RangeFilter
    #obtain querydata to determine ranges for sliders
    # Query the POSTGRES database using dynamic SQL        
    form2, today = range_filter_helper(fields, ranges)
    
    #Sources
    source1_form, source2_form = find_sources(source1, source2)
    
    #Table
    table = table_helper(data, fields, ranges, source1, source2)
            
    return render_template("index.html", form=form, form2=form2, source1_form=source1_form, source2_form=source2_form, today=today, table=table)

def data_converter(fields):
    data = [(field, '-100;100') for field in fields]
    
    today = date.today().strftime('%m/%d/%Y')
    daterange = '01/01/2010 - ' + today
    data.append(('daterange', daterange))
    return data

@app.route("/")
def index():
    global source1
    global source2
    global data
    fields = text_fields[4:-1]
    data = data_converter(fields)
    return build_site(data, source1, source2)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/range_filter", methods=["POST"])
def range_filter():
    global source1
    global source2
    global data
    fields = list(request.form)
    
    #preserve slider values
    data2 = data_converter(fields)
    
    oldData = dict()
    for d in data:
        oldData[d[0]] = d
        
        #rebuild data
        data = []
        for d in data2:
            if d[0] in oldData:
                data.append(oldData[d[0]])
            else:
                data.append(d)
    
    return build_site(data, source1, source2)

@app.route("/source_filter/<source>", methods=["POST"])
def source_filter(source):
    global source1
    global source2
    global data
    if source == "source1":
        source1 = list(request.form)
        
        if len(source1) == 0: #no sources
            source1.append("")
    
    elif source == "source2":
        source2 = list(request.form)
        
        if len(source2) == 0: #no sources
            source2.append("")

    return build_site(data, source1, source2)

@app.route("/data", methods=["POST"])
def data():    
    global data
    global source1
    global source2
    data = [(k, v) for k, v in request.form.items()] 
    return build_site(data, source1, source2)

if __name__ == "__main__":
    app.run()
    #app.run(debug=True)
    print("Working...")