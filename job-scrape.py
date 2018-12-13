#!/usr/bin/env python

import begin
import requests
from bs4 import BeautifulSoup
from slackclient import SlackClient

SLACK_TOKEN = ""
SLACK_CHANNEL = "#jobs"

DICE = "http://www.dice.com"

@begin.start
def run(title='Data Engineer', location='Denver, CO'):

    values = {'q': title, 'l': location}

    try:
        r = requests.get('http://www.dice.com/jobs', params=values)
    except HTTPError as e:
        print(e)

    page_content = BeautifulSoup(r.content, 'html.parser')

    sc = SlackClient(SLACK_TOKEN)

    titleList = page_content.findAll("a", href=True, title=True)
    timeList = page_content.findAll("li", attrs={"class" : "posted col-xs-12 col-sm-2 col-md-2 col-lg-2 margin-top-3 text-wrap-padding"}) 
    
    time = []
    
    for tl in timeList:
        time.append(str(tl.text))
    
    for t,p in zip(titleList, time):
        if t['href'].endswith(location):
            desc = '[' + t['title'] + ']' + ' '  +  '|' + ' ' + location + ' ' + '|' + ' ' + t['href'] + ' ' + '|' + ' ' + p
            #print desc
            sc.api_call(
               "chat.postMessage", channel=SLACK_CHANNEL, text=desc,
               username='jernster', icon_emoji=':robot_face:')
