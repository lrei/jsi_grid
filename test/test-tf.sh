#!/bin/bash
JOBID="test-tf"

# extract job scrit and data
tar xf ${JOBID}.tar.gz

# execute the program
echo "Computing started!"
cd ${JOBID}
python test-tf.py

# prepare results for download
echo "Computing finished!"
cd ..
tar czf ${JOBID}.out.tar.gz ${JOBID}
