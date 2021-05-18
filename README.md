# ICT4D2021-RadioMaliVoterBot

This is the Telegram bot by ICT4D 2021's group three.

This repository intents to provide a clean version, ready to be forked, set up and run using Heroku.

## Installation
There are several steps required to connect your version of this Telegram bot to your RadioMaliVoter.

1. obtain an Telegram bot API key. This is done by using Telegram, more information can be found [here](https://core.telegram.org/bots)
2. make a private copy of this repo
3. enter your database credentials and API key into radioMaliVoterBot.py (lines 20 to 29)
4. connect your version of this repo with your Heroku account
5. enter your Telegram ID into the database of your RadioMaliVoter DJ account
6. Enjoy your Telegram bot!

## Telegram Bot Command Reference
```
  /start
```
This command acts as the entry point for the Telegram bot. It gives an overview of all currently available polls in an enumerated list

```
  /info <number of poll>
```
This command is used to inspect a poll using the numbers displayed in /start's output as an index. It displays start and end dates and vote-counts

```
/delPoll <number of poll>
```
This command is used to remove the poll according to the number it has in /start's outpu. When there are multiple DJ's working on the system, be sure to execute /start just before you delete poll, so the correct poll is selected.

```
/newPoll <name> <start date: YYYY-MM-DD> <start time: HH:MM[:SS]> <end date: YYYY-MM-DD> <end time: HH:MM[:SS]>
```
This command creates a new poll. The name may contain spacesand emojis. The last four, space seperated parameters to this command are required to be parsable as time stemps by your MySQL backend.

```
/setDate <number of poll> <start date: YYYY-MM-DD> <start time: HH:MM[:SS]> <end date: YYYY-MM-DD> <end time: HH:MM[:SS]>
```

This command updates the times connected to a poll, indexed by its number in /start's output to the new dates and times provided as parameters.
