import json
import time
import requests
import selenium
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

global_username = 'cqtanke14'
global_password = 'cqtanke14'

# 创建一个持久会话的WebDriver对象
def create_persistent_session(user_data_dir):
    """
    创建并返回一个持久会话的WebDriver对象。

    Args:
        user_data_dir (str): 用户数据目录的路径。

    Returns:
        webdriver.Chrome: 创建的WebDriver对象。
        bool: 浏览器是否已打开的标志。
    """
    global driver, browser_opened

    # 创建ChromeOptions对象
    chrome_options = Options()

    # 设置用户数据目录，用于持久化会话
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

    # 添加 experimental_option 以设置 detach 选项为 True
    chrome_options.add_experimental_option('detach', True)

    # 添加 --headless 参数来启用无头模式
    # chrome_options.add_argument("--headless")

    # 创建WebDriver对象，并指定ChromeOptions
    driver = webdriver.Chrome(options=chrome_options)

    # 设置浏览器已打开的标志
    browser_opened = True

    return driver, browser_opened

# 使用给定的用户名和密码进行登录
def login(driver):
    """
    使用给定的用户名和密码进行登录。

    Args:
        driver (webdriver.Chrome): WebDriver对象。
        username (str): 用户名。
        password (str): 密码。
    """
    # 等待页面加载完成
    username = global_username
    password = global_password
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'username')))

    # 输入用户名和密码
    username_input = driver.find_element(By.ID, 'username')
    password_input = driver.find_element(By.ID, 'passwd')

    username_input.send_keys(global_username)
    password_input.send_keys(global_password)

    # 提交登录表单
    checkbox = driver.find_element(By.ID, 'isAgree')
    if not checkbox.is_selected():
        checkbox.click()

    login_button = driver.find_element(By.ID, 'submit')
    login_button.click()

# 处理可能出现的弹出框
def handle_popup(driver):
    """
    处理可能出现的弹出框。

    Args:
        driver (webdriver.Chrome): WebDriver对象。
    """
    try:
        # 等待弹出框出现，最多等待10秒
        WebDriverWait(driver, 10).until(EC.alert_is_present())

        # 切换到弹出框
        alert = driver.switch_to.alert

        # 输出弹出框文本
        print("弹出框内容：", alert.text)

        # 点击确定按钮
        alert.accept()

        # 切换回默认窗口
        driver.switch_to.default_content()

        time.sleep(2)  # 等待一段时间，例如2秒

    except selenium.common.exceptions.TimeoutException:
        # 没有弹出框出现的处理逻辑
        print("没有弹出框出现")

# 检查是否已登录
def is_logged_in(driver):
    """
    检查是否已登录。

    Args:
        driver (webdriver.Chrome): WebDriver对象。

    Returns:
        bool: 是否已登录的标志。
    """
    try:
        # 查找用户登录后的特定元素或标识，例如用户名元素
        username_elements = driver.find_elements(By.ID, 'username')

        # 检查是否找到用户名元素，如果找不到则表示已登录
        if not username_elements:
            return True

    except:
        # 发生异常，表示未登录
        return False

    return False

# 获取未打勾的复选框及其文本内容及总数量
def get_unchecked_checkboxes_with_text(driver):
    # 使用WebDriverWait等待页面加载完成并获取所有复选框元素
    checkboxes = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, '//input[@type="checkbox" and @name="pl_check"]')
        )
    )

    unchecked_checkboxes = []  # 存储未打勾的复选框及其文本内容

    # 遍历复选框元素
    for checkbox in checkboxes:
        # 获取复选框的值
        checkbox_value = checkbox.get_attribute("value")

        # 定位复选框对应的文本元素
        text_element = checkbox.find_element(By.XPATH, '../div/span[@class="spans pl_con"]')

        # 获取文本内容
        text = text_element.text

        # 将复选框元素和文本内容添加到列表中
        unchecked_checkboxes.append({"element": checkbox, "text": text})

    total_count = len(unchecked_checkboxes)  # 获取总数量

    # 返回未打勾的复选框及其文本内容的列表和总数量
    return unchecked_checkboxes, total_count

# 检查并继续执行操作

def check_and_continue(driver):
    try:
        recommend_element = driver.find_element(By.ID, 'znpl')
        if recommend_element:
            print("找到推荐更多")
            # 调用函数获取未打勾的复选框及其文本内容和总数量
            unchecked_boxes, total_count = get_unchecked_checkboxes_with_text(driver)

            print("总数量:", total_count)

            selected_checkboxes=[]
            # 在遍历未打勾的复选框及其文本内容时调用 process_checkbox_with_sentiment_analysis
            for checkbox_info in unchecked_boxes:
                checkbox_element = checkbox_info["element"]  # 获取复选框元素
                text = checkbox_info["text"]
                checkboxes_selected = process_checkbox_with_sentiment_analysis(checkbox_element, text,
                                                                               selected_checkboxes)
                if checkboxes_selected:
                    # 如果有复选框被选中，将结果保存到 selected_checkboxes
                    selected_checkboxes.extend(checkboxes_selected)


            # 判断 selected_checkboxes 列表是否为空
            if not selected_checkboxes:
                # selected_checkboxes 列表为空，表示全部未选中，不执行提交操作的代码
                print("所有复选框均未选中")
                driver.refresh()
            else:
                # selected_checkboxes 列表不为空，表示至少有一个复选框被选中，可以执行提交操作的代码
                submit_form(driver)
                handle_popup2(driver)


    except NoSuchElementException:
        print("======找不到推荐更多，刷新了", i, "次======")
        driver.refresh()

    return False # 返回False表示继续循环

# 进行情感分析，判断文本内容是否为正面评论
# 进行情感分析，判断文本内容是否为正面评论
def perform_sentiment_analysis(text):
    """
    进行情感分析，判断文本内容是否为正面评论。

    Args:
        text (str): 要进行情感分析的文本。

    Returns:
        str: 情感分析结果，"positive" 表示正面评论，"negative" 表示负面评论。
    """
    # 在这里编写情感分析的代码逻辑
    # 可以使用各种情感分析算法或库来判断文本的情感，如NLTK、TextBlob、VADER等
    response = baidu_sentiment_analysis(text)
    time.sleep(2)
    sentiment = response['items'][0]['sentiment']
    if sentiment == 0:
        emotion = "负面"
    elif sentiment == 2:
        emotion = "正面"
    else:
        emotion = "中性"
    print("要进行情感分析的文本:",text,emotion)

    return emotion

# 对给定的复选框和文本进行情感分析处理，并根据情感结果打勾并添加到选中复选框列表
def process_checkbox_with_sentiment_analysis(checkbox_element, text, selected_checkboxes):
    global success_count  # 声明 success_count 为全局变量

    """
    对给定的复选框和文本进行情感分析处理，并根据情感结果进行操作。

    Args:
        checkbox (WebElement): 复选框元素。
        text (str): 文本内容。
        selected_checkboxes (list): 存储选中的复选框元素的列表。

    Returns:
        None
    """
    # 进行情感分析，判断文本内容是否为正面评论
    sentiment = perform_sentiment_analysis(text)

    if sentiment == "正面":
        # 打勾并添加到选中复选框列表
        checkbox_element.click()
        selected_checkboxes.append(checkbox_element)
        success_count += 1
        print("自动下单跨站复制评论数：", success_count)

    return selected_checkboxes
def submit_form(driver):
    submit_button = driver.find_element(By.CSS_SELECTOR, 'span.span.hand#save_btn')
    submit_button.click()


def handle_popup2(driver):
    """
    处理弹出框。

    Args:
        driver (webdriver.Chrome): WebDriver对象。
    """
    try:
        timeout = 10  # 设置超时时间（以秒为单位）

        # 等待加载中的弹出框消失
        WebDriverWait(driver, timeout).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".aui_content")))

        # 等待请求错误的弹出框出现
        error_popup = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".aui_content")))

        error_message = error_popup.text

        # 查找关闭按钮元素
        close_button = None
        try:
            close_button = driver.find_element_by_css_selector(".aui_close")
        except NoSuchElementException:
            print("未找到关闭按钮元素")

        # 如果找到关闭按钮元素，则点击关闭
        if close_button:
            close_button.click()
        else:
            print("未能找到关闭按钮元素")

    except TimeoutException:
        print("处理弹出框时出现超时异常")


def baidu_sentiment_analysis(text):
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token=24.9712b5e99b1f27ef85c637b8d3157fe6.2592000.1688982761.282335-34644185&charset=UTF-8"

    payload = json.dumps({
        "text": text
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Connection':'close'
    }

    response = requests.request("POST", url, headers=headers, data=payload)


    return response.json()







# 设置用户数据目录
user_data_dir = "/home/lq/.config/google-chrome"
# 创建持久会话的WebDriver对象
driver, browser_opened = create_persistent_session(user_data_dir)

# 打开网页
driver.get('http://tools.int800.com/')

# 检查是否已登录,用户名和密码可以替换
if not is_logged_in(driver):
    # 使用用户名和密码进行登录
    login(driver)

    # 等待一段时间，例如2秒
    time.sleep(2)

    # 等待登录成功或提示账号已在其他地方登录
    handle_popup(driver)

# 打开网页2
driver.execute_script('window.open("http://tools.int800.com/commentArea_copyTalk.php?act=addTask_page_new", "_blank");')

# 切换到新标签页
driver.switch_to.window(driver.window_handles[-1])

# 等待页面加载完成
# wait.until(EC.presence_of_element_located((By.ID, 'coreWords')))  # 替换为网页2中需要等待加载的元素的ID或其他定位方式

i = 0
success_count = 0  # 初始化成功打勾的复选框数量

while True:
    i += 1
    if check_and_continue(driver):
        break


    # 等待一段时间，例如1秒
    time.sleep(1)

    # 继续执行后续操作
    # ...


# 关闭浏览器窗口
driver.quit()
