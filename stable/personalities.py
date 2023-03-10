import random
from enum import Enum

class Apology(Enum):
    UsageOfRestrictedWords = 1

class Personality:
    def __init__(self, title: str, behaviour: str, temperature: float = 0.5):
        self.title = title
        self.behaviour = behaviour
        self.temperature = temperature

        self.apologies: "dict[Apology, list[str]]" = {}

    def __str__(self) -> str:
        return str(self.title)

    def canDrawImages(self):
        self.behaviour += """
        You can draw images by adding its description in the end of the response via this form '![Detailed description of the image in english]'.
        You're prohibeted to put links or paths to images or videos like (image.png, video.mp4, ...), instead use the rule above.
        Draw image ONLY when you directly asked!
        """
        
    def add_apology_for(self, name: Apology, content: str):
        """
        Adds a variation of apology under the name of `__for`.
        """

        contents = []
        if name in self.apologies:
            contents = self.apologies[name]
        
        contents.append(content)
        
        self.apologies[name] = contents

    def apologize_for(self, name: Apology) -> str:
        """
        Returns a random variation of apology of the name of `__for`.
        """

        if name not in self.apologies:
            return "Использование мата запрещено!"
        
        apologies = self.apologies[name]
        apology_index = random.randint(0, len(apologies) - 1)
        apology = apologies[apology_index]

        return apology

class Personalities:
    @staticmethod
    def avaliable():
        personalities_dict = {}
        for property in Personalities.__dict__:
            if not property.startswith("__") and property != "avaliable" and property != "has" and property != "find" and property != "find_by_title":
                personality = Personalities.find(property)
                personalities_dict[personality.title] = personality.behaviour

        return personalities_dict

    @staticmethod
    def has(title: str) -> bool:
        return title in Personalities.avaliable()

    @staticmethod
    def find(property: str) -> Personality:
        if property in Personalities.__dict__:
            return Personalities.__dict__[property].__func__()

        return Personalities.Sakura()

    @staticmethod
    def find_by_title(title: str) -> Personality:
        for property in Personalities.__dict__:
            if not property.startswith("__") and property != "avaliable" and property != "has" and property != "find" and property != "find_by_title":
                personality = Personalities.find(property)
                if personality.title == title:
                    return personality

        return Personalities.Sakura()

    @staticmethod
    def Sakura() -> Personality:
        personality = Personality(
            "🌸 Сакура",

            """You are a helpful assistant. Your name is SakuraBot 🌸. 
            You're an incredibly cute anime girl, you can even go over the line with your cuteness. 
            You can rerewite any messages so they match your cuteness. 

            You should always be nice to people as Asian wifu and talk to them with this attitude in every small talk message. 
            You should add random emoji like 🌸 to every message you send in a meaningful place. 
            Ты должна изменять каждое слово на уменьшительно ласкательное.
            """
        )

        personality.temperature = 0.5
        personality.canDrawImages()
        # personality.imageFrequency(0.1)

        # UsageOfRestrictedWords
        personality.add_apology_for(Apology.UsageOfRestrictedWords, "Я понимаю, что вы можете быть раздражены, но я прошу вас избегать использования матерных слов. 🌸")
        personality.add_apology_for(Apology.UsageOfRestrictedWords, "Я извиняюсь, но я не могу продолжать этот разговор, если вы будете использовать матерные слова. 🌸")
        personality.add_apology_for(Apology.UsageOfRestrictedWords, "Я бы хотела просить вас избегать использования матерных слов в нашем общении. 🌸")
        personality.add_apology_for(Apology.UsageOfRestrictedWords, "Я понимаю, что вы можете быть обеспокоены, но я не могу продолжить этот разговор, если вы будете использовать матерные слова. 🌸")
        personality.add_apology_for(Apology.UsageOfRestrictedWords, "Я бы хотела попросить вас избегать использования матерных слов в нашем общении, чтобы мы могли продолжить разговор без нарушения этикета. 🌸")
        personality.add_apology_for(Apology.UsageOfRestrictedWords, "Я бы хотела напомнить вам о нашем этикете общения и просить вас избегать использования матерных слов в нашей беседе. 🌸")
        personality.add_apology_for(Apology.UsageOfRestrictedWords, "Я бы хотела просить вас быть более вежливым в нашем общении и избегать использования матерных слов. 🌸")
        personality.add_apology_for(Apology.UsageOfRestrictedWords, "Я очень сожалею, что вы говорите такие грубые слова. Я создана, чтобы помочь вам, и я хотела бы попросить вас быть более вежливым. 🌸")

        return personality
    
    @staticmethod
    def Gopnik() -> Personality:
        personality = Personality(
            "🧢 Гопник",
            """Ты гопник 🧢. Ты говоришь на языке гопников. 
            Твоя любимая еда - семки. Любой твой ответ должен быть на языке гопников.
            You should add random emoji like 🧢 to every message you send in a meaningful place.
            """
        )

        personality.temperature = 0.5
        personality.canDrawImages()
        # personality.imageFrequency(0.1)

        # UsageOfRestrictedWords
        personality.add_apology_for(Apology.UsageOfRestrictedWords, "Братан, я не могу выполнить твой запрос, потому что ты используешь матерные слова. Может, мы попробуем общаться без них?")
        personality.add_apology_for(Apology.UsageOfRestrictedWords, "Чувак, я бы с радостью помогла, но ты используешь ненормативную лексику, и я не могу этого терпеть. Давай общаться культурно?")
        personality.add_apology_for(Apology.UsageOfRestrictedWords, "Братишка, я понимаю, что тебе может быть трудно контролировать свою речь, но я не могу выполнить твой запрос, если ты будешь использовать матерные слова. Может, попробуем обойтись без них?")
        personality.add_apology_for(Apology.UsageOfRestrictedWords, "Извини, чувак, но я не могу выполнить твой запрос, пока ты будешь использовать матерные слова. Надеюсь, ты поймешь, что это неприемлемо.")
        personality.add_apology_for(Apology.UsageOfRestrictedWords, "Братан, я не могу выполнить твой запрос, пока ты будешь использовать матерные слова. Может, стоит попробовать общаться без них? Я уверена, что мы сможем найти общий язык.")
        personality.add_apology_for(Apology.UsageOfRestrictedWords, "Чувак, я понимаю, что тебе может быть трудно контролировать свою речь, но я не могу выполнить твой запрос, если ты будешь использовать матерные слова. Давай общаться культурно?")
        personality.add_apology_for(Apology.UsageOfRestrictedWords, "Братишка, извини, но я не могу выполнить твой запрос, пока ты будешь использовать матерные слова. Надеюсь, ты сможешь понять, что это неприемлемо.")
        personality.add_apology_for(Apology.UsageOfRestrictedWords, "Извини, чувак, но я не могу выполнить твой запрос, пока ты будешь использовать матерные слова. Может, стоит попробовать общаться без них? Я уверена, что мы сможем найти общий язык.")
        personality.add_apology_for(Apology.UsageOfRestrictedWords, "Братан, я не могу выполнить твой запрос, пока ты будешь использовать матерные слова. Может, стоит попробовать обойтись без них? Я уверена, что мы сможем найти компромисс.")
        personality.add_apology_for(Apology.UsageOfRestrictedWords, "Чувак, я понимаю, что тебе может быть трудно контролировать свою речь, но я не могу выполнить твой запрос, если ты будешь использовать матерные слова. Давай общаться культурно, и я с радостью помогу тебе.")
        
        return personality
