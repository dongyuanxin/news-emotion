import re

html_char = {}
html_char['&quot;'] = html_char['&#34;']='"'
html_char['&apos;'] = html_char['&#39;'] = "'"
html_char['&amp;'] = html_char['&#38;'] = '&'
html_char['&lt;'] = html_char['&#60;'] = '<'
html_char['&gt;'] = html_char['&#62;'] = '>'
html_char['&nbsp;'] = html_char['&#160;']= ' '

def Q2B(_char):#全角转半角
    if 65281<=ord(_char)<=65374:
        _char = chr(ord(_char)-65248)
    elif ord(_char)==12288:
        _char = chr(32)
    return _char

def isQ(Char):
    return True if (65281<=ord(Char)<=65374 or ord(Char)==12288) else False

def B2Q(_char):#半角转全角
    if 33<=ord(_char)<=126:
        _char = chr(ord(_char)+65248)
    elif ord(_char)==32:
        _char = chr(12288)
    return _char

def isB(Char):
    return True if (33<=ord(Char)<=126 or ord(Char)==32) else False


def cleanHtml(html_str,special_char=None,to_char=None):

    #这里留个接口，处理特殊字符串
    if special_char:
        special_rule = re.compile('|'.join(set(special_char)))
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
    letter_char = re.compile(r'&[a-z]+;',re.I)
    for char in letter_char.findall(raw):
        raw = re.sub(char,html_char[char],raw)
    '''
    number_char = re.compile(r'&#\d+;',re.I)
    for char in number_char.findall(raw):
        raw = re.sub(char,html_char[char],raw)
    '''

    raw_list = list(raw)
    for i in range(len(raw_list)):
        if isQ(raw_list[i]):
            raw_list[i] = Q2B(raw_list[i])
    raw = ''.join(raw_list)
    
    return raw

def test():
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