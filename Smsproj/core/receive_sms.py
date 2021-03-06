from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request, redirect

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)
    print(body)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if body == 'hello':
        resp.message("Hi!")
    elif body == 'bye':
        resp.message("Goodbye")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)


# from flask import Flask, request, session
# from twilio.twiml.messaging_response import MessagingResponse

# # The session object makes use of a secret key.
# SECRET_KEY = 'a secret key'
# app = Flask(__name__)
# app.config.from_object(__name__)

# # Try adding your own number to this list!
# callers = {
#     "+14158675308": "Rey",
#     "+12349013030": "Finn",
#     "+12348134522": "Chewy",
# }


# @app.route("/", methods=['GET', 'POST'])
# def hello():
#     """Respond with the number of text messages sent between two parties."""
#     # Increment the counter
#     counter = session.get('counter', 0)
#     counter += 1

#     # Save the new counter value in the session
#     session['counter'] = counter

#     from_number = request.values.get('From')
#     if from_number in callers:
#         name = callers[from_number]
#     else:
#         name = "Friend"

#     # Build our reply
#     message = '{} has messaged {} {} times.' \
#         .format(name, request.values.get('To'), counter)

#     # Put it in a TwiML response
#     resp = MessagingResponse()
#     resp.message(message)

#     return str(resp)


# if __name__ == "__main__":
#     app.run(debug=True)


