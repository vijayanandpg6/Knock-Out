"""boxing Skill.

This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.

"""
import requests
import boto3
import json
import time
import random
import hashlib

# ------- Skill specific business logic -------

def on_intent(intent_request, session):
    """Called when the user specifies an intent for this skill."""
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name'

# --------------- Functions that make Gameon API calls -------------

def registerPlayer(session):
     headers = {'content-type': 'application/json', 'x-api-key': session["attributes"]["CONST_API_KEY"] }
    r = requests.post(url = CONST_URL+"players/register", data = data,headers=headers) 
    responseData = r.json()
    return "Player already registered"

def authenticatePlayer(session):
    data ={}
    json ={	"playerToken" : session["attributes"]["CONST_PLAYER_TOKEN"],	"playerName"  : session["attributes"]["CONST_PLAYER_NAME"], "deviceOSType": "iOS",	"appBuildType": "development"}
    headers = {'content-type': 'application/json', 'x-api-key': session["attributes"]["CONST_API_KEY"] }
    r = requests.post(url = CONST_URL+"/players/auth", data = data,json = json,headers = headers) 
    responseData = r.json()
    return session["attributes"]["CONST_SESSION_ID"]

def leaderboardRank(playerName, session):
    data ={}
    try:
        headers = {'content-type': 'application/json', 'x-api-key': session["attributes"]["CONST_API_KEY"] }
        r = requests.get(url = CONST_URL+"matches/"+session["attributes"]["CONST_MATCH_ID"]+"/leaderboard", data = data,headers = headers)
        return "Invalid playerName"

def isNewPlayer(playerName, session):
    data ={}
    try:
        headers = {'content-type': 'application/json', 'x-api-key': session["attributes"]["CONST_API_KEY"] }
        r = requests.get(url = CONST_URL+"matches/"+session["attributes"]["CONST_MATCH_ID"]+"/leaderboard", data = data,headers = headers)
        responseData = r.json()
        leaderboardJson = responseData['leaderboard']
        return "new"

def handle_finish_session_request(intent, session):
    """End the session with a message if the user wants to quit the app."""
    attributes = {"LOG_ERRORS": session["attributes"]["LOG_ERRORS"] }
    reprompt_text = CONS_END_SESSION
    should_end_session = True
    speech_output = (CONS_END_SESSION)
    return build_response(
        attributes,
        build_speechlet_response_without_card(speech_output, reprompt_text, should_end_session)
    )

#---------------- Lambda functions ----------------------------------------

def lambda_handler(event, context):
    """
    Route the incoming request based on type (LaunchRequest, IntentRequest, etc).
    The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])
    print("event:" + json.dumps(event))

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """Called when the session starts."""
    print("on_session_started requestId=" +
          session_started_request['requestId'] + ", sessionId=" +
          session['sessionId'])


def on_launch(launch_request, session):
    """Called when the user launches the skill without specifying what they want."""
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return boxing_intro(session)

def on_session_ended(session_ended_request, session):
    """
    Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here
# --------------- Helpers that build all of the responses -----------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': '<speak>' + output + '</speak>'
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': 'Knock Out'
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': '<speak>' + reprompt_text + '</speak>'
            }
        },
        'shouldEndSession': should_end_session
    }


def build_speechlet_response_without_card(output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'text': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'SSML',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': attributes,
        'response': speechlet_response
    }


