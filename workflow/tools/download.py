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
      project_code:
        type: string
      ega_file_id:
        type: string
      file_name:
        type: string
      file_md5sum:
        type: string
      object_id:
        type: string
"""
files = task_dict.get('input').get('files')
project_code = task_dict.get('input').get('project_code')


task_start = int(time.time())

for _file in files:
    try:
        if project_code in ['LINC-JP', 'BTCA-JP']:
            r = subprocess.check_output(['download_ega_file.py','-p',project_code,'-f', str(_file.get('ega_file_id'))[-2:]+"/"+_file.get('ega_file_id')+".aes", '-o', _file.get('file_name')])
        else:
            r = subprocess.check_output(['download_ega_file.py','-p',project_code,'-f', _file.get('ega_file_id')+".aes", '-o', _file.get('file_name')])
    except Exception, e:
        with open('jt.log', 'w') as f: f.write(str(e))
        sys.exit(1)  # task failed


# complete the task

task_stop = int(time.time())

"""
    output:
      file:  # new field
        type: string
        is_file: true
      ega_file_id:  # passing through
        type: string
      file_name:  # passing through
        type: string
      file_md5sum:  # passing through
        type: string
      object_id:  # passing through
        type: string
"""

output_json = {
    'out_dir': cwd,
    'runtime': {
        'task_start': task_start,
        'task_stop': task_stop
    }
}

save_output_json(output_json)
