#!/usr/bin/python
# -*- coding: utf-8 -*-
from groupy import Client
from groupy import attachments
import bottle
from bottle import request, route, run
import random
import ast
import time
import datetime
from datetime import timedelta
import csv
import sys

__author__ = 'Ryan Thompson'
__version__ = 'development'
"""*****************************************************************************
GroupMe Trolling Bot:
v0.5.0
Updated groupy to v0.8.1
Modified code to run in Docker on unRAID.

v0.4.0 - 4/13/2017
Added the spirit bomb kick.

v0.3.0 - 2/17/2017
Added CSV parsing.
Improved Quadz block speed.
Improved command handling.
Added drake lyrics post every time Tony is mentioned.
Added image posting.

v0.2.2 - 2/12/2017
Improved target acquisition.
Added random Drake lyrics.

v0.2.1 - 2/9/2017
Improved setting user targets.
Added rough execution time estimate.

v0.2.0 - 2/8/2017
Converted to accept callbacks with Bottle.
Converted code to run in bottle instance.
Added '/bad and boujee' command.
Added sendMention function
Added quadzBlock for everyone.

v0.1.3 - 1/31/2017
Added auto kick for Addison.

v0.1.2 - 1/30/2017
Added mention capability to bot.

v0.1.1 - 1/23/2017
Added multiple target code and None handling.

v0.1.0 - 1/10/2017
Bot monitors selected GroupMe for Fill's posts. Will kick him after 3
consecutive posts.
*****************************************************************************"""


# Picks the group to work in. Lists users and their user id's.
def setup(client):
    groups = list(client.groups.list_all())
    i = 0
    if __version__ == "development":
        for g in groups:
            if g.group_id == "27634334":
                group = g
        user_option = ""

    else:
        for g in groups:
            print(i, g, g.group_id)
            i += 1
        user_option = int(input("Which group? "))
        group = groups[user_option]

    print("You chose", group.name.encode())

    # Adds user targets.
    get_target = []
    users = group.members

    # temporary until docker interaction is figured route
    user_option = 'n'

    while user_option != 'n':
        # See if another target is required. If 'Yes', append target list with
        # target.
        user_option = input("Do you want to add a target? (y or n): ")
        if user_option == 'y':
            i = 0
            for u in users:
                print(i, u.nickname, u.user_id)
                i += 1
            user_option = chooseTarget(i)
            get_target.append(users[user_option])
            print("new target: ", get_target[-1], "\n", get_target)

    if user_option == 'No' and len(get_target) == 0:
        get_target = [None]
        print("no targets selected, ", get_target)

    return group, users, get_target


# Choose a target
def chooseTarget(counter):
    choice = counter
    while choice < 0 or choice > counter - 1:
        choice = input("Choose a target (line number): ")
        try:
            int_choice = int(choice)
        except:
            print("You did not enter a number.")
            choice = counter
        else:
            if int_choice < 0 or int_choice > counter - 1:
                print("Choice out of range.")
                choice = counter
            else:
                return int_choice


# Sends a mention with correct args.
def sendMention(message, user_id):
    temp_mention = attachments.Mentions(
        [user_id], [[len(message[0]) - 1, len(message[1]) + 1]])
    fillbot.post(message[0] + message[1], [temp_mention])
    print("posted", message[0] + message[1], [temp_mention])


# Kicks Addison when he joins the group.
# TODO: add multi user shit list checking
def addisonKicker():
    bot_group.refresh()
    temp_users = bot_group.members()
    for t_u in temp_users:
        if int(t_u.user_id) == useful_users['addison']:
            sendMention(["hey @", str(t_u.nickname)], str(t_u.user_id))
            fillbot.post("GTFO")
            bot_group.remove(t_u)
            print("removed @", str(t_u.nickname))
    return


# Quad post blocking.
def quadzBlock(payload):
    if int(payload['id']) != botParameters.msg_hist:
        print(int(payload['id']), "NEQ", botParameters.msg_hist)
        for j in range(2, 0, -1):
            botParameters.msg_hist_user[j] = botParameters.msg_hist_user[j - 1]

        print(payload['text'], "by", payload['sender_id'],
              "aka", payload['name'])

        botParameters.msg_hist_user[0] = int(payload['sender_id'])
        botParameters.msg_hist = int(payload['id'])

        # TODO: Try to use list built in methods to check equality.
        if botParameters.msg_hist_user[0] == \
                botParameters.msg_hist_user[1] and \
                botParameters.msg_hist_user[1] == \
                botParameters.msg_hist_user[2]:
            sendMention(["chill out @", payload['name']], payload['sender_id'])
            botParameters.msg_hist_user[0] = 0
            """
            for t in targets:
                if t is not None:
                    # TODO: Auto kick on a quad post?
                    if msg_hist_user[2] == int(t.user_id):
                        bot_group.remove(t)
                        print("removed target ", payload['name'], "on quadz")
                        fillbot.post("quadz block try again")
            """
    return


# Evaluates and performs spirit bomb
def spiritBombKick(data):
    user = data['sender_id']
    botParameters.user_post_count[user] += 1
    if botParameters.user_post_count[user] == 5:
        temp_img = attachments.Image(botParameters.spirit_bomb_gifs[0])
        fillbot.post('', temp_img)
    elif botParameters.user_post_count[user] == 10:
        temp_img = attachments.Image(botParameters.spirit_bomb_gifs[1])
        fillbot.post('', temp_img)
    elif botParameters.user_post_count[user] == 15:
        temp_img = attachments.Image(botParameters.spirit_bomb_gifs[2])
        fillbot.post('', temp_img)
    elif botParameters.user_post_count[user] == 20:
        temp_img = attachments.Image(botParameters.spirit_bomb_gifs[3])
        fillbot.post('', temp_img)
        time.sleep(1)
        sendMention(["tbh GFY @", data['name']], data['sender_id'])
        time.sleep(1)
        bot_group.remove(targets[0])
        botParameters.user_post_count[user] = 0


# Silences the bot
# TODO: Add length of time for silence
def silenceCommand(command, user, u_id):
    if command == '/silence':
        for key, value in admins.items():
            print(key, value)
            if value == u_id:
                botParameters.silence = not botParameters.silence
                print("bot silence flag is %r" % botParameters.silence)
                if botParameters.silence:
                    fillbot.post("Goodnight.")
                else:
                    fillbot.post("Hello.")
                return
        fillbot.post("YOU DIDN'T SAY THE MAGIC WORD!", [attachments.Image(
            'https://media.giphy.com/media/5ftsmLIqktHQA/giphy.gif')])
        print("%s is not a valid user." % user)
    else:
        print("Not silence command")
    return


# Executes commands if prompted by certain users
def executeCommands(command, user, u_id):
    """
    if command == '/bad and boujee':
        for lyrics in bad_and_boujee:
            fillbot.post(lyrics)
            time.sleep(1)
        print("bad and boujee was requested by %s." % user)
        return '/bad and boujee'
    """

    if command == '/drake':
        print("%s requested some drake lyrics." % user)
        lyrics = random.choice(drizzy_lyrics)
        fillbot.post(lyrics)
        print(lyrics)
        return '<DRAKE>'

    elif command == '/eatshit':
        if u_id != useful_users['bebe']:
            botParameters.eatshit = not botParameters.eatshit
            print("Eat shit toggled to %r" % botParameters.eatshit)
            return '<EATSHIT>'
        else:
            temp_img = attachments.Image(
                'https://i.groupme.com/320x240.gif.9447c57af1224aac910cf77c26e'
                'e421d')
            fillbot.post('', [temp_img])
            return '<EATSHIT> DENINED'

    elif command == '/ANALysis':
        temp_img = attachments.Image(
            'https://i.groupme.com/245x245.gif.550f59867ae4403598936c186b8378e'
            '1.large')
        fillbot.post('', [temp_img])
        return '<ANALysis>'

    # TODO: Add shitlist functionality
    """
    elif command == '/shitlist':
        if sub_command == '-a':
            # need to extract the command from the text
            data_attachments = data['attachments']
            if data_attachments['type'] == 'mentions':
                for u in data_attachments['user_ids']:
    """

    return '<INVALID COMMAND>'


# Gets data from a .csv file.
def getCSVData(archive_path):
    with open(archive_path, 'r') as file:
        csv_data = list(csv.reader(file, delimiter=';', quotechar="'",
                                   quoting=csv.QUOTE_ALL))
        # pass row 1 as .csv data.
        csv_data = csv_data[0]
        # print(csv_data)
    return csv_data


class createAndroid(object):
    # Stores historical messages, user names, enable/disbale flags...

    def __init__(self):
        self.admins = [None]
        self.msg_hist = 1
        self.msg_hist_user = [1, 2, 3]
        self.silence = False
        self.eatshit = True
        self.user_post_count = {}
        self.spirit_bomb_gifs = [
            'https://i.groupme.com/500x455.gif.ee9a23156cc945ab88658893a03d7b2d',
            'https://i.groupme.com/500x501.gif.6bf50b1124cf4d44af29c06f4aaebfc3',
            'https://i.groupme.com/500x278.gif.9c18ffd8d72c4f36af3f2721e3ddfdd9',
            'https://i.groupme.com/250x360.gif.8c25b3fe35f04f18968669bb9f4a6599']


# This is the main loop because it runs on the bottle server. All bot
# functions should be in this function.
@route('/', method='POST')
def runTheTrap():
    start_time = time.time()
    data = request.json
    silenceCommand(data['text'], data['name'], int(data['sender_id']))
    print(data, "\n", data['text'])
    if data and not botParameters.silence:
        """
        # Addison scanner and kicker.
        if data['sender_type'] == 'system':
            print("Checking for unauthorized users...")
            addisonKicker()
        """

        if data['sender_type'] != 'bot' and data['sender_type'] != 'system':
            # quadzBlock(data)

            # 'Eat shit' for Baby Conz.
            # if int(data['sender_id']) == useful_users['bebe'] and \
            #         botParameters.eatshit:
            #         sendMention(["eat shit @", data['name']],
            #                     data['sender_id'])

            # TODO: User target kets to filter for users that post
            # if int(data['sender_id']) == useful_users['fillup']:
            #    spiritBombKick(data)

            # Execute a command
            try:
                if data['text'][0] == '/':
                    ireturn = executeCommands(
                        data['text'], data['name'], int(data['sender_id']))
                    print("Executed %s" % ireturn)
            except:
                print("No command in message...")

            # Posts drake lyrics every time tony posts
            # data_attachments = {}
            for a in data['attachments']:
                data_attachments = a
                if data_attachments['type'] == 'mentions':
                    for u in data_attachments['user_ids']:
                        if int(u) == useful_users['rt']:
                            print("Executed <DRAKE MENTION>")
                            lyrics = random.choice(drizzy_lyrics)
                            fillbot.post(lyrics)
                            break
    print("PROGRAM EXECUTION ESTIMATE: %s secs" % (time.time() - start_time))
    return


print("Initializing...")
groupyClient = Client.from_token('shO3PJp9SVbIzi90xhMbIXspP1S9Ob9aPXq6k0LC')
# Dictionary of user id's to IRL names. Save for later use.
useful_users = {'fillup': 7430058, 'addison': 3359289, 'bebe': 6011409,
                'trey': 6606644, 'damn': 6616638, 'jeff': 963630,
                'seth': 9136487, 'rt': 6357297, 'kersten': 6606645,
                'nik': 6606860, 'tony': 4256997}
admins = {'jeff': 963630, 'seth': 9136487, 'kersten': 6606645, 'rt': 6357297}
print(useful_users, admins)

# Pass quotes, lyrics, etc. into lists via CSV reader.
# bad_and_boujee = getCSVData('bad_and_boujee.csv')
drizzy_lyrics = getCSVData('drizzy_lyrics.csv')
for l in drizzy_lyrics:
    print(l)

print(sys.version)
print("Starting setup @", datetime.datetime.now())
bot_group, users, targets = setup(groupyClient)
bots = groupyClient.bots.list()
for b in bots:
    print(b.name)

# temporarily disable for no interaction
# user_option = chooseTarget(len(bots))
# fillbot = bots[user_option]

fillbot = bots[0]
# fillbot.post("This is a test")
"""
sendMention(["I can do a lot of things... you just haven't figured them out ye"
             "t @", targets[0].nickname], targets[0].user_id)

while user_option != "quit":
    bot_text = input("Post something as bot: ")
    fillbot.post(bot_text)
"""

# user_option = input("Press 'y' to continue: ")

botParameters = createAndroid()

if targets != [None]:
    for t in targets:
        botParameters.user_post_count[t.user_id] = 0

print("End of setup...")
# Must be last! Starts the bottle server to listen for JSON POSTs.
run(host="0.0.0.0", port=5001, debug=True, reloader=True)
