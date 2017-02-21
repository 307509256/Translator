#!/usr/bin/env python
# -*- coding: utf-8 -*-



from unittest import TestCase
from subprocess import Popen, PIPE, check_output
from translate import Translator
import sys

decode = [lambda x:x, lambda x:x.decode('utf-8')][sys.version_info.major > 2]

# 继承了TestCase类
class TestTranslate(TestCase):

    def test_tranlate_english_to_englsih(self):
        translator = Translator(to_lang="en")
        translation = translator.translate("why")
        self.assertEqual(u"why", translation)
        print "ok"

    def test_translate_english_to_Chinese(self):
        translator = Translator(to_lang="zh")
        translation = translator.translate("why")
        # 返回翻译为 "为什么？"，标点符号为英文
        self.assertEqual(u"为什么？", translation)

    # def test_translate_english_to_Chinese(self):
    #     translator = Translator(to_lang="zh")
    #     translation = translator.translate("why")
    #     self.assertEqual(u"为什么这样说呢？", translation)

# class CommandLineTest():
#     def test_command_line_take_zh_as_default_language(self):
#         result = check_output("translate why".split())
#         self.assertIn(u'为什么', result.decode("utf-8"))

 # 测试模块的应用
if __name__ =='__main__':
    TestCase.main()