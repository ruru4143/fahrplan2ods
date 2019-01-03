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

    usage: ./fahrplan2ods.py [--tracks [TRACKS [TRACKS ...]]] # eg CCC
                           [--rooms [ROOMS [ROOMS ...]]] # eg Adams, Borg
                           [--lang [LANG [LANG ...]]] # eg en, de
                           [--do_not_record [DO_NOT_RECORD]] # eg yes, no

#### Example params

    ./fahrplan2ods.py --rooms Borg --lang en

then you get all English talk in Borg
    

    ./fahrplan2ods.py --tracks CCC --rooms Adams

then you get all talks in Adams from CCC eg. Opening/Closing event

### ToDo
* build a clinterface ~~~
* build gui for filter options

