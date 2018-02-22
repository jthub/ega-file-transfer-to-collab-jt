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
      bam_file:
        type: string
        is_file: true
      idx_object_id:
        type: string
      idx_file_name:
        type: string
"""
bam_file = task_dict.get('input').get('bam_file')
idx_object_id = task_dict.get('input').get('idx_object_id')
idx_file_name = task_dict.get('input').get('idx_file_name')

task_start = int(time.time())

# complete the task
# only invoke bai generation when the job has information of index file
if idx_file_name and idx_object_id:
    try:
        subprocess.check_output(['generate_bai_from_bam.py','-i',bam_file,'-o',idx_file_name])
    except Exception, e:
        with open('jt.log', 'w') as f: f.write(str(e))
        sys.exit(1)  # task failed

    # idx_object_id was defined in the job json
    idx_file_size = os.path.getsize(idx_file_name)
    idx_file_md5sum = get_md5(idx_file_name)

    output_json = {
        'idx_file': os.path.join(cwd, idx_file_name),
        'idx_file_name': idx_file_name,
        'idx_object_id': idx_object_id,
        'idx_file_size': idx_file_size,
        'idx_file_md5sum': idx_file_md5sum
    }
else:
    output_json = {
        'task_info': 'skip the bai generation!'
    }


task_stop = int(time.time())

"""
    output:
      # this is the object_id obtained from ICGC service using bundle_id and ega_metadata_file_name as input
      idx_object_id:
        type: string
      idx_file:
        type: string
        is_file: true
      idx_file_name:
        type: string
      idx_file_size:
        type: string
      idx_file_md5sum:
        type: string
"""

output_json.update({
    'runtime': {
        'task_start': task_start,
        'task_stop': task_stop
    }
})

save_output_json(output_json)
