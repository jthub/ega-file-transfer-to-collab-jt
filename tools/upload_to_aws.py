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

if file_md5sum is None:
    file_md5sum = str(get_md5(file_))

file_size = int(os.path.getsize(file_))

task_start = int(time.time())

try:
    print subprocess.check_output(['icgc-storage-client','upload','--file', file_, '--object-id', object_id, '--md5', file_md5sum, '--force'])
except Exception, e:
    with open('jt.log', 'w') as f: f.write(str(e))

    sys.exit(1)  # task failed

# try:
#     r = subprocess.check_output(['curl','https://raw.githubusercontent.com/jt-hub/ega-collab-transfer-tools/master/download_ega_file.py','|','python','-','-p',project_code,'-f', ega_file_id+".aes", '-o', file_name])
# except Exception, e:
#     print e
#     sys.exit(1)  # task failed


# complete the task

task_stop = int(time.time())


output_json = {
    'file': file_,
    'file_md5sum': file_md5sum,
    'file_size' : file_size,
    'runtime': {
        'task_start': task_start,
        'task_stop': task_stop
    }
}

save_output_json(output_json)
