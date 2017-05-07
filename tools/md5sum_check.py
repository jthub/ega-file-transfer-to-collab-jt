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
      file:  # new field
        type: string
        is_file: true
      file_md5sum:
        type: string
"""
file_ = task_dict.get('input').get('file')
file_md5sum = task_dict.get('input').get('file_md5sum')

task_start = int(time.time())

# do the real work here
time.sleep(randint(1,10))


# complete the task

task_stop = int(time.time())

output_json = {
    'runtime': {
        'task_start': task_start,
        'task_stop': task_stop
    }
}

save_output_json(output_json)

# error out with certain rate for testing
#if randint(1,10) > 6:
#    sys.exit(1)
