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

# do the real work here
cmd = 'upload_file_to_collab.py'

try:
    r = subprocess.check_output("%s -i %s -g %s -id %s -md5 %s" % (cmd, file_, bundle_id, object_id, file_md5sum), shell=True)
except Exception, e:
    print e
    sys.exit(1)  # task failed

# index exist
if idx_object_id:
    try:
        r = subprocess.check_output("%s -i %s -g %s -id %s -md5 %s" % (cmd, idx_file, bundle_id, idx_object_id, idx_file_md5sum), shell=True)
    except Exception, e:
        print e
        sys.exit(1)  # task failed  


# complete the task

task_stop = int(time.time())

output_json = {
    'runtime': {
        'task_start': task_start,
        'task_stop': task_stop
    }
}

save_output_json(output_json)

