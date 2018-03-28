#!/usr/bin/python
# -*- coding: UTF-8 -*-

import getopt
import sys
import re

infile = ''
# ./酒店旅游@度假/com.meituan.android.travel:mttravel:9.1.0.18/com/meituan/android/travel/triphomepage/block/TripCategoryView.java:23:import com.meituan.android.base.util.ColorUtils;
# ./金融服务/com.meituan.android.pay.quickpass:library:mainRelease:0.7.7/com/meituan/android/quickpass/manage/lib/service/APDUIntentService.java:9:import com.meituan.android.base.util.ServiceForegroundHelper;
pattern = re.compile(r'^\./(?P<module>.+\d+(?:\.\d+)+[^/]*).*\.java:\d+:(?P<referent>.+);$')

keywords_dict = {}


def parse_args(argv):
    global infile
    try:
        opts, args = getopt.getopt(argv, "hf:", ["file=", "help"])
    except getopt.GetoptError:
        print 'usage: main_logic.py <file>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print 'usage: main_logic.py <file>'
            sys.exit()
        elif opt in ("-f", "--file"):
            infile = arg
    if (not infile) and len(args) > 0:
        infile = args[0]
    if not infile:
        print 'usage: main_logic.py <file>'
        sys.exit(2)

    print '输入的文件为：', infile


def analyse_file():
    with open(infile) as f:
        for line in f:
            # print line
            match = pattern.match(line)
            if match:
                module = match.group('module')
                keyword = match.group('referent')
                # print keyword, module
                construct_model(keyword, module)


def construct_model(keyword, module):
    modules_dict = keywords_dict.get(keyword)
    if not modules_dict:
        keywords_dict[keyword] = {module: 1}
        return
    else:
        # modules_dict = {}
        modules_dict[module] = modules_dict.get(module, 0) + 1


def print_text():
    for keyword, modules in keywords_dict.iteritems():
        for module, count in modules.iteritems():
            print keyword.ljust(80), module.ljust(80), str(count).rjust(5)


def print_tree():
    for keyword, modules in keywords_dict.iteritems():
        print keyword
        for module, count in modules.iteritems():
            print ''.ljust(3), '|'.ljust(6, '_'), module.ljust(80), str(count).rjust(5)


if __name__ == "__main__":
    parse_args(sys.argv[1:])
    analyse_file()
    print '统计结果如下:'
    print_tree()
