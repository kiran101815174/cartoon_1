from flask import Flask,url_for,render_template,redirect,request
from werkzeug.utils import secure_filename
import os
from PIL import Image
UPLOAD_FOLDER = 'app/static/'
from app import app
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
import cv2
import time
def cartoonization(img):
    img=cv2.imread(img)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray=cv2.medianBlur(gray,5)  #5 is kernal size
    edges=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,5,7)
    color=cv2.bilateralFilter(img,5,150,250)
    cartoon=cv2.bitwise_and(color,color,mask=edges)
    return cartoon
@app.route('/')
@app.route('/upload',methods=['POST','GET'])
def upload_image():
    return render_template('index.html')
@app.route('/uploader',methods=['GET','POST'])
def uploader_image():
    if request.method == 'POST':
        file = request.files['file']
        filename2 = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename2))
        path=os.path.join(app.config['UPLOAD_FOLDER'],filename2)
        file2=cartoonization(path)
        file2 = Image.fromarray(file2)
        new_name = "output" + str(time.time()) + ".jpg"

        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            if filename.startswith('output_'):  # not to remove other images
                os.remove('static/' + filename)
        file2.save(os.path.join(app.config['UPLOAD_FOLDER'],new_name))
        return render_template('base.html',filename=new_name)
    return render_template('index.html')


