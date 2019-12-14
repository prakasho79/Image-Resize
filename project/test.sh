#!/bin/bash

# trigger jobs
test=`curl -X POST "http://localhost:8000/create" \
-H "Content-Type: multipart/form-data" \
-H "Accept: application/json" \
-F image_data=@./dataset/dogs_1280p_0.jpg \
-s \
| jq -r '.data.task_id'`

# get status
check=`curl http://localhost:8000/status/${test} -s | jq -r '.status'`

while [ "$check" != "SUCCESS" ]
do
  check=`curl http://localhost:8000/status/${test} -s | jq -r '.status'`
  echo $(curl http://localhost:8000/status/${test} -s)
done