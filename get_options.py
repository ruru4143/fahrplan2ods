import requests
import sys

# you can extract the json_url from ./fahrplan2ods.py
try:
    from fahrplan2ods import json_url
except:
    print("can't get url from fahrplan2ods.py")

# or put in direkt
# json_url = "https://fahrplan.events.ccc.de/congress/2018/Fahrplan/schedule.json"

r = requests.get(json_url)

# preformattin json
all_data = r.json()
schledule = all_data[u'schedule']
conference = schledule[u'conference']
days = conference[u'days']

acronym = conference[u'acronym']  # for the name

tracksset = set()
roomsset = set()
langsset = set()


for day_index in range(len(days)):
    rooms = days[day_index][u'rooms']
    for room in rooms:
        talk_index = rooms[room]
        for talk in range(len(talk_index)):
            tracksset.add(talk_index[talk][u'track'])
            roomsset.add(talk_index[talk][u'room'])
            langsset.add(talk_index[talk][u'language'])


print("for --tracks :")
for track in tracksset:
    print('"' + str(track) + '" ', end='')
print()


print("for --rooms :")
for room in roomsset:
    print('"' + str(room) + '" ', end='')
print()


print("for --lang")
for lang in langsset:
    print('"' + lang + '" ', end='')
print()

sys.exit()