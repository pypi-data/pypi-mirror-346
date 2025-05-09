"""
Flask main app
"""

import logging
import os

from flask import (
    Flask,
    render_template,
    request,
    send_file,
    redirect,
    url_for, Response,
)
from werkzeug.datastructures.file_storage import FileStorage
from werkzeug.wrappers import Response as BaseResponse

from lan_file import file_utils
from lan_file import net

app: Flask = Flask(__name__)
LAN_FOLDER_NAME: str = "lan_folder"
CURRENT_DIR: str = os.getcwd()
LAN_FOLDER: str = os.path.join(CURRENT_DIR, LAN_FOLDER_NAME)
CLIPBOARD_FILE_PATH: str = os.path.join(LAN_FOLDER, 'clipboard.txt')
app.config["UPLOAD_FOLDER"] = LAN_FOLDER_NAME

log: logging.Logger = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)


def read_file():
    try:
        with open(CLIPBOARD_FILE_PATH, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""


def write_file(content):
    with open(CLIPBOARD_FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(content)


@app.route("/", methods=["GET", "POST"])
def index():
    """
    root url
    :return: html file
    """
    files: list = file_utils.get_files_sorted_by_time(LAN_FOLDER)

    if request.method == 'POST':
        content: str = request.form.get('content', '')
        print(f"content: {content}")
        write_file(content)

    return render_template(
        "upload.html",
        files=files,
        content=read_file(),
    )


@app.route("/upload", methods=["GET", "POST"])
def upload_file() -> BaseResponse:
    """
    upload a file
    :return: redirect to root url
    """
    if request.method == "POST":
        file: FileStorage = request.files["file"]
        if file:
            filename: str = str(file.filename)
            if file_utils.is_file_exist(filename, LAN_FOLDER):
                filename = file_utils.rename_file(filename)

            if filename.strip():
                file.save(os.path.join(LAN_FOLDER, filename))

                prompt: str = f"File {filename} uploaded successfully."
                print(prompt)

            return redirect(url_for("index"))

    return redirect(url_for("index"))


@app.route("/download/<filename>")
def download_file(filename: str) -> Response:
    """
    download file
    :param filename: a file already uploaded
    :return: send a file
    """
    file_path = os.path.join(LAN_FOLDER, filename)
    return send_file(file_path, as_attachment=True)


def main() -> None:
    """
    if lan folder not exist, create folder,
    then start service
    """
    if not os.path.exists(LAN_FOLDER):
        os.makedirs(LAN_FOLDER)

    port: int = 5555
    print(f"Running on http://{net.get_local_ip()}:{port}")
    app.run("0.0.0.0", port, debug=False)


if __name__ == "__main__":
    main()
