import telebot
import requests

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.conf import settings

from .models import TelegramUser
from .bot import Controller

bot = telebot.TeleBot(settings.TOKEN)


@csrf_exempt
def index(request):
    if request.method == "GET":
        return HttpResponse("Bot GET")
    if request.method == "POST":
        bot.process_new_updates(
            [telebot.types.Update.de_json(
                request.body.decode("utf-8"))
             ]
        )
        return HttpResponse(status=200)


@bot.message_handler(commands=['start'])
def start(message):
    Controller(message.from_user.id).handle_start_cmd(message.from_user)


@bot.message_handler(content_types=["text"])
def handle_message(message):
    user_id = message.from_user.id
    controller = Controller(user_id)
    user = TelegramUser.objects.get(user_id=user_id)
    if user is not None:
        if user.step == "main_menu":
            controller.handle_main_menu(message.text)
        elif user.step == "faqs":
            controller.handle_faqs_menu(message.text)
        elif user.step == "countries_list":
            controller.handle_countries_menu(message.text)
        elif user.step == "application_name":
            controller.handle_application_name(message.text)
        elif user.step == "application_visa_type":
            controller.handle_application_visa_type(message.text)
        elif user.step == "application_countries":
            controller.handle_application_countries(message.text)
        else:
            controller.handle_unknown()
    else:
        bot.send_message(user_id, "Wrong message")

@bot.message_handler(content_types=["contact"])
def handle_contact(message):
    user_id = message.from_user.id
    controller = Controller(user_id)
    user = TelegramUser.objects.get(user_id=user_id)
    if user is not None:
        controller.handle_application_contact(message.contact.phone_number)


def set_webhook(request, url):
    req = requests.get('https://api.telegram.org/bot'+ settings.TOKEN + '/setwebhook?url=https://' + url + '/bot/')
    res_client = req.json()
    return JsonResponse({"client": res_client})
# bot.polling()
