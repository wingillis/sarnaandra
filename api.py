from flask import Blueprint, request, Response, jsonify
from models import Experiment
from app import opendb
from datetime import datetime

api = Blueprint('api', __name__)

@api.route('/addExp', methods=['POST'])
def addExp():
    '''POST experiment to be added to database'''
    vals = request.json
    print(vals)
    with opendb():
        exp = Experiment.create(name=vals['name'], tags=vals['tags'],
            description=vals['description'],
            date_begin=datetime.now())
        exp.save()
        vals['id'] = exp.id
    return jsonify(vals)


@api.route('/exp', methods=['GET'])
def experiments():
    if request.args.get('all'):
        with opendb():
            vals = [exp for exp in Experiment.select()]
        vals = [dict(name=v.name, description=v.description, tags=v.tags, id=v.id) for v in vals]
        return jsonify(dict(res=vals))
    else:
        return Response(status=404)
