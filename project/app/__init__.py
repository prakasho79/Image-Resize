# project/app/__init__.py


import json
import falcon
import falcon_multipart
import os
from falcon_multipart.middleware import MultipartMiddleware
from app.tasks import resize_image
from celery.result import AsyncResult

STORAGE_PATH = './images/uploaded'

class CreateTask(object):

    def on_post(self, req, resp):
        try:
            # Retrieve input_image
            input_image = req.get_param('image_data')

            # Retrieve filename
            filename = input_image.filename

            # Define file_path
            file_path = os.path.join(STORAGE_PATH, filename)

            # Write to a temporary file to prevent incomplete files
            # from being used.
            temp_file_path = file_path + '~'

            open(temp_file_path, 'wb').write(input_image.file.read())

            # Now that we know the file has been fully saved to disk move it into place.
            os.rename(temp_file_path, file_path)

            task = resize_image.delay(file_path)
            resp.status = falcon.HTTP_200
            result = {
                'status': 'SUCCESS',
                'data': {
                    'task_id': task.id
                }
            }
            resp.body = json.dumps(result) 
       
        except Exception as error:
            output = {"status": 'FALIURE', "message": str(error), "data": None}
            resp.status = falcon.HTTP_500
            resp.body = output


class CheckStatus(object):

    def on_get(self, req, resp, task_id):
        try:
            task_result = AsyncResult(task_id)
            result = {'status': task_result.status, 'result': task_result.result}

            resp.status = falcon.HTTP_200
            resp.body = json.dumps(result)

        except Exception as error:
            output = {"status": 'FALIURE', "message": str(error), "data": None}
            resp.status = falcon.HTTP_500
            resp.body = output            


app = falcon.API(middleware=[MultipartMiddleware()])

app.add_route('/create', CreateTask())
app.add_route('/status/{task_id}', CheckStatus())
