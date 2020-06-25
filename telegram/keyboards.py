import telebot

from telebot import types
from django.utils import translation
from django.utils.translation import gettext as _

from .models import FAQ, Country, VISA_TYPES


def main_menu():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_faqs = types.KeyboardButton(_('btn_faqs'))
    btn_about = types.KeyboardButton(_('btn_about'))
    btn_visas = types.KeyboardButton(_('btn_visas'))
    btn_application = types.KeyboardButton(_('btn_application'))

    menu.row(btn_application)
    menu.row(btn_visas)
    menu.row(btn_faqs)
    menu.row(btn_about)

    return menu

def faqs_menu():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_back = types.KeyboardButton(_('btn_back'))
    menu.row(btn_back)
    questions = FAQ.objects.all()
    for i in range(questions.count()):
        btn = types.KeyboardButton(questions[i].question)
        menu.row(btn)
    return menu

def countries_menu():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_back = types.KeyboardButton(_('btn_back'))
    menu.row(btn_back)
    menu = countries_list_menu_design(menu)
    return menu

def name_enter_menu():
    markup = types.ReplyKeyboardRemove(selective=True)
    return markup

def contact_enter_menu():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    contact_btn = types.KeyboardButton(text=_("Share contact"), request_contact=True)
    menu.add(contact_btn)
    return menu

def visa_type_enter_menu():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for i in range(len(VISA_TYPES)):
        btn = types.KeyboardButton(_(VISA_TYPES[i][1]))
        menu.row(btn)
    return menu

def countries_enter_menu():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    menu = countries_list_menu_design(menu)
    return menu

def countries_list_menu_design(menu):
    countries = Country.objects.all()
    if countries.count() >= 2:
        if countries.count() % 2 == 0:
            for i in range(0, countries.count(), 2):
                btn_count1 = types.KeyboardButton(_(countries[i].name))
                btn_count2 = types.KeyboardButton(_(countries[i+1].name))
                menu.row(btn_count1, btn_count2)
        else:
            for i in range(0, countries.count() - 1, 2):
                btn_count1 = types.KeyboardButton(_(countries[i].name))
                btn_count2 = types.KeyboardButton(_(countries[i+1].name))
                menu.row(btn_count1, btn_count2)
            btn = types.KeyboardButton(countries[countries.count()-1].name)
            menu.row(btn)
    else:
        btn_count1 = types.KeyboardButton(_(countries[0].name))
        menu.row(btn_count1)
    return menu
