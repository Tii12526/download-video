import telebot
from pytube import YouTube
import os

bot = telebot.TeleBot('6367827738:AAHq66KlT2tjNFCBagsjyiSm864p_ytZvwY')

@bot.message_handler(commands=['start'])
def start(message):
  bot.send_message(message.chat.id,'Hello, I am a YouTube downloader bot. Send me a YouTube video link and I will download it for you')

@bot.message_handler(func=lambda message: True)
def message(message):
  if message.text.startswith('https://youtu.be/'):
    message_id = bot.reply_to(message,'⏳').message_id
    yt = YouTube(message.text)
    audio = yt.streams.filter(only_audio=True).first()
    out_file = audio.download()
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    video = yt.streams.get_highest_resolution()
    out_file = video.download()
    base, ext = os.path.splitext(out_file)
    video_file = base + '.mp4'
    os.rename(out_file, video_file)
    bot.delete_message(message.chat.id, message_id)
    try:
      bot.send_chat_action(message.chat.id, 'upload_document')
      bot.send_audio(message.chat.id, open(new_file, 'rb'))
      bot.send_chat_action(message.chat.id, 'upload_video')
      bot.send_video(message.chat.id, open(video_file, 'rb'))
      os.remove(new_file)
    except Exception as e:
      bot.send_chat_action(message.chat.id, 'upload_document')
      bot.send_document(message.chat.id, open(video_file, 'rb'))
  else:
    bot.reply_to(message, 'Only YouTube links are allowed')


bot.polling(none_stop=True)