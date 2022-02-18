# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import pandas as pd
import re, random
from bs4 import BeautifulSoup as bs
import requests

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

res_table = pd.read_csv("./actions/RESPONSE_EXP_LIGA.csv", encoding='utf-8')

class ActionRephraseResponse(Action):

    def name(self) -> Text:
        return "action_rephrase_legal"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.latest_message['entities'])

        self.intent = tracker.get_intent_of_latest_message()

        self.utter_row = res_table[res_table['intent'] == self.intent]

        first_response = self.utter_row['response'].values[0].split(' / ')
        first_response = random.sample(first_response, 1)[0]
        dispatcher.utter_message(text=first_response)

        utter_link_text = self.utter_row["utter_link"].values[0].split(' / ')
        utter_link_text = random.sample(utter_link_text, 1)[0]
        dispatcher.utter_message(text=utter_link_text)

        url = self.utter_row["utter_send_link"].values[0].split(' / ')
        url = random.sample(url, 1)[0]
        req = requests.get(url)
        soup = bs(req.text, 'html.parser')
        title = soup.find_all('div', {'class': 'board_input02'})[1].find('dd').text
        title = '제목: %s' % title
        url = '주소: %s' % url
        
        dispatcher.utter_message(text=title)
        dispatcher.utter_message(text=url)

        utter_ask_more_text = self.utter_row["utter_ask_more"].values[0].split(' / ')
        utter_ask_more_text = random.sample(utter_ask_more_text, 1)[0]
        dispatcher.utter_message(text=utter_ask_more_text)

        return []
