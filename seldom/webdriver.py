# -*- coding: utf-8 -*-
import time
import warnings
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from .logging.log import Log


LOCATOR_LIST = {
    'css': By.CSS_SELECTOR,
    'css selector': By.CSS_SELECTOR,
    'id': By.ID,
    'name': By.NAME,
    'xpath': By.XPATH,
    'link_text': By.LINK_TEXT,
    'link text': By.LINK_TEXT,
    'partial_link_text': By.PARTIAL_LINK_TEXT,
    'partial link text': By.PARTIAL_LINK_TEXT,
    'tag': By.TAG_NAME,
    'tag name': By.TAG_NAME,
    'class_name': By.CLASS_NAME,
    'class name': By.CLASS_NAME
}

log = Log()


class WebDriver(object):
    """
        Seldom framework for the main class, the original
    selenium provided by the method of the two packaging,
    making it easier to use.
    """
    driver = None
    original_window = None
    timeout = 0

    def get(self, url):
        """
        get url.:打开指定页面

        Usage:
        self.get("https://www.baidu.com")
        """
        self.driver.get(url)
        log.info('Open url:{}'.format(url))

    def open(self, url):
        """
        open url.

        Usage:
        self.open("https://www.baidu.com")
        """
        self.get(url)

    def close(self):
        """
        关闭当前打开页面窗口
        Usage:
        self.close()
        """
        self.driver.close()
        log.info('浏览器操作:关闭当前浏览器的窗口')

    def quit(self):
        """
        关闭当前打开的浏览器
        Usage:
        self.quit()
        """
        self.driver.quit()
        log.info('浏览器操作:关闭浏览器')

    def back(self):
        """后退/返回到上一页面"""
        self.driver.back()
        log.info('浏览器操作:后退/返回到上一页面')

    def forward(self):
        """前进到上一页面（相对于后退而言）"""
        self.driver.forward()
        log.info('浏览器操作:前进到上一页面（相对于后退而言）')

    def refresh(self):
        """刷新当前页面"""
        self.driver.refresh()
        log.info('浏览器操作:刷新当前页面')

    def max_window(self):
        """
        Set browser window maximized.设置浏览器窗口全屏化

        Usage:
        self.max_window()
        """
        self.driver.maximize_window()
        log.info(message='浏览器窗口全屏化')

    def set_window(self, wide, high):
        """
        Set browser window wide and high.
        指定设置浏览器窗口大小
        Usage:
        self.set_window(wide,high)
        """
        self.driver.set_window_size(wide, high)
        log.info('设置浏览器窗口大小:wide:{wide}, wide:{high}'.format(wide=wide, high=high))

    def find_element(self, by, element):
        """寻找元素,页面符合条件的第一个节点"""
        try:
            LOCATOR_LIST[by]
        except KeyError:
            raise ValueError("元素类型:'{}' 不支持.".format(by))

        try:
            if by == 'id':
                elem = self.driver.find_element_by_id(element)
            elif by == 'xpath':
                elem = self.driver.find_element_by_xpath(element)
            elif by == 'name':
                elem = self.driver.find_element_by_name(element)
            elif by == 'class_name':
                elem = self.driver.find_element_by_class_name(element)
            elif by == 'link_text':
                elem = self.driver.find_element_by_link_text(element)
            elif by == 'css selector' or by == 'css':
                elem = self.driver.find_element_by_css_selector(element)
            elif by == 'partial link text':
                elem = self.driver.find_element_by_partial_link_text(element)
            elif by == 'tag name':
                elem = self.driver.find_element_by_tag_name(element)
            else:
                raise NameError(
                    "Please enter the correct targeting element,'id_/name/class_name/tag/link_text/xpath/css'.")

        except NoSuchElementException as msg:
            # Utility(self.driver).screen_png('NoSuchElement_%s.png' % text)
            log.warn(msg)
            raise NoSuchElementException('未找到元素,类型:%s, 值:%s' % (by, element))
        else:
            return elem

    def write(self, by, element, text, clear=False):
        """
        给指定元素输入内容
        :param by: 定位元素类型
        :param element: 定位元素的值
        :param text: 输入的内容
        :param clear: 是否需要执行清除操作
        :return:
        """
        find_element = self.find_element(by=by, element=element)
        if find_element:
            if clear:
                find_element.clear()
            if by == 'css selector':
                self.css_write_script(element, text)
            else:
                find_element.send_keys(text)
                log.info('输入:%s (类型:%s, 值:%s)' % (text, by, element))

    def click(self, by, element, description=None):
        """
        点击指定元素
        :param by: 定位元素类型
        :param element: 定位元素的值
        :param description: 操作的元素的描述, 主要是为了方便日志的输出
        :return:
        """
        find_element = self.find_element(by=by, element=element)
        if description is None:
            description = find_element.text
            if description == '':
                description = find_element.get_attribute('textContent')
        if find_element:
            if by == 'css selector':
                self.css_click_script(element)
            else:
                find_element.click()
                if description == '':
                    log.info('点击/选中(类型:%s, 值:%s)' % (by, element))
                else:
                    log.info('点击:%s (类型:%s, 值:%s)' % (description, by, element))

    def click_text(self, text):
        """
        Click the element by the link text
        一般适用于<a> </a>中的文本内容的点击操作
        Usage:
        self.click_text("新闻")
        """
        # self.find_element(by, element)
        self.driver.find_element_by_link_text(text).click()
        log.info('click_text操作:%s' % text)

    def submit(self, by, element):
        """
        针对表单事件的提交操作, 与点击方法类似
        Usage:
        driver.submit(css="#el")
        """
        elem = self.find_element(by, element)
        elem.submit()
        log.info('submit提交:(类型:%s, 值:%s)' % (by, element))

    def css_click_script(self, element):
        """
        仅适用于css类型的点击操作, 并且会在需要点击区域进行标识
        :param element:
        :return:

        """
        js = """var elm = document.querySelectorAll("{css}")[0];
                            elm.style.border="2px solid red";
                            elm.click();""".format(css=element)
        self.execute_script(js)
        log.info('css_script操作:点击,(类型:css, 值:%s)' % element)

    def css_write_script(self, element, value):
        """
        仅适用于css类型的输入操作, 并且会在需要点击区域进行标识
        :param element:
        :return:

        """
        js = """var elm = document.querySelectorAll("{css}")[0];
                                    elm.style.border="2px solid red";
                                    elm.value = "{value}";""".format(css=element, value=value)
        self.execute_script(js)
        log.info('css_script操作:输入:%s, (类型:css, 值:%s)' % (value, element))

    def execute_script(self, script):
        """
        Execute JavaScript scripts.

        Usage:
        self.execute_script("window.scrollTo(200,1000);")
        """
        self.driver.execute_script(script)

    def clear(self, by, element):
        """
        Clear the contents of the input box.
        清除元素内容
        Usage:
        self.clear(css="#el")
        """
        find_element = self.find_element(by, element)
        if find_element:
            find_element.clear()
        log.info("清除输入框元素(元素类型, 值: {by}, {value})".format(by=by, value=element))

    def get_text(self, by, element) -> str:
        """获取元素文字"""
        find_element = self.find_element(by, element)
        if find_element:
            data = find_element.text
            return data

    def get_key_value(self, by, element, key: str) -> str:
        """通过元素中的key, 获取到value"""
        elem = self.find_element(by, element)
        if elem:
            data = elem.get_attribute(key)
            return data

    def slow_click(self, by, element):
        """
        Moving the mouse to the middle of an element. and click element.
        Usage:
        self.slow_click(css="#el")
        """
        elem = self.find_element(by, element)
        ActionChains(self.driver).move_to_element(elem).click(elem).perform()

    def right_click(self, by, element):
        """
        鼠标右键
        Usage:
        self.right_click(css="#el")
        """
        elem = self.find_element(by, element)
        ActionChains(self.driver).context_click(elem).perform()
        log.info('鼠标操作:右击。操作元素类型:%s, 值:%s' % (by, element))

    def move_to_element(self, by, element):
        """
        鼠标悬停
        Usage:
        self.move_to_element(css="#el")
        """
        elem = self.find_element(by, element)
        ActionChains(self.driver).move_to_element(elem).perform()
        log.info('鼠标操作:鼠标悬停。操作元素类型:%s, 值:%s' % (by, element))

    def click_and_hold(self, by, element):
        """
        鼠标左键点击不放, 一般不单独使用
        Usage:
        self.move_to_element(css="#el")
        """
        elem = self.find_element(by, element)
        ActionChains(self.driver).click_and_hold(elem).perform()

    def double_click(self, by, element):
        """
        鼠标操作:双击（左键）

        Usage:
        self.double_click(css="#el")
        """
        elem = self.find_element(by, element)
        ActionChains(self.driver).double_click(elem).perform()
        log.info('鼠标操作:双击（左键）。操作元素类型:%s, 值:%s' % (by, element))

    def drag_and_drop(self, source_by, source_element, target_by, target_element):
        """鼠标拖放操作"""
        source_find_element = self.find_element(source_by, source_element)
        target_find_element = self.find_element(target_by, target_element)
        ActionChains(self.driver).drag_and_drop(source_find_element, target_find_element).perform()
        log.info('鼠标操作:从 %s 拖放到 %s' % (source_element, target_element))

    def scroll_into_view(self, by, element):
        """
        不在可视范围内拖动滚动条至元素所在位置
        :param by:
        :param element:
        :return:
        """
        to_element = self.find_element(by, element)
        self.driver.execute_script('arguments[0].scrollIntoView()', to_element)
        log.info('拖动滚动条至元素所在位置, 元素类型:%s, 值:%s' % (by, element))
        to_element.click()

    def window_scroll(self, width=None, height=None):
        """
        拖动滚动条到指定位置
        Usage:
        self.window_scroll(width=300, height=500)
        """
        if width is None:
            width = "0"
        if height is None:
            height = "0"
        js = "window.scrollTo({w},{h});".format(w=str(width), h=str(height))
        self.execute_script(js)

    def get_display(self, by, element):
        """
        检查元素是否可见, 可见返回True, 否则返回False

        Usage:
        self.get_display(css="#el")
        """
        elem = self.find_element(by, element)
        return elem.is_displayed()

    def get_title(self):
        """
        获取当前url的title标题

        Usage:
        self.get_title()
        """
        title = self.driver.title
        log.info('当前窗口页面title:%s' % title)
        return title

    def get_url(self):
        """
        获取当前页面的URL地址

        Usage:
        self.get_url()
        """
        url = self.driver.current_url
        log.info('当前窗口页面URL:%s' % url)
        return url

    def implicitly_wait(self, secs=10):
        """
        设置全局隐式等待时间, 默认10秒

        Usage:
        self.wait(10)
        """
        self.driver.implicitly_wait(secs)
        log.info('全局隐式等待时间:%s S' % secs)

    def get_alert_text(self):
        """
        获取alert警告弹窗的提示内容

        Usage:
        self.get_alert_text()
        """
        alert_text = self.driver.switch_to.alert.text
        log.info('alert警告弹窗内容:%s' % alert_text)
        return alert_text

    def accept_alert(self):
        """
        alert弹窗, 进行允许操作.

        Usage:
        self.accept_alert()
        """
        self.driver.switch_to.alert.accept()
        log.info('alert警告弹窗操作:accept')

    def dismiss_alert(self):
        """
        alert弹窗, 进行取消操作.

        Usage:
        self.dismiss_alert()
        """
        self.driver.switch_to.alert.dismiss()
        log.info('alert警告弹窗操作:dismiss')

    def switch_to_frame(self, by, element):
        """
        切换到frame组件中
        driver.switch_to.frame('frame_name')  通过<frame> id = 'frame_name'</frame>
        driver.switch_to.frame(1)  通过<frame> </frame>便签值进行定位, 从0开始
        driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0]) 用WebElement对象来定位
        Usage:
        self.switch_to_frame(css="#el")
        """
        if by == 'id' or by == 'name':
            self.driver.switch_to.frame(element)
            log.info('切换到frame <frame>key:%s, value:%s' % (by, element))
        else:
            elem = self.find_element(by, element)
            self.driver.switch_to.frame(elem)
            log.info('切换到frame <frame>key:%s, value:%s' % (by, element))

    def switch_to_frame_out(self):
        """
        在进入到frame后, 退出当前的进入frame组件, 回到默认页面中

        Usage:
        self.switch_to_frame_out()
        """
        self.driver.switch_to.default_content()
        log.info('退出/返回到上一个 Frame')

    def switch_to_old_window(self, target_window):
        """
        此方法主要用于在自动化操作后, 在当前页面的基础上在新的窗口中打开一个新的页面, 完成对新的页面的操作后, 
        需要回到原来的目标窗口页面继续操作时使用。
        这里适用两个窗口间进行来回切换
        需要在跳转前获取到目标窗口的句柄, 获取方式:target_window = driver.current_window_handle
        :param target_window:
        :return:True/False
        """
        all_handles = self.driver.window_handles
        if target_window in all_handles:
            for handle in all_handles:
                if handle != target_window:
                    self.driver.switch_to.window(handle)
                    log.info('切换window窗口成功')
                    return True
        else:
            log.warn('当前需要切换的window窗口句柄不存在, 不执行切换操作')
            return False

    @property
    def current_window_handle(self):
        """
        返回当前窗口对应的handle session值

        :Usage:
            self.current_window_handle
        """
        current_handle = self.driver.current_window_handle
        log.info('当前窗口的handle值:%s' % current_handle)
        return current_handle

    @property
    def new_window_handle(self):
        """
        返回最后一个窗口对应的handle session值

        :Usage:
            self.new_window_handle
        """
        new_handle = self.window_handles
        log.info('当前浏览器中最后一个窗口的handle值')
        return new_handle[-1]

    @property
    def window_handles(self):
        """
        返回当前浏览器中打开的所有窗口的handle session值

        :Usage:
            self.window_handles
        """
        all_handles = self.driver.window_handles
        log.info('当前浏览器中所有窗口的handle值')
        return all_handles

    def switch_to_window(self, window_name):
        """
        Switches focus to the specified window.

        :Args:
         - window_name: The name or window handle of the window to switch to.

        :Usage:
            self.switch_to_window('main')
        """
        self.driver.switch_to.window(window_name)
        log.info('切换到handle对应的窗口, handle值:%s' % window_name)

    def screenshots(self, file_path):
        """
        Saves a screenshots of the current window to a PNG image file.

        Usage:
        self.screenshots('/Screenshots/foo.png')
        """
        self.driver.save_screenshot(file_path)

    def select(self, by, element, value=None, text=None, index=None):
        """
        Constructor. A check is made that the given element is, indeed, a SELECT tag. If it is not,
        then an UnexpectedTagNameException is thrown.

        :Args:
         - css - element SELECT element to wrap
         - value - The value to match against

        Usage:
            <select name="NR" id="nr">
                <option value="10" selected="">每页显示10条</option>
                <option value="20">每页显示20条</option>
                <option value="50">每页显示50条</option>
            </select>

            self.select(css="#nr", value='20')
            self.select(css="#nr", text='每页显示20条')
            self.select(css="#nr", index=2)
        """
        elem = self.find_element(by, element)
        if value is not None:
            Select(elem).select_by_value(value)
            log.info('Select选择,通过value:%s' % value)
        elif text is not None:
            Select(elem).select_by_visible_text(text)
            log.info('Select选择,通过text:%s' % text)
        elif index is not None:
            Select(elem).select_by_index(index)
            log.info('Select选择,通过index:%s' % index)
        else:
            raise ValueError(
                '"value" or "text" or "index" options can not be all empty.')

    def get_cookies(self):
        """
        Returns a set of dictionaries, corresponding to cookies visible in the current session.
        Usage:
            self.get_cookies()
        """
        return self.driver.get_cookies()

    def get_cookie(self, name):
        """
        Returns information of cookie with ``name`` as an object.
        Usage:
            self.get_cookie()
        """
        return self.driver.get_cookie(name)

    def add_cookie(self, cookie_dict):
        """
        Adds a cookie to your current session.
        Usage:
            self.add_cookie({'name' : 'foo', 'value' : 'bar'})
        """
        if isinstance(cookie_dict, dict):
            self.driver.add_cookie(cookie_dict)
        else:
            raise TypeError("Wrong cookie type.")

    def add_cookies(self, cookie_list):
        """
        Adds a cookie to your current session.
        Usage:
            cookie_list = [
                {'name' : 'foo', 'value' : 'bar'},
                {'name' : 'foo', 'value' : 'bar'}
            ]
            self.add_cookie(cookie_list)
        """
        if isinstance(cookie_list, list):
            for cookie in cookie_list:
                if isinstance(cookie, dict):
                    self.driver.add_cookie(cookie)
                else:
                    raise TypeError("Wrong cookie type.")
        else:
            raise TypeError("Wrong cookie type.")

    def delete_cookie(self, name):
        """
        Deletes a single cookie with the given name.
        Usage:
            self.delete_cookie('my_cookie')
        """
        self.driver.delete_cookie(name)

    def delete_all_cookies(self):
        """
        Delete all cookies in the scope of the session.
        Usage:
            self.delete_all_cookies()
        """
        self.driver.delete_all_cookies()

    @staticmethod
    def sleep(sec):
        """
        Usage:
            self.sleep(seconds)
        """
        time.sleep(sec)
