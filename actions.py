# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime

import logging
import requests
import json
import duckling

API_URL = "https://cricapi.com/api/"
API_KEY = "D62orraNNkMKUesB4rdyZ582ExK2"

# Duckling
d = duckling.Duckling()
d.load()


class ActionCurrentMatches(Action):

    def name(self):
        return "action_current_matches"

    def run(self, dispatcher, tracker, domain):
        res = requests.get(API_URL + "matches" + "?apikey=" + API_KEY)
        try:
            if res.status_code == 200:
                data = res.json()["matches"]
                today_matches = [each_match for each_match in data if datetime.strptime(each_match["date"],
                                                                                        "%Y-%m-%dT%H:%M:%S.%fZ").date() == datetime.today().date()]
                recent_match = today_matches[0]
                upcoming_match = today_matches[1]

                out_message = "A {} match is happening between {} and {}.".format(
                    recent_match["type"], recent_match["team-1"], recent_match["team-2"])

                dispatcher.utter_message(out_message)

                out_message = "Another {} match is between {} vs {}.".format(upcoming_match["type"],
                                                                            upcoming_match["team-1"],
                                                                            upcoming_match["team-2"])

                dispatcher.utter_message(out_message)
        except:
            dispatcher.utter_message("Sorry! I'm not able to get upcoming matches.")
        return []


class ActionMatchForecast(Action):

    def name(self):
        return "action_match_forecast"

    def run(self, dispatcher, tracker, domain):
        res = requests.get(API_URL + "matches" + "?apikey=" + API_KEY)
        if res.status_code == 200:
            data = res.json()["matches"]
            time = tracker.get_slot('time')
            message = tracker.latest_message.get('text')
            parse_message = d.parse(message)
            get_time = parse_message[0]['value']['value'].split('T')[0]
            get_time_obj = datetime.strptime(get_time, "%Y-%m-%d").date()
            today_matches = [each_match for each_match in data if datetime.strptime(each_match["date"],
                                                                                    "%Y-%m-%dT%H:%M:%S.%fZ").date() == get_time_obj]
            recent_match_date = get_time
            try:
                recent_match = today_matches[0]
                try:
                    upcoming_match = today_matches[1]
                except:
                    upcoming_match = ''

                out_message = "On {} there is a {} match is happening between {} and {}.".format(recent_match_date,
                    recent_match["type"], recent_match["team-1"], recent_match["team-2"])

                dispatcher.utter_message(out_message)

                if upcoming_match != '':
                    out_message = "And there is an another {} match between {} vs {}.".format(upcoming_match["type"],
                                                                                upcoming_match["team-1"],
                                                                                upcoming_match["team-2"])

                    dispatcher.utter_message(out_message)
            except:
                dispatcher.utter_message('There is no matches on {}'.format(recent_match_date))
        return []

