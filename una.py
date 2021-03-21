import speech_recognition as sr
import os
import logging
import sys
import pyttsx3
import webbrowser
import random
import datetime
import urllib.request
import re


# output in console | speak text | save text in log file
def massage_output(text):
    print('UNA: %s' % text)
    logger.info('UNA: %s' % text)
    talk(text)


# recording user speech to te
def user_speech():
    # recording speech
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        print('UNA: Слушает вас')
        # delete noises from microphone
        rec.adjust_for_ambient_noise(source, duration=1)
        audio = rec.listen(source)
    try:
        # transform speech to text
        text = rec.recognize_google(audio, language="ru-ru").lower()
        print('User:  ' + text)
        logger.info('User: %s', text)
        return text
    # if speech recognizer don't understand - function starts again
    except sr.UnknownValueError:
        text = 'Повторите: '
        print('UNA: ' + text)
        logger.info('UNA: %s', text)
        text = user_speech()
        return text


def creation_user():
    text = user_speech()
    # remember user name
    user = text
    massage_output('Ваше имя %s ?' % user)
    text = user_speech()
    if 'да' in text:
        massage_output('Приятно познакомится, %s' % user)
        user_name = open('user_info.txt', 'w')
        user_name.writelines(user)
    else:
        massage_output('Пожалуйста, повторите ваше имя.')
        creation_user()


# speech synthesizer
def talk(words):
    engine.say(words)
    engine.runAndWait()


def user_commands(user_name):
    end_words = ['пока', 'до свидания', 'до встречи']
    coin_flip_words = ['подбрось монету', 'кинь монету', 'подбрось монетку',
                       'кинь монетку', 'брось монету', 'брось монетку']
    open_youtube_words = ['открой youtube', 'включи youtube']
    play_music_words = ['включи песню', 'найди песню', 'включи музыку', 'найди песню']
    todo_list_words = ['открой ежедневник', 'открой todo лист', 'открой to do лист', 'открой туду лист']
    text = user_speech()

    # finding keywords in lists to start necessary function
    for word in end_words:
        if word in text:
            close_session(user_name)

    for word in coin_flip_words:
        if word in text:
            coin_flip()
            break

    for word in open_youtube_words:
        if word in text:
            webbrowser.open('https://www.youtube.com/')
            break

    for word in play_music_words:
        if word in text:
            play_music()
            break

    for word in todo_list_words:
        if word in text:
            todo_list()
            break


def coin_flip():
    coin = random.getrandbits(10) % 2
    if coin:
        massage_output('Выпала решка')
    else:
        massage_output('Выпал орёл')


def close_session(user_name):
    massage_output('До встречи, %s' % user_name)
    logger.info('Program finished')
    sys.exit()


def play_music():
    massage_output('Какую песню вы хотите поставить?')
    text = user_speech()
    massage_output('Включаю песню %s' % text)
    # create video link
    video_name = str(text)
    video_name = video_name.replace(' ', '+')
    print(video_name)
    # launch music youtube video
    html = urllib.request.urlopen('https://www.youtube.com/results?search_query=%s' % video_name)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode('utf8'))
    video_url = 'https://www.youtube.com/watch?v=' + video_ids[0]
    webbrowser.open(video_url)


def todo_list():
    massage_output('Что вы хотите сделать в ежедневнике?')
    text = user_speech()
    if 'добавить задачу' in text:
        todo_file = open('todo.txt', 'a')
        massage_output('Как называется ваша задача?')
        task_name = user_speech()
        massage_output('На какую дату вы запланировали выполнение задачи?')
        task_data = user_speech()
        massage_output('Какой статус задачи')
        task_status = user_speech()
        task_id = sum(1 for line in open('todo.txt', 'r'))+1
        current_time = datetime.datetime.today().strftime("%d-%m-%Y/%H:%M:%S")
        # all element of task
        todo_task = str(task_id) + '|' + current_time + '|' + task_name + '|' + task_data + '|' + task_status + '\n'
        logger.info('Изменён файл todo.txt со следующими изминениями: %s' % todo_task)
        # upload to todo_file
        todo_file.write(todo_task)
        todo_file.close()


# creating object of registrar logs
logger = logging.getLogger('UNA')

# initialize speech synthesizer
engine = pyttsx3.init()


def main():
    # create and config log file
    logging.basicConfig(filename='logs.txt', filemode='w', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S')

    logger.info('Program started')

    # create and config speech synthesizer
    voices = engine.getProperty('voices')
    # change voice
    engine.setProperty('voice', 'ru')
    # change speech speed
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 120)

    # creating new user if user_info don't exists
    if not os.path.exists('user_info.txt'):
        print('UNA: Привет, я Юна - голосовой помошник. Как мне к вам обращаться?')
        logger.info('UNA: Привет, я Юна - голосовой помошник. Как мне к вам обращаться?')
        talk('Привет, я Юна - голосовой помошник. Как мне к вам обращаться?')
        creation_user()
    # remember user name
    user_name = open('user_info.txt', 'r')
    user_name = user_name.readline()
    print('UNA: Привет, %s. Чем я могу вам помочь?' % user_name)
    logger.info('UNA: Привет, %s. Чем я могу вам помочь?' % user_name)
    talk('%s. Чем я могу вам помочь?' % user_name)
    while True:
        user_commands(user_name)


if __name__ == "__main__":
    main()

