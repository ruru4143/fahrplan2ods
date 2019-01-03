import requests
import pyexcel
import argparse


def add_lists(list1, list2):
    for append_item in list2:
        list1.append(append_item)


parser = argparse.ArgumentParser(description='creat a list of talks with filteroptions')

# argparse:
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('--tracks', type=str, nargs='*',
                    help='filter the tracks, eg CCC')
parser.add_argument('--rooms', type=str, nargs='*',
                    help='filter the rooms, eg Adams')
parser.add_argument('--lang', type=str, nargs='*',
                    help='filter the language, eg de, en')
parser.add_argument('--do_not_record', type=str, nargs='?',
                    help='filter if its recorded eg "yes", "no')

args = parser.parse_args()

# Filtering options: (if anything is empty, it doesn't filter)
if args.lang is None:
    languages_f = []
else:
    languages_f = args.lang # de / en

if args.tracks is None:
    tracks_f = []
else:
    tracks_f = args.tracks # Adams, Borg ...

if args.rooms is None:
    rooms_f = []
else:
    rooms_f = args.rooms # CCC, Ethics, Society & Politics....

if args.do_not_record is None:
    do_not_record_f = None
elif args.do_not_record.lower() == 'yes':
    do_not_record_f = True # True/False, off==Non
elif args.do_not_record.lower() == 'no':
    do_not_record_f = False # True/False, off==Non

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
        if rooms_f == [] or room in rooms_f: # filter rooms

            talk_index = rooms[room]
            for talk in range(len(talk_index)):
                track = talk_index[talk][u'track']
                language = talk_index[talk][u'language']
                do_not_record = talk_index[talk][u'do_not_record']

                if tracks_f == [] or track in tracks_f:
                    if languages_f == [] or language in languages_f:
                        if do_not_record_f == None or do_not_record_f == do_not_record:
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