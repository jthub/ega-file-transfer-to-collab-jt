#!/usr/bin/env python

import subprocess
import os
import sys
import time
from utils import get_task_dict, save_output_json

task_dict = get_task_dict(sys.argv[1])

allowed_codes = { 'LIRI-JP', 'PACA-CA' , 'PRAD-CA', 'RECA-EU', 'PAEN-AU', 'PACA-AU',
'BOCA-UK','OV-AU', 'MELA-AU', 'BRCA-UK', 'PRAD-UK', 'CMDI-UK', 'LINC-JP',
'ORCA-IN', 'BTCA-SG', 'LAML-KR', 'LICA-FR', 'CLLE-ES', 'ESAD-UK', 'PAEN-IT'}

manifest = task_dict.get('input').get('manifest')
study_id = task_dict.get('input').get('study_id')

run = study_id in allowed_codes

task_start = int(time.time())
task_info = ''

if run:

    tmp_dir = '/tmp'

    try:
        download_container = "quay.io/baminou/dckr_icgc_download"
        subprocess.check_output(['docker', 'pull', download_container])

        for file in manifest.get('files'):
            subprocess.check_output(['docker', 'run',
                                     '-e', 'ACCESSTOKEN',
                                     '-e', 'STORAGEURL=' + os.environ.get('STORAGEURL_AWS'),
                                     '-e', 'METADATAURL=' + os.environ.get('METADATAURL_AWS'),
                                     download_container,
                                     '-id', file.get('object_id'), '-o', tmp_dir])
            if not os.path.isfile(tmp_dir + "/" + file.get('file_name')):
                task_info = "Error: File " + file.get('object_id') + ":" + file.get(
                    'file_name') + " couldn't be downloaded from collab."
            else:
                os.remove(tmp_dir + "/" + file.get('file_name'))
    except Exception, e:
        task_info = "Error: " + str(e)

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