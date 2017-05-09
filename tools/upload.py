#!/usr/bin/env python

import os
import sys
import json
import time
from random import randint
from utils import get_task_dict, save_output_json
import subprocess

task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

"""
    input:
      bundle_id:
        type: string
      object_id:
        type: string
      file:
        type: string
        is_file: true
      file_name:
        type: string
      file_size:
        type: integer
      file_md5sum:
        type: string
      # the follow params are optional
      idx_object_id:
        type: string
      idx_file:
        type: string
        is_file: true
      idx_file_name:
        type: string
      idx_file_size:
        type: integer
      idx_file_md5sum:
        type: string
"""
bundle_id = task_dict.get('input').get('bundle_id')
object_id = task_dict.get('input').get('object_id')
file_ = task_dict.get('input').get('file')
file_name = task_dict.get('input').get('file_name')
file_size = task_dict.get('input').get('file_size')
file_md5sum = task_dict.get('input').get('file_md5sum')

idx_object_id = task_dict.get('input').get('idx_object_id')
idx_file = task_dict.get('input').get('idx_file')
idx_file_name = task_dict.get('input').get('idx_file_name')
idx_file_size = task_dict.get('input').get('idx_file_size')
idx_file_md5sum = task_dict.get('input').get('idx_file_md5sum')


task_start = int(time.time())


subprocess.call(['upload_file_to_collab.py','-i',file_,'-g', bundle_id, '-id', object_id, '-md5', file_md5sum])


# complete the task

task_stop = int(time.time())

output_json = {
    'runtime': {
        'task_start': task_start,
        'task_stop': task_stop
    }
}

save_output_json(output_json)

