#!/usr/bin/env python

from utils import get_task_dict, save_output_json
import subprocess
import os
import sys
import time

task_dict = get_task_dict(sys.argv[1])

manifest = task_dict.get('input').get('manifest')

task_start = int(time.time())
task_info = ''

tmp_dir = '/tmp'

try:
    download_container = "quay.io/baminou/dckr_icgc_download"
    subprocess.check_output(['docker', 'pull', download_container])

    for file in manifest.get('files'):
        subprocess.check_output(['docker','run',download_container,
                                 '-e', 'ACCESSTOKEN',
                                 '-e', 'STORAGEURL=' + os.environ.get('STORAGEURL_COLLAB'),
                                 '-e', 'METADATAURL=' + os.environ.get('METADATAURL_COLLAB'),
                                 '-id',file.get('object_id'), '-o', tmp_dir])
        if not os.path.isfile(tmp_dir+"/"+file.get('file_name')):
            task_info = "Error: File "+file.get('object_id')+":"+file.get('file_name')+" couldn't be downloaded from collab."
        else:
            os.remove(tmp_dir+"/"+file.get('file_name'))
except Exception, e:
    task_info = "Error: "+str(e)

task_stop = int(time.time())

output_json = {
    'runtime': {
        'task_start': task_start,
        'task_stop': task_stop,
    },
    'task_info': task_info
}

save_output_json(output_json)

if task_info != '':
    sys.exit(1)