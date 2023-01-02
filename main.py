'''
   _____          __                       .__  .__              ________
  /  _  \   _____/  |_  ____   ____   ____ |  | |  |   ____      \______ \
 /  /_\  \ /    \   __\/  _ \ /    \_/ __ \|  | |  |  /  _ \      |    |  \
/    |    \   |  \  | (  <_> )   |  \  ___/|  |_|  |_(  <_> )     |    `   \
\____|__  /___|  /__|  \____/|___|  /\___  >____/____/\____/     /_______  / /\
        \/     \/                 \/     \/                              \/  \/
   ______  __  __                                          __  __
  / ____ \/ / / ________  _________  ____ _____ ___  ___  / / / ________  _________ ___  ____  _________
 / / __ `/ / / / ___/ _ \/ ___/ __ \/ __ `/ __ `__ \/ _ \/ / / / ___/ _ \/ ___/ __ `__ \/ __ \/ ___/ __ \
/ / /_/ / /_/ (__  /  __/ /  / / / / /_/ / / / / / /  __/ /_/ (__  /  __/ /  / / / / / / /_/ (__  / /_/ /
\ \__,_/\____/____/\___/_/  /_/ /_/\__,_/_/ /_/ /_/\___/\____/____/\___/_/  /_/ /_/ /_/\____/____/\____/
 \____/
                ___________    .__
  ____   ____   \__    ___/___ |  |   ____   ________________    _____
 /  _ \ /    \    |    |_/ __ \|  | _/ __ \ / ___\_  __ \__  \  /     \
(  <_> )   |  \   |    |\  ___/|  |_\  ___// /_/  >  | \// __ \|  Y Y  \
 \____/|___|  /   |____| \___  >____/\___  >___  /|__|  (____  /__|_|  /
            \/               \/          \/_____/            \/      \/
'''


'''
Attention!
This code is only to blacklist toxic people from ur group/groups.
If u need help, dm me on telegram and i will help u.
'''

from pyrogram import Client, filters, types, idle
from pyrogram.types import (InlineQueryResultArticle, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton)
import asyncio
import sqlite3
import contextlib
import time

'''
How to get api_id and api_hash?
0. Sign up for Telegram using any application.
1. Log in to your Telegram core: https://my.telegram.org.
2. Go to 'API development tools' and fill out the form.
3. You will get basic addresses as well as the api_id and api_hash parameters required for user authorization.
4. For the moment each number can only have one api_id connected to it.
'''
api_id = 10475996 # put your api_id
api_hash = "59e438d2b2ba12ab84b9c2ae57d624c9" # put your api_hash
api_key = "5895491685:AAFscZD_9TE_argrHidkWb4h109c9S2F6vw" # paste your bot token given from @BotFather

with Client("my_account", api_id, api_hash, api_key) as app:
    pass

# this variable is needed to execute the commands: /block and /unblock
owner = [5913258033] # put your account telegram id here. (i added already you 

@app.on_message(filters.command("start"))
async def start(_:app, message: types.Message):
    if message.chat.type == 'group':
        await app.send_message("🤖 | Используйте эту команду в ЛС бота")
    elif message.chat.type == 'supergoup':
        await app.send_message("🤖 | Используйте эту команду в ЛС бота")
    else:
        await send_message(
        chat_id=message.chat.id,
         text=f"""<b>👋 | Добро пожаловать!
🤖 | Я бот, который ведёт базу скам пользователей.
🆘 | Подробнее - /help.</b>""",
            reply_markup=InlineKeyboardMarkup(
                 [
                    [
                         InlineKeyboardButton('📃 | пользовательское соглашение', url='https://noziss.ru/bot')
                     ], [
                     InlineKeyboardButton('👑 | Создатель', url='https://t.me/NoZiss')
                ], [
                    InlineKeyboardButton('➕ | Добавь в чат', url='https://t.me/StopScamBLBot?startgroup=new'),
                ]]
             ),)

@app.on_message(filters.command("database"))
async def database(_:app, message: types.Message):
    if message.from_user.id in owner:
        await app.send_document(chat_id=5913258033, document="blacklist.db", caption="Привет, NoZiss. \n \n 🗒️ | Ваша бд готова")
    else:
        await message.reply("Прости,но ты не админ")

@app.on_message(filters.command("help"))
async def help(_:app, message: types.Message):
        await app.send_message(
               chat_id=message.chat.id,
               text="""<b>Помощь по Stop-Scam!

🤖 |  Я веду базу пользователей, которые индентифицируются как опасные.

➕ | Добавь меня в чат, и я буду предупреждать, если напишет скамер

📃 | Благодаря нашему боту, вы можете быть уверены, что участники вашего чата не будут обмануты!

~ @StopScamBLBot</b>""",
        reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "🔙  | назад", callback_data="start"),
                                    ]]
                            ),)

# when a user join in the group, the bot examine if a user is on the database, if yes, the user will be banned.
@app.on_message(filters.new_chat_members & filters.group)
async def blacklist(client, message):
    # opening database (if u don't have created the database yet, u need to create one. (table name: "users", column name: "id", type: "TEXT".)
    database = sqlite3.connect("blacklist.db")

    # define cursor to edit the database
    c = database.cursor()

    # check if the user is on the database's blacklist.
    exists = c.execute(f"select id from users where id='{message.from_user.id}'").fetchone()
    if exists:
        #await app.kick_chat_member(message.chat.id, message.from_user.id)
        await message.reply(
            f"<b>{message.from_user.first_name}</b> находится в черном списке, потому что он определен как опасный.")

    # save database's edit
    database.commit()
    # close the database
    database.close()

#command to add a user in blacklist (/block @username)
@app.on_message(filters.command("block"))
async def block_command(client, message):
    #if message.from_user.id in owner:
    database = sqlite3.connect("blacklist.db")
    c = database.cursor()
    isadmin = c.execute(f"select id from admins where id='{message.from_user.id}'").fetchone()
    if isadmin or message.from_user.id in owner:
        target = await app.get_users(message.command[1])

        exists = c.execute(f"select id from users where id='{target.id}'").fetchone()
        if exists:
            await message.reply(f"{target.first_name} уже в черном списке.")
        else:
            # remove this comment if u want use SimpleBlacklist on single group   app.kick_chat_member(message.chat.id, message.command[1], int(time.time() + 604800)) # ban target for 1 week from group
            c.execute(f"INSERT INTO users VALUES ('{target.id}')")
            database.commit()
            await message.reply(f"{target.first_name} успешно добавлен в черный список.")
            database.close()


# command to remove a user from blacklist (/unblock @username)
@app.on_message(filters.command("unblock"))
async def unblock_command(client, message):
        database = sqlite3.connect("blacklist.db")
        c = database.cursor()
        isadmin = c.execute(f"select id from admins where id='{message.from_user.id}'").fetchone()
        if isadmin or message.from_user.id in owner:
            target = await app.get_users(message.command[1])

            exists = c.execute(f"select id from users where id='{target.id}'").fetchone()
            if exists:
                c.execute(f"DELETE FROM users WHERE id = '{target.id}'") # remove the old blacklisted person from database.
                # remove this comment if u want use SimpleBlacklist in a single group app.unban_chat_member(message.chat.id, target.id) # unban the user from group
                await message.reply(f"{target.first_name} успешно удален из черного списка.")
                database.commit()
                database.close()
            else:
                await message.reply(f"{target.first_name} не существует в черном списке базы данных.")



@app.on_message(filters.command("setadmin"))
async def setadmin_command(client, message):
    db = sqlite3.connect("blacklist.db")
    c = db.cursor()
    admin = c.execute(f"select id from admins where id='{message.from_user.id}'").fetchone()
    if admin:
        target = await app.get_users(message.command[1])
        isadmin = c.execute(f"select id from admins where id='{target.id}'").fetchone()
        if isadmin:
            await message.reply("Этот пользователь уже является администратором бота.")
        else:
            c.execute(f"insert into admins values('{target.id}')"); db.commit()
            await message.reply(f"Успешно добавил {target.first_name} в администрацию бота.\n\nЧто бы убрать, используй /unsetadmin @username/ID")
    db.close()


@app.on_message(filters.command("unsetadmin"))
async def unsetadmin_command(client, message):
    db = sqlite3.connect("blacklist.db")
    c = db.cursor()
    admin = c.execute(f"select id from admins where id='{message.from_user.id}'").fetchone()
    if admin:
        target = await app.get_users(message.command[1])
        if target.id in owner:
            await message.reply("Вы не можете удалить из админов владельца.")
            db.close()
            return;
        isadmin = c.execute(f"select id from admins where id='{target.id}'").fetchone()
        if isadmin:
            c.execute(f"DELETE FROM admins where id='{target.id}'"); db.commit()
            await message.reply(f" {target.id} успешно удален из администрации.\n\n Что бы добавить его, используйте /setadmin @username/ID")
        else:
            await message.reply(f"{target.first_name} isn't admin.")
    db.close()


@app.on_message(filters.command("ping"))
async def ping(_, message):
    start_time = time.time()
    pong = await message.reply_text("Подождите...")
    end_time = time.time()
    ping = round((end_time - start_time) * 1000, 3)
    await pong.edit_text(
        f"<b>⌛Ping:</b> <code>{ping}ms</code>")

@app.on_callback_query()
async def button(bot, update):
      cb_data = update.data
      if "start" in cb_data:
        await update.message.delete()
        await start(bot, update.message)


@app.on_message(filters.text)
async def check_messages(client, message):
    db = sqlite3.connect("blacklist.db"); c = db.cursor()
    isblacklisted = c.execute(f"select id from users where id='{message.from_user.id}'").fetchone()
    if isblacklisted: await message.reply(f"⚠️ {message.from_user.mention} человек из черного списка. \n \n ❗ Не совершайте с этим пользователем никаких слелок, не переводите деньги просто так!")
    db.close()

# run bot
app.run()
