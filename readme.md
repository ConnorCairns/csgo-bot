# CS:GO Discord Bot

Bot made to handle team picking and map vetoing for CS:GO 10 mans. Uses https://discordpy.readthedocs.io/en/latest/

## Installation

#### Prerequisites

Python 3.6 or higher required.
In the bot home directory you will need to create a file called .env and put:

```
DISCORD_TOKEN="[Your discord bot's token]"
LOBBY_ID="[Discord lobby channel ID]"
TEAM1_ID="[Discord team 1 channel ID]"
TEAM2_ID="[Discord team 2 channel ID]"
```

The token can be found on https://discordapp.com/developers/applications by creating a new application and adding a bot. Channel ID can be found by enabling developer mode on discord (Settings -> Appearance -> Advanced) then right clicking on a channel and selecting `Copy ID`

---

Running in a virtual environment is recommended, to do so navigate to repo home directory then:

`python3 -m venv bot-env`

`source bot-env/bin/activate`

After the virtual environment is running:

`pip install -r requirements.txt`

`python bot.py`

## Commands

`/10man`

Starts team picking with two randomly selected captains

---

`/veto`

If teams have been chosen, start a veto with captains controlling. If no teams have been chosen, starts a veto with author controlling

---

`/veto [captain 2]`

Starts a veto with author and captain specified in argument controlling

---

`/cancel`

Cancel 10man match and start again fresh

---

`/reload`

Reload all cogs
