#!/usr/bin/env python

import os
import sys
import json
import time
from random import randint
from utils import get_task_dict, save_output_json

task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

"""
    input:
      file:
        type: string
        is_file: true
"""
file_name = task_dict.get('input').get('file_name')
input_dir = task_dict.get('input').get('input_dir')

task_start = int(time.time())

# do the real work here
task_info = ''

try:
    os.remove(os.path.join(input_dir,file_name))
except:
    pass
# complete the task
task_stop = int(time.time())

output_json = {
    'runtime': {
        'task_start': task_start,
        'task_stop': task_stop
    },
    'task_info': task_info
}

save_output_json(output_json)

if task_info.startswith('Error'):
    sys.exit(1)
