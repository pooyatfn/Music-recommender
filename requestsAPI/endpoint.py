from flask import Flask, request, render_template, redirect, abort

from db.configs import *
from db.connection import Connection
from db.queries import *
from object_storage import uploader
from rabbitMQ import id_process
from utils.logger import Logger

logger = Logger("endpoint.log")
postgresql = Connection(POSTGRESQL_URL)
service1 = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in {'wav', 'mp3'}


@service1.route('/')
def index():
    return render_template('upload.html')


@service1.route('/upload', methods=['POST'])
def upload_file():
    try:
        file, email = check_input_correctness()
    except ValueError:
        logger.error(f"Incorrect file name or not allowed format")
        return 'Incorrect file name or not allowed format'
    except FileNotFoundError:
        logger.error(f"File not found")
        return 'File not found'
    if not postgresql.open():
        abort(500)

    params = (email,)
    try:
        results = postgresql.execute_query(INSERT_DATA_INTO_REQUEST_TABLE, params)
        postgresql.close()
        inserted_id = str(results[0][0])
    except Exception as e:
        logger.error(f"Inserting data to postgres failed: {e}")
        abort(500)

    try:
        uploader.upload_file(file, inserted_id)
    except Exception as e:
        logger.error(f"Uploading file to object storage failed: {e}")
        abort(500)

    try:
        id_process.send_id(inserted_id)
    except Exception as e:
        logger.error(f"Inserting into rabbitMQ failed: {e}")
        abort(500)

    return render_template('success.html')


def check_input_correctness():
    if 'voice_file' not in request.files:
        return redirect(request.url)
    file = request.files['voice_file']
    email = request.form['email']
    if file.filename == '' or not allowed_file(file.filename):
        raise ValueError
    if not file:
        raise FileNotFoundError
    return file, email


if __name__ == '__main__':
    service1.run(debug=True)
