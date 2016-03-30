import re
import json
from sys import argv

def parse_time(time_string):
    hours = int(re.findall(r'(\d+):\d+:\d+,\d+', time_string)[0])
    minutes = int(re.findall(r'\d+:(\d+):\d+,\d+', time_string)[0])
    seconds = int(re.findall(r'\d+:\d+:(\d+),\d+', time_string)[0])
    milliseconds = int(re.findall(r'\d+:\d+:\d+,(\d+)', time_string)[0])

    return (hours*3600 + minutes*60 + seconds) * 1000 + milliseconds

def parse_srt(srt_string):
    srt_list = []

    for line in srt_string.split('\n\n'):
        if line != '':
            index = int(re.match(r'\d+', line).group())

            pos = re.search(r'\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+', line).end() + 1
            content = line[pos:]
            start_time_string = re.findall(r'(\d+:\d+:\d+,\d+) --> \d+:\d+:\d+,\d+', line)[0]
            end_time_string = re.findall(r'\d+:\d+:\d+,\d+ --> (\d+:\d+:\d+,\d+)', line)[0]
            start_time = parse_time(start_time_string)
            end_time = parse_time(end_time_string)

            srt_list.append( {
                'index': index, 
                'content': content,
                'start': start_time,
                'end': end_time
            } )

    return srt_list

if len(argv) == 3:
    srt_filename = argv[1]
    out_filename = argv[2]
    srt = open(srt_filename, 'r').read()
    parsed_srt = parse_srt(srt)
    open(out_filename, 'w').write(json.dumps(parsed_srt, indent=2, sort_keys=True))
elif len(argv) == 1:
    print('Type \'srttojson.py filename.srt filename.json\'')
else: print('Wrong command.')
