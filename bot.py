import telebot
import random
import os
from telebot.types import Message
import csv

# TOKEN = os.environ.get('TOKEN')
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)


# reading the CSV file with triggers and answers
def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as file:  # read content from CSV
        reader = csv.reader(file, delimiter='\t')
        output_list = list(reader)
        return output_list


def clean_list(my_list):  # clean CSV list of empty cells
    my_list = list(filter(None, my_list))
    return tuple(my_list)


def clean_upper_list(my_list):
    all_list = []
    for line in my_list:
        line = clean_list(line)
        all_list.append(line)
    return all_list


triggers_all = tuple(clean_upper_list(read_csv('triggers.csv')))  # use tuples to speed up search and iterations
print(triggers_all)
answers_all = tuple(clean_upper_list(read_csv('answers.csv')))


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    bot.reply_to(message, 'Привет, я AliExpress бот. Напиши команду /alik и свой вопрос, а я попробую ответить.')

@bot.message_handler(commands=['alik'])
def send_welcome(message: Message):
    reply = message.text.lower()  # lowercase user's message to avoid case affect search
    count = 0  # count the line where the trigger happens
    for line in triggers_all:  # run through each list of trigger
        for each in line:  # run through each word in list
            if each in reply:  # if the trigger word is in the list
                bot.reply_to(message, random.choice(answers_all[count]))  # pick a random answer from the corresponding answer line
                print(each)
                break  # to prevent answering multiple times to several trigger word
        else:
            bot.reply_to(message, 'Ничего не понял. Попробуй перефразировать.')
        count = count + 1


@bot.message_handler(content_types=['voice'])
def handle_docs_audio(message):
    bot.reply_to(message, 'Я пока не умею распознавать голос.')


if __name__ == '__main__':
    bot.polling(none_stop=True)

