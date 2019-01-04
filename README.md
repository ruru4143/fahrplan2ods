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
                           [--get_options]


#### Example params
if you want german non technical or scientific talks, this would be your settings:

    ./fahrplan2ods.py --lang de --tracks "Ethics, Society & Politics" "Resilience" "Art & Culture" "Entertainment"

if you don't know what to do
    
    ./fahrplan2ods.py --get_options

if you want all talks from CCC in romm Adams:

    ./fahrplan2ods.py --tracks CCC --rooms Adams


### ToDo
* build a clinterface ~~~
* build gui for filter options

