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

CONST_Skill_name = "knock out"

# Constants
CONST_Trainer_Name = "Mike"
Combinations = ["Jab. ", "Cross. ", "Hook. ", "Upper Cut. "]
CONST_URL = "https://api.amazongameon.com/v1/"

# Amazon Polly Voices
CONST_Alexa_Voice = '<voice>'
CONST_Matthew_Voice = '<voice name="Matthew">'
CONST_Kendra_Voice = '<voice name="Kendra">'
CONST_Salli_Voice = '<voice name="Salli">'

CONST_Voice_Start = '<voice>'
CONST_Voice_End = '</voice>'

#Sound effects
CONST_BELLS_2 = "<audio src=\"soundbank://soundlibrary/sports/box/box_04\"/>"
CONST_BELLS_5 = "<audio src=\"soundbank://soundlibrary/sports/box/box_08\"/>"
CONST_PUNCHES_4 = "<audio src=\"soundbank://soundlibrary/sports/box/box_02\"/>"
CONST_PUNCHES_MANY = "<audio src=\"soundbank://soundlibrary/sports/box/box_07\"/>"
CONST_POINTS = "<audio src=\"soundbank://soundlibrary/alarms/beeps_and_bloops/bell_01\"/>"
CONST_Gameshow_Outro = "<audio src=\"soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_intro_01\"/>"
CONST_Beeps = "<audio src=\"soundbank://soundlibrary/computers/beeps_tones/beeps_tones_08\"/>"
CONST_BEEPS_2 = "<audio src=\"soundbank://soundlibrary/alarms/beeps_and_bloops/bell_05\"/>"

# Alexa dialogues
# 1. Introduction
CONST_INTRO_1 = CONST_Beeps + "Welcome to " + CONST_Skill_name + ". " + "Boxing, is an unarmed combat sport, and has it's history as early as 1500 BC. "
CONST_INTRO_1 += "If you are an existing user, you can continue from your last saved progress once you start the session. "
CONST_INTRO_1 += "Boxing is not only a hobby that you can learn, but also a tiring sport, a fitness regimen, and also a highly successful form of self defence. "
#CONST_INTRO_1 += "It helps you to learn discipline, self control, and gain enormous self confidence with regular practice. "
# CONST_INTRO_1 += "If you are an existing user, you can continue from your last saved progress once you start the session for today. "
CONST_INTRO_1 += "To customize your experience, we have 2 trainers, Mike, and Laila, whom you can choose to train with. "
CONST_INTRO_1 += "Along your way, you will be awarded with points, and you can compete with others, who are training just like you. "
CONST_INTRO_1 += "Tell me to start the session when you are ready. "

# 2. Trainers
CONST_Trainers = "Begining is always the hardest and you have done that already. Yay! Let me introduce you to both the trainers. "
CONST_Trainers += CONST_Matthew_Voice + " Hi, I am Mike. " + CONST_Voice_End
CONST_Trainers += CONST_Salli_Voice + " Hi, I am Laila. " + CONST_Voice_End
CONST_Trainers += CONST_Voice_Start + " Which trainer would you like to choose. Trainer Mike, or Trainer Laila? " + CONST_Voice_End

# 2. Trainers old
CONST_TRAINERS_OLD1 = "Welcome back to your training session. Consistencey is the key. We have retrieved your progress from last saved. "
CONST_TRAINERS_OLD2 = "Let me re introduce you to your trainers. "
CONST_TRAINERS_OLD2 += CONST_Matthew_Voice + " Hi, I am Mike. " + CONST_Voice_End
CONST_TRAINERS_OLD2 += CONST_Salli_Voice + " Hi, I am Laila. " + CONST_Voice_End
CONST_TRAINERS_OLD2 += CONST_Voice_Start + " Which trainer would you like to choose for today's session. Trainer Mike, or Trainer Laila? " + CONST_Voice_End

# 3. Choose trainer
CONST_Choose_Trainer_99 = "Hello, I am your trainer "
CONST_Choose_Trainer = "There are two ways you can start training. You can start by learning the basic punches, which I highly recommend. "
CONST_Choose_Trainer += "Other is you can choose to shadow box using various combinations with varied difficulty. "
CONST_Choose_Trainer += "Would you like to start with, The basics? or, Shadow boxing? "

# 3. Choose trainer old
CONST_Choose_Trainer_OLD_99 = "Hello, I am your trainer "
CONST_Choose_Trainer_OLD = "Since you are an existing user, you might have already known the basics. "
CONST_Choose_Trainer_OLD += "You can practice the basics again, or you can choose to shadow box using various combinations with varied difficulty. "
CONST_Choose_Trainer_OLD += "Would you like to start with, The basics? or Shadow boxing? "

# 4. The Basics
CONST_Basics = CONST_BELLS_2 + "Boxing is a sport which is easy to pick up but very hard to master. That said, modern boxing has 4 types of punches. "
CONST_Basics += "Jab, Cross, Hook, Upper Cut. "
CONST_Basics += "Start by standing in upright postion with a firm posture. Both of your fists clenched, directly in front of your face with your thumb pointing towards you. "
CONST_Basics += "This will be your guard position, when you are not performing any of your punches. "
CONST_Basics += "Number one, The Jab. A quick, straight punch with your right hand, or your lead hand, directing straight to the opponent's face. This punch does not generate much power, but it is your most important punch in boxing. Used for both defence and attack, helps you to guage your distance, and also to help you to cover against your opponent's punches. "
CONST_Basics += "Number two, The Cross. Jab is quicker punch, but The Cross, is a powerful straight punch where you generate your power from your shoulders. For more additional power, you rotate your torso or hips counter clockwise and generate power for your punches. "
CONST_Basics += "Remember after each punches you need to resume to your guard position unless, your doing a combination of punches. "
CONST_Basics += "Number three, The Hook. A semi circular punch thrown with the lead hand to the side of the opponent's head. From the guard position, the elbow is drawn back with a horizontal fist, knuckles pointing forward and the elbow bent. The torso and hips are rotated clockwise, propelling the fist through a tight, clockwise arc across the front of the body and connecting with the target. "
CONST_Basics += "Number four, The Upper Cut. This is a vertical punch with your rear hand. The rear hand drops below the level of the opponent's chest and the knees are bent slightly. From this position, the rear hand is thrust upwards in a rising arc towards the opponent's chin or torso. At the same time, the knees push upwards, the torso and hips rotate counter clockwise, and the rear heel turns outward, mimicking the body movement of the cross. "
CONST_Basics += "Even though we gave you a descriptive of all the punches, we recommend we you check your stance and punches with a professional so that you do not do it wrong. "
CONST_Basics += "That being said you have completed your basic training. You have gained five points for your training. " + CONST_BEEPS_2
CONST_Basics2 = "Would you like to start with shadow boxing training?"

# 5. Shadow boxing intro
CONST_Shadow_Boxing = "Let us begin with shadow boxing combinations. You will have ten sets of combinations, and for completing the round you will gain ten points. "
CONST_Shadow_Boxing += "Hope, you are ready. Now, let us begin. " + CONST_BELLS_2

# 6. Shadow boxing end
CONST_Shadow_Boxing_End = "You have completed your shadow boxing round. You have gained ten points for your training." + CONST_BEEPS_2
CONST_Shadow_Boxing_End2 = "It is important to have adequate rest when you become tired, inorder to train better. Would you like to continue with your training, or end the session? "

# 5. Shadow boxing intro old
CONST_Shadow_Boxing_OLD = "Let us continue with our next round of shadow boxing combinations. In this round, you will have ten sets of combinations, and for completing the round you will gain ten points. "
CONST_Shadow_Boxing_OLD += "Hope, you are ready to start this round. Now, let us begin. " + CONST_BELLS_2

# 6. Shadow boxing end old
CONST_Shadow_Boxing_OLD_End = "You have completed your shadow boxing round. You have gained ten points for your training." + CONST_BEEPS_2
CONST_Shadow_Boxing_OLD_End2 = "It is important to have adequate rest when you become tired, inorder to train better. Would you like to continue with your training, or end the session? "

# 7. End session
CONS_END_SESSION = "We have saved your progress and hope to see you for your next session. Thank you for using knock out. Have a Great Day. "

# Make sure you use question marks or periods.

def on_intent(intent_request, session):
    """Called when the user specifies an intent for this skill."""
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    # Dispatch to your skill's intent handlers
    #print("***********************intent section***************************")
    #print(intent_name)
    if intent_name == "ChooseTrainerIntent":
        return handle_choosetrainerintent_request(intent, session)
    elif intent_name == "StartSessionIntent":
        return handle_startsessionintent_request(intent, session)
    elif intent_name == "BasicsIntent":
        return handle_basicsintent_request(intent, session) 
    elif intent_name == "ShadowBoxingIntent":
        return handle_shadowboxingintent_request(intent, session)
    elif intent_name == "RepeatShadowBoxingIntent":
        return handle_repeatshadowboxingintent_request(intent, session)
    elif intent_name == "EndSessionIntent":
        return handle_endsessionintent_request(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return handle_get_help_request(intent, session)
    elif intent_name == "AMAZON.StopIntent":
        return handle_finish_session_request(intent, session)
    elif intent_name == "AMAZON.CancelIntent":
        return handle_finish_session_request(intent, session)
    else:
        raise ValueError("Invalid intent")

# --------------- Functions that make Gameon API calls -------------

def registerPlayer(session):
    data ={}
    result = "Invalid playerName"
    #result = leaderboardRank(session["attributes"]["CONST_PLAYER_NAME"])
    try:
        headers = {'content-type': 'application/json', 'x-api-key': session["attributes"]["CONST_API_KEY"] }
        r = requests.post(url = CONST_URL+"players/register", data = data,headers=headers) 
        responseData = r.json()
        session["attributes"]["CONST_PLAYER_TOKEN"] =  responseData['playerToken']
        session["attributes"]["CONST_EXTERNAL_PLAYER_ID"] = responseData['externalPlayerId']
        return session["attributes"]["CONST_EXTERNAL_PLAYER_ID"]
    except Exception as err:
        session["attributes"]["LOG_ERRORS"] = session["attributes"]["LOG_ERRORS"] + "register player {0}".format(err)
        return "Exception: {0}".format(err)
    return "Player already registered"

def authenticatePlayer(session):
    data ={}
    try:
        json ={	"playerToken" : session["attributes"]["CONST_PLAYER_TOKEN"],	"playerName"  : session["attributes"]["CONST_PLAYER_NAME"], "deviceOSType": "iOS",	"appBuildType": "development"}
        headers = {'content-type': 'application/json', 'x-api-key': session["attributes"]["CONST_API_KEY"] }
        r = requests.post(url = CONST_URL+"/players/auth", data = data,json = json,headers = headers) 
        responseData = r.json()
        session["attributes"]["CONST_SESSION_ID"] =  responseData['sessionId']
        session["attributes"]["CONST_SESSION_EXPIRATION_DATE"] = responseData['sessionExpirationDate']
        return session["attributes"]["CONST_SESSION_ID"]
    except Exception as err:
        session["attributes"]["LOG_ERRORS"] = session["attributes"]["LOG_ERRORS"] + "authenticate player {0}".format(err)
        return "Exception: {0}".format(err)

def leaderboardRank(playerName, session):
    data ={}
    try:
        headers = {'content-type': 'application/json', 'x-api-key': session["attributes"]["CONST_API_KEY"] }
        r = requests.get(url = CONST_URL+"matches/"+session["attributes"]["CONST_MATCH_ID"]+"/leaderboard", data = data,headers = headers)
        responseData = r.json()
        leaderboardJson = responseData['leaderboard']
        for player in leaderboardJson:
            if playerName==player['playerName']:
                session["attributes"]["CONST_EXTERNAL_PLAYER_ID"] =  player['externalPlayerId']
                session["attributes"]["CONST_RANK"] = player['rank']
                session["attributes"]["CONST_PLAYER_NAME"] = player['playerName']
                session["attributes"]["CONST_SCORE"] = player['score']
                return str(session["attributes"]["CONST_RANK"])
        return "Invalid playerName"
    except Exception as err:
        session["attributes"]["LOG_ERRORS"] = session["attributes"]["LOG_ERRORS"] + "leaderboard rank {0}".format(err)
        return "Exception: {0}".format(err)

def isNewPlayer(playerName, session):
    data ={}
    try:
        headers = {'content-type': 'application/json', 'x-api-key': session["attributes"]["CONST_API_KEY"] }
        r = requests.get(url = CONST_URL+"matches/"+session["attributes"]["CONST_MATCH_ID"]+"/leaderboard", data = data,headers = headers)
        responseData = r.json()
        leaderboardJson = responseData['leaderboard']
        for player in leaderboardJson:
            if playerName==player['playerName']:
                session["attributes"]["CONST_EXTERNAL_PLAYER_ID"] =  player['externalPlayerId']
                session["attributes"]["CONST_RANK"] = player['rank']
                session["attributes"]["CONST_PLAYER_NAME"] = player['playerName']
                session["attributes"]["CONST_SCORE"] = player['score']
                return str(session["attributes"]["CONST_EXTERNAL_PLAYER_ID"])
        return "new"
    except Exception as err:
        session["attributes"]["LOG_ERRORS"] = session["attributes"]["LOG_ERRORS"] + "is new player {0}".format(err)
        return "new"

def increaseScore(session):
    enterMatch(session)
    data ={}
    try:
        headers = {'content-type': 'application/json', 'x-api-key': session["attributes"]["CONST_API_KEY"], 'Session-Id' : session["attributes"]["CONST_SESSION_ID"] }
        json ={	"score" : session["attributes"]["CONST_SCORE"]}
        r = requests.put(url = CONST_URL+"matches/"+session["attributes"]["CONST_MATCH_ID"]+"/score", data = data,json = json,headers = headers)
        responseData = r.json()
        session["attributes"]["CONST_SCORE"] = responseData['score']
        #session["attributes"]["CONST_MESSAGE"] = responseData['message']
        return str(session["attributes"]["CONST_SCORE"])
    except Exception as err:
        session["attributes"]["LOG_ERRORS"] = session["attributes"]["LOG_ERRORS"] + "increase score {0}".format(err)
        return "Exception: {0}".format(err)

def enterMatch(session):
    data ={}
    try:
        headers = {'content-type': 'application/json', 'x-api-key': session["attributes"]["CONST_API_KEY"], 'Session-Id' : session["attributes"]["CONST_SESSION_ID"] }
        r = requests.post(url = CONST_URL+"matches/"+session["attributes"]["CONST_MATCH_ID"]+"/enter", data = data,headers = headers) 
        responseData = r.json()
        #MATCH_ID = responseData['matchId']
        #attemptsRemaining =  responseData['attemptsRemaining']
        #session["attributes"]["CONST_TOURNAMENTID"] = responseData['tournamentId']
        return session["attributes"]["CONST_TOURNAMENTID"]
    except Exception as err:
        session["attributes"]["LOG_ERRORS"] = session["attributes"]["LOG_ERRORS"] + "enter match {0}".format(err)
        return "Exception: {0}".format(err)

def enterPlayerTournament(session):
    data ={}
    try:
        #json ={	"playerToken" : session["attributes"]["CONST_PLAYER_TOKEN"],	"playerName"  : session["attributes"]["CONST_PLAYER_NAME"], "deviceOSType": "iOS",	"appBuildType": "development"}
        headers = {'content-type': 'application/json', 'x-api-key': session["attributes"]["CONST_API_KEY"], 'Session-Id' : session["attributes"]["CONST_SESSION_ID"] }
        r = requests.post(url = CONST_URL+"player-tournaments/"+session["attributes"]["CONST_TOURNAMENTID"]+"/enter", data = data, headers = headers) 
        responseData = r.json()
        #MATCH_ID = responseData['matchId']
        #attemptsRemaining =  responseData['attemptsRemaining']
        #session["attributes"]["CONST_TOURNAMENTID"] = responseData['tournamentId']
        return session["attributes"]["CONST_TOURNAMENTID"]
    except Exception as err:
        session["attributes"]["LOG_ERRORS"] = session["attributes"]["LOG_ERRORS"] + "enter player tournament {0}".format(err)
        return "Exception: {0}".format(err)



# --------------- Functions that control the skill's behavior -------------

# --------------- Functions that control the skill's behavior -------------
def boxing_intro(session):
    """If we wanted to initialize the session to have some attributes we could add those here."""
    intro = ( CONST_INTRO_1 )
    main_user_id = str(session['user']['userId'])
    hash_obj = hashlib.sha1( bytes(main_user_id, 'utf-8'))
    #user_id = str(main_user_id[19:39] + main_user_id[65:85] + main_user_id[200:])
    #user_id = str(main_user_id[200:])
    user_id = str(hash_obj.hexdigest())
    should_end_session = False
    speech_output = intro 
    reprompt_text = intro
    attributes = {"speech_output": speech_output,
                  "reprompt_text": speech_output,
                  "CONST_API_KEY": "",
                  "CONST_MATCH_ID": "",
                  "CONST_PLAYER_TOKEN": "",
                  "CONST_EXTERNAL_PLAYER_ID": "",
                  "CONST_SESSION_EXPIRATION_DATE": "",
                  "CONST_SESSION_ID": "xx",
                  "CONST_SESSION_EXPIRATION_DATE": "",
                  "CONST_SCORE": 0,
                  "CONST_PLAYER_SCORE": 0,
                  "CONST_RANK": 0,
                  "CONST_PLAYER_NAME": user_id,
                  "CONST_MESSAGE": "",
                  "CONST_TRAINER": "Mike",
                  "CONST_IS_NEW": "true",
                  "CONST_TOURNAMENTID": "",
                  "LOG_ERRORS": ""
                  }

    return build_response(attributes, build_speechlet_response(
        CONST_Skill_name, speech_output, reprompt_text, should_end_session))

def handle_startsessionintent_request(intent, session):
    main_user_id = str(session['user']['userId'])
    user_id = session["attributes"]["CONST_PLAYER_NAME"]
    playerId = "not new"
    playerId = isNewPlayer(user_id, session)
    
    #session["attributes"]["CONST_PLAYER_NAME"] = user_id
    #session["attributes"]["CONST_IS_NEW"] = "false"
    if(playerId == "new"):
        registerPlayer(session)
        authenticatePlayer(session)
        enterPlayerTournament(session)
        #enterMatch(session)
        #session["attributes"]["CONST_SCORE"] = int(session["attributes"]["CONST_SCORE"])
        increaseScore(session)
        session["attributes"]["CONST_IS_NEW"] = "true"
    else:
        authenticatePlayer(session)
        enterPlayerTournament(session)
        enterMatch(session)
        increaseScore(session)
        session["attributes"]["CONST_IS_NEW"] = "false"

    is_new = str(session["attributes"]["CONST_IS_NEW"])
    attributes = {"CONST_API_KEY": session["attributes"]["CONST_API_KEY"],
                  "CONST_MATCH_ID": session["attributes"]["CONST_MATCH_ID"],
                  "CONST_PLAYER_TOKEN": session["attributes"]["CONST_PLAYER_TOKEN"],
                  "CONST_EXTERNAL_PLAYER_ID": session["attributes"]["CONST_EXTERNAL_PLAYER_ID"],
                  "CONST_SESSION_ID": session["attributes"]["CONST_SESSION_ID"],
                  "CONST_SESSION_EXPIRATION_DATE": session["attributes"]["CONST_SESSION_EXPIRATION_DATE"],
                  "CONST_SCORE": session["attributes"]["CONST_SCORE"],
                  "CONST_PLAYER_SCORE": session["attributes"]["CONST_PLAYER_SCORE"],
                  "CONST_RANK": session["attributes"]["CONST_RANK"],
                  "CONST_PLAYER_NAME": session["attributes"]["CONST_PLAYER_NAME"],
                  "CONST_MESSAGE": session["attributes"]["CONST_MESSAGE"],
                  "CONST_TRAINER": session["attributes"]["CONST_TRAINER"],
                  "CONST_IS_NEW": session["attributes"]["CONST_IS_NEW"],
                  "CONST_TOURNAMENTID": session["attributes"]["CONST_TOURNAMENTID"],
                  "LOG_ERRORS": session["attributes"]["LOG_ERRORS"]
                  }
    should_end_session = False
    user_gave_up = intent['name']
    reprompt_text = "Tell me to start the session when you are ready. "
    speech_output=(CONST_Trainers)
    return build_response(attributes,build_speechlet_response(CONST_Skill_name, speech_output, reprompt_text, should_end_session))


def handle_choosetrainerintent_request(intent, session):
    trainer_name = str(intent["slots"]["TrainerName"]["value"])
    session["attributes"]["CONST_TRAINER"] = trainer_name
    attributes = {"CONST_API_KEY": session["attributes"]["CONST_API_KEY"],
                  "CONST_MATCH_ID": session["attributes"]["CONST_MATCH_ID"],
                  "CONST_PLAYER_TOKEN": session["attributes"]["CONST_PLAYER_TOKEN"],
                  "CONST_EXTERNAL_PLAYER_ID": session["attributes"]["CONST_EXTERNAL_PLAYER_ID"],
                  "CONST_SESSION_ID": session["attributes"]["CONST_SESSION_ID"],
                  "CONST_SESSION_EXPIRATION_DATE": session["attributes"]["CONST_SESSION_EXPIRATION_DATE"],
                  "CONST_SCORE": session["attributes"]["CONST_SCORE"],
                  "CONST_PLAYER_SCORE": session["attributes"]["CONST_PLAYER_SCORE"],
                  "CONST_RANK": session["attributes"]["CONST_RANK"],
                  "CONST_PLAYER_NAME": session["attributes"]["CONST_PLAYER_NAME"],
                  "CONST_MESSAGE": session["attributes"]["CONST_MESSAGE"],
                  "CONST_TRAINER": session["attributes"]["CONST_TRAINER"],
                  "CONST_IS_NEW": session["attributes"]["CONST_IS_NEW"],
                  "CONST_TOURNAMENTID": session["attributes"]["CONST_TOURNAMENTID"],
                  "LOG_ERRORS": session["attributes"]["LOG_ERRORS"]
                  }
    should_end_session = False
    user_gave_up = intent['name']
    reprompt_text =  "Which trainer would you like to choose. Trainer Mike, or Trainer Laila? "
    is_new = str(session["attributes"]["CONST_IS_NEW"])
    if(is_new =="true"):
        if(trainer_name.lower() == "mike"):
            speech_output=(CONST_Matthew_Voice + CONST_Choose_Trainer_99 + trainer_name + ". " + CONST_Choose_Trainer + CONST_Voice_End)
        else:
            speech_output=(CONST_Salli_Voice + CONST_Choose_Trainer_99 + trainer_name + ". " + CONST_Choose_Trainer + CONST_Voice_End)
    return build_response(attributes,build_speechlet_response(CONST_Skill_name, speech_output, reprompt_text, should_end_session))

	
def handle_basicsintent_request(intent, session):
    attributes = {"CONST_API_KEY": session["attributes"]["CONST_API_KEY"],
                  "CONST_MATCH_ID": session["attributes"]["CONST_MATCH_ID"],
                  "CONST_PLAYER_TOKEN": session["attributes"]["CONST_PLAYER_TOKEN"],
                  "CONST_EXTERNAL_PLAYER_ID": session["attributes"]["CONST_EXTERNAL_PLAYER_ID"],
                  "CONST_SESSION_ID": session["attributes"]["CONST_SESSION_ID"],
                  "CONST_SESSION_EXPIRATION_DATE": session["attributes"]["CONST_SESSION_EXPIRATION_DATE"],
                  
                  }
    should_end_session = False
    user_gave_up = intent['name']
    reprompt_text = "you have completed your basic training. "
    session["attributes"]["CONST_SCORE"] = (int(session["attributes"]["CONST_SCORE"]) + 5)
    
    return build_response(attributes,build_speechlet_response(CONST_Skill_name, speech_output, reprompt_text, should_end_session))

	
def handle_shadowboxingintent_request(intent, session):
    should_end_session = False
    user_gave_up = intent['name']
    reprompt_text = "Yet to be implemented" 
    response_output = ""
    for i in range(0,10):
        random_number1 = random.randint(0,3)
        random_number2 = random.randint(0,3)
        random_number3 = random.randint(0,3)
        random_number4 = random.randint(0,3)
        response_output = (response_output + Combinations[random_number1] + Combinations[random_number2] + Combinations[random_number3] + Combinations[random_number4])
    session["attributes"]["CONST_SCORE"] = (int(session["attributes"]["CONST_SCORE"]) + 10)
    increaseScore(session)
    leaderboardRank(str(session["attributes"]["CONST_PLAYER_NAME"]), session)
    attributes = {"CONST_API_KEY": session["attributes"]["CONST_API_KEY"],
                  "CONST_MATCH_ID": session["attributes"]["CONST_MATCH_ID"],
                  "CONST_PLAYER_TOKEN": session["attributes"]["CONST_PLAYER_TOKEN"],
                  "CONST_EXTERNAL_PLAYER_ID": session["attributes"]["CONST_EXTERNAL_PLAYER_ID"],
                  "CONST_SESSION_ID": session["attributes"]["CONST_SESSION_ID"],
                  "CONST_SESSION_EXPIRATION_DATE": session["attributes"]["CONST_SESSION_EXPIRATION_DATE"],
                  "CONST_SCORE": session["attributes"]["CONST_SCORE"],
                  "CONST_PLAYER_SCORE": session["attributes"]["CONST_PLAYER_SCORE"],
                  "CONST_RANK": session["attributes"]["CONST_RANK"],
                  "CONST_PLAYER_NAME": session["attributes"]["CONST_PLAYER_NAME"],
                  "CONST_MESSAGE": session["attributes"]["CONST_MESSAGE"],
                  "CONST_TRAINER": session["attributes"]["CONST_TRAINER"],
                  "CONST_IS_NEW": session["attributes"]["CONST_IS_NEW"],
                  "CONST_TOURNAMENTID": session["attributes"]["CONST_TOURNAMENTID"],
                  "LOG_ERRORS": session["attributes"]["LOG_ERRORS"]
                  }
    score_update = "Your total points are " + str(session["attributes"]["CONST_SCORE"]) + ", and you are ranked currently at number " + str(session["attributes"]["CONST_RANK"]) + ". "
    trainer_name = str(session["attributes"]["CONST_TRAINER"])
    if(trainer_name.lower() == "mike"):
        speech_output = (CONST_Matthew_Voice + CONST_Shadow_Boxing + response_output + CONST_Shadow_Boxing_End + score_update + CONST_Shadow_Boxing_End2 + CONST_Voice_End)
    else:
        speech_output = (CONST_Salli_Voice + CONST_Shadow_Boxing + response_output + CONST_Shadow_Boxing_End + score_update + CONST_Shadow_Boxing_End2 + CONST_Voice_End)
    return build_response(attributes,build_speechlet_response(CONST_Skill_name, speech_output, reprompt_text, should_end_session))


def handle_repeatshadowboxingintent_request(intent, session):
    should_end_session = False
    user_gave_up = intent['name']
    reprompt_text = "Yet to be implemented" 
    response_output = ""
    for i in range(0,10):
        random_number1 = random.randint(0,3)
        random_number2 = random.randint(0,3)
        random_number3 = random.randint(0,3)
        random_number4 = random.randint(0,3)
        response_output = (response_output + Combinations[random_number1] + Combinations[random_number2] + Combinations[random_number3] + Combinations[random_number4])
    session["attributes"]["CONST_SCORE"] = (int(session["attributes"]["CONST_SCORE"]) + 10)
    increaseScore(session)
    leaderboardRank(str(session["attributes"]["CONST_PLAYER_NAME"]), session)
    attributes = {"CONST_API_KEY": session["attributes"]["CONST_API_KEY"],
                  "CONST_MATCH_ID": session["attributes"]["CONST_MATCH_ID"],
                  "CONST_PLAYER_TOKEN": session["attributes"]["CONST_PLAYER_TOKEN"],
                  "CONST_EXTERNAL_PLAYER_ID": session["attributes"]["CONST_EXTERNAL_PLAYER_ID"],
                  "CONST_SESSION_ID": session["attributes"]["CONST_SESSION_ID"],
                  "CONST_SESSION_EXPIRATION_DATE": session["attributes"]["CONST_SESSION_EXPIRATION_DATE"],
                  "CONST_SCORE": session["attributes"]["CONST_SCORE"],
                  "CONST_PLAYER_SCORE": session["attributes"]["CONST_PLAYER_SCORE"],
                  "CONST_RANK": session["attributes"]["CONST_RANK"],
                  "CONST_PLAYER_NAME": session["attributes"]["CONST_PLAYER_NAME"],
                  "CONST_MESSAGE": session["attributes"]["CONST_MESSAGE"],
                  "CONST_TRAINER": session["attributes"]["CONST_TRAINER"],
                  "CONST_IS_NEW": session["attributes"]["CONST_IS_NEW"],
                  "CONST_TOURNAMENTID": session["attributes"]["CONST_TOURNAMENTID"],
                  "LOG_ERRORS": session["attributes"]["LOG_ERRORS"]
                  }
    score_update = "Your total points are " + str(session["attributes"]["CONST_SCORE"]) + ", and you are ranked currently at number " + str(session["attributes"]["CONST_RANK"]) + ". "
    trainer_name = str(session["attributes"]["CONST_TRAINER"])
    if(trainer_name.lower() == "mike"):
        speech_output = (CONST_Matthew_Voice + CONST_Shadow_Boxing_OLD + response_output + CONST_Shadow_Boxing_OLD_End + score_update + CONST_Shadow_Boxing_OLD_End2 + CONST_Voice_End)
    else:
        speech_output = (CONST_Salli_Voice + CONST_Shadow_Boxing_OLD + response_output + CONST_Shadow_Boxing_OLD_End + score_update + CONST_Shadow_Boxing_OLD_End2 + CONST_Voice_End)
    return build_response(attributes,build_speechlet_response(CONST_Skill_name, speech_output, reprompt_text, should_end_session))


def handle_get_help_request(intent, session):
    attributes = {"CONST_API_KEY": session["attributes"]["CONST_API_KEY"],
                  "CONST_MATCH_ID": session["attributes"]["CONST_MATCH_ID"],
                  "CONST_PLAYER_TOKEN": session["attributes"]["CONST_PLAYER_TOKEN"],
                  "CONST_EXTERNAL_PLAYER_ID": session["attributes"]["CONST_EXTERNAL_PLAYER_ID"],
                  "CONST_SESSION_ID": session["attributes"]["CONST_SESSION_ID"],
                  "CONST_SESSION_EXPIRATION_DATE": session["attributes"]["CONST_SESSION_EXPIRATION_DATE"],
                  "CONST_SCORE": session["attributes"]["CONST_SCORE"],
                  "CONST_PLAYER_SCORE": session["attributes"]["CONST_PLAYER_SCORE"],
                  "CONST_RANK": session["attributes"]["CONST_RANK"],
                  "CONST_PLAYER_NAME": session["attributes"]["CONST_PLAYER_NAME"],
                  "CONST_MESSAGE": session["attributes"]["CONST_MESSAGE"],
                  "CONST_TRAINER": session["attributes"]["CONST_TRAINER"],
                  "CONST_IS_NEW": session["attributes"]["CONST_IS_NEW"],
                  "CONST_TOURNAMENTID": session["attributes"]["CONST_TOURNAMENTID"],
                  "LOG_ERRORS": session["attributes"]["LOG_ERRORS"]
                  }
    speech_output = "Just ask {} for your titles!".format(CONST_Skill_name)
    reprompt_text = "what can I help you with?"
    should_end_session = False
    return build_response(
        attributes,
        build_speechlet_response(CONST_Skill_name, speech_output, reprompt_text, should_end_session)
    )

def handle_endsessionintent_request(intent, session):
    attributes = {"LOG_ERRORS": session["attributes"]["LOG_ERRORS"] }
    should_end_session = True
    user_gave_up = intent['name']
    reprompt_text = CONS_END_SESSION
    speech_output = (CONS_END_SESSION)
    return build_response(
        attributes,
        build_speechlet_response(CONST_Skill_name, speech_output, reprompt_text, should_end_session)
    )

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


