import requests
import pyexcel

def add_lists(list1, list2):
    for append_item in list2:
        list1.append(append_item)

json_url = "https://fahrplan.events.ccc.de/congress/2018/Fahrplan/schedule.json"

r = requests.get(json_url)

# preformattin json
all_data = r.json()
schledule = all_data[u'schedule']
conference = schledule[u'conference']
days = conference[u'days']

acronym = conference[u'acronym'] # for the name
name_of_the_output_file = "talks_" + acronym + "_watchlist.ods"


# gen talks list
talks = []
for day_index in range(len(days)):
    talks.append([])
    talks[day_index].append(["Day " + str(day_index + 1), "Seen?", ""])
    rooms = days[day_index][u'rooms']
    first_time = True
    for room in rooms:
        talk_index = rooms[room]
        for talk in range(len(talk_index)):
            title = talk_index[talk][u'title']
            talks[day_index].append([title, "", ""])

# calc max days per day
max_talks_per_day = 0
for day in talks:
    if max_talks_per_day < len(day):
        max_talks_per_day = len(day)

# make all days the same length
for day_index in range(len(talks)):
    while len(talks[day_index]) < max_talks_per_day:
        talks[day_index].append(["","",""])

# puting day 1 into the output list
output_list = []
for talk in talks[0]:
    output_list.append(talk)

# putting all other days into the output list
for day_index in range(1, len(talks)):
    for talk_index in range(max_talks_per_day):
        add_lists(output_list[talk_index], talks[day_index][talk_index])

# save it as ods
pyexcel.save_as(array=output_list, dest_file_name=name_of_the_output_file)