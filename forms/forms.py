from flask import Markup
from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput, html_params
from wtforms.validators import Required
from models.models import Articles, Title_Comparison

# Non-digit fields that should be hidden in the sliders form
# We are still loading these into the form for indexing simplicity--possibly refactor?
# >>> Also should be prioritized in the table display <<<
#text_fields2 = ["title1", "title2", "source1", "source2", "normal_display", "sources_display", \
    #"title1_date", "title2_date", "lower_display"]

text_fields = ["title1", "title2", "source1", "source2", "normal_display", "sources_display", \
    "title1_date", "title2_date", "lower_display", "id1", "id2"]

toUser = {'ttr_title': 'Lexical Diversity (Title)', 'vad_neg_title': 'VADER Sentiment - Negative (Title)', 'vad_neu_title': 'VADER Sentiment - Neutral (Title)', 'vad_pos_title': 'VADER Sentiment - Positive (Title)', 'fke_title': 'Flesch-Kincaid Readability (Title)', 'smog_title': 'SMOG Grade Readability (Title)', 'stop_title': 'Stop Words (Title)', 'wordlen_title': 'Average Word Length (Title)', 'wc_title': 'Word Count (Title)', 'nb_pobj_title': 'Probability of Objectivity (Title)', 'nb_psubj_title': 'Probability of Subjectivity (Title)', 'quotes_title': 'Quote Usage (Title)', 'exclaim_title': 'Exclamation Mark Usage (Title)', 'allpun_title': 'Punctuation Usage (Title)', 'allcaps_title': 'All Capitalization Usage (Title)', 'cc_title': 'Coordinating Conjunction Usage (Title)', 'cd_title': 'Cardinal Number Usage (Title)', 'dt_title': 'Determiner Usage (Usage)', 'ex_title': "Existential 'There' Usage (Title)", 'fw_title': 'Foreign Word Usage (Title)', 'in_pos_title': 'Preposition/Subordinating Conjunction Usage (Title)', 'jj_title': 'Adjective Usage (Title)', 'jjr_title': 'Comparative Adjective Usage (Title)', 'jjs_title': 'Superlative Adjective Usage (Title)', 'ls_title': 'List Item Marker Usage (Title)', 'md_title': 'Modal Usage (Title)', 'nn_title': 'Singular/Mass Noun Usage (Title)', 'nns_title': 'Plural Noun Usage (Title)', 'nnp_title': 'Singular Proper Noun Usage (Title)', 'nnps_title': 'Plural Proper Noun Usage (Title)', 'pdt_title': 'Predeterminer Usage (Title)', 'pos_title': 'Possessive Ending Usage (Title)', 'prp_title': 'Personal Pronoun Usage (Title)', 'prp1_title': 'Possessive Pronoun Usage (Title)', 'rb_title': 'Adverb Usage (Title)', 'rbr_title': 'Comparative Adverb Usage (Title)', 'rbs_title': 'Superlative Adverb Usage (Title)', 'rp_title': 'Particle Usage (Title)', 'sym_title': 'Symbol Usage (Title)', 'to_title': "'to' Usage (Title)", 'uh_title': 'Interjection Usage (Title)', 'wp1_title': "Possessive 'Wh- Pronoun Usage (Title)", 'wrb_title': 'Wh- Adverb Usage (Title)', 'vb_title': 'Base Form Verb Usage (Title)', 'vbd_title': 'Past Tensive Verb Usage (Title)', 'vbg_title': 'Gerund/Present Participle Verb Usage (Title)', 'vbn_title': 'Past Participle Verb Usage (Title)', 'vbp_title': 'Non-Third Person Singular Present Verb Usage (Title)', 'vbz_title': 'Third Person Singular Present Verb Usage (Title)', 'wdt_title': 'Wh- Determiner Usage (Title)', 'wp_title': 'Wh- Pronoun Usage (Title)', 'ingest_title': 'Ingestion Words (Title)', 'cause_title': 'Causation Words (Title)', 'insight_title': 'Insight Words (Title)', 'cogmech_title': 'Cognitive Process Words (Title)', 'sad_title': 'Sad Words (Title)', 'inhib_title': 'Inhibition Words (Title)', 'certain_title': 'Certain Words (Title)', 'tentat_title': 'Tentative Words (Title)', 'discrep_title': 'Discrepancy Words (Title)', 'space_title': 'Space Words (Title)', 'time_title': 'Time Words (Title)', 'excl_title': 'Exclusive Words (Title)', 'incl_title': 'Inclusive Words (Title)', 'relativ_title': 'Relative Words (Title)', 'motion_title': 'Motion Words (Title)', 'quant_title': 'Quantifying Words (Title)', 'number_title': 'Number Words (Title)', 'swear_title': 'Swear Words (Title)', 'funct_title': 'Function Words (Title)', 'ppron_title': 'Personal Pronoun Usage (Title)', 'pronoun_title': 'Pronoun Usage (Title)', 'we_title': "'we' Usage (Title)", 'i_title': "'I' Usage (Title)", 'shehe_title': "'he'/'she' Usage (Title)", 'you_title': "'you' Usage (Title)", 'ipron_title': 'Impersonal Pronoun Usage (Title)', 'they_title': "'they' Usage (Title)", 'death_title': 'Death Words (Title)', 'bio_title': 'Biological Process Words (Title)', 'body_title': 'Body Words (Title)', 'hear_title': 'Auditory Words (Title)', 'feel_title': 'Somatic Words (Title)', 'percept_title': 'Perception Process Words (Title)', 'see_title': 'Visual Words (Title)', 'filler_title': 'Filler Words (Title)', 'health_title': 'Health Words (Title)', 'sexual_title': 'Sexual Words (Title)', 'social_title': 'Social Words (Title)', 'family_title': 'Family Words (Title)', 'friend_title': 'Friend Words (Title)', 'humans_title': 'Human Words (Title)', 'affect_title': 'Affective Process Words (Title)', 'posemo_title': 'Positive Emotion Words (Title)', 'negemo_title': 'Negative Emotion Words (Title)', 'anx_title': 'Anxiety Words (Title)', 'anger_title': 'Anger Words (Title)', 'assent_title': 'Assent Words (Title)', 'nonfl_title': 'Non-fluency Words (Title)', 'verb_title': 'Verb Usage (Title)', 'article_title': 'Article Usage (Title)', 'past_title': 'Past Tense Usage (Title)', 'auxverb_title': 'Auxiliary Verb Usage (Title)', 'future_title': 'Future Tense Usage (Title)', 'present_title': 'Present Tense Usage (Title)', 'preps_title': 'Preposition Usage (Title)', 'adverb_title': 'Adverb Usage (Title)', 'negate_title': 'Negation Usage (Title)', 'conj_title': 'Conjunction Usage (Title)', 'home_title': 'Home Words (Title)', 'leisure_title': 'Leisure Words (Title)', 'achieve_title': 'Achievement Words (Title)', 'work_title': 'Work Words (Title)', 'relig_title': 'Religious Words (Title)', 'money_title': 'Money Words (Title)', 'bias_count_title': 'Bias Words (Title)', 'assertives_count_title': 'Assertives (Title)', 'factives_count_title': 'Factives (Title)', 'hedges_count_title': 'Hedges (Title)', 'implicatives_count_title': 'Implicatives (Title)', 'report_verbs_count_title': 'Reporting Verbs (Title)', 'positive_op_count_title': 'Positive Opinion (Title)', 'negative_op_count_title': 'Negative Opinion (Title)', 'wneg_count_title': 'Weak Negative (Title)', 'wpos_count_title': 'Weak Positive (Title)', 'wneu_count_title': 'Weak Neutral (Title)', 'sneg_count_title': 'Strong Negative (Title)', 'spos_count_title': 'Strong Positive (Title)', 'sneu_count_title': 'Strong Neutral (Title)', 'harmvirtue_title': 'Moral Foundation: Care (Title)', 'harmvice_title': 'Moral Foundation: Harm (Title)', 'fairnessvirtue_title': 'Moral Foundation: Fairness (Title)', 'fairnessvice_title': 'Moral Foundation: Cheating (Title)', 'ingroupvice_title': 'Moral Foundation: Betrayal (Title)', 'ingroupvirtue_title': 'Moral Foundation: Loyalty (Title)', 'authorityvirtue_title': 'Moral Foundation: Authority (Title)', 'authorityvice_title': 'Moral Foundation: Subversion (Title)', 'purityvirtue_title': 'Moral Foundation: Purity (Title)', 'purityvice_title': 'Moral Foundation: Degradation (Title)', 'moralitygeneral_title': 'General Moral Foundation (Title)'}

""" Convert name to user friendly name """

def convertToUser(field):
    if field in toUser:
        return toUser[field]
    
    return field

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
        check = ""
        if checked:
            check = " active"
        html.append("<li><label class='btn btn-light btn-block{}'>".format(check))
        if checked:
            check = " checked = 'checked'"
        html.append("<input type='checkbox'%s autocomplete='off' class='invisible field-btn'" \
            "%s>%s</label></li>" % 
                    (check, html_params(**options), convertToUser(field_id)))
    html.append("</div>")
    html.append("</ul>")
    html.append("</div>")
    return "".join(html)

class FieldSelection(FlaskForm):
    Fields = None
    def __init__(self, field_tuples):
        self.Fields = Markup(select_multi_checkbox( fields=field_tuples ) )

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
        html.append("<label for='%s' class='slider-label'>%s</label></div></li>" % (slider_id, convertToUser(slider_id)))
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
            html.append("<th scope=\"col\">%s</th>" % convertToUser(fields[i]))
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