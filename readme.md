# CS:GO Discord Bot

Bot made to handle team picking and map vetoing for CS:GO 10 mans. Uses https://discordpy.readthedocs.io/en/latest/

## Installation

#### Prerequisites

Python 3.6 or higher required.
In the bot home directory you will need to create a file called .env and on the first line put:

`DISCORD_TOKEN="[Your discord bot's token]"`

The token can be found on https://discordapp.com/developers/applications by creating a new application and adding a bot.

---

Running in a virtual environment is recommended, to do so navigate to bots home directory then:

`python3 -m venv bot-env`
`source bot-env/bin/activate`

After the virtual environment is running:

`pip install -r requirements.txt`
`python bot.py`

## Commands

`/10man [captain 1] [captain 2]`

Starts team picking with two captains

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
