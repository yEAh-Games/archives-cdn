import colored as coloured
import json
import os
os.chdir("C:/Users/tbngu/Python/")


def colour(text: str, colour: str) -> str:
    """ Changes the colour of text """
    return coloured.stylize(text, coloured.fg(colour))


with open("roots.json", encoding="utf-8") as f:
    dictionary = json.load(f)

print(colour(f"\n{'━' * 44}", "yellow"))
print(colour("     WELCOME TO THE INVERSE DICTIONARY!", "yellow"))
print("You give the definition, we invent the word!")
print(colour('━', "yellow") * 44)

while True:
    segments = []
    remains = []
    definition = input(colour("\nWrite a definition: ", "red"))

    for definition_word in definition.split():
        has_root = False
        for root in dictionary:
            rootmeaning = root["meaning"].lower().split()
            if definition_word.lower() in rootmeaning:
                if definition_word.lower() != "a":
                    segments.append(root["root"].split(",")[0])
                    has_root = True
        if not has_root:
            remains.append(definition_word)

    for segment in segments:
        if segment.startswith("-") and segment.endswith("-"):
            continue
        if segment.startswith("-"):
            segments.remove(segment)
            segments.insert(0, segment)
        if segment.endswith("-"):
            segments.remove(segment)
            segments.insert(-1, segment)

    remains.insert(0, "".join(segments))
    word = "".join(remains).replace("-", "")
    if word[-1] in ("i", "u"):
        word += "e"

    print(colour(word, "light_green"))
