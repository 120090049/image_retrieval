from flask import Flask, request, redirect, render_template
import subprocess
import os
from werkzeug.utils import secure_filename
from save_movie_info import movie_info_list
import sys
import numpy as np
from io import BytesIO
import cv2

UPLOAD_FOLDER = "C:\\Users\\13237\\Videos\\videos_temp"
sys.path.append('E:/CSC3170/image_retrieval/backend')
from server import Server

server = Server()

app = Flask(__name__)

@app.route('/')  # 首页
def index():
    return render_template('admin/first_page_threefunc.html')

@app.route('/back', methods=['GET'])
def back():
    # 在这里执行返回操作，例如重定向到首页
    return redirect('/')

@app.route('/functwo_page1')  # 跳转到functwo页面
def functwo_page1():
    return render_template('admin/functwo_page1.html')

# image retrieval page
@app.route('/upload', methods=['POST'])  
def upload_file():
    if 'imageUpload' not in request.files:
        return redirect(request.url)
    file = request.files['imageUpload']
    movie_name = request.form['movieInput']
    if file and movie_name:
        # 读取文件内容到缓冲区
        in_memory_file = BytesIO()
        file.save(in_memory_file)
        in_memory_file.seek(0)
        file_bytes = np.asarray(bytearray(in_memory_file.read()), dtype=np.uint8)    
        # 使用 OpenCV 解码图像数据
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        server.retrieve_img(movie_name, img)

    return 'No file or movie name provided'

@app.route('/functhree_page1')  # 跳转到functhree页面
def functhree_page1():
    return render_template('admin/functhree_page1.html')


# 上传电影信息
@app.route('/upload2', methods=['POST'])  
def upload_file2():
    if 'movieUpload' not in request.files:
        return redirect(request.url)
    
    file = request.files['movieUpload']
    movie_name = request.form['movieName']
    movie_type = request.form['movieType']
    movie_year = request.form['movieYear']
    movie_country = request.form['movieCountry']

    if file and movie_name and movie_type and movie_year and movie_country:
        filename = secure_filename(file.filename)
        movie_dir = os.path.join(UPLOAD_FOLDER, filename)  # 修改为您希望保存电影的路径
        file.save(movie_dir)

        # 将电影信息添加到列表中
        movie_info_list.append({
            'name': movie_name,
            'type': movie_type,
            'year': movie_year,
            'country': movie_country,
            'file_path':movie_dir
        })
        server.insert(movie_name, movie_year, movie_dir, movie_country)

        # 打印电影信息
        print(movie_info_list)

        return 'Movie information saved successfully.'
    
    return 'Missing information in the form.'


if __name__ == '__main__':
    app.run(debug=True)


