import json
import requests
# This class implements a wrapper on the User Modeling service
class WatsonRelationshipExtractionService:
    API_RELATIONSHIP = "https://gateway.watsonplatform.net/laser/service/api/v1/sire/3f5141fc-1de8-418b-bc6c-0682937c7e93"
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def _formatPOSTData(self, text):
        return {
            'txt': text,
            'sid': 'ie-en-news',
            'rt': 'json'
        }

    def extractRelationship(self, text):
        if self.API_RELATIONSHIP is None:
            raise Exception("No User Modeling service is bound to this app")
        payload = self._formatPOSTData(text)
        r = requests.post(self.API_RELATIONSHIP,
                          auth=(self.user, self.password),
                          headers={'content-type': 'application/json'},
                          params=payload
        )
        print("Profile Request sent. Status code: %d, content-type: %s" % (r.status_code, r.headers['content-type']))
        if r.status_code != 200:
            try:
                error = json.loads(r.text)
            except:
                raise Exception("API error, http status code %d" % r.status_code)
            raise Exception("API error %s: %s" % (error['error_code'], error['user_message']))
        return json.loads(r.text)





class WatsonUserModelingService:
    API_PROFILE = "api/v2/profile"
    API_VISUALIZATION = "api/v2/visualize"

    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password

    def _formatPOSTData(self, text):
        return {
            'contentItems': [{
                                 'userid': 'dummy',
                                 'id': 'dummyUuid',
                                 'sourceid': 'twitter',
                                 'contenttype': 'text/plain',
                                 'language': 'en',
                                 'content': text
                             }]
        }

    # Calls the User Modeling API to analyze a piece of text and obtain
    # Personality, Values and Needs traits.
    def requestPortrait(self, text):
        if self.url is None:
            raise Exception("No User Modeling service is bound to this app")
        data = self._formatPOSTData(text)
        r = requests.post(self.url + self.API_PROFILE,
                          auth=(self.user, self.password),
                          headers={'content-type': 'application/json'},
                          data=json.dumps(data)
        )
        print("Profile Request sent. Status code: %d, content-type: %s" % (r.status_code, r.headers['content-type']))
        if r.status_code != 200:
            try:
                error = json.loads(r.text)
            except:
                raise Exception("API error, http status code %d" % r.status_code)
            raise Exception("API error %s: %s" % (error['error_code'], error['user_message']))
        return json.loads(r.text)

    # Builds a visualization of a portrait object, calling the visualize
    # API in User Modeling
    def requestVisualization(self, data):
        if self.url is None:
            raise Exception("No User Modeling service is bound to this app")
        r = requests.post(self.url + self.API_VISUALIZATION,
                          auth=(self.user, self.password),
                          headers={'content-type': 'application/json'},
                          data=json.dumps(data)
        )
        print("Viz Request sent. Status code: %d, content-type: %s" % (r.status_code, r.headers['content-type']))
        if r.status_code == 200:
            return r.text
        else:
            return "Error building visualization"