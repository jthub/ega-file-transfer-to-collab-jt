#!/usr/bin/env python

import os
import sys
import time
import subprocess
from utils import get_md5, get_task_dict, save_output_json

task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

"""
    input:
      file:
        type: string
      file_name:
        type: string
      file_md5sum:
        type: string
      object_id:
        type: string
      bundle_id: bundle_id
        type: string
      file_size:
        type: string
"""
file_ = task_dict.get('input').get('file')
file_name = task_dict.get('input').get('file_name')
file_md5sum = task_dict.get('input').get('file_md5sum')
object_id = task_dict.get('input').get('object_id')
idx_file_ = task_dict.get('input').get('idx_file')
idx_file_name = task_dict.get('input').get('idx_file_name')
idx_object_id = task_dict.get('input').get('idx_object_id')
idx_file_md5sum = task_dict.get('input').get('idx_file_md5sum')

if file_md5sum is None:
    file_md5sum = str(get_md5(file_))


if idx_file_ and idx_file_md5sum is None:
    idx_file_md5sum = str(get_md5(idx_file_))

file_size = int(os.path.getsize(file_))


task_start = int(time.time())

try:
    print subprocess.check_output(['icgc-storage-client','upload','--file', file_, '--object-id', object_id, '--md5', file_md5sum, '--force'])
except Exception, e:
    with open('jt.log', 'w') as f: f.write(str(e))
    sys.exit(1)

if idx_object_id:
    file_size+= + int(os.path.getsize(idx_file_))
    try:
        print subprocess.check_output(['icgc-storage-client','upload','--file', idx_file_, '--object-id', idx_object_id, '--md5', idx_file_md5sum, '--force'])
    except Exception, e:
        with open('jt.log', 'w') as f: f.write(str(e))
        sys.exit(1)  # task failed

task_stop = int(time.time())


output_json = {
    'file': file_,
    'file_md5sum': file_md5sum,
    'idx_file': idx_file_,
    'idx_file_md5sum': idx_file_md5sum,
    'file_size' : file_size,
    'runtime': {
        'task_start': task_start,
        'task_stop': task_stop
    }
}

save_output_json(output_json)
