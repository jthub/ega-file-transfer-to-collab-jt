#!/usr/bin/env python

import os
import sys
import json
import time
from random import randint
from utils import get_task_dict, save_output_json, get_md5
import subprocess


task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

"""
    input:
      input_dir:
        type: string
      files:
        type: array
"""
files = task_dict.get('input').get('files')
input_dir = task_dict.get('input').get('input_dir')

task_start = int(time.time())

for file in files:
    # only invoke bai generation when the job has information of index file
    if file.get('file_name').endswith('.bam'):
        try:
            subprocess.check_output(['samtools','index',os.path.join(input_dir, file.get('file_name'))])
        except Exception, e:
            with open('jt.log', 'w') as f: f.write(str(e))
            sys.exit(1)  # task failed

task_stop = int(time.time())

output_json = {
    'runtime': {
        'task_start': task_start,
        'task_stop': task_stop
    }
}

save_output_json(output_json)