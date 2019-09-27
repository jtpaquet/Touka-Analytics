from mongoengine import DynamicDocument, StringField, ReferenceField, DateTimeField, DictField, ListField
from numpy import random
import datetime

users = ["Jérémy Talbot-Pâquet", "Pierre-Olivier Marotte", "Étienne Rouleau"]
pseudos = {"Jérémy Talbot-Pâquet": "Djézeune", "Pierre-Olivier Marotte": "Pierre-Poom", "Étienne Rouleau": "Roulo", "William Lacasse": "Lakasse", "Christophe Landry-bergeron": "Krostif", "Jérôme Sirois Charron": "Jirome", "Vincent Masson-Boutin": "Vinssan", "Étienne Godbout": "Godbout", "Meggie Lacasse": "Méganie"}


class Members(DynamicDocument):
    name = StringField(required=True, choices=pseudos.keys(), unique=True)

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        self.pseudo = pseudos.get(str(self.name))


class Users(DynamicDocument):
    name = StringField(default="NPC" + str(random.randint(low=100000, high=999999)))
    email = StringField()


class Messages(DynamicDocument):
    author = StringField(required=True)
    date = DateTimeField(default=datetime.datetime.utcnow(), required=True)
    type = StringField(required=True)
    content = StringField()
    share = DictField()
    reactions = ListField()
    file = ListField()
    photo = ListField()
    audio_file = ListField()
    video = ListField()
    gif = ListField()
    sticker = DictField()
    plan = ListField()
    user = ListField()

    meta = {'ordering': ['date'], 'allow_inheritance': True}


class TextMessages(Messages):
    content = StringField()


class ImageMessages(Messages):
    content = StringField()
