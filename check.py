import requests
from selenium import webdriver
import yaml
from urllib3.exceptions import InsecureRequestWarning
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
# from capture import Capture
import timeStampMD5
import os
from HTML import generator
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
# 忽略因使用https造成的不安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def check_url(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code, response.elapsed.total_seconds()
    except requests.exceptions.ConnectionError:
        # 如果默认80端口连接失败，则尝试443端口的https连接
        try:
            https_url = url.replace("http://", "https://")
            response = requests.get(https_url, timeout=5, verify=False)
            return response.status_code, response.elapsed.total_seconds()
        except Exception as e:
            return "连接失败", 0
    except Exception as e:
        return "连接失败", 0


def get_info(url):
    # 配置Chrome以无界面模式运行
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 添加无界面选项
    chrome_options.add_argument("--disable-gpu")  # 禁用GPU加速，某些系统/版本下可能需要
    chrome_options.add_argument("--window-size=1920x1080")  # 设置窗口大小，这对一些需要特定分辨率的页面很有用

    # 注意：这里需要根据实际环境配置webdriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        driver.get(url)
        driver.implicitly_wait(5)  # 根据需要调整等待时间
        title = driver.title  # 获取页面标题
        timestamp_md5 = timeStampMD5.now_timestamp_md5()
        url_simplified = url.replace("http://", "").replace("https://", "").split("/")[0]
        filename = f"{url_simplified}_{timestamp_md5}.png"
        # 确保screenshot目录存在
        screenshot_dir = 'screenshot'
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        # 截图并保存路径
        screenshot_path = os.path.join(screenshot_dir, filename)
        driver.save_screenshot(screenshot_path)
        return title, screenshot_path
    finally:
        driver.quit()


def check(url):
    # 检查URL是否以http://或https://开头，如果不是，则自动添加http://
    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'http://' + url
    status_code, response_time = check_url(url)
    title, screenshot_path = get_info(url) if status_code == 200 else "获取标题失败"
    return {
        'status_code': status_code,
        'response_time': response_time,
        'title': title,
        'screenshot_path': screenshot_path
        }


def start(urls):
    results = {}
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(check, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                results[url] = data
                print(f"Processed {url}")
            except Exception as exc:
                print(f"{url} generated an exception: {exc}")

    results_file = f'{timeStampMD5.now_timestamp_md5()}.yaml'
    # 保存结果到yaml文件
    with open(results_file, 'w') as file:
        yaml.dump(results, file, allow_unicode=True)
    generator(results_file)
