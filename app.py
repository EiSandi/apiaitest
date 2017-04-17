# #!/usr/bin/env python

# from __future__ import print_function
# from future.standard_library import install_aliases
# install_aliases()

# from urllib.parse import urlparse, urlencode
# from urllib.request import urlopen, Request
# from urllib.error import HTTPError

# import json
# import os

# from flask import Flask
# from flask import request
# from flask import make_response

# # Flask app should start in global layout
# app = Flask(__name__)


# @app.route('/webhook', methods=['POST'])
# def webhook():
#     req = request.get_json(silent=True, force=True)

#     print("Request:")
#     print(json.dumps(req, indent=4))

#     res = processRequest(req)

#     res = json.dumps(res, indent=4)

#     print("final result---")
#     print(json.dumps(res, indent=4))

#     r = make_response(res)
#     r.headers['Content-Type'] = 'application/json'
#     return r


# def processRequest(req):
#     if req.get("result").get("action") != "yahooWeatherForecast":
#         return {}
#     baseurl = "https://query.yahooapis.com/v1/public/yql?"
#     yql_query = makeYqlQuery(req)
#     print('yql_query',yql_query)
#     if yql_query is None:
#         return {}
#     yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
#     print("urlencode---")
#     print(urlencode({'q': yql_query}))
#     result = urlopen(yql_url).read()
#     data = json.loads(result)
#     print("json.loads data")
#     print(data)
#     res = makeWebhookResult(data)
#     return res


# def makeYqlQuery(req):

#     result = req.get("result")
#     parameters = result.get("parameters")
#     city = parameters.get("geo-city")
#     if city is None:
#         return None

#     return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


# def makeWebhookResult(data):
#     query = data.get('query')
#     if query is None:
#         return {}

#     result = query.get('results')
#     if result is None:
#         return {}

#     channel = result.get('channel')
#     if channel is None:
#         return {}

#     item = channel.get('item')
#     location = channel.get('location')
#     units = channel.get('units')
#     if (location is None) or (item is None) or (units is None):
#         return {}

#     condition = item.get('condition')
#     if condition is None:
#         return {}

#     # print(json.dumps(item, indent=4s
#     speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
#              ", the temperature is " + condition.get('temp') + " " + units.get('temperature')

#     print("Response:")
#     print(speech)

#     return {
#         "speech": speech,
#         "displayText": speech,
#         # "data": data,
#         # "contextOut": [],
#         "source": "apiai-weather-webhook-sample"
#     }


# if __name__ == '__main__':
#     port = int(os.getenv('PORT', 5000))

#     print("Starting app on port %d" % port)

#     app.run(debug=False, port=port, host='0.0.0.0')



#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") == "movietest":
        baseurl = "https://api.themoviedb.org/3/discover/movie?primary_release_year=2016&sort_by=vote_average.desc&api_key=9b13737dd0119d542aabe1bf7bda84fc&format=json"
        yql_url = baseurl + "&format=json"
    else:
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = makeYqlQuery(req)
        print('yql_query',yql_query)
        if yql_query is None:
            return {}
        yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"

    result = urlopen(yql_url).read()
    data = json.loads(result)
    print('json.loads(result)')
    print(data)

    res = makeWebhookResult(data,req)
    return res


 def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"



def makeWebhookResult(data,req): 
    if req.get("result").get("action") == "movietest":
        speech= "Movies:"
        for movies in data['results']:
            speech  = speech + "," + str(movies.get('title'))
            print("Response:")
            print(speech)
    else:
        query = data.get('query')
        if query is None:
            return {}

        result = query.get('results')
        if result is None:
            return {}

        channel = result.get('channel')
        if channel is None:
            return {}

        item = channel.get('item')
        location = channel.get('location')
        units = channel.get('units')
        if (location is None) or (item is None) or (units is None):
            return {}

        condition = item.get('condition')
        if condition is None:
            return {}

        
        speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
                 ", the temperature is " + condition.get('temp') + " " + units.get('temperature')

        print("Response:")
        print(speech)


    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')