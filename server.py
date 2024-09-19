from flask import Flask, request, send_from_directory, redirect, url_for
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 确保上传文件夹存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return '''
    <h1>局域网文件上传下载示例</h1>
    <form action="/upload" method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="上传">
    </form>
    <a href="/download">下载文件</a>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return f'文件 {filename} 上传成功！<br><a href="/">返回</a>'
    return '上传失败！<br><a href="/">返回</a>'

@app.route('/download')
def download_file():
    # 这里简单返回上传文件夹中的所有文件，实际应用中可以根据需求修改
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return f'<h1>可供下载的文件：</h1><ul>{"".join(f"<li><a href=\"/download/{file}\">{file}</a></li>" for file in files)}</ul>'

@app.route('/download/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
