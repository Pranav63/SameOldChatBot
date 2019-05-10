# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from datetime import datetime

import logging
import requests
import json
from rasa_core_sdk import Action

logger = logging.getLogger(__name__)

API_URL= "https://cricapi.com/api/"
API_KEY="96Wb94tmIYhlje0VbloSnf0weN52"

class ApiAction(Action):
	def name(self):
		return "action_match_news"

	def run(self, dispatcher, tracker, domain):
		res = requests.get(API_URL + "matches" + "?apikey=" + API_KEY)
		if res.status_code == 200:
			data = res.json()["matches"]
			recent_match = data[0]
			upcoming_match = data[1]
			upcoming_match["date"] = datetime.strptime(upcoming_match["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
			next_date = upcoming_match["date"].strftime("%d %B %Y")

			out_message = "Here some IPL quick info:\n1.The match between {} and {} was recently held and {} won.".format(recent_match["team-1"], recent_match["team-2"], recent_match["winner_team"])

			dispatcher.utter_message(out_message)

			out_message = "2.The next match is {} vs {} on {}".format(upcoming_match["team-1"], upcoming_match["team-2"], next_date)

			dispatcher.utter_message(out_message)

		return []