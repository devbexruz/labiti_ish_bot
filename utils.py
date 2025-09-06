from typing import List, Dict
from aiogram.types import CallbackQuery

dictionary: Dict[str, str] = {}

import json
with open("translate.json", "r", encoding="utf-8") as f:
    dictionary = json.load(f)

def to_translate(lang, text):
    if lang == "uz":
        return text
    if text in dictionary:
        return dictionary[text][lang]
    print(lang, ":", text)
    return text

def call_text(call: CallbackQuery) -> str | None:
    """
    CallbackQuery dan bosilgan tugma matnini qaytaradi.
    Agar topilmasa None qaytadi.
    """
    if not call.message.reply_markup:
        return None

    for row in call.message.reply_markup.inline_keyboard:
        for button in row:
            if button.callback_data == call.data:
                return button.text
    return None


def call_selectable_markup(call: CallbackQuery) -> str | None:
    """
    CallbackQuery dan bosilgan tugma matnini qaytaradi.
    Agar topilmasa None qaytadi.
    """
    if not call.message.reply_markup:
        return None
    markup = call.message.reply_markup
    for row in markup.inline_keyboard:
        for button in row:
            if button.callback_data[:6]=="select":
                button.text = button.text[2:]
                button.callback_data = button.callback_data[6:]
            elif button.callback_data == call.data:
                button.text = "✅ "+button.text
    return markup

if __name__ == "__main__":
    with open("questions.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    with open("translate.json", "r", encoding="utf-8") as f:
        ndata = json.load(f)
    
    for text, questions in list(data.items()):
        for question in questions:
            if "options" not in question:
                continue
            for opt in question["options"]:
                if opt not in data:
                    ndata[opt] = {}


    with open("translate.json", "w", encoding="utf-8") as f:
        json.dump(ndata, f, ensure_ascii=False, indent=4)
