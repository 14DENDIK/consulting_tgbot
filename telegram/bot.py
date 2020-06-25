import telebot

from telebot import util
from django.utils.translation import gettext as _
from django.conf import settings
from .models import TelegramUser, FAQ, Country, VISA_TYPES, Application
from django.utils import translation
from . import keyboards

bot = telebot.TeleBot(settings.TOKEN)


class Controller:
    def __init__(self, user_id):
        self.user_id = user_id
        self.user, create = TelegramUser.objects.get_or_create(user_id=self.user_id)
        translation.activate('ru')


    def handle_start_cmd(self, msg_from_user):
        if msg_from_user.first_name is not None:
            name = msg_from_user.first_name
            if msg_from_user.last_name is not None:
                name += " " + msg_from_user.last_name
        self.user.full_username = name
        self.user.save()
        self.display_main_menu()

    def handle_main_menu(self, text):
        if text in ['FAQs', '❓Часто задаваемые вопросы']:
            self.display_faqs_menu()
        elif text in ['About', 'О нас']:
            large_text = open("about_text.txt", "rb").read()
            large_text = util.split_string(large_text, 5000)
            bot.send_message(self.user_id, large_text)
        elif text in ['btn_visas', '🛂Перечень документов']:
            self.display_countries_menu()
        elif text in ['btn_application', '📋Оставить заявление']:
            self.display_application_name()
        else:
            self.handle_unknown()

    def handle_faqs_menu(self, text):
        if text in ['Back', '🔙Назад']:
            self.display_main_menu()
        else:
            exists = None
            faqs = FAQ.objects.all()
            for faq in faqs:
                if faq.question == text:
                    exists = faq
                    break
            if exists is not None:
                bot.send_message(self.user_id, exists.answer)
            else:
                bot.send_message(self.user_id, _("There is no such question"))
                self.display_faqs_menu()

    def handle_countries_menu(self, text):
        if text in ['Back', '🔙Назад']:
            self.display_main_menu()
        else:
            exists = None
            countries = Country.objects.all()
            for country in countries:
                if country.name == text:
                    exists = country
                    break
            if exists is not None:
                bot.send_document(self.user_id, exists.docs)
            else:
                bot.send_message(self.user_id, _("There is no such country"))
                self.display_countries_menu()

    def handle_application_name(self, text):
        if text is not None and text != " ":
            self.user.full_name = text
            self.user.save()
            self.display_application_contact()
        else:
            bot.send_message(self.user_id, _("Enter valid name"))
            self.display_application_name()

    def handle_application_contact(self, contact):
        self.user.phone_num = contact
        self.user.save()
        self.display_application_visa_type()

    def handle_application_visa_type(self, text):
        exists = None
        for i in range(len(VISA_TYPES)):
            if text == _(VISA_TYPES[i][1]):
                exists = VISA_TYPES[i][0]
                break
        if exists is not None:
            Application.objects.get_or_create(client=self.user.full_name, phone_num=self.user.phone_num, visa_type=exists)
            self.display_application_countries()
        else:
            bot.send_message(self.user_id, _("Wrong visa type"))

    def handle_application_countries(self, text):
        exists = None
        countries = Country.objects.all()
        for country in countries:
            if country.name == text:
                exists = country
                break
        if exists is not None:
            application = Application.objects.filter(client=self.user.full_name).last()
            application.country = exists.name
            application.save()
            bot.send_message(self.user_id, _("Your application reached us.\nWe will get you back soon.\nThank You."))
            self.display_main_menu()
        else:
            bot.send_message(self.user_id, _("There is no such country"))

    def handle_unknown(self):
        bot.send_message(self.user_id, _("Wrong Command"))
        # self.display_main_menu()

    def display_main_menu(self):
        self.user.step = 'main_menu'
        self.user.save()
        bot.send_message(self.user_id, _("Main menu"), reply_markup=keyboards.main_menu())

    def display_faqs_menu(self):
        self.user.step = "faqs"
        self.user.save()
        bot.send_message(self.user_id, _("What question interests you?"), reply_markup=keyboards.faqs_menu())

    def display_countries_menu(self):
        self.user.step = "countries_list"
        self.user.save()
        bot.send_message(self.user_id, _("Countries we work with"), reply_markup=keyboards.countries_menu())

    def display_application_name(self):
        self.user.step = "application_name"
        self.user.save()
        bot.send_message(self.user_id, _("Enter your name:"), reply_markup=keyboards.name_enter_menu())

    def display_application_contact(self):
        self.user.step = "application_contact"
        self.user.save()
        bot.send_message(self.user_id, _("Share your contact"), reply_markup=keyboards.contact_enter_menu())

    def display_application_visa_type(self):
        self.user.step = "application_visa_type"
        self.user.save()
        bot.send_message(self.user_id, _("What visa type you want to get"), reply_markup=keyboards.visa_type_enter_menu())

    def display_application_countries(self):
        self.user.step = "application_countries"
        self.user.save()
        bot.send_message(self.user_id, _("Choose country"), reply_markup=keyboards.countries_enter_menu())
