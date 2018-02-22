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
files = task_dict.get('input').get('files')
input_dir = task_dict.get('input').get('input_dir')
idx_object_id = task_dict.get('input').get('idx_object_id')
idx_file_name = task_dict.get('input').get('idx_file_name')

task_start = int(time.time())

for file in files:
    # only invoke bai generation when the job has information of index file
    if idx_file_name and idx_object_id:
        try:
            subprocess.check_output(['generate_bai_from_bam.py','-i',os.path.join(input_dir, file.get('file_name')),'-o',os.path.join(input_dir, file.get('idx_file_name'))])
        except Exception, e:
            with open('jt.log', 'w') as f: f.write(str(e))
            sys.exit(1)  # task failed