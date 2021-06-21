import re

import emoji

IBM_WATSON_CRED_URL = "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/522fd06e-2cb7-4384-be62-89678168fac2"
IBM_WATSON_CRED_PASSWORD = "DbunDPsEH7oOVs5CxjacPTEWgRAWBHDPyLu_yLGtxWDC"
url = "https://acobot-brainshop-ai-v1.p.rapidapi.com/get"
import re

import aiohttp
from google_trans_new import google_translator
from pyrogram import filters

from DaisyX import BOT_ID
from DaisyX.helper_extra.aichat import add_chat, get_session, remove_chat
from DaisyX.pyrogramee.pluginshelper import admins_only, edit_or_reply
from DaisyX import pbot as Nezuko

translator = google_translator()
import requests


def extract_emojis(s):
    return "".join(c for c in s if c in emoji.UNICODE_EMOJI)


async def fetch(url):
    try:
        async with aiohttp.Timeout(10.0):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    try:
                        data = await resp.json()
                    except:
                        data = await resp.text()
            return data
    except:
        print("AI response Timeout")
        return


yone_chats = []
en_chats = []

@Nezuko.on_message(
    filters.command("chatbot") & ~filters.edited & ~filters.bot & ~filters.private
)
@admins_only
async def hmm(_, message):
    global yone_chats
    if len(message.command) != 2:
        await message.reply_text(
            "ι σηℓу яєcσgηιzє `/chatbot on` αη∂ `/chatbot off` σηℓу"
        )
        message.continue_propagation()
    status = message.text.split(None, 1)[1]
    chat_id = message.chat.id
    if status == "ON" or status == "on" or status == "On":
        lel = await edit_or_reply(message, "`ρяσcєѕѕιηg...`")
        lol = add_chat(int(message.chat.id))
        if not lol:
            await lel.edit("Akiro ᴀɪ αℓяєα∂у αcтιναтє∂ ιη тнιѕ cнαт")
            return
        await lel.edit(
            f"Akiro ᴀɪ ѕυccєѕѕƒυℓℓу α∂∂є∂ ƒσя υѕєяѕ ιη тнє cнαт  {message.chat.id}"
        )

    elif status == "OFF" or status == "off" or status == "Off":
        lel = await edit_or_reply(message, "`ρяσcєѕѕιηg...`")
        Escobar = remove_chat(int(message.chat.id))
        if not Escobar:
            await lel.edit("Akiro ᴀɪ ωαѕ ησт αcтιναтє∂ ιη тнιѕ cнαт")
            return
        await lel.edit(
            f"Akiro ᴀɪ ѕυccєѕѕƒυℓℓу ∂єαcтιναтє∂ ƒσя υѕєяѕ ιη тнє cнαт {message.chat.id}"
        )

    elif status == "EN" or status == "en" or status == "english":
        if not chat_id in en_chats:
            en_chats.append(chat_id)
            await message.reply_text("Eηgℓιѕн ᴀɪ cнαт єηαвℓє∂!")
            return
        await message.reply_text("ᴀɪ cнαт ιѕ αℓяєα∂у ∂ιѕαвℓє∂.")
        message.continue_propagation()
    else:
        await message.reply_text(
            "ι σηℓу яєcσgηιzє `/chatbot on` αη∂ `/chatbot off` σηℓу"
        )


@Nezuko.on_message(
    filters.text
    & filters.reply
    & ~filters.bot
    & ~filters.edited
    & ~filters.via_bot
    & ~filters.forwarded,
    group=2,
)
async def hmm(client, message):
    if not get_session(int(message.chat.id)):
        return
    if not message.reply_to_message:
        return
    try:
        senderr = message.reply_to_message.from_user.id
    except:
        return
    if senderr != BOT_ID:
        return
    msg = message.text
    chat_id = message.chat.id
    if msg.startswith("/") or msg.startswith("@"):
        message.continue_propagation()
    if chat_id in en_chats:
        test = msg
        test = test.replace("nezuko", "Aco")
        test = test.replace("nezuko", "Aco")
        URL = "https://api.affiliateplus.xyz/api/chatbot?message={test}&botname=@titan1v0_bot&ownername=@DARK_DEVIL_OP"

        try:
            r = requests.request("GET", url=URL)
        except:
            return

        try:
            result = r.json()
        except:
            return

        pro = result["message"]
        try:
            await Yone.send_chat_action(message.chat.id, "typing")
            await message.reply_text(pro)
        except CFError:
            return

    else:
        u = msg.split()
        emj = extract_emojis(msg)
        msg = msg.replace(emj, "")
        if (
            [(k) for k in u if k.startswith("@")]
            and [(k) for k in u if k.startswith("#")]
            and [(k) for k in u if k.startswith("/")]
            and re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []
        ):

            h = " ".join(filter(lambda x: x[0] != "@", u))
            km = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", h)
            tm = km.split()
            jm = " ".join(filter(lambda x: x[0] != "#", tm))
            hm = jm.split()
            rm = " ".join(filter(lambda x: x[0] != "/", hm))
        elif [(k) for k in u if k.startswith("@")]:

            rm = " ".join(filter(lambda x: x[0] != "@", u))
        elif [(k) for k in u if k.startswith("#")]:
            rm = " ".join(filter(lambda x: x[0] != "#", u))
        elif [(k) for k in u if k.startswith("/")]:
            rm = " ".join(filter(lambda x: x[0] != "/", u))
        elif re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []:
            rm = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", msg)
        else:
            rm = msg
            # print (rm)
        try:
            lan = translator.detect(rm)
        except:
            return
        test = rm
        if not "en" in lan and not lan == "":
            try:
                test = translator.translate(test, lang_tgt="en")
            except:
                return
        # test = emoji.demojize(test.strip())

        # Kang with the credits bitches @InukaASiTH
        test = test.replace("nezuko", "Aco")
        test = test.replace("nezuko", "Aco")
        URL = f"https://api.affiliateplus.xyz/api/chatbot?message={test}&botname=@titan1v0_bot&ownername=@DARK_DEVIL_OP"
        try:
            r = requests.request("GET", url=URL)
        except:
            return

        try:
            result = r.json()
        except:
            return
        pro = result["message"]
        if not "en" in lan and not lan == "":
            try:
                pro = translator.translate(pro, lang_tgt=lan[0])
            except:
                return
        try:
            await Nezuko.send_chat_action(message.chat.id, "typing")
            await message.reply_text(pro)
        except CFError:
            return


@Nezuko.on_message(
    filters.text & filters.private & ~filters.edited & filters.reply & ~filters.bot
)
async def inuka(client, message):
    msg = message.text
    if msg.startswith("/") or msg.startswith("@"):
        message.continue_propagation()
    u = msg.split()
    emj = extract_emojis(msg)
    msg = msg.replace(emj, "")
    if (
        [(k) for k in u if k.startswith("@")]
        and [(k) for k in u if k.startswith("#")]
        and [(k) for k in u if k.startswith("/")]
        and re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []
    ):

        h = " ".join(filter(lambda x: x[0] != "@", u))
        km = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", h)
        tm = km.split()
        jm = " ".join(filter(lambda x: x[0] != "#", tm))
        hm = jm.split()
        rm = " ".join(filter(lambda x: x[0] != "/", hm))
    elif [(k) for k in u if k.startswith("@")]:

        rm = " ".join(filter(lambda x: x[0] != "@", u))
    elif [(k) for k in u if k.startswith("#")]:
        rm = " ".join(filter(lambda x: x[0] != "#", u))
    elif [(k) for k in u if k.startswith("/")]:
        rm = " ".join(filter(lambda x: x[0] != "/", u))
    elif re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []:
        rm = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", msg)
    else:
        rm = msg
        # print (rm)
    try:
        lan = translator.detect(rm)
    except:
        return
    test = rm
    if not "en" in lan and not lan == "":
        try:
            test = translator.translate(test, lang_tgt="en")
        except:
            return

    # test = emoji.demojize(test.strip())

    # Kang with the credits bitches @InukaASiTH
    test = test.replace("nezuko", "Aco")
    test = test.replace("nezuko", "Aco")
    URL = f"https://api.affiliateplus.xyz/api/chatbot?message={test}&botname=@titan1v0_bot&ownername=@DARK_DEVIL_OP"
    try:
        r = requests.request("GET", url=URL)
    except:
        return

    try:
        result = r.json()
    except:
        return

    pro = result["message"]
    if not "en" in lan and not lan == "":
        pro = translator.translate(pro, lang_tgt=lan[0])
    try:
        await Nezuko.send_chat_action(message.chat.id, "typing")
        await message.reply_text(pro)
    except CFError:
        return


@Nezuko.on_message(
    filters.regex("nezuko|nezuko|Nezuko|Nezuko|Nezuko")
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.forwarded
    & ~filters.reply
    & ~filters.channel
    & ~filters.edited
)
async def inuka(client, message):
    msg = message.text
    if msg.startswith("/") or msg.startswith("@"):
        message.continue_propagation()
    u = msg.split()
    emj = extract_emojis(msg)
    msg = msg.replace(emj, "")
    if (
        [(k) for k in u if k.startswith("@")]
        and [(k) for k in u if k.startswith("#")]
        and [(k) for k in u if k.startswith("/")]
        and re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []
    ):

        h = " ".join(filter(lambda x: x[0] != "@", u))
        km = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", h)
        tm = km.split()
        jm = " ".join(filter(lambda x: x[0] != "#", tm))
        hm = jm.split()
        rm = " ".join(filter(lambda x: x[0] != "/", hm))
    elif [(k) for k in u if k.startswith("@")]:

        rm = " ".join(filter(lambda x: x[0] != "@", u))
    elif [(k) for k in u if k.startswith("#")]:
        rm = " ".join(filter(lambda x: x[0] != "#", u))
    elif [(k) for k in u if k.startswith("/")]:
        rm = " ".join(filter(lambda x: x[0] != "/", u))
    elif re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []:
        rm = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", msg)
    else:
        rm = msg
        # print (rm)
    try:
        lan = translator.detect(rm)
    except:
        return
    test = rm
    if not "en" in lan and not lan == "":
        try:
            test = translator.translate(test, lang_tgt="en")
        except:
            return

    # test = emoji.demojize(test.strip())

    # Kang with the credits bitches @InukaASiTH
    test = test.replace("nezuko", "Aco")
    test = test.replace("nezuko", "Aco")
    URL = f"https://api.affiliateplus.xyz/api/chatbot?message={test}&botname=@titan1v0_bot&ownername=@DARK_DEVIL_OP"
    try:
        r = requests.request("GET", url=URL)
    except:
        return

    try:
        result = r.json()
    except:
        return
    pro = result["message"]
    if not "en" in lan and not lan == "":
        try:
            pro = translator.translate(pro, lang_tgt=lan[0])
        except Exception:
            return
    try:
        await Nezuko.send_chat_action(message.chat.id, "typing")
        await message.reply_text(pro)
    except CFError:
        return


__help__ = """
**Cʜᴀᴛʙᴏᴛ**
Akiro AI 2.5 cαη ∂єтє¢т & яєρℓу υρтσ 200 ℓαηgυαgєѕ
 
 ✮ /chatbot `[ON|OFF]` *:* єηαвℓєѕ|∂ιѕαвℓєѕ ᴀɪ cнαт мσ∂є (EXCLUSIVE)
"""

__mod_name__ = "AI Cʜᴀᴛʙᴏᴛ🤖"
