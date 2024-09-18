# XunfeiOCR
本项目是一个基于 讯飞OCR 的 文字识别系统，支持通过上传图片文件或提供图片链接来识别图像中的文本。该项目使用了 OpenCV 进行图像预处理，并集成了 OCR API 进行文字识别。系统提供了简单的前端界面，用户可以通过网页上传图片或者输入图片 URL，识别并返回图像中的文本信息。

# 在线体验
- 您可以通过访问：https://api.rensr.site/ 来在线体验本项目
- 也可以通过GET方法调用本项目的OCR接口：https://api.rensr.site/ocr?url=图片链接

## 功能简介

- **上传图片**：用户可以选择从本地上传图片进行识别。
- **输入图片 URL**：用户可以输入图片的 URL 进行文字识别。
- **图像处理**：应用会对上传的图像进行预处理以优化识别效果。
- **OCR 识别**：应用使用讯飞的 OCR API 对处理后的图像进行文字识别。
- **结果展示**：识别结果会在前端页面展示给用户。

## 技术栈

- **前端**：HTML、CSS、JavaScript
- **后端**：Python、Flask
- **图像处理**：OpenCV、Matplotlib
- **OCR**：讯飞的 OCR API

## 讯飞 OCR 技术

本项目使用讯飞的 OCR 技术进行文字识别。讯飞提供的 OCR API 支持高效的文字识别，并且可以处理多种语言和文本格式。你需要在讯飞的开发者平台申请 API Key 和 Secret，然后在代码中配置这些凭证。

### 讯飞 OCR API 配置

1. **申请 API 凭证**：前往 [讯飞开放平台](https://www.xfyun.cn/) 注册并申请 OCR API，获取 `APPId`、`APIKey` 和 `APISecret`。
2. **配置凭证**：在 `main.py` 文件中，更新 `APPId`、`APISecret` 和 `APIKey` 为你在讯飞平台申请到的凭证。

## 环境要求

确保你已经安装了以下 Python 包：

- Flask==2.3.2
- flask-cors==3.0.10
- opencv-python==4.7.0.72
- numpy==1.25.0
- matplotlib==3.7.1
- requests==2.31.0

可以使用以下命令安装所有依赖：

```bash
pip install -r requirements.txt
```

## 使用方法

1. **运行应用程序**：在项目根目录下，运行以下命令启动 Flask 服务：

    ```bash
    nohup python3 app.py & tail -f nohup.out 
    ```

2. **访问 Web 页面**：打开浏览器并访问 `http://localhost:3456`，你将看到应用的主页。

3. **上传图片或输入 URL**：在主页上，你可以选择上传本地图片或输入图片 URL，然后点击“开始识别”按钮进行文字识别。

4. **查看结果**：识别结果会显示在页面上的文本框中。

## 配置说明

- **API 配置**：在 `main.py` 文件中，更新 `APPId`、`APISecret` 和 `APIKey` 为你自己的 API 凭证。
- **图像处理**：你可以根据需要调整 `img.py` 文件中的图像处理逻辑，以适应不同的图像类型和 OCR 需求。

## 许可证

本项目遵循 [MIT 许可证](LICENSE)。你可以自由使用、修改和分发代码，但请保留原始的许可证声明。

## 贡献

如果你有改进建议或发现了 bug，请提交 issue 或 pull request，我们欢迎社区的贡献！

## 联系方式

如果你有任何问题或需要帮助，请通过以下方式联系我：

- **邮箱**：957452088@qq.com
