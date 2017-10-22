"""
清洗网页标签
全角和半角的转换
"""

#encoding:utf-8
import re

# 网页中的字符实体
# 需要更多的补充
html_char = {}
html_char['&quot;'] = html_char['&#34;']='"'
html_char['&apos;'] = html_char['&#39;'] = "'"
html_char['&amp;'] = html_char['&#38;'] = '&'
html_char['&lt;'] = html_char['&#60;'] = '<'
html_char['&gt;'] = html_char['&#62;'] = '>'
html_char['&nbsp;'] = html_char['&#160;']= ' '

def Q2B(_char):
    """
    全角字符转半角字符
    :param _char: 待转换字符
    :return: 转化后的字符
    """
    if 65281<=ord(_char)<=65374:
        _char = chr(ord(_char)-65248)
    elif ord(_char)==12288:
        _char = chr(32)
    return _char

def isQ(Char):
    """
    判断是否是全角字符
    :param Char: 待判断字符
    :return: bool值
    """
    return True if (65281<=ord(Char)<=65374 or ord(Char)==12288) else False

def B2Q(_char):
    """
    半角字符转全角字符
    :param _char: 待转换字符
    :return: 转化后的字符
    """
    if 33<=ord(_char)<=126:
        _char = chr(ord(_char)+65248)
    elif ord(_char)==32:
        _char = chr(12288)
    return _char

# 类似 isQ(Char)
def isB(Char):
    return True if (33<=ord(Char)<=126 or ord(Char)==32) else False


def cleanHtml(html_str,special_char=None,to_char=None):
    """
    清洗html标签
    :param html_str: html文本
    :param special_char: 自定义的需要处理的特殊字符列表（迭代器类型）
    :param to_char: special_char的转化目标
    :return: html中的正文部分
    """

    # 如果有需要处理的额外字符
    if special_char:
        special_rule = re.compile('|'.join(set(special_char))) # '|'在正则表达式中代表'或'。所有的特殊字符都要替换
        if not to_char:
            to_char = ''

    #CDATA 部分由 "<![CDATA[" 开始，由 "]]>" 结束：
    cdata_rule = re.compile(r'<![CDATA[.*]]>',re.I | re.S)

    #去除脚本（随时会出现）
    script_rule = re.compile(r'<script.*?</script>',re.I | re.S)

    #取出<head>..</head>和中间的内容，style也在里面，不需要再写了
    head_rule = re.compile(r'<head.*?/head>',re.I | re.S)

    #为了以防一些文本不是全部截取html代码，还是写一下以防万一
    style_rule = re.compile(r'<style.*?/style>',re.I | re.S)

    #处理注释
    comment_rule = re.compile(r'<!.*?>',re.I | re.S)
    
    #处理换行
    br_rule = re.compile(r'<br\s*?/{0,1}>',re.I)

    #html标签
    html_rule = re.compile(r'<.*?/{0,1}>',re.I)

    if special_char:
        raw = special_rule.sub(to_char,html_str)
    else:
        raw = html_str

    raw = cdata_rule.sub('',raw)
    raw = script_rule.sub('',raw)
    raw = head_rule.sub('',raw)
    raw = style_rule.sub('',raw)
    raw = comment_rule.sub('',raw)
    raw = br_rule.sub('\n',raw)
    raw = html_rule.sub('',raw)

    global html_char
    letter_char = re.compile(r'(&[a-z]+;)|(&#\d+;)',re.I)
    for _,__ in letter_char.findall(raw): # _，__分别对应两种形式的字符实体
        if _ not in html_char.keys() and __ not in html_char.keys(): # 针对字符实体不在html_char的情况
            continue
        if _ in html_char.keys():
            raw = re.sub(_,html_char[_],raw)
        else:
            raw = re.sub(__, html_char[__], raw)

    raw_list = list(raw)
    for i in range(len(raw_list)):
        if isQ(raw_list[i]):
            raw_list[i] = Q2B(raw_list[i])
    raw = ''.join(raw_list)
    
    return raw

# 测试函数
def test():
    # 下面是一段html的测试代码
    test_html = """
        
    <div id="sidebar">

    <div id="tools">
    <h5 id="tools_example"><a href="/example/xmle_examples.asp">&nbsp;XML 实例,特殊字符：１５（处理之后应该没有了）</a></h5>
    <h5 id="tools_quiz"><a href="/xml/xml_quiz.asp">&#60;XML 测验&gt;</a></h5>
    <h3>&#39;ｖｅｖｅｖ&#39;</h3>
    </div>

    <div id="ad">
    <script type="text/javascript"><!--
    google_ad_client = "ca-pub-3381531532877742";
    /* sidebar-160x600 */
    google_ad_slot = "3772569310";
    google_ad_width = 160;
    google_ad_height = 600;
    //-->
    </script>
    <script type="text/javascript"
    src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
    </script>
    </div>

    </div>
    """

    print(cleanHtml(test_html,'】１５'))

if __name__=='__main__':
    test()