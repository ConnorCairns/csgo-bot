# CS:GO Discord Bot

Bot made to handle team picking and map vetoing for CS:GO 10 mans. Uses https://discordpy.readthedocs.io/en/latest/

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
