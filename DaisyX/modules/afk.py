import random, html

from DaisyX import dispatcher
from DaisyX.modules.disable import (
    DisableAbleCommandHandler,
    DisableAbleMessageHandler,
)
from DaisyX.modules.sql import afk_sql as sql
from DaisyX.modules.users import get_user_id
from telegram import MessageEntity, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, Filters, MessageHandler, run_async

AFK_VID = "https://telegra.ph/file/47d3aca81e02ff5c07a97.mp4"
USER_BACK = "https://telegra.ph/file/ba032f0f461723ee24dde.mp4"
AFK_REASON_VID = "https://telegra.ph/file/d56d712ced752433fdde0.mp4"
AFK_GROUP = 7
AFK_REPLY_GROUP = 8


@run_async
def afk(update: Update, context: CallbackContext):
    args = update.effective_message.text.split(None, 1)
    user = update.effective_user

    if not user:  # ignore channels
        return

    if user.id in [777000, 1087968824]:
        return

    notice = ""
    if len(args) >= 2:
        reason = args[1]
        if len(reason) > 100:
            reason = reason[:100]
            notice = "\nYour afk reason was shortened to 100 characters."
    else:
        reason = ""

    sql.set_afk(update.effective_user.id, reason)
    fname = update.effective_user.first_name
    try:
        afk = [
                "{} is now AFK!",
                "bye bye, {}!",
                "{} is now away!",
        ]
        chosen_msg = random.choice(afk)
        update.effective_message.reply_animation(AFK_VID, caption=chosen_msg.format(fname))
    except BadRequest:
        pass


@run_async
def no_longer_afk(update: Update, context: CallbackContext):
    user = update.effective_user
    message = update.effective_message

    if not user:  # ignore channels
        return

    res = sql.rm_afk(user.id)
    if res:
        if message.new_chat_members:  # dont say msg
            return
        firstname = update.effective_user.first_name
        try:
            options = [
                "{} is back!",
                "welcome back {}!",
                "Yo, {} is here!",
                "{} is online!",
                "{} is finally here!",
                "Welcome back! {}",
            ]
            chosen_option = random.choice(options)
            update.effective_message.reply_animation(USER_BACK, caption=chosen_option.format(firstname))
        except:
            return


@run_async
def reply_afk(update: Update, context: CallbackContext):
    bot = context.bot
    message = update.effective_message
    userc = update.effective_user
    userc_id = userc.id
    if message.entities and message.parse_entities(
        [MessageEntity.TEXT_MENTION, MessageEntity.MENTION]
    ):
        entities = message.parse_entities(
            [MessageEntity.TEXT_MENTION, MessageEntity.MENTION]
        )

        chk_users = []
        for ent in entities:
            if ent.type == MessageEntity.TEXT_MENTION:
                user_id = ent.user.id
                fst_name = ent.user.first_name

                if user_id in chk_users:
                    return
                chk_users.append(user_id)

            if ent.type != MessageEntity.MENTION:
                return

            user_id = get_user_id(message.text[ent.offset : ent.offset + ent.length])
            if not user_id:
                # Should never happen, since for a user to become AFK they must have spoken. Maybe changed username?
                return

            if user_id in chk_users:
                return
            chk_users.append(user_id)

            try:
                chat = bot.get_chat(user_id)
            except BadRequest:
                print("Error: Could not fetch userid {} for AFK module".format(user_id))
                return
            fst_name = chat.first_name

            check_afk(update, context, user_id, fst_name, userc_id)

    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        fst_name = message.reply_to_message.from_user.first_name
        check_afk(update, context, user_id, fst_name, userc_id)


def check_afk(update, context, user_id, fst_name, userc_id):
    if sql.is_afk(user_id):
        user = sql.check_afk_status(user_id)
        if int(userc_id) == int(user_id):
            return
        if not user.reason:
            res = "{} is afk".format(fst_name)
            update.effective_message.reply_animation(AFK_REASON_VID, caption=html.escape(user.reason))
        else:
            res = "{} is afk.\nReason: <code>{}</code>".format(
                html.escape(fst_name), html.escape(user.reason)
            )
            update.effective_message.reply_animation(AFK_REASON_VID, caption=html.escape(user.reason))



AFK_HANDLER = DisableAbleCommandHandler("afk", afk)
AFK_REGEX_HANDLER = DisableAbleMessageHandler(
    Filters.regex(r"^(?i)brb(.*)$"), afk, friendly="afk"
)
NO_AFK_HANDLER = MessageHandler(Filters.all & Filters.group, no_longer_afk)
AFK_REPLY_HANDLER = MessageHandler(Filters.all & Filters.group, reply_afk)

dispatcher.add_handler(AFK_HANDLER, AFK_GROUP)
dispatcher.add_handler(AFK_REGEX_HANDLER, AFK_GROUP)
dispatcher.add_handler(NO_AFK_HANDLER, AFK_GROUP)
dispatcher.add_handler(AFK_REPLY_HANDLER, AFK_REPLY_GROUP)

__mod_name__ = "AFK🏃"
__command_list__ = ["afk"]
__handlers__ = [
    (AFK_HANDLER, AFK_GROUP),
    (AFK_REGEX_HANDLER, AFK_GROUP),
    (NO_AFK_HANDLER, AFK_GROUP),
    (AFK_REPLY_HANDLER, AFK_REPLY_GROUP),
]
