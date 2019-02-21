from __future__ import print_function

import random
# ------------------------------------------------------------------------------
# ---------------------------- Main Handler ------------------------------------
# ------------------------------------------------------------------------------

def lambda_handler(event, context):
    """ 
    This is the Main Handler function that will call other functions.
    We get two inputs : event , context
    """
    
    if event['request']['type'] == "LaunchRequest":
        return onLaunch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return onIntent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return onSessionEnd(event['request'], event['session'])
        
# ------------------------------------------------------------------------------
# ----------------------------- Event Handlers ---------------------------------
# ------------------------------------------------------------------------------

def onLaunch(launchRequest, session):
    """
    This function welcomes the user , if the person does not Know how to 
    interact with the Skill 
    """
    
    return welcomeGuest()
    

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def onIntent(intentRequest, session):
             
    intent = intentRequest['intent']
    intentName = intentRequest['intent']['name']
    
    if intentName == "LevelSelection":
        return level_selection(intent, session)
    elif intentName =="Start":
        return start_game(intent,session)
    elif intentName == "AlphabetChosen":
        return set_alphabet(intent,session)
    elif intentName=="Stop":
        return next_game(intent,session)
    elif intentName=="Description":
        return description(intent,session)
    elif intentName == "AMAZON.HelpIntent":
        return welcomeGuest()
    elif intentName == "AMAZON.CancelIntent" or intentName == "AMAZON.StopIntent":
        return handleSessionEndRequest()
    else:
        return default(intent, session)
        

def onSessionEnd(sessionEndedRequest, session):
    """ 
    Called when the user ends the session.
    """
    print("on_session_ended requestId=" + sessionEndedRequest['requestId'] + ", sessionId=" + session['sessionId'])
        
    
# ------------------------------------------------------------------------------
# --------------------------- Behaviour Handlers -------------------------------
# ------------------------------------------------------------------------------

def welcomeGuest():
    """
    Gives Welcome Instructions to user
    """
    
    sessionAttributes = {}
    cardTitle = "Welcome"
    speech_output ="This is Game of Alphabets by Mohit Arora. You can say help or rules to listen the game rules, otherwise  " \
                    "choose level of difficulty by saying easy or hard. "
                   
    reprompt_text = "Choose level of difficulty, simply say easy or hard. "
    shouldEndSession = False
    
    return buildResponse(sessionAttributes, buildSpeechletResponse(cardTitle, speech_output, reprompt_text, shouldEndSession))


def default(intent,session):
    """
    default intent
    """
    
    
    cardTitle = "Default"
    if session.get('attributes',{}) and 'turn' in session['attributes']:
        speechOutput="Hmm, that was not a valid response. Tell me your number. "
    elif session.get('attributes',{}) and 'level' in session['attributes']:
        speechOutput= "Hmm, that was not a valid response. Would you like to play the game as first player or as second player? simply say first or second.  "
    else:
        speechOutput="Hmm, that was not a valid response, choose level of difficulty, simply say easy or hard. "
        
    repromptText="Hmm, that was not a valid response. If you are unaware of the game rules simply say rules or to quit the game say goodbye. " 
    if session.get('attributes',{}):
        sessionAttributes = session['attributes']
    else:
        sessionAttributes={}
    shouldEndSession=False
        
    return buildResponse(sessionAttributes, buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession))

    

def description(intent,session):
    """
    Explaining description and rules of the game to the user.
    """
    
    sessionAttributes = {}
    card_title = "Help"
    should_end_session = False
    Choice=intent['slots']['choose']['value']
    if session.get('attributes',{}) and 'Alexa_number' in session.get('attributes',{}):
        speech_output="It's your turn now, choose your alphabet. "
        reprompt_text="It's your turn now, choose your alphabet. To quit the game, simply say goodbye. "
        return buildResponse(session['attributes'], buildSpeechletResponse(
        card_title, speech_output, reprompt_text, should_end_session))
     
    elif(Choice=='help' or Choice=='rules'):
        speech_output = "Game of Alphabets is a short entertaining alphabet game for all age groups. This game has two players: user and alexa, Player 1 starts with a alphabet from a, b or c. \
        Player 2 then can say any alphabet from the 3 alphabets  following the alphabet said by player 1. The game continues like this and the one who says Z loses. \
        for example: if alexa forces user to speak Z, alexa will be the winner. \
        To start the game, first choose level of difficulty, simply say easy or hard. "
        reprompt_text ="To start the game, first choose level of difficulty, simply say easy or hard. "
        
    
    else:
        speech_output = "Hmm, that was not a valid response. "
        reprompt_text= "Hmm, that was not a valid response. "

    return buildResponse(sessionAttributes, buildSpeechletResponse(card_title, speech_output, reprompt_text, should_end_session))


def create_turn_attribute(Turn):
    return {"turn":Turn}

def start_game(intent,session):

    '''
    It sets the turn of the user and starts the game.
    
    '''
    card_title = "Game Start"
    should_end_session = False
    if session.get('attributes',{}) and 'Alexa_number' in session.get('attributes',{}):
        speech_output="It's your turn now, choose your alphabet. "
        reprompt_text="It's your turn now, choose your alphabet. To quit the game, simply say goodbye. "
        return buildResponse(session['attributes'], buildSpeechletResponse(
        card_title, speech_output, reprompt_text, should_end_session))
 
       
    elif('level' not in session.get('attributes',{})):
        speech_output= "First choose level of difficulty, simply say easy or hard. "
        reprompt_text = "First choose level of difficulty, simply say easy or hard. "
        return buildResponse({}, buildSpeechletResponse(
        card_title, speech_output, reprompt_text, should_end_session))

    else:
        Turn=intent['slots']['turn']['value']
        session['attributes']['turn']=Turn
        if(Turn=='second'):
            Level=session['attributes']['level']
            if(Level=='hard'):   
                alexa_number=1;
            else:
                alexa_number=random.choice([1,2,3])
            alexa_alphabet=chr(alexa_number+96)
            speech_output="Okay, let's start the game. My alphabet is: " + alexa_alphabet +\
            ".      Its yor turn now, What is your alphabet? "
            reprompt_text=" Its yor turn now, what is your alphabet? "
            session['attributes']['Alexa_number']=alexa_number
            
        elif(Turn=='1st'):
            speech_output="Okay, let's start the game, what is your alphabet? "
            reprompt_text=" What is your alphabet? "
    
        else:
            speech_output ="Would you like to play the game as first player or as second player? simply say first or second.  "
            reprompt_text= "Would you like to play the game as first player or as second player? simply say first or second.  "

        
        return buildResponse(session['attributes'], buildSpeechletResponse(
        card_title, speech_output, reprompt_text, should_end_session))


def create_level_attribute(Level):
    return {'level':Level}

def level_selection(intent, session):
    
    '''
    
    Sets the level of the game.
    
    '''

    
    card_title = "Level"
    should_end_session = False
    if session.get('attributes',{}) and 'Alexa_number' in session.get('attributes',{}):
        speech_output="It's your turn now, choose your alphabet. "
        reprompt_text="It's your turn now, choose your alphabet. To quit the game, simply say goodbye. "
        return buildResponse(session['attributes'], buildSpeechletResponse(
        card_title, speech_output, reprompt_text, should_end_session))
 
    else:
        Level=intent['slots']['level']['value']
        session_attributes=create_level_attribute(Level)
        speech_output="You chose " + Level + " as the level of difficulty. Would you like to play the game as first player or as second player? simply say first or second.  "
        reprompt_text="Would you like to play the game as first player or as second player? simply say first or second.  "

    return buildResponse(session_attributes, buildSpeechletResponse(
        card_title, speech_output, reprompt_text, should_end_session))


def create_total_attribute(alexa_number):
    return {"Alexa_number": alexa_number}



def set_alphabet(intent, session):
    
    '''
    
    Adding the number chosen by the user to the total. Choose a number for alexa and add that number to the total too.
    Also decides who is the winner when the total becomes 25 or more
    
    '''
    
    card_title = "Set"
    should_end_session = False

    if 'level' not in session.get('attributes',{}):
        speech_output= "First, choose level of difficulty, simply say easy or hard.  "
        reprompt_text = "First, choose level of difficulty, simply say easy or hard.  "
        return buildResponse({}, buildSpeechletResponse(
            card_title, speech_output, reprompt_text, should_end_session))

    if 'turn' not in session.get('attributes',{}):
        speech_output= "Would you like to play the game as first player or as second player? simply say first or second.  "
        reprompt_text="Would you like to play the game as first player or as second player? simply say first or second.  "

        return buildResponse(session['attributes'], buildSpeechletResponse(
            card_title, speech_output, reprompt_text, should_end_session))

        
    else:
        Level=session['attributes']['level']
        
        if 'alphabet' in intent['slots']: 
            user_string=(intent['slots']['alphabet']['value'])
            user_alphabet=user_string[0].upper()
            user_number=ord(user_alphabet)-64
            print(user_number)
            print(user_alphabet)            
            if(not user_alphabet.isalpha()):
                speech_output=" Hmm, that was not a valid response. Choose valid alphabet, try again. "
                reprompt_text=" Hmm, that was not a valid response. Choose a number from 1 to 3, try again. You can say goodbye to quit the game. "
                return buildResponse(session['attributes'], buildSpeechletResponse(
                    card_title, speech_output, reprompt_text, should_end_session))
        
            if session.get('attributes',{}) and 'Alexa_number' in session.get('attributes',{}):
                alexa_number=session['attributes']['Alexa_number']
            
            else:
                alexa_number=0
    
            if user_number<alexa_number or user_number>alexa_number+3 or user_number>26:
                speech_output=user_alphabet +" is not a valid alphabet. You can only choose among: " + chr(alexa_number+1+64) + ", " + chr(alexa_number+2+64) + ", or  " + chr(alexa_number+3+64)+ " alphabets.  Try again. "
                reprompt_text=user_alphabet +" is not a valid alphabet. Try again. "
                return buildResponse(session['attributes'], buildSpeechletResponse(
                    card_title, speech_output, reprompt_text, should_end_session))
        
            
            
            if(Level=='easy'):
            
                if(user_number>=21):
                    rem=user_number%4
                    rem=5-rem
                    if(rem==5):
                        alexa_number=user_number+1
                    elif(rem==4):
                            alexa_number=user_number+random.choice([1,2,3])
                    else:
                            alexa_number=user_number+rem
                else:
                        alexa_number=user_number+random.choice([1,2,3])
                        
                
            elif(Level=='hard'):
                rem=user_number%4
                rem=5-rem
                if(rem==5):
                    alexa_number=user_number+1
                elif(rem==4):
                    alexa_number=user_number+random.choice([1,2,3])
                else:
                    alexa_number=user_number+rem
        
            if(alexa_number>26):
                alexa_number=26
                    
            alexa_alphabet=chr(alexa_number+64)
            if(alexa_alphabet=='Z'):
                speech_output = "Your alphabet is: " + \
                user_alphabet+ ". "\
                "My alphabet is: "+alexa_alphabet +  \
                ". Congratulations! you won. Thank you for playing Game Of Alphabets. Please take out a moment to rate and review the skill. Have a nice day! "
                reprompt_text= "Thank you for playing Game Of Alphabets. Please take out a moment to rate and review the skill. Have a nice day!"
                should_end_session=True
                should_end_session=True
            
            elif(alexa_alphabet=='Y'):
                speech_output = "Your alphabet is: " + \
                user_alphabet+ ". "\
                    "My alphabet is: "+alexa_alphabet +  \
                    ". Now you can only choose Z, so you lose... Better luck next time. Thank you for playing Game Of Alphabets. Please take a moment to rate and review the skill. Have a nice day! "
                reprompt_text= "Thank you for playing Game Of Alphabets. Please take a moment to rate and review the skill. Have a nice day!"
                should_end_session=True
                
            
            else:
                speech_output = "Your alphabet is:" + user_alphabet + ".  " "My alphabet is: " + alexa_alphabet + ".      Its your turn now, choose a alphabet.  "
                reprompt_text = "Its your turn now. "

        else:
            speech_output="Hmm, that was not a valid response. You can only choose among: " + chr(alexa_number+1+64) + ", " + chr(alexa_number+2+64) + ", or  " + chr(alexa_number+3+64)+ ".  Try again. " 
            reprompt_text="Hmm, that was not a valid response. Choose a valid alphabet, try again. You can say goodbye to quit the game. " 
    
        
        session['attributes']['Alexa_number']=alexa_number
        
        if(alexa_number<26):
            return buildResponse(session['attributes'], buildSpeechletResponse(
            card_title, speech_output, reprompt_text, should_end_session))
        else:
            return buildResponse({}, buildSpeechletResponse(
            card_title, speech_output, reprompt_text, should_end_session))
            



def next_game(intent, session):

    '''
    
    Starts new game or end the session depending on the user's input.
    
    '''
    cardTitle = "New Game"
    
    Continue=intent['slots']['continue']['value']

    if Continue=='goodbye' or Continue =='good bye' or Continue =='exit' or Continue == 'quit': 
        speechOutput="Thank you for playing Game of alphabets. Please take a moment to rate and review the skill. Have a nice day!"
        sessionAttributes = {}
        repromptText=None
        shouldEndSession=True
    else:
        if session.get('attributes',{}) and 'turn' in session['attributes']:
            speechOutput="Hmm, that was not a valid response. Tell me your number. "
        elif session.get('attributes',{}) and 'level' in session['attributes']:
            speechOutput= "Hmm, that was not a valid response. Would you like to play the game as first player or as second player? simply say first or second.  "
        else:
            speechOutput="Hmm, that was not a valid response, choose level of difficulty, simply say easy or hard. "
        shouldEndSession=False
    repromptText="Hmm, that was not a valid response. If you are unaware of the game rules simply say rules or to quit the game say goodbye. " 
    if session.get('attributes',{}):
        sessionAttributes = session['attributes']
    else:
        sessionAttributes={}
    
        
    return buildResponse(sessionAttributes, buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession))

def handleSessionEndRequest():
    cardTitle = "Session Ended"
    speechOutput = "Thank you for playing Game of alphabets. Please take a moment to rate and review the skill. Have a nice day! "
    shouldEndSession = True
    return buildResponse({}, buildSpeechletResponse(cardTitle, speechOutput, None, shouldEndSession))    

# ------------------------------------------------------------------------------
# --------------------------- Response Builders --------------------------------
# ------------------------------------------------------------------------------

def buildSpeechletResponse(title, output, repromptTxt, endSession):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
            },
            
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
            },
            
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': repromptTxt
                }
            },
        'shouldEndSession': endSession
    }


def buildResponse(sessionAttr , speechlet):
    return {
        'version': '1.0',
        'sessionAttributes': sessionAttr,
        'response': speechlet
    }
