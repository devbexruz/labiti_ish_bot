import json
from deep_translator import GoogleTranslator

# Input va output fayl nomlari
input_path = "translate.json"   # sizning faylingiz
output_path = "output.json" # tarjima qilingan fayl

# Faylni o'qish
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Translator obyektlari
translator_ru = GoogleTranslator(source="uz", target="ru")
translator_en = GoogleTranslator(source="uz", target="en")
num = len(data)
n = 0
import os
os.system("cls")
print(f"{n} / {num}\n{round(n*100/num, 1)} %")
# Har bir matnni tarjima qilish
for key, value in data.items():
    if not value.get("ru"):
        try:
            value["ru"] = translator_ru.translate(key)
        except Exception as e:
            print(f"RU tarjima xatosi: {key} -> {e}")

    if not value.get("en"):
        try:
            value["en"] = translator_en.translate(key)
        except Exception as e:
            print(f"EN tarjima xatosi: {key} -> {e}")
    n+=1
    os.system("cls")
    print(f"{n} / {num}\n{round(n*100/num, 1)} %")

# Natijani saqlash
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ Tarjima tugadi. Fayl saqlandi: {output_path}")
