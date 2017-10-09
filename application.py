from flask import Flask, request, render_template, jsonify
from datetime import datetime
from collect.elastic_search import search_keyword, search_area

application = Flask(__name__)


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/search', methods=['GET'])
def search():
    try:
        keyword = request.args['keyword']
        the_date_time = request.args['datetime']
        size = request.args['size']
        formatted_datetime = datetime.strptime(the_date_time, '%Y-%m-%dT%H:%M').strftime('%a %b %d %H:%M:%S +0000 %Y')
        size = max(min(int(size), 100),1)

        return jsonify({'status': True, 'msg': search_keyword(size=size, keyword=keyword, datetime=formatted_datetime)})
    except Exception as e:
        return jsonify({'status': False, 'msg': str(e)})


@application.route('/geospatial', methods=['GET'])
def geospatial():
    try:
        lng = float(request.args['select_lng'])
        lat = float(request.args['select_lat'])
        size = max(min(int(request.args['size']), 100),1)
        return jsonify({'status': True, 'msg': search_area(size=size, lng=lng, lat=lat)})
    except Exception as e:
        return jsonify({'status': False, 'msg': str(e)})


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=7890)
