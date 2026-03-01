#!/bin/bash

PROJECT_ROOT=/storage4tb-1/Aish/LiMeNEx_Network/src

cd $PROJECT_ROOT || exit 1

mkdir -p logs

source /home/iiitd/miniconda3/etc/profile.d/conda.sh
conda activate /home/iiitd/miniconda3/envs/limenexNetwork

export PYTHONPATH=$PROJECT_ROOT

exec -a Limenex gunicorn app:server \
--bind 192.168.30.176:5201 \
--workers 4 \
--timeout 2000 \
--access-logfile $PROJECT_ROOT/logs/access.log \
--error-logfile $PROJECT_ROOT/logs/error.log \
--capture-output \
--log-level info