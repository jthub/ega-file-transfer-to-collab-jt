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
      ega_metadata_git_repo:
        type: string
      ega_metadata_path:
        type: string
      project_code:
        type: string
      bundle_id:  # EGAR or EGAZ ID
        type: string
      ega_dataset_id:
        type: string
      ega_sample_id:
        type: string
      ega_metadata_file_name:
        type: string
"""
ega_metadata_git_repo = task_dict.get('input').get('ega_metadata_git_repo')
ega_metadata_path = task_dict.get('input').get('ega_metadata_path')
project_code = task_dict.get('input').get('project_code')
bundle_id = task_dict.get('input').get('bundle_id')
ega_dataset_id = task_dict.get('input').get('ega_dataset_id')
ega_sample_id = task_dict.get('input').get('ega_sample_id')
ega_metadata_file_name = task_dict.get('input').get('ega_metadata_file_name')
ega_expriment_id = task_dict.get('input').get('ega_expriment_id')
ega_run_id = task_dict.get('input').get('ega_run_id')

# do the real work here
task_start = int(time.time())


#project_code = task_dict.get('input').get('project_code')
#dataset = task_dict.get('input').get('ega_dataset_id')
#experiment = input_json['input']['experiment_accession']
#run = input_json['input']['run_accession']
#sample = input_json['input']['sample_accession']
#study = input_json['input']['study_accession']
output_file = task_dict.get('input').get('ega_metadata_file_name')
metadata_repo = task_dict.get('input').get('metadata_repo_url')

subprocess.call(['prepare_ega_xml_audit.py',
  '-i',metadata_repo,
  '-p',project_code,
  '-o',output_file,
  '-d',ega_dataset_id,
  '-e',ega_expriment_id,
  '-r',ega_run_id,
  '-sa',ega_sample_id])


# complete the task
task_stop = int(time.time())


"""
    output:
      xml_file:
        type: string
        is_file: true
      xml_file_name:  # passing through from ega_metadata_file_name
        type: string
      xml_file_size:
        type: integer
      xml_file_md5sum:
        type: string
"""

output_json = {
    'xml_file': os.path.join(cwd, output_file),
    'xml_file_name': output_file,
    'xml_file_size': os.path.getsize(output_file),
    'xml_file_md5sum': get_md5(output_file),
    'runtime': {
        'task_start': task_start,
        'task_stop': task_stop
    }
}

save_output_json(output_json)

