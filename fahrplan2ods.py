#!/bin/python
default = "https://fahrplan.events.ccc.de/rc3/2020/Fahrplan/schedule.json"

import pyexcel

import argparse
import itertools
import operator
import datetime

isoformat = '%Y-%m-%dT%H:%M:%S.%f%z'

def add_lists(list1, list2):
    for append_item in list2:
        list1.append(append_item)


def get_args():
    # argparse:
    parser = argparse.ArgumentParser(description='creates a list of talks with filteroptions')

    parser.add_argument('--tracks', type=str, nargs='*',
                        help='filter the tracks, eg CCC')
    parser.add_argument('--rooms', type=str, nargs='*',
                        help='filter the rooms, eg Adams')
    parser.add_argument('--lang', type=str, nargs='*',
                        help='filter the language, eg de, en')
    parser.add_argument('--do_not_record', type=str, nargs='?',
                        help='filter if its recorded eg "yes", "no')
    parser.add_argument('--get_options', action='store_true',
                        help='gives you the possible options')
    parser.add_argument('--url', type=str, nargs='?',
                        help='')  # todo combine url and local
    parser.add_argument('--local', action='store_true',
                        help='')  # todo combine url and local
    args = parser.parse_args()

    if args.get_options:
        # todo make something more smooth
        import get_options

    # Filtering options: (if anything is empty, it doesn't filter)
    args_dict = {}

    if args.url:
        args_dict['url'] = args.url  # CCC, Ethics, Society & Politics....
    else:
        args_dict['url'] = default  # todo remove default and return help with error

    if args.local:
        args_dict['local'] = True
    else:
        args_dict['local'] = False

    filters = []
    # theoretical possible filter:
    #     # Out[3]: dict_keys(['url', 'id', 'guid', 'logo', 'date', 'start', 'duration', 'room', 'slug', 'title',
    #     'subtitle', 'track', 'type', 'language', 'abstract', 'description', 'recording_license', 'do_not_record',
    #     'persons', 'links', 'attachments', 'day', 'time', 'day_num'])

    if args.lang:
        filters.append(('language', args.lang))  # de / en

    if args.tracks:
        filters.append(('track', args.tracks))  # Adams, Borg ...

    if args.rooms:
        filters.append(('room', args.rooms))  # CCC, Ethics, Society & Politics....

    if args.do_not_record:
        if args.do_not_record.lower() == 'yes':
            filters.append(('do_not_record', [True]))  # True/False, off==Non
        elif args.do_not_record.lower() == 'no':
            filters.append(('do_not_record', [False]))  # True/False, off==Non

    args_dict["filters"] = filters
    return args_dict


def _get_raw_json(url, local):
    if local:
        import json
        with open(url, 'r') as file:
            raw = file.read()
        data = json.loads(raw)
    else:
        import requests
        raw = requests.get(url)
        data = raw.json()
    return data


def get_fahrplan(url, local):
    # preformatting json
    all_data = _get_raw_json(url, local)

    schledule = all_data[u'schedule']
    conference = schledule[u'conference']

    acronym = conference[u'acronym']  # for the name
    name_of_the_output_file = "talks_" + acronym + "_watchlist.ods"

    return conference, name_of_the_output_file

def extract_talks(days):
    days = conference['days']

    talks = [rooms['rooms'].values() for rooms in days]
    talks = itertools.chain(*talks)  # unpack and join: [[[talk, ...], ...], ...] to [[talk, ...], ...]
    talks = itertools.chain(*talks)  # unpack and join: [[talk, ...], ...] to [talk, ...]
    talks = list(talks)

    first_day = datetime.datetime.fromisoformat(conference["start"])
    talks = add_easy_to_read_date_metadata(talks, first_day)

    return talks

def add_easy_to_read_date_metadata(list, first_day=None):
    for i in range(len(list)):
        date = datetime.datetime.fromisoformat(list[i]["date"])

        list[i]["day"] = date.strftime("%x")
        list[i]["time"] = date.strftime("%X")
        if first_day:
            list[i]["day_num"] = (datetime.datetime.strptime(date.strftime("%x"), "%x") - first_day).days + 1

    return list

def filter_talks(talks, filters):
    for name, value in filters:
        talks = list(filter(lambda talk: talk[name] in value, talks))

    return list(talks)

if __name__ == '__main__':
    args = get_args()
    conference, name_of_the_output_file = get_fahrplan(args["url"], args["local"])

    talks = extract_talks(conference)
    talks = filter_talks(talks, args["filters"])

    talks_str = []


    result_list = []

    sortby = "day_num"
    talks.sort(key=operator.itemgetter(sortby))
    for day, talks_of_the_day in itertools.groupby(talks, key=operator.itemgetter(sortby)):
        day_index = day - 1
        talks_str.append([])
        talks_str[day_index].append(["Day " + str(day_index + 1), "Seen?", ""])

        first_time = True

        talks.sort(key=operator.itemgetter(sortby))
        for room, talks in itertools.groupby(talks_of_the_day, key=operator.itemgetter("room")):
                talks = list(talks)
                for talk in range(len(talks)):
                    track = talks[talk][u'track']
                    language = talks[talk][u'language']
                    do_not_record = talks[talk][u'do_not_record']

                    title = talks[talk][u'title']
                    talks_str[day_index].append([title, "", ""])


    # calc max days per day
    max_talks_per_day = 0
    for day in talks_str:
        if max_talks_per_day < len(day):
            max_talks_per_day = len(day)

    # make all days the same length
    for day_index in range(len(talks_str)):
        while len(talks_str[day_index]) < max_talks_per_day:
            talks_str[day_index].append(["", "", ""])

    # puting day 1 into the output list
    output_list = []
    for talk in talks_str[0]:
        output_list.append(talk)

    # putting all other days into the output list
    for day_index in range(1, len(talks_str)):
        for talks in range(max_talks_per_day):
            add_lists(output_list[talks], talks_str[day_index][talks])

    # save it as ods
    pyexcel.save_as(array=output_list, dest_file_name=name_of_the_output_file)
    print(output_list)
    print("file saved.")
