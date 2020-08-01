import os
# import magic
import urllib.request
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
import codecs
import pandas as pd
import os
import json

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST','GET'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            f = codecs.open(filename, 'r', encoding="utf8")
            html = f.read()
            soup = BeautifulSoup(html, 'html.parser')
            message_id = []
            date_time = []
            description = []
            from_name = []
            title = []

            for message in soup.find_all('div', attrs={'class': 'message'}):
                try:
                    message_id.append(message['id'])
                except:
                    message_id.append('')
                try:
                    date_time.append(message.find('div', attrs={'class': 'pull_right date details'})['title'])
                except:
                    date_time.append('')

                try:
                    description.append(message.find('div', attrs={'class': 'description'}).text)
                except:
                    description.append('')

                try:
                    from_name.append(message.find('div', attrs={'class': 'from_name'}).text)
                except:
                    from_name.append('')

                try:
                    title.append(message.find('div', attrs={'class': 'title bold'}).text)
                except:
                    title.append('')

            index = []
            for i in range(1, len(message_id) + 1):
                index.append(i)

            keys = ['index','message id', 'Date and Time', 'form name', 'title', 'description']

            tuples = list(zip(index,message_id, date_time, from_name, title, description))
            df = pd.DataFrame(tuples, columns=keys)
            trans_df = df.set_index("index").T
            return trans_df.to_dict()
            
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)


if __name__ == "__main__":
    app.run(host='127.0.0.1',port=6789)