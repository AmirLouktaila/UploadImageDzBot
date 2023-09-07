import telebot
import requests
import base64
import os

Mytext = '''
✅ يمكنك رفع اي صورة والحصول على رابط مباشر
فقط ارسل اي صورة وسيتم رفعها 
على سيرفر
'''
TOKEN = "6255631110:AAHtiHnsWxWCUIDVPXYZ5PoGTQGU5Dyf9pc"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, Mytext)

@bot.message_handler(content_types=['photo'])
def photo(message):
    print('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
    a = 0  
    names_code = "photo" + str(a) + ".png"
    with open(names_code, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    with open(names_code, "rb") as image_file:
        image_bytes = image_file.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        print(image_base64)
        response = requests.post(f'https://api.imgbb.com/1/upload?key=a0311c87e15deb38fbb7920f4670869f', data={"image": image_base64})
        if response.status_code == 200:
            r_json = response.json()
            print(r_json)
  
            bot.send_message(message.chat.id, f"صورتك تم رفعها بنجاح: {r_json['data']['url']}")
        else:
            print("Failed to upload the file. Status code:", response.status_code)
    
 
    os.remove(names_code)



bot.infinity_polling()
