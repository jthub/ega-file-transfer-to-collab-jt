#!/usr/bin/env python

import os
import sys
import json
import time
from random import randint
from utils import get_task_dict, save_output_json

task_dict = get_task_dict(sys.argv[1])

task_start = int(time.time())

# do the real work here
time.sleep(randint(1,10))


# complete the task

task_stop = int(time.time())

cwd = os.getcwd()

output_json = {
    'bai_file': os.path.join(cwd, 'bai_file.xml'),
    'runtime': {
        'task_start': task_start,
        'task_stop': task_stop
    }
}

save_output_json(output_json)
