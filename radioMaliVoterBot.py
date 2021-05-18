#!/usr/bin/env python

import logging
from typing import Dict

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    PicklePersistence,
    CallbackContext,
)

import mysql.connector
import os

# please enter your database credentials below:
mydb = mysql.connector.connect(
  host="",
  database="",
  user="user",
  password="secret123"
)

# please enter your valid Telegram api token here
TOKEN = "TELEGRAM_API_TOKEN"

# this next line is needed for Heroku's webhook and should remain as is.
# Heroku will shutdown the bot after sixty seconds, when it does not
# bind to PORT.
PORT = int(os.environ.get("PORT", 80))

strings ={
    "en": {
        "start-greeting-1": "Hello, {}. You are registered at {}.\n",
        "start-greeting-2": "Here is an overview over your polls:\n\n",
        "start-hints" : "Would you like to create a new Poll?\nYou can use the /newPoll command for that!\nEnter '/delPoll X' to delete poll number X.\nUse /help to see a list of all available commands.",
        "start-error" : "unauthorized. Please tell admin to add {}Use /start to get back into the main menu\n",
        "greeting" : "Hello! This is Radio Mali Voter Bot!\nType /help for an overview of all the available commands\n",
        "choose_lang": "To set your preferred language to english, send /en.\n",
        "poll_overview_intro": "This is an overview of all your polls.\n",
        "create_poll_hint": "To create a new poll, enter /newPoll.\n",
        "language_confirmation": "Your language has now been set to English.\nSee /help in case of problems.\n",
        "help_hint": 
"""/start shows the main menu and lists all your polls
/setTime can change the times associated with a poll
/newPoll can be used to enter a new poll into the system
/delPoll can be used to delete a poll from the system
/info can be used to retrive information regarding a poll

/en sets the preferred language to English
/fr définit la langue préférée sur le français
""",
        "newPoll-error-generic" : "An internal Error occurred while trying to create your poll. Please try again later.\n",
        "newPoll-success": "Your new poll has been added to the system.\n",
        "newPoll-error-usage": "usage:\n/newPoll <name of the poll> <yyyy-mm-dd> <hh:mm:ss> <yyyy-mm-dd> <hh:mm:ss>\n\nlike so:\n'/newPoll just a test 2021-05-05 12:20:12 2021-05-05 12:20:13'\nUse /start to get back into the main menu\n",
        "delPoll-usage": "Please add the number of the poll you are trying to remove to this command. The corresponding numbers can be found in /start.\n",
        "delPoll-error-parse" : "Sorry, I was not able to get the number of the poll you tried to delete! Can you tell me again? Use the command like '/delPoll X' to delete poll number X\nEnter /start to see all polls and their numbers.\nUse /start to get back into the main menu\n",
        "delPoll-error-undefined" : "Oh no, something went wrong as I tried to delete your poll. Please try again later\nUse /start to get back into the main menu\n",
        "delPoll-error-index" : "Mh. I appears that the number you entered was either to high or to low. Please make sure you were trying to delete the correct poll.\nSee /start for a list of all your polls!\nUse /start to get back into the main menu\n",
        "info-error-args": "Sorry, but I was not able to understand what poll you wanted to inspect!\nUse /start to get back into the main menu\n",
        "info-error-negative": "Oh, excuse me, but you cannot use a negative number here.\nUse /start to get back into the main menu\n",
        "info-error-no-info": "I was not able to find any information on poll number {}.\nAre you sure that was the correct number you were interested in? Maybe try again later.\nUse /start to get back into the main menu\n",
        "info-start-end": "Start: {}\nEnd: {}\n\n",
        "info-vote": "{} (☎️ {}) - {} votes\n",
        "info-sum": "total number of votes: {}",
        "info-error-no-poll": "Sorry, I was unable to find out more about your poll '{}'!\nMaybe retry this command at a later time or contact the RadioMaliVoterBot-Team.Use /start to get back into the main menu\n",
        "newPoll-error-no-parse": "I was not able to turn the last bits of what you wrote into dates and times for starting and ending the poll!\nUse /start to get back into the main menu\n",
        "newPoll-error-sys-not-working": "I wanted to enter your new poll to the system, but it did not work. Maybe try again later or contact the RadioMaliVoterBot-Team...Use /start to get back into the main menu\n",
        "delPoll-success": "Alright, you successfully deleted the poll!",
        "setTime-usage": "/setTime <poll> <yyyy-mm-dd> <hh:mm:ss> <yyyy-mm-dd> <hh:mm:ss>\n",
        "setTime-error-parse": "I am sorry, but I was not able to read the correct time from what you wrote!Use /start to get back into the main menu\n",
        "setTime-error-generic": "Oh! Something went wrong and I was not able to set the new time in the system!Use /start to get back into the main menu\n",
    },
    "fr" : {
        "start-greeting-1": "Bonjour, {}. Vous êtes inscrit sur {}.\n",
        "start-greeting-2": "Voici un aperçu de vos sondages: \n\n",
        "start-hints" : "Souhaitez-vous créer un nouveau sondage? \nVous pouvez utiliser la commande /newPoll pour cela! \nEntrez '/delPoll X' pour supprimer le numéro d'interrogation X.\nVoir /help en cas de problème.\n",
        "start-error" : "non autorisé. Veuillez dire à l'administrateur d'ajouter {} Utiliser /start pour revenir au menu principal\n",
        "greeting" : "Bonjour! Ceci est RadioMaliVoterBot! \nTapez /help pour un aperçu de toutes les commandes disponibles\n",
        "choose_lang": "Pour définir votre langue préférée sur l'anglais, envoyez /fr\n",
        "poll_overview_intro": "Ceci est un aperçu de tous vos sondages.\n",
        "create_poll_hint": "Pour créer un nouveau sondage, entrez /newPoll. \n",
        "language_confirmation": "Votre langue est désormais définie sur le français. \nVoir /help en cas de problème.\n",
        "help_hint": 
"""/start affiche le menu principal & répertorie tous vos sondages.
/newPoll peut être utilisé pour entrer un nouveau sondage dans le système
/delPoll peut être utilisé pour supprimer un sondage du système
/info peut être utilisé pour récupérer des informations concernant un sondage

/en sets the preferred language to English
/fr définit la langue préférée sur le français
""",
        "newPoll-error-generic" : "Une erreur interne s'est produite lors de la tentative de création de votre sondage. Veuillez réessayer plus tard.\n",
        "newPoll-success": "Votre nouveau sondage a été ajouté au système.\n",
        "newPoll-error-usage": "usage:\n/newPoll <name of the poll> <yyyy-mm-dd> <hh:mm:ss> <yyyy-mm-dd> <hh:mm:ss>\n\nlike so:\n'/newPoll juste un test 2021-05-05 12:20:12 2021-05-05 12:20:13'\nUtilisez /start pour revenir au menu principal\n",
        "delPoll-usage": "Veuillez ajouter le numéro du sondage que vous essayez de supprimer à cette commande. Les numéros correspondants se trouvent dans /start.\n",
        "delPoll-error-parse" : "Désolé, je n'ai pas pu obtenir le numéro du sondage que vous avez essayé de supprimer! Pouvez-vous me le redire? \nUtilisez la commande comme '/delPoll X' pour supprimer le numéro de sondage X \nEntrez /info à voir tous les sondages et leurs numéros. \nUtilisez /start pour revenir au menu principal \n",
        "delPoll-error-undefined" : "Oh non, quelque chose s'est mal passé lorsque j'ai essayé de supprimer votre sondage. Veuillez réessayer plus tard\nUtilisez /start pour revenir au menu principal\n",
        "delPoll-error-index" : "Mh. Il semble que le nombre que vous avez entré était soit trop élevé, soit trop bas. Veuillez vous assurer que vous essayez de supprimer le sondage correct. \nVoir /start pour une liste de tous vos sondages! \nUtilisez /start pour revenir au menu principal\n",
        "info-error-args": "Désolé, mais je n'ai pas pu comprendre quel sondage vous vouliez inspecter!\nUtilisez /start pour revenir au menu principal\n",
        "info-error-negative": "Oh, excusez-moi, mais vous ne pouvez pas utiliser un nombre négatif ici.\nUtilisez /start pour revenir au menu principal\n",
        "info-error-no-info": "Je n'ai trouvé aucune information sur le numéro de sondage {}. \nEtes-vous sûr que c'était le bon numéro qui vous intéressait? Peut-être réessayer plus tard.\nUtilisez /start pour revenir au menu principal\n",
        "info-start-end": "démarrer: {}\nfinir: {}\n\n",
        "info-vote": "{} (☎️ {}) - {} les votes\n",
        "info-sum": "nombre total de votes: {}",
        "info-error-no-poll": "Désolé, je n'ai pas pu en savoir plus sur votre sondage '{}'! \nPeut-être réessayer cette commande plus tard ou contacter l'équipe RadioMaliVoterBot. \nUtilisez /start pour revenir au menu principal\n",
        "newPoll-error-no-parse": "Je n'ai pas pu transformer les derniers morceaux de ce que vous avez écrit en dates et heures de début et de fin du sondage!\nUtilisez /start pour revenir au menu principal\n",
        "newPoll-error-sys-not-working": "Je voulais entrer votre nouveau sondage dans le système, mais cela n'a pas fonctionné. Peut-être réessayer plus tard ou contacter l'équipe RadioMaliVoterBot ...\nUtilisez /start pour revenir au menu principal\n",
        "delPoll-success": "Très bien, vous avez supprimé le sondage avec succès!",
        "setTime-usage": "/setTime <poll> <yyyy-mm-dd> <hh:mm:ss> <yyyy-mm-dd> <hh:mm:ss>\n",
        "setTime-error-parse": "Je suis désolé, mais je n'ai pas pu lire l'heure correcte d'après ce que vous avez écrit!\nUtilisez /start pour revenir au menu principal\n",
        "setTime-error-generic": "Oh! Une erreur s'est produite et je n'ai pas pu régler la nouvelle heure dans le système!\nUtilisez /start pour revenir au menu principal\n",
    }
}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

default_language = "en"
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext):
    cur = mydb.cursor()
    val = [(update.effective_user.id)]
    sql = "SELECT DJ.Name, RadioStation.Name FROM DJ, RadioStation WHERE TelegramID = %s AND DJ.RadioStation = RadioStation.Id"
    cur.execute(sql, val)
    rows = cur.fetchall()
    mydb.commit()
    registeredUser = (len(rows)) > 0
    if registeredUser:
        reply_text = strings[context.user_data.get("language", default_language)]["start-greeting-1"].format(rows[0][0], rows[0][1])
        cur = mydb.cursor()
        val = [(update.effective_user.id)]
        sql = "SELECT DISTINCT Poll.Name, Poll.StartDate, Poll.EndDate FROM DJ, RadioStation, Poll WHERE DJ.RadioStation = RadioStation.id AND RadioStation.id = Poll.RadioStation AND DJ.TelegramID = %s ORDER BY Poll.Id"
        cur.execute(sql, val)
        rows = cur.fetchall()
        reply_text +=  strings[context.user_data.get("language", default_language)]["start-greeting-2"]
        for n, row in enumerate(rows):
            reply_text += "{}. {}\n".format(n+1, row[0])
        print(rows)
        reply_text += "\n"
        reply_text += strings[context.user_data.get("language", default_language)]["start-hints"]
    else:
        reply_text = strings[context.user_data.get("language", default_language)]["start-error"].format(val)
    update.message.reply_text(reply_text, reply_markup=None)    

def help(update: Update, _: CallbackContext):
    reply_text = ""
    for lang in strings:
        reply_text += "[{}]\n".format(lang.upper())
        reply_text += strings[lang]["help_hint"] + "\n"
    update.message.reply_text(reply_text)

def set_french(update: Update, context: CallbackContext):
    context.user_data["language"] = "fr"
    update.message.reply_text(strings["fr"]["language_confirmation"])

def set_english(update: Update, context: CallbackContext):
    context.user_data["language"] = "en"
    update.message.reply_text(strings["en"]["language_confirmation"])

def info(update: Update, context: CallbackContext):
    if len(context.args) != 1:
        update.message.reply_text(strings[context.user_data.get("language", default_language)]["info-error-args"]) # "usage:\n/info <poll number>")
        return
    try:
        rowNumber = int(context.args[0])-1
        if rowNumber < 0:
            update.message.reply_text(strings[context.user_data.get("language", default_language)]["info-error-negative"]) # "a poll number cannot be negative")
            return
        cur = mydb.cursor()
        val = [(update.effective_user.id)]
        sql = "SELECT DISTINCT Poll.Id, Poll.Name, Poll.StartDate, Poll.EndDate FROM Poll,DJ,RadioStation WHERE DJ.RadioStation = RadioStation.id AND RadioStation.id = Poll.RadioStation AND DJ.TelegramID = %s ORDER BY Poll.Id"
        cur.execute(sql, val)
        rows = cur.fetchall()
        pollId = rows[rowNumber][0]
        pollName = rows[rowNumber][1]
        startDate = rows[rowNumber][2]
        endDate = rows[rowNumber][3]
    except:
        update.message.reply_text(strings[context.user_data.get("language", default_language)]["info-error-no-info"].format(rowNumber+1)) # "I was not able to find any information on poll number {}.\nAre you sure that was the correct number you were interested in? Maybe try again later."
        return
    try:
        cur = mydb.cursor()
        val = [pollId]
        sql = "SELECT r.Name, r.Anwser, r.Count, r.StartDate, r.EndDate, r.Number FROM Results r WHERE `Poll Id` = %s"
        cur.execute(sql, val)
        rows = cur.fetchall()
        try:
            totalVotes = 0
            reply_text = "{}\n\n".format(pollName)
            reply_text += strings[context.user_data.get("language", default_language)]["info-start-end"].format(rows[0][3],rows[0][4]) #"Start: {}\nEnd: {}\n\n"
            for line in rows:
                reply_text += strings[context.user_data.get("language", default_language)]["info-vote"].format(line[1], line[5], line[2]) #"{} (☎️ {}) - {} votes\n"
                totalVotes += int(line[2])
            reply_text += strings[context.user_data.get("language", default_language)]["info-sum"].format(totalVotes) #"total number of votes: {}"
            update.message.reply_text(reply_text)
        except Exception as e:
            raise e
    except Exception as e:
        update.message.reply_text(strings[context.user_data.get("language", default_language)]["info-error-no-poll"]) #"Sorry, I was unable to find out more about your poll '{}'!\nMaybe retry this command at a later time or contact the RadioMaliVoterBot-Team.")

def newPoll(update: Update, context: CallbackContext):
    if len(context.args) < 5 or context.args == [""]:
        update.message.reply_text(strings[context.user_data.get("language", default_language)]["newPoll-error-usage"])
        return
    try:
        startDate = context.args[-4]
        startTime = context.args[-3]
        endDate = context.args[-2]
        endTime = context.args[-1]
        cur = mydb.cursor()
        cur.execute("SELECT RadioStation from DJ where TelegramID = %s", [update.effective_user.id])
        radiostationid = cur.fetchall()[0][0]
        val = [" ".join(context.args[:-4]), radiostationid, "{} {}".format(startDate, startTime), "{} {}".format(endDate, endTime)]
        sql = "INSERT INTO Poll (Name, RadioStation, StartDate, EndDate) VALUES (%s, %s, %s, %s)"
        cur.execute(sql, val)
        mydb.commit()
    except mysql.connector.Error as e:
        if e.errno == 1292:
            update.message.reply_text(strings[context.user_data.get("language", default_language)]["newPoll-error-no-parse"])
        else:
            update.message.reply_text(strings[context.user_data.get("language", default_language)]["newPoll-error-sys-not-working"]) #"I wanted to enter your new poll to the system, but it did not work. Maybe try again later or contact the RadioMaliVoterBot-Team...")
        return
    update.message.reply_text(strings[context.user_data.get("language", default_language)]["newPoll-success"])
    
def delPoll(update: Update, context: CallbackContext):
    if len(context.args) != 1:
        update.message.reply_text(strings[context.user_data.get("language", default_language)]["delPoll-usage"])
        return
    try:
        rowNumber = int(context.args[0])-1
        if rowNumber < 0:
            raise Exception()
    except:
        update.message.reply_text(strings[context.user_data.get("language", default_language)]["delPoll-error-parse"])
        return
    try:
        cur = mydb.cursor()
        val = [(update.effective_user.id)]
        sql = "SELECT DISTINCT Poll.Id, Poll.Name FROM Poll,DJ,RadioStation WHERE DJ.RadioStation = RadioStation.id AND RadioStation.id = Poll.RadioStation AND DJ.TelegramID = %s ORDER BY Poll.Id"
        cur.execute(sql, val)
        rows = cur.fetchall()
        try:
            idToDel = rows[rowNumber][0]
            pollName = rows[rowNumber][1]
        except:
            update.message.reply_text(strings[context.user_data.get("language", default_language)]["delPoll-error-index"])
            return
        cur.execute("DELETE FROM Poll WHERE Id = %s", [idToDel])
        mydb.commit()
        update.message.reply_text(strings[context.user_data.get("language", default_language)]["delPoll-success"].format(pollName)) #"you have deleted the poll called '{}'."
    except Exception as e:
        print(e)
        update.message.reply_text(strings[context.user_data.get("language", default_language)]["delPoll-error-undefined"])

def setTime(update: Update, context: CallbackContext):
    if len(context.args) != 5:
        update.message.reply_text(strings[context.user_data.get("language", default_language)]["setTime-usage"])#"usage:\n/setTime <pollNr> <start date> <start time> <end date> <end time>")
        return
    try:
        rowNumber = int(context.args[0])-1
        if rowNumber < 0:
            raise Exception()
        cur = mydb.cursor()
        val = [(update.effective_user.id)]
        sql = "SELECT DISTINCT Poll.Id, Poll.Name, Poll.StartDate, Poll.EndDate FROM Poll,DJ,RadioStation WHERE DJ.RadioStation = RadioStation.id AND RadioStation.id = Poll.RadioStation AND DJ.TelegramID = %s ORDER BY Poll.Id"
        cur.execute(sql, val)
        rows = cur.fetchall()
        pollId = rows[rowNumber][0]
        pollName = rows[rowNumber][1]
        startDate = rows[rowNumber][2]
        endDate = rows[rowNumber][3]

    except:
        update.message.reply_text(strings[context.user_data.get("language", default_language)]["setTime-error-parse"])
        return
    try:
        cur = mydb.cursor()
        val = ["{} {}".format(context.args[1],context.args[2]), "{} {}".format(context.args[3],context.args[4]), pollId]
        sql = "UPDATE Poll SET StartDate = %s, EndDate = %s WHERE Id = %s"
        cur.execute(sql, val)
        mydb.commit()
    except Exception as e:
        update.message.reply_text(strings[context.user_data.get("language", default_language)]["setTime-error-generic"])
        
def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("fr", set_french))
    dispatcher.add_handler(CommandHandler("en", set_english))
    dispatcher.add_handler(CommandHandler("info", info))
    dispatcher.add_handler(CommandHandler("setTime", setTime))
    dispatcher.add_handler(CommandHandler("newPoll", newPoll))
    dispatcher.add_handler(CommandHandler("delPoll", delPoll))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, help))
    dispatcher.add_handler(CommandHandler("help", help))
    
    # Start the Bot
    PORT = int(os.environ.get('PORT', '8443'))
    
    # add handlers
    updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN,
                      webhook_url="https://radiomalivoterbot.herokuapp.com/" + TOKEN)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
