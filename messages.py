import random 

# Messages
atasozu_templates = [
    "Bir zamanlar bilge bir adam olan <@{user_id}> demişti ki: ***{message}***",
    "Ünlü Japon bilim adamı <@{user_id}> bir gün şöyle demişti: ***{message}***",
    "Antik Yunan filozofu <@{user_id}> vaktiyle şöyle buyurmuştu: ***{message}***",
    "<@{user_id}> bir gün dedi ki: ***{message}***",
    "Tarihin tozlu sayfalarından: <@{user_id}> şöyle demiş: ***{message}***"
]

bira_responses = [
    "Birisi bira mı dedi? 🍻",
    "Canım bira çekti amk.",
    "Bira mı var dediniz beyler?",
    "Şöyle buz gibi bir bira olsa da içsek.",
    "Bira konuşuluyorsa beni de çağırın.",
    "Bakkaldan aldım bira, oturasın y*rağıma."
]


# Regex Responses
on_message_regex_responses = [
    (r"^sa$", "as"),
    (r"\bbira\b", random.choice(bira_responses)),
]

on_message_regex_reactions = [
    (r"\bbira\b", "🍻"),
]