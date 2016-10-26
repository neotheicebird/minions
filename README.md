Minions
=======

If you are a minion lover or if you are just bored with work, you can chat with this SlackBot and pass some time.

![chat_with_minions](img/chat_with_minions.png)

Installation
============

To install this bot, follow these instructions:

1 - If you do not have a slack team yet, Go up to [Slack web api page](https://api.slack.com/) and click on sign up/Sign in

2 - After signing in, you need to create a new for your team. Head up to [add bot integration page](https://my.slack.com/services/new/bot) and create a bot named "minions"

3 - Copy the API Token given to "minions". *example token: xoxb-96562090935-UOeCc0q70QABbmAMf3FYyS15*

4 - Open `token.json` file in your local directory and paste the token into the field for `token`. Your `token.json` should now look like:

```
{
    "id": "",
    "token": "xoxb-96562090935-UOeCc0q70QABbmAMf3FYyS15"
}
```

5 - Type `python minions.py` in a terminal and run it.

6 - Head over to slack, create a new channel and invite @minions or invite it to an existing channel.

![create_slack_channel](img/create_slack_channel.png)