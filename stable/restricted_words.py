import re
from pymorphy2 import MorphAnalyzer

morph_analyzer = MorphAnalyzer()

class RestrictedWords:
    # Swears in a base form, in lowercase.
    words = [
        "fuck",
        "shit",
        "bitch",
        "asshole",
        "faggot",

        "хуй",
        "хуё",
        "нахуй",
        "еби",
        "ебал",
        "проеб",
        "пизда",
        "пиздец",
        "еблан",
        "уёбише",
        "блят",
        "бляд",
        "блять",
        "ебать",
        "блядь",
        "блять",
        "блядина",
        "блядство",
        "взъебка",
        "взъебывать",
        "въебать",
        "въебенить",
        "выебать",
        "выебон",
        "выебываться",
        "выпердеть",
        "высраться",
        "гандон",
        "говно",
        "говнюк",
        "дерьмо",
        "долбоеб",
        "долбоёб",
        "ебало",
        "ебальник",
        "ебануть",
        "ебануться",
        "ебать",
        "ебаться",
        "ебёт",
        "жопа",
        "заебать",
        "заебаться",
        "заебись",
        "заёб",
        "заёбывать",
        "залупа",
        "залупаться",
        "засрать",
        "захуярить",
        "злоебучий",
        "ибать",
        "мандавошка",
        "ебать",
        "сука",
        "мудак",
        "дрочить",
        "ебло",
        "ебучий",
        "ебаный",
        "ебнуть",
        "пидр",
        "пидарас",
    ]
    pattern = r".*?|".join(words)

    exceptions = [
        "застрахуй"
    ]

    @staticmethod
    def replace(text: str, replacement: str = "*") -> str:
        for word in RestrictedWords.words:
            text = re.sub(word + r"\w*", replacement * len(word), text, flags = re.IGNORECASE + re.UNICODE)
            
            word_base_form = morph_analyzer.parse(word)[0].normal_form # type: ignore
            text = text.replace(word_base_form, replacement * len(word))

        return text

    @staticmethod
    def presence(text: str) -> bool:
        words: list[str] = re.findall(RestrictedWords.pattern + r"|\w+", text, re.IGNORECASE + re.UNICODE)

        for word in words:
            if word in RestrictedWords.words:
                return True
            
            word_base_form = morph_analyzer.parse(word)[0].normal_form # type: ignore
            if word_base_form in RestrictedWords.words: 
                return True
            
        return False

# Пример использования
text = "Застрахуй Любят Это блядское сообщение содержит матерные слова, пиздато такие как пошла Пиздапроёбина пиздАпроЕбина, гавна есть тут моча и жапо."

contains = RestrictedWords.presence(text)
print(contains)

filterted_text = RestrictedWords.replace(text)
print(filterted_text)

# print(morph_analyzer.parse("гавна")[0].normal_form)
