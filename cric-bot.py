import requests
from datetime import datetime

class ScoreGet:
    def __init__(self):
        self.url_get_all_matches = "https://cricapi.com/api/matches/"
        self.get_score = "https://cricapi.com/api/cricketScore"
        self.apikey = "hmJFYygonzc44nLQqP87a55SqK42"
        self.unique_id = ""

    def get_unique_id(self):
        uri_params = {
            "apikey" : self.apikey
            }
        resp = requests.get(self.url_get_all_matches, params=uri_params)
        resp_dict = resp.json()
        uid_found = 0
        for i in resp_dict['matches']:
            if i['team-1'] == "India" or i['team-2'] == "India" and i['matchStarted'] == 'true':
                todays_date = datetime.today().strftime('%Y-%m-%d')
                if todays_date == i['date'].split('T')[0]:
                    self.unique_id = i['unique_id']
                    uid_found = 1
                    break
        if not uid_found:
            self.unique_id = -1

        send_data = self.get_score_current(self.unique_id)
        return send_data

    def get_score_current(self, unique_id):
        data = ""
        if unique_id == -1:
            data = "*No India Matches today* 😢" 
        else:
            uri_params = {
                'apikey' : self.apikey,
                'unique_id' : unique_id
            }
            resp = requests.get(self.get_score, params=uri_params)
            data_json = resp.json()

            try:
                data = "*Here's the score :* \n" + data_json['stat'] + "\n" + data_json['score']
            except KeyError as e:
                print(e)
            
        return data



if __name__ == "__main__":
    obj_score = ScoreGet()
    whatsapp_msg = obj_score.get_unique_id()
    from twilio.rest import Client

    # Enter your twilio credentials here

    a_sid = "Your Twilio Account SID"
    auth_token = "Your Twilio Auth Token"

    Client = Client(a_sid, auth_token)

    whatsapp_no = "<Enter your Whatsapp number here>"  # Eg: whatsapp_no = "+919747406685"
    

    messege = Client.messages.create(body=whatsapp_msg, from_='whatsapp:+14155238886', to="whatsapp:" + whatsapp_no)