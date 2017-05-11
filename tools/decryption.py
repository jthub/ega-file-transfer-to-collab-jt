#!/usr/bin/env python

import os
import sys
import json
import time
from random import randint
import subprocess
from utils import get_task_dict, save_output_json


task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

"""
    input:
      input_file:
        type: string
        is_file: true
      ega_file_id:  # passing through
        type: string
      file_name:  # passing through
        type: string
      file_size:  # passing through
        type: string
      file_md5sum:  # passing through
        type: string
      object_id:  # passing through
        type: string
"""
input_file = task_dict.get('input').get('input_file')
ega_file_id = task_dict.get('input').get('ega_file_id')
file_name = task_dict.get('input').get('file_name')
file_size = task_dict.get('input').get('file_size')
file_md5sum = task_dict.get('input').get('file_md5sum')
object_id = task_dict.get('input').get('object_id')


task_start = int(time.time())

subprocess.call(['curl','https://raw.githubusercontent.com/jt-hub/ega-collab-transfer-tools/master/decrypt_ega_file.py','|','python','-','-i',input_file,'-o', file_name])


# complete the task

task_stop = int(time.time())

"""
    output:
      file:
        type: string
        is_file: true
      ega_file_id:  # passing through
        type: string
      file_name:  # passing through
        type: string
      file_size:  # passing through
        type: string
      file_md5sum:  # passing through
        type: string
      object_id:  # passing through
        type: string
"""

output_json = {
    'file': os.path.join(cwd, file_name),
    'ega_file_id': ega_file_id,
    'file_name': file_name,
    'file_size': file_size,
    'file_md5sum': file_md5sum,
    'object_id': object_id,
    'runtime': {
        'task_start': task_start,
        'task_stop': task_stop
    }
}

save_output_json(output_json)
