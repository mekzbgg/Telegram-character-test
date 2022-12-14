from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import  ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import json
import time
import os


async def json_sorgulama(id):
    try:
        file_json = "jsonFile/data.json"
        jsonFile = open(file_json, "r", encoding="utf-8")
        data = json.load(jsonFile)
        jsonFile.close()
        for user in data:
            if user["user_id"] == id:
                return user["user_language"]
    except:
        pass
    
    return False

async def json_guncelleme_secenekler(id, secenek):
    try:
        file_json = "jsonFile/data.json"
        jsonFile = open(file_json, "r", encoding="utf-8")
        data = json.load(jsonFile)
        jsonFile.close()
        for user in data:
            if user["user_id"] == id:
                user[secenek] += 1
                with open(file_json, mode='w', encoding="utf-8") as f:
                    f.write(json.dumps(data, indent=2,ensure_ascii=False))
                return True
    except:
        pass

async def json_sifirlama(id):
    try:
        file_json = "jsonFile/data.json"
        jsonFile = open(file_json, "r", encoding="utf-8")
        data = json.load(jsonFile)
        jsonFile.close()
    except:
        data = []
        
    for user in data:
        if user["user_id"] == id:
            for harf in ["A","B","C","D","E","F","G","A1","B2","C3"]:
                user[harf] = 0
            
            user["sorular"] = []

            with open(file_json, mode='w', encoding="utf-8") as f:
                f.write(json.dumps(data, indent=2,ensure_ascii=False))
            
            break

async def json_guncelleme_sorular(id, a, start):
    file_json = "jsonFile/data.json"
    jsonFile = open(file_json, "r", encoding="utf-8")
    data = json.load(jsonFile)
    jsonFile.close()
    for user in data:
        if user["user_id"] == id:
            if start == True:
                user["sorular"] = [a]
                for harf in ["A","B","C","D","E","F","G","A1","B2","C3"]:
                    user[harf] = 0
                with open(file_json, mode='w', encoding="utf-8") as f:
                    f.write(json.dumps(data, indent=2,ensure_ascii=False))
                return True
                
            sorular = user["sorular"]
            if len(sorular) == 28:
                harf_1_str = ""
                harf_1 = 0
                harf_2_str = ""
                harf_2 = 0
                for harf in ["A","B","C","D","E","F","G"]:
                    if harf_1 < user[harf]:
                        harf_1_str = harf
                        harf_1 = user[harf]
                
                for harf in ["A","B","C","D","E","F","G"]:
                    if harf_2 < user[harf] and harf_1 > user[harf]:
                        harf_2_str = harf
                        harf_2 = user[harf]
                islem = [harf_1_str, harf_2_str, user["A1"], user["B2"], user["C3"]]
                return islem
            if a in sorular:
                return False
            else:
                sorular.append(a)

                with open(file_json, mode='w', encoding="utf-8") as f:
                    f.write(json.dumps(data, indent=2,ensure_ascii=False))
                return True

async def json_sorgu(call):
    status = False
    file_json = "jsonFile/data.json"
    try:
        jsonFile = open(file_json, "r", encoding="utf-8")
        data = json.load(jsonFile)
        jsonFile.close()
        a = 0
        for user in data:
            if user["user_id"] == call["from"]["id"]:
                status = True
                break
            a += 1
    except:
        pass

    if status == True:
        data[a]["user_language"] = call.data
        with open(file_json, mode='w', encoding="utf-8") as f:
            f.write(json.dumps(data, indent=2,ensure_ascii=False))
    if status == False:
        information = {
            "user_id": call["from"]["id"],
            "user_language": call.data,
            "A": 0,
            "B": 0,
            "C": 0,
            "D": 0,
            "E": 0,
            "F": 0,
            "G": 0,
            "A1": 0,
            "B2": 0,
            "C3": 0,
            "sorular": [],
        }

        a = []
        if not os.path.isfile(file_json):
            a.append(information)
            with open(file_json, mode='w', encoding="utf-8") as f:
                f.write(json.dumps(a, indent=2,ensure_ascii=False))
        else:
            with open(file_json, encoding="utf-8") as feedsjson:
                feeds = json.load(feedsjson)

            feeds.append(information)
            with open(file_json, mode='w', encoding="utf-8") as f:
                f.write(json.dumps(feeds, indent=2,ensure_ascii=False))

async def makeKeyboard(language, i):
    if language == "tr":
        secilen_dil_sorulari = json.load(open('jsonFile/tr/tr-sorular.json', "r", encoding="utf-8"))

    if language == "en":
        secilen_dil_sorulari = json.load(open('jsonFile/en/en-sorular.json', "r", encoding="utf-8"))

    if language == "ch":
        secilen_dil_sorulari = json.load(open('jsonFile/ch/ch-sorular.json', "r", encoding="utf-8"))

    if language == "ru":
        secilen_dil_sorulari = json.load(open('jsonFile/ru/ru-sorular.json', "r", encoding="utf-8"))

    markup = types.InlineKeyboardMarkup()
    question = secilen_dil_sorulari[f"Soru{str(i)}"]["soru"]
    for key,value in secilen_dil_sorulari[f"Soru{str(i)}"]["Cevaplar"].items():
        markup.add(types.InlineKeyboardButton(text=value,callback_data=key.strip()))
    return markup,question
    
bot = Bot(token="5751844075:AAHeSQGQiOym1aqAUA7jSQrSGBqIEuChprA")
dp = Dispatcher(bot)

# Butonlar (Dil se??enekleri)
yiffo_tr = InlineKeyboardButton("???????? T??rk??e ????????", callback_data="tr")
yiffo_en = InlineKeyboardButton("???????? English ????????",callback_data="en")
yiffo_ru = InlineKeyboardButton("???????? ?????????????? ????????",callback_data="ru")
yiffo_ch = InlineKeyboardButton("???????? ????????? ????????",callback_data="ch")
keyboard_diller = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(yiffo_tr,yiffo_en).add(yiffo_ch,yiffo_ru)

#Sosyal Medya Butonlar??
yiffo_insta = InlineKeyboardButton(text="Instagram", url="https://www.instagram.com/yiffoo/")
yiffo_youtube = InlineKeyboardButton(text="Youtube", url="https://www.youtube.com/c/yiffo/videos")
yiffo_opensea = InlineKeyboardButton(text="Opensea", url="https://opensea.io/collection/jokkalari-collection")
keyboard_sosyal_media = InlineKeyboardMarkup().add(yiffo_insta, yiffo_youtube, yiffo_opensea)

# Dil se??ildikten sonra komut butonlar??
yiffo_testTR = InlineKeyboardButton(text="Yiffo Ki??ilik Test",url="http://t.me/yiffosbot")
yiffo_testEN = InlineKeyboardButton(text="Yiffo Personality Test",url="http://t.me/yiffosbot")
yiffo_testCH = InlineKeyboardButton(text="??????????????????",url="http://t.me/yiffosbot")
yiffo_testRU = InlineKeyboardButton(text="???????? ???????????????? ??????????",url="http://t.me/yiffosbot")
keyboard_inlinekomutlarTR = InlineKeyboardMarkup().add(yiffo_testTR)
keyboard_inlinekomutlarEN = InlineKeyboardMarkup().add(yiffo_testEN)
keyboard_inlinekomutlarRU = InlineKeyboardMarkup().add(yiffo_testCH)
keyboard_inlinekomutlarCH = InlineKeyboardMarkup().add(yiffo_testRU)

# YEN?? GELEN K??????Y?? KAR??ILAMA
@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS])
async def user_joined_chat(message: types.Message):
    print("buraya giriyor")
    first_name = message.new_chat_members[0]["first_name"]
    id = message.chat.id
    await bot.send_message(chat_id=id, text="Welcome please select language " + first_name,
                           reply_markup=keyboard_diller)

# Dil se??imi yap??l??rken
@dp.callback_query_handler(text=["tr","en","ch","ru"])
async def yiffo_test_go(call: types.CallbackQuery):

    await json_sorgu(call)
    if call.data == "tr":
        await call.message.answer(text="Test i??in yiffo'ya /start komutunu verin",reply_markup=keyboard_inlinekomutlarTR)
    elif call.data == "en":
        await call.message.answer(text="Give /start to yiffo for testing",reply_markup=keyboard_inlinekomutlarEN)
    elif call.data == "ch":
        await call.message.answer(text="??? /start ??? yiffo ????????????",reply_markup=keyboard_inlinekomutlarRU)
    elif call.data == "ru":
        await call.message.answer(text="?????????? /start yiffo ?????? ????????????????????????",reply_markup=keyboard_inlinekomutlarCH)

# Dil se??imi yenileme
@dp.message_handler(commands=["language"])
async def yiffo_go(message: types.Message):
    first_name = message["from"]["first_name"]
    await message.answer(text="Welcome please select language " + first_name,
                           reply_markup=keyboard_diller)

async def yiffo_Test(messageID, language, i):
    markup,soru = await makeKeyboard(language, i)
    await bot.send_message(chat_id=messageID ,text=soru, reply_markup=markup)

# Test ba??lang??c??
@dp.message_handler(commands=["start"])
async def yiffo_go(message: types.Message):
    durum = message.chat.type
    answer = await json_sorgulama(message.from_id)
    if durum == "group":
        if answer == False:
            await message.answer(text="Welcome please select language " + str(message["from"]["first_name"]),
                reply_markup=keyboard_diller)
        else:
            if answer == "tr":
                await message.answer(text="L??tfen start komutunu Yiffoya ??zelden yaz??n gruba de??il bota " + str(message["from"]["first_name"]),
                reply_markup=keyboard_inlinekomutlarTR)
            if answer == "en":
                await message.answer(text="Please type the start command specifically for Yiff Oya, not the group, but the note. " + str(message["from"]["first_name"]),
                reply_markup=keyboard_inlinekomutlarEN)
            if answer == "ch":
                await message.answer(text="????????????????????? Yiff Oya ????????????????????????????????????????????????" + str(message["from"]["first_name"]),
                reply_markup=keyboard_inlinekomutlarCH)
            if answer == "ru":
                await message.answer(text="????????????????????? Yiff Oya ????????????????????????????????????????????????" + str(message["from"]["first_name"]),
                reply_markup=keyboard_inlinekomutlarRU)
    elif durum == "private":
        await json_sifirlama(message.from_id)
        a = random.randint(1,28)
        await json_guncelleme_sorular(message.from_id, a, True)
        await yiffo_Test(message.from_id, answer, a)

@dp.callback_query_handler(text=["A","B","C","D","E","F","G","A1","B2","C3"])
async def yiffo_test_cevap(call: types.CallbackQuery):
    id = call["from"]["id"]
    language = await json_sorgulama(id)
    await bot.delete_message(id, call["message"]["message_id"]) #Soru silme
    while True:
        randomSoruId = random.randint(1,28)
        answer = await json_guncelleme_sorular(id, randomSoruId, False)
        if answer == True:
            await yiffo_Test(id, language, randomSoruId)
            await json_guncelleme_secenekler(id, call.data)
            break
        elif answer == False:
            pass
        else:
            await json_guncelleme_secenekler(id, call.data)
            if language == "tr":
                harf_1 = answer[0]
                harf_2 = answer[1]
                A1 = answer[2]
                B2 = answer[3]
                C3 = answer[4]

                analiz = json.load(open("jsonFile/tr/tr-cevaplar.json","r",encoding="utf-8"))
                logo_photo = open("image/tr/yiffo.jpeg","rb")
                await bot.send_photo(chat_id=id,photo=logo_photo)
                hayvan_logo = open(f'image/tr/{analiz[harf_1]["Hayvan??"]}.jpeg',"rb")
                await bot.send_photo(chat_id=id,photo=hayvan_logo)
                await bot.send_message(chat_id=id,text="<strong> Ya??ad??????n??z Karakter </strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_1]["??sim"])
                await bot.send_message(chat_id=id,text=analiz[harf_1]["Hayvan??"])
                await bot.send_message(chat_id=id,text=f"%{A1*25} ????itselsiniz & %{B2*25} G??rselsiniz & %{C3*25} Dokunsals??n??z" )
                await bot.send_message(chat_id=id,text="<strong>  Belirgin ??zellikler </strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_1]["Belirgin ??zellikler"])
                await bot.send_message(chat_id=id,text="<strong>  G????l?? Ve Zay??f Y??nleri </strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_1]["G????l?? Ve Zay??f Y??nleri"])
                await bot.send_message(chat_id=id,text="<strong> A??k Hayat??, Ya??am Bi??imi </strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_1]["A??k Hayat??, Ya??am Bi??imi"])
                await bot.send_message(chat_id=id,text="<strong> ??al????ma Prensipler Ve Stratejileri </strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_1]["??al????ma Prensipler Ve Stratejileri"])
                await bot.send_message(chat_id=id,text="<strong> Bask??n Karakter </strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_2]["??sim"])
                await bot.send_message(chat_id=id,text=analiz[harf_2]["Hayvan??"])
                await bot.send_message(chat_id=id,text="<strong>  Belirgin ??zellikler </strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_2]["Belirgin ??zellikler"])
                await bot.send_message(chat_id=id,text="<strong> G????l?? Ve Zay??f Y??nleri </strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_2]["G????l?? Ve Zay??f Y??nleri"])
                await bot.send_message(chat_id=id,text="<strong> A??k Hayat??, Ya??am Bi??imi </strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_2]["A??k Hayat??, Ya??am Bi??imi"])
                await bot.send_message(chat_id=id,text="<strong> ??al????ma Prensipler Ve Stratejileri </strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_2]["??al????ma Prensipler Ve Stratejileri"])
                await bot.send_message(chat_id=id,text="Sosyal Medya Hesaplar??m??z",reply_markup=keyboard_sosyal_media)
                await bot.send_message(chat_id="-1001704058828",text=call["from"]["first_name"] + ' ' + 'karakteri' + ' ' +  analiz[harf_1]["??sim"])

            if language == "en":
                harf_1 = answer[0]
                harf_2 = answer[1]
                A1 = answer[2]
                B2 = answer[3]
                C3 = answer[4]

                analiz = json.load(open("jsonFile/en/en-cevaplar.json","r",encoding="utf-8"))
                logo_photo = open("image/en/yiffo.jpeg", "rb")
                await bot.send_photo(chat_id=id, photo=logo_photo)
                hayvan_logo = open(f'image/en/{analiz[harf_1]["Hayvan??"]}.jpeg', "rb")
                await bot.send_photo(chat_id=id, photo=hayvan_logo)
                await bot.send_message(chat_id=id,text="The Character You Live In")
                await bot.send_message(chat_id=id,text=analiz[harf_1]["??sim"])
                await bot.send_message(chat_id=id,text=analiz[harf_1]["Hayvan??"])
                await bot.send_message(chat_id=id,text=f"{A1*25}% You are auditory & {B2*25}% you are visual & {C3*25}% You are tactile" )
                await bot.send_message(chat_id=id,text="<strong>Distinctive Features</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_1]["Belirgin ??zellikler"])
                await bot.send_message(chat_id=id,text="<strong>Strengths And Weaknesses</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_1]["G????l?? Ve Zay??f Y??nleri"])
                await bot.send_message(chat_id=id,text="<strong>Love Life, Lifestyle</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_1]["A??k Hayat??, Ya??am Bi??imi"])
                await bot.send_message(chat_id=id,text="<strong>Working Principles and Strategies</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_1]["??al????ma Prensipler Ve Stratejileri"])

                await bot.send_message(chat_id=id,text="<strong>Dominant</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_2]["??sim"])
                await bot.send_message(chat_id=id,text=analiz[harf_2]["Hayvan??"])
                await bot.send_message(chat_id=id,text="<strong>Distinctive Features</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_2]["Belirgin ??zellikler"])
                await bot.send_message(chat_id=id,text="<strong>Strengths And Weaknesses</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_2]["G????l?? Ve Zay??f Y??nleri"])
                await bot.send_message(chat_id=id,text="<strong>Love Life, Lifestyle</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_2]["A??k Hayat??, Ya??am Bi??imi"])
                await bot.send_message(chat_id=id,text="<strong>Working Principles and Strategies</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_2]["??al????ma Prensipler Ve Stratejileri"])
                await bot.send_message(chat_id=id,text="Our Social Media Accounts",reply_markup=keyboard_sosyal_media)
                await bot.send_message(chat_id="-1001704058828",text=call["from"]["first_name"] + ' ' + 'character' + ' ' +  analiz[harf_1]["??sim"])

            if language == "ch":
                harf_1 = answer[0]
                harf_2 = answer[1]
                A1 = answer[2]
                B2 = answer[3]
                C3 = answer[4]

                analiz = json.load(open("jsonFile/ch/ch-cevaplar.json","r",encoding="utf-8"))
                logo_photo = open("image/ch/yiffo.jpeg", "rb")
                await bot.send_photo(chat_id=id, photo=logo_photo)
                hayvan_logo = open(f'image/ch/{analiz[harf_1]["Hayvan??"]}.jpeg', "rb")
                await bot.send_photo(chat_id=id, photo=hayvan_logo)
                await bot.send_message(chat_id=id,text="<strong>??????????????????</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_1]["??sim"])
                await bot.send_message(chat_id=id,text=analiz[harf_1]["Hayvan??"])
                await bot.send_message(chat_id=id,text=f"{A1*25}% ??????????????? & {B2*25}% ??????????????? & {C3*25}% ???????????????" )
                await bot.send_message(chat_id=id,text="<strong>????????????</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_1]["Belirgin ??zellikler"])
                await bot.send_message(chat_id=id,text="<strong>???????????????</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_1]["G????l?? Ve Zay??f Y??nleri"])
                await bot.send_message(chat_id=id,text="<strong>???????????????????????????</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_1]["A??k Hayat??, Ya??am Bi??imi"])
                await bot.send_message(chat_id=id,text="<strong>?????????????????????</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_1]["??al????ma Prensipler Ve Stratejileri"])

                await bot.send_message(chat_id=id,text="<strong>?????????</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_2]["??sim"])
                await bot.send_message(chat_id=id,text=analiz[harf_2]["Hayvan??"])
                await bot.send_message(chat_id=id,text="<strong>????????????</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_2]["Belirgin ??zellikler"])
                await bot.send_message(chat_id=id,text="<strong>???????????????</strong>,parse_mode=types.ParseMode.HTML")
                await bot.send_message(chat_id=id,text=analiz[harf_2]["G????l?? Ve Zay??f Y??nleri"])
                await bot.send_message(chat_id=id,text="<strong>???????????????????????????</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_2]["A??k Hayat??, Ya??am Bi??imi"])
                await bot.send_message(chat_id=id,text="<strong>?????????????????????</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_2]["??al????ma Prensipler Ve Stratejileri"])
                await bot.send_message(chat_id=id,text="???????????????????????????",reply_markup=keyboard_sosyal_media)
                await bot.send_message(chat_id="-1001704058828",text=call["from"]["first_name"] + ' ' + '??????' + ' ' +  analiz[harf_1]["??sim"])

            if language == "ru":
                harf_1 = answer[0]
                harf_2 = answer[1]
                A1 = answer[2]
                B2 = answer[3]
                C3 = answer[4]

                analiz = json.load(open("jsonFile/ru/ru-cevaplar.json","r",encoding="utf-8"))
                logo_photo = open("image/ru/yiffo.jpeg", "rb")
                await bot.send_photo(chat_id=id, photo=logo_photo)
                hayvan_logo = open(f'image/ru/{analiz[harf_1]["Hayvan??"]}.jpeg', "rb")
                await bot.send_photo(chat_id=id, photo=hayvan_logo)
                await bot.send_message(chat_id=id,text="<strong>????????????????, ?? ?????????????? ???? ????????????</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_1]["??sim"])
                await bot.send_message(chat_id=id,text=analiz[harf_1]["Hayvan??"])
                await bot.send_message(chat_id=id,text=f"%{A1*25} ???? ???????????????? & %{B2*25} ???? ???????????? & %{C3*25} ???? ??????????????????" )
                await bot.send_message(chat_id=id,text="<strong>?????????????????????????? ??????????</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_1]["Belirgin ??zellikler"])
                await bot.send_message(chat_id=id,text="<strong>?????????????? ?? ???????????? ??????????????</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_1]["G????l?? Ve Zay??f Y??nleri"])
                await bot.send_message(chat_id=id,text="<strong>?????????? ??????????, ?????????? ??????????</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_1]["A??k Hayat??, Ya??am Bi??imi"])
                await bot.send_message(chat_id=id,text="<strong>???????????????? ???????????? ?? ??????????????????</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_1]["??al????ma Prensipler Ve Stratejileri"])

                await bot.send_message(chat_id=id,text="<strong>??????????????????????</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_2]["??sim"])
                await bot.send_message(chat_id=id,text=analiz[harf_2]["Hayvan??"])
                await bot.send_message(chat_id=id,text="<strong>?????????????????????????? ??????????</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_2]["Belirgin ??zellikler"])
                await bot.send_message(chat_id=id,text="<strong>?????????????? ?? ???????????? ??????????????</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_2]["G????l?? Ve Zay??f Y??nleri"])
                await bot.send_message(chat_id=id,text="<strong>?????????? ??????????, ?????????? ??????????</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_2]["A??k Hayat??, Ya??am Bi??imi"])
                await bot.send_message(chat_id=id,text="<strong>???????????????? ???????????? ?? ??????????????????</strong>",parse_mode=types.ParseMode.HTML)
                await bot.send_message(chat_id=id,text=analiz[harf_2]["??al????ma Prensipler Ve Stratejileri"])
                await bot.send_message(chat_id=id,text="???????? ???????????????? ?? ???????????????????? ??????????",reply_markup=keyboard_sosyal_media)
                await bot.send_message(chat_id="-1001704058828",text=call["from"]["first_name"] + ' ' + '????????????????' + ' ' +  analiz[harf_1]["??sim"])


            await json_sifirlama(id)
            break

executor.start_polling(dp)