from typing import List, Dict
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
