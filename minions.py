#!/usr/bin/python
"""
This is the minions chat bot. Chat with minions and get amused.
"""

from slackclient import SlackClient
import json
import time
import re

def find_bot_id_overwrite_tokenfile():
    api_call = slack_client.api_call("users.list")

    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                with open(TOKEN_FILE, 'w') as tokenfp:
                    api_info["id"] = user.get('id')
                    json.dump(api_info, tokenfp)
                    # print(api_info)
                    print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
    else:
        print("could not find bot user with the name " + BOT_NAME)

def minion_response(message):
    """
        The response minions give to what to say to them, Banana.

    """
    words = re.findall(r"[A-Za-z@#]+|\S", message)
    resp = "Kampai"
    if words:
        for word in words:
            g = (minion_answer for minion_answer, trigger_keys in minionlang.items() if word in trigger_keys)
            try:
                resp = next(g)
                break
            except StopIteration:
                continue
    return resp

def handle_message(message, channel):
    """
        Receives messages directed at the bot and determines if they
        are valid messages. If so, then acts on the messages. If not,
        returns back what it needs for clarification.
    """
    # response = "Not sure what you/ mean. Use the *" + EXAMPLE_COMMAND + \
    #            "* message with numbers, delimited by spaces."
    # if message.startswith(EXAMPLE_COMMAND):
    #     response = "Sure...write some more code then I can do that!"
    response = minion_response(message)
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None

TOKEN_FILE = "token.json"

# instantiate Slack & Twilio clients
with open(TOKEN_FILE, 'r') as tokenfp:
    api_info = json.load(tokenfp)

slack_client = SlackClient(api_info["token"])

BOT_NAME = 'minions'

with open("minion.json", "r") as minionlangfp:
    minionlang = json.load(minionlangfp)

# starterbot's ID as an environment variable
BOT_ID = api_info["id"]
if not BOT_ID:
    find_bot_id_overwrite_tokenfile()

# constants
AT_BOT = "<@" + BOT_ID + ">"

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            message, channel = parse_slack_output(slack_client.rtm_read())
            if message and channel:
                handle_message(message, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")