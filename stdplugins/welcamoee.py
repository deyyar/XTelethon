"""Greetings

Commands:

.clearwelcome

.savewelcome <Welcome Message>"""

from telethon import events, utils

from telethon.tl import types

from os.path import join, dirname, realpath

from uniborg.util import admin_cmd

import json

WD = dirname(realpath(__file__))

config = {}

def get_config():

    global config

    file = open(join(WD, "config.json"), "r")

    config = json.loads(file.read())

    file.close()

def save_config():

    file = open(join(WD, "config.json"), "w")

    file.write(json.dumps(config))

    file.close()

@borg.on(events.ChatAction())  # pylint:disable=E0602

async def _(event):

    if event.user_joined or event.user_added:

        get_config()

        global config

        chat = await event.get_chat()

        if event.user_joined:

            if "welcome" not in config:

                config["welcome"] = {}

                config["welcome"]["title"] = ""

                config["welcome"]["id"] = ""

                save_config()

            if "id" not in config["welcome"]:

                config["welcome"]["id"] = ""

            if config["welcome"]["id"] == "":

                if config["welcome"]["title"] != "":

                    await event.client.send_message(

                        chat,

                        config["welcome"]["title"],

                        reply_to=event.action_message.id,

                    )

            else:

                caption = config["welcome"]["title"]

                await event.client.send_file(

                    chat,

                    config["welcome"]["id"],

                    caption=caption if caption != "" else None,

                    reply_to=event.action_message.id,

                )

@borg.on(admin_cmd(pattern="savewelcome"))

async def _(event):

    if event.fwd_from:

        return

    global config

    if "welcome" not in config:

        config["welcome"] = {}

    if "title" not in config["welcome"]:

        config["welcome"]["title"] = ""

    if "id" not in config["welcome"]:

        config["welcome"]["id"] = ""

    if event.reply_to_msg_id != None:

        message_id = 0

        chat = event.chat_id

        msg = await event.client.get_messages(chat, ids=event.reply_to_msg_id)

        if msg.text:

            config["welcome"]["title"] = msg.text

        if msg.voice:

            config["welcome"]["id"] = utils.pack_bot_file_id(msg.voice)

        if msg.photo:

            config["welcome"]["id"] = utils.pack_bot_file_id(msg.photo)

        if msg.audio:

            config["welcome"]["id"] = utils.pack_bot_file_id(msg.audio)

        if msg.sticker:

            config["welcome"]["id"] = utils.pack_bot_file_id(msg.sticker)

        if msg.file:

            config["welcome"]["id"] = utils.pack_bot_file_id(msg.file)

        if msg.video:

            config["welcome"]["id"] = utils.pack_bot_file_id(msg.video)

        await event.client.send_message(chat, "done")

    save_config()

@borg.on(admin_cmd(pattern="clearwelcome"))

async def _(event):

    if event.fwd_from:

        return

    global config

    if "welcome" not in config:

        config["welcome"] = {}

    config["welcome"]["title"] = ""

    config["welcome"]["id"] = ""

    save_config()

    chat = event.chat_id

    await event.client.send_message(chat, "done")

