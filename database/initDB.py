from mongoengine import connect
from datetime import datetime
from utilsDB import Users, Members, Messages, TextMessages, ImageMessages, pseudos

db = connect('ToukaAnalytics')

# Reset DB
db.drop_database('ToukaAnalytics')

# Create DB
member1 = Members(name="Jérémy Talbot-Pâquet").save()
member2 = Members(name="Pierre-Olivier Marotte").save()

user1 = Users(name="Jeremy", email="jtpaquet@gmail.com").save()
user2 = Users(name="Pierre-Olivier").save()
user3 = Users(email=' @gmail.com').save()

message1 = TextMessages(content="Bienvenue sur Touka", author=member1, date=datetime(year=2017, month=9, day=23, hour=23)).save()
message2 = TextMessages(content="Super", author=member2, date=datetime(year=2018, month=9, day=23, hour=23)).save()
message3 = TextMessages(content="Ok", author=member1), date=datetime(year=2019, month=9, day=22, hour=23).save()
message4 = ImageMessages(content="5542525334.jpg", author=member2, date=datetime(year=2019, month=9, day=23, hour=23)).save()


# Iterate through messages
for member in Members.objects:
    for message in Messages.objects(author=member):
        print(message.date, '-', message.author.name, ':', message.content)
    num_posts = Messages.objects(author=member).count()
    print(member.pseudo, "has posted", num_posts, "times.")
    print("=============")

