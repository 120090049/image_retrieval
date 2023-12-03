from flask import Flask, request, redirect, render_template
import subprocess
import os
from werkzeug.utils import secure_filename
from save_movie_info import movie_info_list

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

# 第一个上传页面
@app.route('/upload', methods=['POST'])  
def upload_file():
    if 'imageUpload' not in request.files:
        return redirect(request.url)
    
    file = request.files['imageUpload']
    movie = request.form['movieInput']

    if file and movie:
        filename = secure_filename(file.filename)
        filepath = os.path.join(r'C:\Users\jingyiYang\Desktop\CSC3170project\sf_web_system-master\src\main\resources\templates\admin', filename)
        file.save(filepath)

        try:
            subprocess.run(['python', 'C:\\Users\\jingyiYang\\Desktop\\CSC3170project\\sf_web_system-master\\src\\main\\resources\\try.py', filepath, movie], check=True)
            return 'Python script executed successfully.'
        except subprocess.CalledProcessError:
            return 'Failed to execute Python script.'

    return 'No file or movie name provided'

@app.route('/functhree_page1')  # 跳转到functhree页面
def functhree_page1():
    return render_template('admin/functhree_page1.html')


# 第二个上传页面
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
        filepath = os.path.join(r'C:\Users\jingyiYang\Desktop\CSC3170project\sf_web_system-master\src\main\resources\templates\admin', filename)  # 修改为您希望保存电影的路径
        file.save(filepath)

        # 将电影信息添加到列表中
        movie_info_list.append({
            'name': movie_name,
            'type': movie_type,
            'year': movie_year,
            'country': movie_country,
            'file_path':filepath
        })

        # 打印电影信息
        print(movie_info_list)

        return 'Movie information saved successfully.'
    
    return 'Missing information in the form.'


if __name__ == '__main__':
    app.run(debug=True)


