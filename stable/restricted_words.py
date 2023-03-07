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
        "нахуй",
        "пизда",
        "пиздец",
        "еблан",
        "уёбише",
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

    @staticmethod
    def replace(text: str, replacement: str = "*") -> str:
        words: list[str] = re.findall(r"\w+", text, re.UNICODE)
        for word in words:
            word = word.lower()
            
            if word in RestrictedWords.words:
                text = text.replace(word, replacement * len(word))
                break
            
            parsed_word = morph_analyzer.parse(word)[0]
            if str(parsed_word.normal_form).lower() in RestrictedWords.words: # type: ignore
                text = text.replace(word, replacement * len(word))
        
        return text

    @staticmethod
    def presence(text: str) -> bool:
        words: list[str] = re.findall(r"\w+", text, re.UNICODE)
        for word in words:
            word = word.lower()

            if word in RestrictedWords.words:
                return True
            
            parsed_word = morph_analyzer.parse(word)[0]
            if parsed_word.normal_form in RestrictedWords.words: # type: ignore
                return True
            
        return False


# # Пример использования
# text = "Это сообщение содержит матерные слова, такие как пошла пидр."

# contains = RestrictedWords.presence(text)
# print(contains)

# filterted_text = RestrictedWords.replace(text)
# print(filterted_text)
