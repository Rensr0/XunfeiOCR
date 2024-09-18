import cv2
import numpy as np
from matplotlib import pyplot as plt
import requests
import time
import os

# 设置中文字体
plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

def download_image(url, save_dir='./uploads/'):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    timestamp = str(int(time.time()))
    save_path = os.path.join(save_dir, f"{timestamp}.jpg")

    # Check if URL starts with http:// or https://
    if not url.startswith(('http://', 'https://')):
        raise ValueError("无效的URL方案。URL必须以http://或https://开头")

    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return save_path
    else:
        raise Exception(f"无法下载图片，状态码: {response.status_code}")

def preprocess_captcha_image(image_path, output_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"图像文件 {image_path} 未找到。请确保路径正确。")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite(output_path, binary)

    plt.figure(figsize=(10, 6))
    plt.subplot(1, 2, 1)
    plt.title('原始图像')
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.title('处理后的图像')
    plt.imshow(binary, cmap='gray')
    plt.axis('off')
    plt.savefig('processed_image_plot.png')
    plt.close()

def process_user_image(image_url_or_path):
    try:
        if image_url_or_path.startswith(('http://', 'https://')):
            image_path = download_image(image_url_or_path)
        else:
            image_path = image_url_or_path
        output_path = image_path.replace(".jpg", "_processed.jpg")
        preprocess_captcha_image(image_path, output_path)
        return output_path
    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")
        return None