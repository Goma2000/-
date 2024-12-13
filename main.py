import os
try:
    from telethon.sessions import StringSession
    import asyncio, re, json, shutil
    from kvsqlite.sync import Client as uu
    from telethon.tl.types import KeyboardButtonUrl
    from telethon.tl.types import KeyboardButton, ReplyInlineMarkup
    from telethon import TelegramClient, events, functions, types, Button
    from telethon.tl.types import DocumentAttributeFilename
    import time, datetime, random 
    from datetime import timedelta
    from telethon.errors import (
        ApiIdInvalidError,
        PhoneNumberInvalidError,
        PhoneCodeInvalidError,
        PhoneCodeExpiredError,
        SessionPasswordNeededError,
        PasswordHashInvalidError
    )
    from plugins.messages import *
    from plugins.get_gift import *
except:
    os.system("pip install telethon kvsqlite")
    try:
        from telethon.sessions import StringSession
        import asyncio, re, json, shutil
        from kvsqlite.sync import Client as uu
        from telethon.tl.types import KeyboardButtonUrl
        from telethon.tl.types import KeyboardButton
        from telethon import TelegramClient, events, functions, types, Button
        from telethon.tl.types import DocumentAttributeFilename
        import time, datetime, random 
        from datetime import timedelta
        from telethon.errors import (
            ApiIdInvalidError,
            PhoneNumberInvalidError,
            PhoneCodeInvalidError,
            PhoneCodeExpiredError,
            SessionPasswordNeededError,
            PasswordHashInvalidError
        )
        from plugins.messages import *
        from plugins.get_gift import *
    except Exception as errors:
        print('An Error with: ' + str(errors))
        exit(0)

if not os.path.isdir('database'):
    os.mkdir('database')

API_ID = "22256614"
API_HASH = "4f9f53e287de541cf0ed81e12a68fa3b"
admin = 746153603  # Added the admin ID as requested

# Replace with your bot token
token = "8038490917:AAEN1rnnEBtF5XLcg-dUBDYvFnhtzOavM1M"
client = TelegramClient('BotSession', API_ID, API_HASH).start(bot_token=token)
bot = client

# Create DataBase
db = uu('database/elhakem.ss', 'bot')

if not db.exists("accounts"):
    db.set("accounts", [])

if not db.exists("bad_guys"):
    db.set("bad_guys", [])

if not db.exists("force"):
    db.set("force", [])

@client.on(events.NewMessage(pattern="/start", func = lambda x: x.is_private))
async def start(event):
    print("Start command received")  # Log when /start is received
    user_id = event.chat_id
    bans = db.get('bad_guys') if db.exists('bad_guys') else []
    async with bot.conversation(event.chat_id) as x:
        buttons = [
            [
                Button.inline("اضافة حساب", data="add"),
                Button.inline("جلب الروابط", data="get_gift"),
            ],
            [
                Button.inline("الانضمام لقناة", data="join_channel"),
                Button.inline("مغادرة قناة", data="leave_channel"),
            ],
            [
                Button.inline("نسخة احتياطية", data="zip_all"),
                Button.inline("جلب جلسة", data="get_session"),
            ],
            [
                Button.inline("عدد حسابات البوت", data="get_accounts_count"),
            ],
            [
                Button.inline("تنظيف الحسابات", data="check"),
                Button.inline("مغادرة القنوات", data="leave_all"),
            ],
        ]
        print("Sending start message with buttons")  # Log before sending the message
        await event.reply("**- مرحبا بك في بوت جلب روابط المميز من حساباتك المسجلة 🔗**\n\n- اختر من الازرار ادناه ما تود فعله.", buttons=buttons)

@client.on(events.callbackquery.CallbackQuery())
async def start_lis(event):
    print("Callback query received")  # Log when a callback query is received
    data = event.data.decode('utf-8')
    user_id = event.chat_id
    if data == "back" or data == "cancel":
        buttons = [
            [
                Button.inline("اضافة حساب", data="add"),
                Button.inline("جلب الروابط", data="get_gift"),
            ],
            [
                Button.inline("الانضمام لقناة", data="join_channel"),
                Button.inline("مغادرة قناة", data="leave_channel"),
            ],
            [
                Button.inline("نسخة احتياطية", data="zip_all"),
                Button.inline("جلب جلسة", data="get_session"),
            ],
            [
                Button.inline("عدد حسابات البوت", data="get_accounts_count"),
            ],
            [
                Button.inline("تنظيف الحسابات", data="check"),
                Button.inline("مغادرة القنوات", data="leave_all"),
            ],
        ]
        await event.edit("**- مرحبا بك في بوت جلب روابط المميز من حساباتك المسجلة 🔗**\n\n- اختر من الازرار ادناه ما تود فعله.", buttons=buttons)

    # Add logging for the other callback actions
    print(f"Processing data: {data}")
    if data == "add":
        print("Add account action triggered")  # Log when the add account action is triggered
        async with bot.conversation(event.chat_id) as x:
            await x.send_message("✔️الان ارسل رقمك مع رمز دولتك , مثال :+201000000000")
            txt = await x.get_response()
            phone_number = txt.text.replace("+", "").replace(" ", "")
            app = TelegramClient(StringSession(), API_ID, API_HASH)
            await app.connect()
            password=None
            try:
                code = await app.send_code_request(phone_number)
            except (ApiIdInvalidError):
                await x.send_message("ʏᴏᴜʀ **ᴀᴩɪ_ɪᴅ** ᴀɴᴅ **ᴀᴩɪ_ʜᴀsʜ** ᴄᴏᴍʙɪɴᴀᴛɪᴏɴ ᴅᴏᴇsɴ'ᴛ ᴍᴀᴛᴄʜ ᴡɪᴛʜ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴩᴩs sʏsᴛᴇᴍ.")
                return
            except (PhoneNumberInvalidError):
                await x.send_message("ᴛʜᴇ **ᴩʜᴏɴᴇ_ɴᴜᴍʙᴇʀ** ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ᴅᴏᴇsɴ'ᴛ ʙᴇʟᴏɴɢ ᴛᴏ ᴀɴʏ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴄᴄᴏᴜɴᴛ.")
                return
            await x.send_message("- تم ارسال كود التحقق الخاص بك علي حسابك علي تليجرام.\n\n- ارسل الكود بالتنسيق التالي : 1 2 3 4 5")
            txt = await x.get_response()
            code = txt.text.replace(" ", "")
            try:
                await app.sign_in(phone_number, code, password=None)
                string_session = app.session.save()
                data = {"phone_number": phone_number, "two-step": "لا يوجد", "session": string_session}
                accounts = db.get("accounts")
                accounts.append(data)
                db.set("accounts", accounts)
                await x.send_message("- تم حفظ الحساب بنجاح ✅")
            except (PhoneCodeInvalidError):
                await x.send_message("ᴛʜᴇ ᴏᴛᴩ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs **ᴡʀᴏɴɢ.**")
                return
            except (PhoneCodeExpiredError):
                await x.send_message("ᴛʜᴇ ᴏᴛᴩ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs **ᴇxᴩɪʀᴇᴅ.**")
                return
            except (SessionPasswordNeededError):
                await x.send_message("- ارسل رمز التحقق بخطوتين الخاص بحسابك")
                txt = await x.get_response()
                password = txt.text
                try:
                    await app.sign_in(password=password)
                except (PasswordHashInvalidError):
                    await x.send_message("ᴛʜᴇ ᴩᴀssᴡᴏʀᴅ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs ᴡʀᴏɴɢ.")
                    return
                string_session = app.session.save()
                data = {"phone_number": phone_number, "two-step": password, "session": string_session}
                accounts = db.get("accounts")
                accounts.append(data)
                db.set("accounts", accounts)
                await x.send_message("- تم حفظ الحساب بنجاح ✅")

# Add the logging for other callback queries as needed...
client.run_until_disconnected()