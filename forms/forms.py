from flask import Markup
from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput, html_params
from wtforms.validators import Required
from models.models import Title_Comparison

# Non-digit fields that should be hidden in the sliders form
# We are still loading these into the form for indexing simplicity--possibly refactor?
# >>> Also should be prioritized in the table display <<<
text_fields = ["title1", "title2", "source1", "source2", "id1", "id2", "normal_display", "sources_display", \
    "title1_date", "title2_date", "lower_display"]

toUser = {'normal_display': 'Titles', 'sources_display': 'Sources (Primary, Secondary)', 'ttr_title': 'Lexical Diversity', 'vad_neg_title': 'VADER Sentiment - Negative', 'vad_neu_title': 'VADER Sentiment - Neutral', 'vad_pos_title': 'VADER Sentiment - Positive', 'fke_title': 'Flesch-Kincaid Readability', 'smog_title': 'SMOG Grade Readability', 'stop_title': 'Stop Words', 'wordlen_title': 'Average Word Length', 'wc_title': 'Word Count', 'nb_pobj_title': 'Probability of Objectivity', 'nb_psubj_title': 'Probability of Subjectivity', 'quotes_title': 'Quote Usage', 'exclaim_title': 'Exclamation Mark Usage', 'allpun_title': 'Punctuation Usage', 'allcaps_title': 'All Capitalization Usage', 'cc_title': 'Coordinating Conjunction Usage', 'cd_title': 'Cardinal Number Usage', 'dt_title': 'Determiner Usage (Usage)', 'ex_title': "Existential 'There' Usage", 'fw_title': 'Foreign Word Usage', 'in_pos_title': 'Preposition/Subordinating Conjunction Usage', 'jj_title': 'Adjective Usage', 'jjr_title': 'Comparative Adjective Usage', 'jjs_title': 'Superlative Adjective Usage', 'ls_title': 'List Item Marker Usage', 'md_title': 'Modal Usage', 'nn_title': 'Singular/Mass Noun Usage', 'nns_title': 'Plural Noun Usage', 'nnp_title': 'Singular Proper Noun Usage', 'nnps_title': 'Plural Proper Noun Usage', 'pdt_title': 'Predeterminer Usage', 'pos_title': 'Possessive Ending Usage', 'prp_title': 'Personal Pronoun Usage', 'prp1_title': 'Possessive Pronoun Usage', 'rb_title': 'Adverb Usage', 'rbr_title': 'Comparative Adverb Usage', 'rbs_title': 'Superlative Adverb Usage', 'rp_title': 'Particle Usage', 'sym_title': 'Symbol Usage', 'to_title': "'to' Usage", 'uh_title': 'Interjection Usage', 'wp1_title': "Possessive 'Wh- Pronoun Usage", 'wrb_title': 'Wh- Adverb Usage', 'vb_title': 'Base Form Verb Usage', 'vbd_title': 'Past Tensive Verb Usage', 'vbg_title': 'Gerund/Present Participle Verb Usage', 'vbn_title': 'Past Participle Verb Usage', 'vbp_title': 'Non-Third Person Singular Present Verb Usage', 'vbz_title': 'Third Person Singular Present Verb Usage', 'wdt_title': 'Wh- Determiner Usage', 'wp_title': 'Wh- Pronoun Usage', 'ingest_title': 'Ingestion Words', 'cause_title': 'Causation Words', 'insight_title': 'Insight Words', 'cogmech_title': 'Cognitive Process Words', 'sad_title': 'Sad Words', 'inhib_title': 'Inhibition Words', 'certain_title': 'Certain Words', 'tentat_title': 'Tentative Words', 'discrep_title': 'Discrepancy Words', 'space_title': 'Space Words', 'time_title': 'Time Words', 'excl_title': 'Exclusive Words', 'incl_title': 'Inclusive Words', 'relativ_title': 'Relative Words', 'motion_title': 'Motion Words', 'quant_title': 'Quantifying Words', 'number_title': 'Number Words', 'swear_title': 'Swear Words', 'funct_title': 'Function Words', 'ppron_title': 'Personal Pronoun Usage', 'pronoun_title': 'Pronoun Usage', 'we_title': "'we' Usage", 'i_title': "'I' Usage", 'shehe_title': "'he'/'she' Usage", 'you_title': "'you' Usage", 'ipron_title': 'Impersonal Pronoun Usage', 'they_title': "'they' Usage", 'death_title': 'Death Words', 'bio_title': 'Biological Process Words', 'body_title': 'Body Words', 'hear_title': 'Auditory Words', 'feel_title': 'Somatic Words', 'percept_title': 'Perception Process Words', 'see_title': 'Visual Words', 'filler_title': 'Filler Words', 'health_title': 'Health Words', 'sexual_title': 'Sexual Words', 'social_title': 'Social Words', 'family_title': 'Family Words', 'friend_title': 'Friend Words', 'humans_title': 'Human Words', 'affect_title': 'Affective Process Words', 'posemo_title': 'Positive Emotion Words', 'negemo_title': 'Negative Emotion Words', 'anx_title': 'Anxiety Words', 'anger_title': 'Anger Words', 'assent_title': 'Assent Words', 'nonfl_title': 'Non-fluency Words', 'verb_title': 'Verb Usage', 'article_title': 'Article Usage', 'past_title': 'Past Tense Usage', 'auxverb_title': 'Auxiliary Verb Usage', 'future_title': 'Future Tense Usage', 'present_title': 'Present Tense Usage', 'preps_title': 'Preposition Usage', 'adverb_title': 'Adverb Usage', 'negate_title': 'Negation Usage', 'conj_title': 'Conjunction Usage', 'home_title': 'Home Words', 'leisure_title': 'Leisure Words', 'achieve_title': 'Achievement Words', 'work_title': 'Work Words', 'relig_title': 'Religious Words', 'money_title': 'Money Words', 'bias_count_title': 'Bias Words', 'assertives_count_title': 'Assertives', 'factives_count_title': 'Factives', 'hedges_count_title': 'Hedges', 'implicatives_count_title': 'Implicatives', 'report_verbs_count_title': 'Reporting Verbs', 'positive_op_count_title': 'Positive Opinion', 'negative_op_count_title': 'Negative Opinion', 'wneg_count_title': 'Weak Negative', 'wpos_count_title': 'Weak Positive', 'wneu_count_title': 'Weak Neutral', 'sneg_count_title': 'Strong Negative', 'spos_count_title': 'Strong Positive', 'sneu_count_title': 'Strong Neutral', 'harmvirtue_title': 'Moral Foundation: Care', 'harmvice_title': 'Moral Foundation: Harm', 'fairnessvirtue_title': 'Moral Foundation: Fairness', 'fairnessvice_title': 'Moral Foundation: Cheating', 'ingroupvice_title': 'Moral Foundation: Betrayal', 'ingroupvirtue_title': 'Moral Foundation: Loyalty', 'authorityvirtue_title': 'Moral Foundation: Authority', 'authorityvice_title': 'Moral Foundation: Subversion', 'purityvirtue_title': 'Moral Foundation: Purity', 'purityvice_title': 'Moral Foundation: Degradation', 'moralitygeneral_title': 'General Moral Foundation'}

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
    html = ["<div class='sliders-container' align='center' style='border:2px solid #ccc; width:300px; height: " \
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
        html.append("<li %s><div class='bd-highlight field-slider' id='%s_container'>" % (hidden_option, slider_id))
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