from flask import Blueprint, request, Response

api = Blueprint('api', __name__)

@api.route('/addExp', methods=['POST'])
def addExp():
    vals = request.json
    print(vals)
    return Response(status=200)
