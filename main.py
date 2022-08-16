import subprocess, json, rich, time

console = rich.get_console()

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

def format_generic_info(info_dict):
    info_str = ''
    for name in info_dict:
        info_str += name
        info_str += ': ' 
        info_str += str(info_dict[name])
        info_str += '\n'
    return info_str

console.clear()

battery_status = get_info('battery-status')
location = get_info('location')
audio_info = get_info('audio-info')
telephony_deviceinfo = get_info('telephony-deviceinfo')
wifi_connectioninfo = get_info('wifi-connectioninfo')

console.print()

with console.status('Printing data...'):
    time.sleep(2)
    console.clear()
    print(format_generic_info(battery_status))
    print(format_generic_info(location))
    print(format_generic_info(audio_info))
    print(format_generic_info(telephony_deviceinfo))
    print(format_generic_info(wifi_connectioninfo))

