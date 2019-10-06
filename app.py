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
from forms.forms import FieldSelection, FieldSliders, text_fields, makeHTMLTable, SourceSelection
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
form3 = -1
sources = {-1}

Bootstrap(app)

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
    
    return form2, q, today

def table_helper(data, fields, ranges, sources, q):
    global form3
    
    from_date, to_date = data[-1][1].split(" - ")

    # Convert dates from the daterange plugin's format to Year-Month-Day
    from_date = datetime.strptime(from_date, '%m/%d/%Y').strftime("%Y-%m-%d")
    to_date = datetime.strptime(to_date, '%m/%d/%Y').strftime("%Y-%m-%d")

    # Convert ranges from semicolon delimited strings to lists
    converted_ranges = []
    for r in ranges:
        converted_ranges.append(tuple(map(int, r.split(";"))))

    q += " WHERE "
    
    for i in range(len(fields)):
        if not fields[i] in text_fields:
            q += "CAST(%s AS float) >= %f and CAST(%s AS float) <= %f and " % \
                 (fields[i], converted_ranges[i][0], \
                    fields[i], converted_ranges[i][1])
    
    # Filter by date range
    q += "title1_date >= '%s' and title1_date " \
         "<= '%s'" % (from_date, to_date)
    
    # Execute the query
    cursor.execute(q)
    
    # Fetch all results of the query
    results = cursor.fetchall()
    
    #Find sources in results
    resultSources = [x[1][3:-4].split("</p><p>") for x in results]
    
    f1 = lambda x: (x[0], True)
    f2 = lambda x: (x[1], True)
    
    #find all sources in data (only need to do once
    if form3 == -1:
        allSources = set([f(x) for x in resultSources for f in (f1, f2)]) 
        sortedSources = sorted(list(allSources))
        form3 = SourceSelection(sortedSources)        
    
    i = 0
    while i < len(results) and not -1 in sources:
        if not resultSources[i][0] in sources and not resultSources[i][1] in sources:
            results = results[:i] + results[i + 1:]
            resultSources = resultSources[:i] + resultSources[i + 1:]
            i -= 1
            
        i += 1
    
    # Make a dynamic HTML table to display the selected fields
    table = makeHTMLTable(fields, results)      
    return table, form3
    
def buildSite(data, sources):
    fields, ranges = zip(*(data[:-1]))

    #Field Selection
    form = FieldSelection()
    
    #RangeFilter
    #obtain querydata to determine ranges for sliders
    # Query the POSTGRES database using dynamic SQL    
    cursor.execute("select * from Articles")
    
    form2, q, today = range_filter_helper(fields, ranges)
    
    #Table
    table, form3 = table_helper(data, fields, ranges, sources, q)
            
    return render_template("index.html", form=form, form2=form2, form3=form3, today=today, table=table)

def dataConverter(fields):
    data = [(field, '-100;100') for field in fields]
    
    today = date.today().strftime('%m/%d/%Y')
    daterange = '01/01/2010 - ' + today
    data.append(('daterange', daterange))
    return data

@app.route("/")
def index():
    global sources
    global data
    fields = text_fields[4:-1]
    data = dataConverter(fields)
    return buildSite(data, sources)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/range_filter", methods=["POST"])
def range_filter():
    global sources
    global data
    fields = list(request.form)
    fields = fields[1:]   
    data = dataConverter(fields)
    return buildSite(data, sources)

@app.route("/source_filter", methods=["POST"])
def source_filter():
    global sources
    global data
    sources = set(request.form)
    return buildSite(data, sources)

@app.route("/data", methods=["POST"])
def data():    
    global data
    global sources
    data = [(k, v) for k, v in request.form.items()] 
    return buildSite(data, sources)

if __name__ == "__main__":
    app.run()
    #app.run(debug=True)
    print("Working...")