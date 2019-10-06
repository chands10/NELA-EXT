from flask import Markup
from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput, html_params
from wtforms.validators import Required
from models.models import Articles

# Non-digit fields that should be hidden in the sliders form
# We are still loading these into the form for indexing simplicity--possibly refactor?
# >>> Also should be prioritized in the table display <<<
text_fields = ["title1", "title2", "source1", "source2", "normal_display", "sources_display", \
    "title1_date", "title2_date", "lower_display"]

# Query attribute/field names from the database
field_names = sorted([column.key for column in Articles.__table__.columns if not column.key in text_fields])
field_names = text_fields + field_names

# Required for checkbox initialization
field_tuples = [(x, True) for x in field_names[4:9]] + [(x, False) for x in field_names[10:-1]]

""" Multiple checkbox (buttons) form for DB fields """

def select_multi_checkbox(fields, ul_class="", **kwargs):
    kwargs.setdefault("type", "btn")
    html = ["<div class='fields-container' align='left' style='border:2px solid #ccc; width:300px; height: " \
        "400px; overflow-y: scroll;'>"]
    html.append("<ul %s style='list-style-type: none;'>" % html_params(id="fields", class_=ul_class))
    html.append("<div data-toggle='buttons'>")
    for label, checked in fields:
        field_id = "%s" % (label)
        options = dict(kwargs, name=label, id=field_id)
        html.append("<li><label class='btn btn-light btn-block'>")
        html.append("<input type='checkbox' autocomplete='off' class='invisible field-btn'" \
            "%s>%s</label></li>" % 
                    (html_params(**options), field_id))
    html.append("</div>")
    html.append("</ul>")
    html.append("</div>")
    return "".join(html)

class FieldSelection(FlaskForm):
    #Fields = None
    Fields = Markup(select_multi_checkbox( fields=field_tuples ) )
    #def __init__(self, fields2):
        #fields2 = set(fields2)
        ## Required for checkbox initialization
        #field_tuples = [(x, x in fields2) for x in field_names[4:-1]]
        #self.Fields = Markup(select_multi_checkbox( fields=field_tuples ) )

class SourceSelection(FlaskForm):
    Sources = None
    def __init__(self, source_tuples):
        self.Sources = Markup(select_multi_checkbox( fields=source_tuples ) )


""" Multiple slider form for DB field filtering """
""" Sliders are initialized in initSliders.js   """

def multi_field_sliders(fields, bounds, ranges, ul_class="", **kwargs):
    kwargs.setdefault("type", "text")
    html = ["<div class='sliders-container' align='center' style='border:2px solid #ccc; width:350px; height: " \
        "375px; overflow-y: scroll;'>"]
    html.append("<ul %s style='list-style-type: none;'>" % (html_params(id="fields", class_=ul_class)))
    for i in range(len(fields)):
        field = fields[i]
        
        if field in bounds:
            currentBound = bounds[field]
        else:
            currentBound = (-100, 100) #does not matter

	
        currentRange = tuple(map(int, ranges[i].split(";")))
        
        #check if user updated slider
        lowerBound = max(currentRange[0], currentBound[0])
        upperBound = min(currentRange[1], currentBound[1])
        currentRange = (lowerBound, upperBound)
        
        slider_id = "%s" % (field)
        slider_settings = "data-type='double' data-min='{0}' data-max='{1}' data-from='{2}' data-to='{3}' data-grid='true'".format(currentBound[0], currentBound[1], currentRange[0], currentRange[1])
        options = dict(kwargs, name=field, id=slider_id)
        hidden_option = "hidden" if slider_id in text_fields else ""
        html.append("<li %s><div class='pl-4 pt-5 bd-highlight field-slider' id='%s_container'>" % (hidden_option, slider_id))
        html.append("<input %s class='js-range-slider' %s/> " % (html_params(**options), slider_settings))
        html.append("<label for='%s' class='slider-label'>%s</label></div></li>" % (slider_id, slider_id))
    html.append("</ul>")
    html.append("</div>")
    return "".join(html)

class FieldSliders(FlaskForm):
    Sliders = None

    def __init__(self, fields, bounds, ranges):
        self.Sliders = Markup(multi_field_sliders (fields=fields, bounds=bounds, ranges=ranges) )
        
        
""" Generate HTML for the datatable """
        
def makeHTMLTable(fields, queryResults):
    html = ["<table id=\"data\" class=\"table table-striped table-bordered\" " \
         "style=\"background-color: white;\" cellspacing=\"0\">"]
    
    # Table head
    html.append("<thead><tr>")
    i = 0
    while i < len(fields):
        if fields[i] == "title1_date" and i+1 < len(fields) and \
             fields[i+1] == "title2_date":
            html.append("<th scope=\"col\">Dates</th>")
            i += 2
        else:
            html.append("<th scope=\"col\">%s</th>" % fields[i])
            i += 1
        
    # Table body
    html.append("<tbody>")
    for i in range(len(queryResults)):
        html.append("<tr>")
        j = 0
        while j < len(fields):
            if fields[j] == "title1_date" and j+1 < len(fields) and \
                 fields[j+1] == "title2_date":
                html.append("<td>%s<br><br>%s</td>" % (queryResults[i][j], queryResults[i][j+1]))
                j += 2  
            elif fields[j] in text_fields:
                html.append("<td>%s</td>" % queryResults[i][j])
                j += 1
            else:
                html.append("<td>%s</td>" % queryResults[i][j])
                j += 1
        html.append("</tr>")
            
    html.append("</tbody></table>")
    return Markup("".join(html))