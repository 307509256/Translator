#!/usr/bin/env python
# _*_ coding:utf-8 _*_

__author__ = 'libw'

"""
date : 2016-8-6 sa
sys : win 10.1 pro
python version : 2.7.9
memo : 在安装第三方包全部失败的悲伤情绪中

定义一个类，传入需要翻译的单词，进行逻辑处理。
也方便打包供其他类库调用
"""

import json
from textwrap import wrap

try:
    import urllib2 as request
    from urllib import quote
except:
    raise ("引用出现问题")


# from urllib import request
#     from urllib.parse import quote
class Translator:
    __doc__ = "翻译类，含有主要逻辑"

    # 内置函数
    def __init__(self, to_lang, from_lang='en'):
        """
        :type to_lang: str
        """
        self.from_lang = from_lang
        # 判断参数为object
        assert isinstance(to_lang, object)
        self.to_lang = to_lang
        self.source_list = []

    # 公共函数
    def translate(self, source):
        """

        :type source: object
        """
        if self.to_lang == self.from_lang:
            assert isinstance(source, object)
            return source
        self.source_list = wrap(source, 1000, replace_whitespace=False)
        return ' '.join(self._get_translation_from_translater(s) for s in self.source_list)

    # 私有函数
    def _get_translation_from_translater(self, source):
        jsons = self._get_jsons_from_translater(source)
        data = json.loads(jsons)
        translation = data['responseData']['translatedText']
        if not isinstance(translation, bool):
            return translation
        else:
            matches = data['matches']
            for match in matches:
                if not isinstance(match['translation'], bool):
                    next_best_match = match['translation']
                    break
            return next_best_match

    def _get_jsons_from_translater(self, source):
        escaped_source = quote(source, '')
        headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'}
        api_url = 'http://mymemory.translated.net/api/get?q=%s&langpair=%s|%s'
        # 应用网站API
        req = request.Request(url=api_url % (escaped_source, self.from_lang, self.to_lang), headers=headers)
        r = request.urlopen(req)
        return r.read().decode('utf-8')

def main(defvals=None):
    """
    :rtype: object
    """
    import argparse
    import sys
    import locale

    if defvals is None:
        defvals = {'f': 'en', 't': 'zh'}

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('text', metavar='text', nargs='+', help='a string to translate(use ""when it\'s a sentence)')
    parser.add_argument('-t', '--to', dest='to_lang', type=str, default=defvals['t'],
                        help='To language (e.g. zh, zh-TW, en, ja, ko). Default is '+defvals['t']+'.')
    parser.add_argument('-f', '--from', dest='from_lang', type=str, default=defvals['f'],
                        help='From language (e.g. zh, zh-TW, en, ja, ko). Default is '+defvals['f']+'.')
    args = parser.parse_args()
    translator = Translator(from_lang=args.from_lang, to_lang=args.to_lang)
    for text in args.texts:
        translation = translator.translate(text)
        if sys.version_info.major == 2:
            translation = translation.encode(locale.getpreferredencoding())
            sys.stdout.write(translation)
            sys.stdout.write("\n")

if __name__ == '__main__':
    main()
