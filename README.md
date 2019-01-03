# fahrplan2ods

This is an little python script that downloads the fahrplan and generates a ods for it. Now you can color the talks, that you want to watch or something like this.

And it has filtering options!

![example_image](https://github.com/ruru4143/fahrplan2ods/blob/master/example_ods.png)

### Dependencies
* pyexcel
* pyexcel-ods
* requests

### Installation / Usage
    
    git clone https://github.com/ruru4143/fahrplan2ods.git
    cd fahrplan2ods
    
if you don't want the fahrplan from 35c3 change the json-url in fahrplan2ods.py
or if you want to filter after: language, track, do_not_record, room.

    ./fahrplan2ods.py

now you have a "talks_EVENTACRONYM_watchlist.ods"

### ToDo
* build a clinterface ~~~
* build gui for filter options

