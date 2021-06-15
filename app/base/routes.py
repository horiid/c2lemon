from app.base import blueprint
from flask import redirect, url_for, render_template, request
from jinja2 import TemplateNotFound
import os, json

@blueprint.route('/')
def index():
    return render_template('index.html')

@blueprint.route('/<template>')
def route_template(template):
    try:
        if template == 'index':
            return redirect(url_for('base_blueprint.index'))
        if not template.endswith('.html'):
            template+='.html'
        segment=get_current_segment(request)
        # 200 OK
        return render_template(template, segment=segment)
    except TemplateNotFound:
        # 404 not found
        return render_template('404.html'), 404
    except:
        # 500 Internal Server Error
        return render_template('500.html'), 500

@blueprint.route('/config', methods=['GET'])
def config():
    if not os.path.isfile('./dataset_conf.json'):
        dialog="Path to the dataset is not configured, create a file \"dataset_conf.json\" at " \
            + os.path.abspath('./') \
            + ", the key name for the path must be set as 'dataset_path'."
        return render_template('config.html', dialog=dialog)
    
    dialog="Path to the dataset is configured:"
    conf_f = open(os.path.abspath('./dataset_conf.json'), 'r')
    dataset_path = json.load(conf_f)
    try:
        dialog += " " + dataset_path['dataset_path']
    except KeyError:
        dialog = """The Config File exists, but the structure is not what to be expected. 
        Confirm the key name for dataset path is set as 'dataset_path'."""
    return render_template('config.html', dialog=dialog)

# get current URL segment and return it (index if none)
def get_current_segment(request):
    try:
        segment=request.path.split('/')[-1]
        if segment == '':
            segment='index'
        return segment
    except:
        return None
