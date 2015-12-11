#!/usr/bin/env python
# encoding: utf-8

import vim
import markdown_parser
import webbrowser
import os, platform
import commands
import threading
import markdown_server
import markdown_lib

def markdownPreviewWithDefaultCodeStyle():
    cssName = vim.eval("a:args1")
    currentpath = commands.getstatusoutput("pwd")[1]

    content = getHead(cssName)
    content += getBuff()
    content += getBody()

    file = open(os.path.join(currentpath, 'tmp.html'), 'w')
    file.write(content)
    file.close()

    url = 'file:///' + currentpath + '/tmp.html'
    webbrowser.open(url)

def markdownPreviewWithCustomCodeStyle():
    cssName     = vim.eval("a:args1")
    codeName    = vim.eval("a:args2")
    currentpath = commands.getstatusoutput("pwd")[1]

    content = getHead(cssName, codeName)
    content += getBuff()
    content += getBody()

    file = open(os.path.join(currentpath, 'tmp.html'), 'w')
    file.write(content)
    file.close()

    url = 'file:///' + currentpath + '/tmp.html'
    webbrowser.open(url)

SERVER = None
def liveMarkdownPreviewStart():
    global SERVER
    SERVER = markdown_server.Server(20013)
    threads = []
    threads.append(SERVER)
    for thread in threads:
        thread.start()

    content = getHead()
    content += getBuff()
    content += getBody()
    currentpath = commands.getstatusoutput("pwd")[1]
    file = open(os.path.join(currentpath, 'tmp.html'), 'w')
    file.write(content)
    file.close()
    url = 'file:///' + currentpath + '/tmp.html'
    webbrowser.open(url)

def liveMarkdownPreviewEnd():
    global SERVER
    if SERVER != None:
        SERVER.endServer()

def getBuff():
    buff = ''
    for line in vim.current.buffer:
        buff += line + '\n'
    return markdown_parser.markdown(buff)

def getHead(cssstyle = 'Github', codesytle = 'default'):
    if vim.eval("exists('g:MarkDownResDir')") == '1':
        cssDir = vim.eval('g:MarkDownResDir')
    else:
        if platform.system() == 'Windows':
            cssDir = os.path.join(vim.eval('$HOME'), 'vimfiles', 'MarkDownRes')
        elif vim.eval("has('nvim')") == '1':
            cssDir = os.path.join(vim.eval('$HOME'),'.nvim', 'MarkDownRes')
        else:
            cssDir = os.path.join(vim.eval('$HOME'), '.vim', 'MarkDownRes')

    content = "<html>\n"
    content += '<meta charset="UTF-8" />\n'
    content += '<head>'
    content += '<link rel="stylesheet" href="' + cssDir + '/code-styles/' + codesytle + '.css">\n'
    content += '<link href="' + cssDir + '/' + cssstyle + '.css" media="all" rel="stylesheet"/>\n'
    content += '<script src="' + cssDir + '/js/highlight.min.js"></script>\n'
    content += '<script src="' + cssDir + '/js/highlight.pack.js"></script>\n'
    content += '<script src="' + cssDir + '/js/jquery-1.11.3.min.js"></script>\n'
    content += '<script>hljs.initHighlightingOnLoad();</script>\n'
    content += '</head>\n<body id="content">'
    return content

def getBody():
    return "</body></html>\r\n\r\n\r\n\r\n"
