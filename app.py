from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from img import process_user_image
from main import perform_ocr

app = Flask(__name__)
CORS(app, resources={r"/ocr": {"origins": "*"}})  # 允许所有来源访问 /ocr 路径

# 配置上传文件夹
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 确保上传文件夹存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/ocr', methods=['GET', 'POST'])
def ocr():
    if request.method == 'POST':
        # 处理文件上传
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                processed_image_path = process_user_image(file_path)
                if processed_image_path:
                    text_content = perform_ocr(processed_image_path)
                    return jsonify({"captcha_text": text_content})
                else:
                    return jsonify({"error": "图像处理失败"}), 500
            else:
                return jsonify({"error": "不支持的文件类型"}), 400
        else:
            return jsonify({"error": "未提供文件"}), 400

    elif request.method == 'GET':
        # 处理 URL 请求
        image_url = request.args.get('url')
        if image_url:
            processed_image_path = process_user_image(image_url)
            if processed_image_path:
                text_content = perform_ocr(processed_image_path)
                return jsonify({"captcha_text": text_content})
            else:
                return jsonify({"error": "图像处理失败"}), 500
        else:
            return jsonify({"error": "url 参数是必需的"}), 400

    return jsonify({"error": "无效请求"}), 400

def allowed_file(filename):
    allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3456)
