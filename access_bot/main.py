from operator import truediv
from random import shuffle
from unittest import case
from requests import session
from soupsieve import match
import telebot
from pymongo import MongoClient
from PIL import Image
from io import BytesIO
from bson.objectid import ObjectId
from keyboa import Keyboa
import hashlib

tb = telebot.TeleBot('5741190584:AAGb78QKF2izX89S4Nz4aPJ1RD-m2vN4Urs')
client = MongoClient()
db = client.asses
users = db['users']
capy = db['capybaras_row']
sessions = db['sessions']

numbers = [
  [{"text": "1", "callback_data": "0", "isChecked":False}, {"text": "2", "callback_data": "1", "isChecked":False}, {"text": "3", "callback_data": "2", "isChecked":False}],
  [{"text": "4", "callback_data": "3", "isChecked":False}, {"text": "5", "callback_data": "4", "isChecked":False}, {"text": "6", "callback_data": "5", "isChecked":False}],
  [{"text": "7", "callback_data": "6", "isChecked":False}, {"text": "8", "callback_data": "7", "isChecked":False}, {"text": "9", "callback_data": "8", "isChecked":False}],
  {"text": "Выбрать все", "callback_data": "10", "isChecked":False},
  {"text": "Готово", "callback_data": "9", "isChecked":False}
]

def update_keyboard(keyboard):
    for row in keyboard:
        if (isinstance(row, dict)):
            row["text"] = row["text"].replace("✅", "")
            if (row["isChecked"] == True):
                row["text"] = "✅" + row["text"]
        else:
            for button in row:
                button["text"] = button["text"].replace("✅", "")
                if (button["isChecked"] == True):
                    button["text"] = "✅" + button["text"]
    return (keyboard)

def change_button(keyboard, button):
    if button == "9":
        keyboard[3]["isChecked"] = not keyboard[3]["isChecked"]
    if button == "0":
        keyboard[0][0]["isChecked"] = not keyboard[0][0]["isChecked"]
    if button == "1":
        keyboard[0][1]["isChecked"] = not keyboard[0][1]["isChecked"]
    if button == "2":
        keyboard[0][2]["isChecked"] = not keyboard[0][2]["isChecked"]
    if button == "3":
        keyboard[1][0]["isChecked"] = not keyboard[1][0]["isChecked"]
    if button == "4":
        keyboard[1][1]["isChecked"] = not keyboard[1][1]["isChecked"]
    if button == "5":
        keyboard[1][2]["isChecked"] = not keyboard[1][2]["isChecked"]
    if button == "6":
        keyboard[2][0]["isChecked"] = not keyboard[2][0]["isChecked"]
    if button == "7":
        keyboard[2][1]["isChecked"] = not keyboard[2][1]["isChecked"]
    if button == "8":
        keyboard[2][2]["isChecked"] = not keyboard[2][2]["isChecked"]
    return keyboard

def get_checked_ids(keyboard):
    ids = []
    id = 0
    for i in range(3):
        for j in range(3):
            if (keyboard[i][j]["isChecked"] == True):
                ids.append(id)
            id += 1
    return ids

def check_all(keyboard):
    for i in range(3):
        for j in range(3):
            keyboard[i][j]["isChecked"] = True
    return keyboard

keyboard = Keyboa(items=numbers)

@tb.message_handler(commands=['start', 'go'])
def start_handler(message):
    msg = tb.send_message(message.chat.id, "Привет, отправь логин и пароль")
    tb.register_next_step_handler(msg, auth)


@tb.message_handler(commands=['image'])
def image_handler(message):
    if(isAuth(message) != True):
        return
    image_pack, ids, label = get_image_pack()
    tb.send_media_group(message.chat.id, image_pack)
    session = get_session(message)
    newValue = { "$set": { 'keyboard':  numbers, 'ids': ids} }
    
    filter = {"_id": ObjectId(session["_id"])}
    sessions.update_one(filter, newValue)
    tb.send_message(chat_id=message.chat.id, reply_markup=keyboard(), text="Выберите все изображения относящиеся к класу '{}'".format(label))


@tb.message_handler(commands=['exit'])
def exit(message):
    if(isAuth(message) == False):
        return
    newValue = { "$set": { 'isAuth': False } }
    id = hashlib.shake_128(repr(message.chat.id).encode()).hexdigest(12)
    filter = {"_id": ObjectId(id)}
    sessions.update_one(filter, newValue)
    msg = tb.send_message(message.chat.id, "Успешно")
    



@tb.callback_query_handler(func=lambda call: True)
def answerHandler(call: telebot.types.CallbackQuery):
    session = get_session(call.message)
    if(call.data == "9"):
        doneHandler(session, call)
        return
    if(call.data == "10"):
        keys = update_keyboard(check_all(session["keyboard"]))
    else:
        keys = update_keyboard(change_button(session["keyboard"], call.data))
    newValue = { "$set": { 'keyboard':  keys} }
    filter = {"_id": ObjectId(session["_id"])}
    sessions.update_one(filter, newValue)
    keys = Keyboa(keys)
    # text = call.message.text
    # tb.delete_message(call.message.chat.id, call.message.id)
    tb.edit_message_reply_markup(chat_id = call.message.chat.id, message_id= call.message.id, inline_message_id= call.inline_message_id, reply_markup = keys())
# def number_handler(message):
def doneHandler(session, call):
    ids = get_checked_ids(session["keyboard"])
    filter = {"_id": ObjectId(session["_id"])}
    for index, id in enumerate(session["ids"]):
        filter = {"_id": ObjectId(id)}
        newValue = { "$inc": { 'send_count':  1} }
        if index in ids:
            newValue["$inc"]["append"] = 1
        else:
            newValue["$inc"]["declined"] = 1
        capy.update_one(filter, newValue)
    tb.edit_message_reply_markup(chat_id = call.message.chat.id, message_id= call.message.id, inline_message_id= call.inline_message_id, reply_markup = None)
    tb.send_message(call.message.chat.id, "Ваше мнение обязательно будет учтено")
    image_handler(call.message)
    
    

def isAuth(message):
    session = get_session(message)
    if(session):
        if session["isAuth"] == True:
            return True
    msg = tb.send_message(message.chat.id, "Вы не авторизованы")
    #tb.register_next_step_handler(msg, start_handler)
    return False

# def end_handler(message):
def get_session(message):
    id = hashlib.shake_128(repr(message.chat.id).encode()).hexdigest(12)
    session = sessions.find_one({"_id": ObjectId(id)})
    return session
    

def get_image_pack():
    image = capy.aggregate([{ "$sample": { "size": 1 }}])
    label = image.next()["label"]
    images = capy.aggregate([{"$match": {'label': label}}, { "$sample": { "size": 9 }}])
    image_pack = []
    ids = []
    for image in images:
        bimg = Image.open(BytesIO(image['image']))
        bimg = bimg.resize([150,150])
        bimg = telebot.types.InputMediaPhoto(bimg)
        ids.append(image["_id"])
        image_pack.append(bimg)
    return [image_pack, ids, label]


def auth(message):
    data = message.text.split() 
    if (len(data) != 2):
        tb.send_message(message.chat.id, r'Неправильно введен логин\пароль')
        tb.register_next_step_handler(message, auth)
        return

    check = users.find_one({ 
        'username': str(data[0]),
        'password': str(data[1]),
    })
    if check is None:
        tb.send_message(message.chat.id, r'Неправильно введен логин\пароль')
        tb.register_next_step_handler(message, auth)


    else: 
        id = hashlib.shake_128(repr(message.chat.id).encode()).hexdigest(12)
        ses = get_session(message)
        if ses is None:
            sessions.insert_one({"_id": ObjectId(id), "isAuth": True})
        else:
            newValue = { "$set": { 'isAuth': True } }
            filter = {"_id": ObjectId(id)}
            sessions.update_one(filter, newValue)
        msg = tb.send_message(message.chat.id, 'Успешно')
        image_handler(message)

tb.polling(none_stop=True, interval=0)