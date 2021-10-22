
# -*- coding:utf-8 -*-
import wx
import sys,traceback,requests,re,datetime
from requests.adapters import HTTPAdapter
requests.packages.urllib3.disable_warnings()



def 网页_COOKIE合并更新(原COOKIE, 新COOKIE):
    '传入的Cookie可以是文本型也可以是字典,返回更新后的COOKIE,字典型'
    最新Cookie = {}
    临时Cookie = {}
    if type(原COOKIE) == str:
        if 原COOKIE.find(";") == -1:
            名称 = 原COOKIE[0:原COOKIE.find("=")].strip(' ')
            值 = 原COOKIE[原COOKIE.rfind(名称) + len(名称) + 1:len(原COOKIE)].strip(' ')
            if 名称 and 值:
                最新Cookie = {名称: 值}
        else:
            cookie数组 = cookie.split(';')
            for x in cookie数组:
                名称 = x[0:x.find("=")].strip(' ')
                值 = x[原COOKIE.rfind(名称) + len(名称) + 1:len(x)].strip(' ')
                if 名称 and 值:
                    最新Cookie[名称] = 值
    else:
        最新Cookie = 原COOKIE

    if type(新COOKIE) == str:
        if 新COOKIE.find(";") == -1:
            名称 = 新COOKIE[0:新COOKIE.find("=")].strip(' ')
            值 = 新COOKIE[新COOKIE.rfind(名称) + len(名称) + 1:len(新COOKIE)].strip(' ')
            if 名称 and 值:
                临时Cookie = {名称: 值}
        else:
            cookie数组 = cookie.split(';')
            for x in cookie数组:
                名称 = x[0:x.find("=")].strip(' ')
                值 = x[新COOKIE.rfind(名称) + len(名称) + 1:len(x)].strip(' ')
                if 名称 and 值:
                    临时Cookie[名称] = 值
    else:
        临时Cookie = 新COOKIE

    for x in 临时Cookie:
        最新Cookie[x] = 临时Cookie[x]

    return 最新Cookie


class 网页返回类型:
    def __init__(self):
        self.源码 = ''
        self.字节集 = b'' #返回字节集,如图片,视频等文件需要
        self.cookie = {}
        self.协议头 = {}
        self.状态码 = 0
        self.原对象 = None
        self.json = {}

class 网页_访问_会话:
    'requests.session()'

    def __init__(self,重试次数=0):
        self._requests = requests.session()
        if 重试次数:
            self._requests.mount('http://', HTTPAdapter(max_retries=重试次数))
            self._requests.mount('https://', HTTPAdapter(max_retries=重试次数))

 
    def 网页_访问(self,url, 方式=0, 参数='', cookie='', 协议头={}, 允许重定向=True, 代理地址=None, 编码=None, 证书验证=False, 上传文件=None, 补全协议头=True,json={},连接超时=15, 读取超时=15):
        """
        :param url: 链接,能自动补全htpp,去除首尾空格
        :param 方式: 0.get 1.post 2.put 3.delete 4.head 5.options
        :param 参数: 可以是文本也可以是字典
        :param cookie: 可以是文本也可以是字典
        :param 协议头: 可以是文本也可以是字典
        :param 允许重定向: True 或 False 默认允许
        :param 代理地址: 账号:密码@IP:端口  或  IP:端口
        :param 编码: utf8,gbk·······
        :param 证书验证: 默认为False,需要引用证书时传入证书路径
        :param 上传文件: {'upload': ('code.png', 图片字节集, 'image/png')}
        :param 补全协议头: 默认补全常规协议头
        :param json: post提交参数时可能使用的类型
        :param 连接超时: 默认15
        :param 读取超时: 默认15
        :return: 返回网页对象
        """

        网页 = 网页返回类型()
        try:
            url = url.strip(' ')
            url = url if url.startswith('http') else 'http://' + url
            _cookie = {}
            _协议头 = {}
            传入参数 = {}
            if url.find('/', 8) != -1:
                host = url[url.find('://') + 3:url.find('/', 8)]
            else:
                host = url[url.find('://') + 3:]

            if type(协议头) == str:
                协议头数组 = 协议头.split('\n')
                for x in 协议头数组:
                    名称 = x[0:x.find(':')].strip(' ')
                    值 = x[x.rfind(名称) + len(名称) + 1:len(x)].strip(' ')
                    if 名称 and 值:
                        _协议头[名称] = 值
            else:
                _协议头 = 协议头

            if 补全协议头:
                if not 'Host' in _协议头:
                    _协议头['Host'] = host
                if not 'Accept' in _协议头:
                    _协议头['Accept'] = '*/*'
                if not 'Content-Type' in _协议头:
                    _协议头['Content-Type'] = 'application/x-www-form-urlencoded'
                if not 'User-Agent' in _协议头:
                    _协议头['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36'
                if not 'Referer' in _协议头:
                    _协议头['Referer'] = url

            if type(cookie) == str:
                if cookie.find(";") == -1:
                    名称 = cookie[0:cookie.find("=")].strip(' ')
                    值 = cookie[cookie.rfind(名称) + len(名称) + 1:len(cookie)].strip(' ')
                    if 名称 and 值:
                        _cookie = {名称: 值}
                else:
                    cookie数组 = cookie.split(';')
                    for x in cookie数组:
                        名称 = x[0:x.find("=")].strip(' ')
                        值 = x[cookie.rfind(名称) + len(名称) + 1:len(x)].strip(' ')
                        if 名称 and 值:
                            _cookie[名称] = 值
            else:
                _cookie = cookie

            传入参数['url'] = url
            传入参数['verify'] = 证书验证
            传入参数['cookies'] = _cookie
            传入参数['headers'] = _协议头
            传入参数['allow_redirects'] = 允许重定向
            if 参数:
                if 方式 == 0:
                    传入参数['params'] = 参数
                else:
                    传入参数['data'] = 参数
            if json:
                传入参数['json'] = json
            if 上传文件:
                传入参数['files'] = 上传文件
            if 代理地址:
                传入参数['proxies'] = {"http": "http://" + 代理地址, "https": "https://" + 代理地址}
            if 连接超时 and 读取超时:
                传入参数['timeout'] = (连接超时, 读取超时)

            # 发送
            if 方式 == 0:
                网页对象 = requests.get(**传入参数)
            elif 方式 == 1:
                网页对象 = requests.post(**传入参数)
            elif 方式 == 2:
                网页对象 = requests.put(**传入参数)
            elif 方式 == 3:
                网页对象 = requests.delete(**传入参数)
            elif 方式 == 4:
                网页对象 = requests.head(**传入参数)
            elif 方式 == 5:
                网页对象 = requests.options(**传入参数)

            if 编码:
                网页对象.encoding = 编码

            网页.原对象 = 网页对象
            网页.源码 = 网页对象.text
            网页.cookie = dict(网页对象.cookies)
            网页.状态码 = 网页对象.status_code
            网页.协议头 = 网页对象.headers
            网页.字节集 = 网页对象.content
            try:
                网页.json = 网页对象.json()
            except:
                pass
        except:
            print(sys._getframe().f_code.co_name, "函数发生异常", url)
            # print("错误发生时间：", str(datetime.datetime.now()))
            # print("错误的详细情况：", traceback.format_exc())
        return 网页



def 网页_访问(url, 方式=0, 参数='', cookie='', 协议头={}, 允许重定向=True, 代理地址=None, 编码=None,证书验证=False, 上传文件=None,补全协议头=True,json={}, 连接超时=15, 读取超时=15):
    """
    :param url: 链接,能自动补全htpp,去除首尾空格
    :param 方式: 0.get 1.post 2.put 3.delete 4.head 5.options
    :param 参数: 可以是文本也可以是字典
    :param cookie: 可以是文本也可以是字典
    :param 协议头: 可以是文本也可以是字典
    :param 允许重定向: True 或 False 默认允许
    :param 代理地址: 账号:密码@IP:端口  或  IP:端口
    :param 编码: utf8,gbk·······
    :param 证书验证: 默认为False,需要引用证书时传入证书路径
    :param 上传文件: {'upload': ('code.png', 图片字节集, 'image/png')}
    :param 补全协议头: 默认补全常规协议头
    :param json: post提交参数时可能使用的类型
    :param 连接超时: 默认15
    :param 读取超时: 默认15
    :return: 返回网页对象
    """

    网页 = 网页返回类型()
    try:
        url = url.strip(' ')
        url = url if url.startswith('http') else 'http://' + url
        _cookie = {}
        _协议头 = {}
        传入参数 = {}
        if url.find('/',8) != -1:
            host = url[url.find('://')+3:url.find('/', 8)]
        else:
            host = url[url.find('://')+3:]

        if type(协议头) == str:
            协议头数组 = 协议头.split('\n')
            for x in 协议头数组:
                名称 = x[0:x.find(':')].strip(' ')
                值 = x[x.rfind(名称) + len(名称)+1:len(x)].strip(' ')
                if 名称 and 值:
                    _协议头[名称] = 值
        else:
            _协议头 = 协议头

        if 补全协议头:
            if not 'Host' in _协议头:
                _协议头['Host'] = host
            if not 'Accept' in _协议头:
                _协议头['Accept'] = '*/*'
            if not 'Content-Type' in _协议头:
                _协议头['Content-Type'] = 'application/x-www-form-urlencoded'
            if not 'User-Agent' in _协议头:
                _协议头['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36'
            if not 'Referer' in _协议头:
                _协议头['Referer'] = url

        if type(cookie) == str:
            if cookie.find(";") == -1:
                名称 = cookie[0:cookie.find("=")].strip(' ')
                值 = cookie[cookie.rfind(名称) + len(名称) + 1:len(cookie)].strip(' ')
                if 名称 and 值:
                    _cookie = {名称: 值}
            else:
                cookie数组 = cookie.split(';')
                for x in cookie数组:
                    名称 = x[0:x.find("=")].strip(' ')
                    值 = x[cookie.rfind(名称) + len(名称) + 1:len(x)].strip(' ')
                    if 名称 and 值:
                        _cookie[名称] = 值
        else:
            _cookie = cookie


        传入参数['url'] = url
        传入参数['verify'] = 证书验证
        传入参数['cookies'] = _cookie
        传入参数['headers'] = _协议头
        传入参数['allow_redirects'] = 允许重定向
        if 参数:
            if 方式 == 0:
                传入参数['params'] = 参数
            else:
                传入参数['data'] = 参数
        if json:
            传入参数['json'] = json
        if 上传文件:
            传入参数['files'] = 上传文件
        if 代理地址:
            传入参数['proxies'] = {"http": "http://" + 代理地址, "https": "https://" + 代理地址}
        if 连接超时 and 读取超时:
            传入参数['timeout'] = (连接超时,读取超时)

        #发送
        if 方式 == 0:
            网页对象 = requests.get(**传入参数)
        elif 方式 == 1:
            网页对象 = requests.post(**传入参数)
        elif 方式 == 2:
            网页对象 = requests.put(**传入参数)
        elif 方式 == 3:
            网页对象 = requests.delete(**传入参数)
        elif 方式 == 4:
            网页对象 = requests.head(**传入参数)
        elif 方式 == 5:
            网页对象 = requests.options(**传入参数)


        if 编码:
            网页对象.encoding = 编码

        网页.原对象 = 网页对象
        网页.源码 = 网页对象.text
        网页.cookie = dict(网页对象.cookies)
        网页.状态码 = 网页对象.status_code
        网页.协议头 = 网页对象.headers
        网页.字节集 = 网页对象.content
        try:
            网页.json = 网页对象.json()
        except:
            pass
    except:
        print(sys._getframe().f_code.co_name, "函数发生异常",url)
        # print("错误发生时间：", str(datetime.datetime.now()))
        # print("错误的详细情况：", traceback.format_exc())
    return 网页


class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='http调试', size=(716, 491),name='frame',style=541072960)
        self.启动窗口 = wx.Panel(self)
        self.Centre()
        self.编辑框url = wx.TextCtrl(self.启动窗口,size=(523, 35),pos=(11, 14),value='',name='text',style=0)
        self.按钮1 = wx.Button(self.启动窗口,size=(81, 35),pos=(601, 15),label='发送',name='button')
        self.按钮1.Bind(wx.EVT_BUTTON,self.按钮1_按钮被单击)
        self.组合框1 = wx.ComboBox(self.启动窗口,value='GET',pos=(540, 18),name='comboBox',choices=['GET', 'POST'],style=16)
        self.组合框1.SetSize((54, 25))
        self.编辑框提交信息 = wx.TextCtrl(self.启动窗口,size=(680, 82),pos=(13, 51),value='提交信息',name='text',style=1073741856)
        self.编辑框cookie = wx.TextCtrl(self.启动窗口,size=(340, 127),pos=(12, 134),value='cookie',name='text',style=1073741856)
        self.编辑框协议头 = wx.TextCtrl(self.启动窗口,size=(340, 126),pos=(353, 134),value='协议头',name='text',style=1073741856)
        self.编辑框返回值 = wx.TextCtrl(self.启动窗口,size=(450, 183),pos=(12, 263),value='',name='text',style=1073741856)
        self.编辑框返回协议头 = wx.TextCtrl(self.启动窗口,size=(230, 183),pos=(465, 263),value='',name='text',style=1073741856)


    def 按钮1_按钮被单击(self,event):
        url=self.编辑框url.GetValue()
        data=self.编辑框提交信息.GetValue()
        xyt=self.编辑框协议头.GetValue()
        cookie=self.编辑框cookie.GetValue()


        pd=self.组合框1.GetStringSelection()
        print(pd)
        if pd == "GET":
                    fhz=网页_访问(url,0,data,cookie,xyt)
                    结果=fhz.源码
                    print(结果)
                    self.编辑框返回协议头.Clear()
                    self.编辑框返回值.Clear()
                    self.编辑框返回协议头.write(str(fhz.协议头))
                    self.编辑框返回值.write(结果)   
        else:
                    fhz=网页_访问(url,1,data,cookie,xyt)
                    结果=fhz.源码
                    print(结果)
                    self.编辑框返回协议头.Clear()
                    self.编辑框返回值.Clear()
                    self.编辑框返回协议头.write(str(fhz.协议头))
                    self.编辑框返回值.write(结果)       

    
        
  

class myApp(wx.App):
    def  OnInit(self):
        self.frame = Frame()
        self.frame.Show(True)
        return True

if __name__ == '__main__':
    app = myApp()
    app.MainLoop()