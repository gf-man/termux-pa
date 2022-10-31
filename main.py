#! /data/data/com.termux/files/usr/bin/python

import subprocess, json, time, rich

from rich.columns import Columns
from rich.panel import Panel
from rich.layout import Layout

console = rich.get_console()
layout = Layout()

def get_info(info_type):
    with console.status('Getting info from termux-' + info_type + '...'):
        completed_process = subprocess.run('termux-' + info_type, capture_output=True, text=True)
    if completed_process.returncode == 0:
        completed_process_output = json.loads(completed_process.stdout)
        print('Got info from termux-' + info_type)
        return completed_process_output
    else:
        print('Error getting info from termux-' + info_type)
        return {'error finding info' : info_type}

def format_generic_info(info):
    info_str = ''
    info_raw = info['raw']
    for name in info_raw:
        name_split = name.split('_')
        for word in name_split:
            if word == "PROPERTY":
                name_split.remove(word)
        name_wrapped = '\n'.join(name_split)
        info_str += name_wrapped
        info_str += ': ' 
        info_str += str(info_raw[name])
        if not name == list(info_raw)[-1]: 
            info_str += '\n'
    info_panel = Panel(info_str, title=info['name'])
    return info_panel

console.clear()

info_type_dict = {
    'battery-status':{'name':'Battery', 'raw':None, 'panel':None},
    'location':{'name':'Location', 'raw':None, 'panel':None},
    'audio-info':{'name':'Audio', 'raw':None, 'panel':None},
    'telephony-deviceinfo':{'name':'Telephone', 'raw':None, 'panel':None},
    'wifi-connectioninfo':{'name':'Wi-Fi', 'raw':None, 'panel':None},
    }


for item in info_type_dict:
    info_type_dict[item]['raw'] = get_info(item)
    info_type_dict[item]['panel'] = format_generic_info(info_type_dict[item]) 

time.sleep(1)


console.print()

with console.status('Printing data...'):
    #console.clear()
    info_group = []
    for item in info_type_dict:
        info_group.append(info_type_dict[item]['panel'])

console.print(Columns(info_group))

input("Press enter to exit:")

options = ["B", "L", "A", "T", "W"]
user_input = input("Pick a Letter: B, L, A, T, W")
if user_input in options:
   print("GOOD")
else:
    print("Invalid input")
