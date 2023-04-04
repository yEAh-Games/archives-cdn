#!/usr/bin/env python3

# Copyright (c) 2017 Ognjen Galic
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import os.path

import time

version = "1.1"

header = (
"<html>"
"<head>"
"    <title>Index of {}</title>"
"</head>"
"<body bgcolor=\"white\">"
"    <h1>Index of {}</h1>"
"    <hr>"
"    <pre>"
)

footer = (
"   </pre>"
"   <hr>"
"   <span style=\"font-size: 12px\">generated by </span><a style=\"font-size: \
    12px\" href=\"https://github.com/smclt30p/mkindex\">mkindex.py {}</a>"
"</body>"
"</html>".format(version)
)

def getlink(path, file, isDir):

    fileLen = len(file)
    filesz = os.path.getsize(path + "/" + file)
    mtime = os.path.getmtime(path + "/" + file)
    mtime = time.strftime('%d-%b-%Y %H:%M', time.localtime(mtime))


    if not isDir:
        return "<a href=\"{}\">{}</a>{}{}           {}<br>".format(file, file, (50 - fileLen) * " ", mtime , filesz)
    else:
        return "<a href=\"{}\">{}/</a>{}{}           -<br>".format(file, file,  (49 - fileLen) * " ", mtime)



def listfiles(path):

    displaypath = path

    if path == ".":
        displaypath = "/"
    elif displaypath.startswith("./"):
        displaypath = displaypath[1:]

    idx = open(path + "/index.html", "w")

    # Write the header
    idx.write(header.format(displaypath, displaypath))

    # Write back link
    idx.write("<a href=\"..\">..</a><br>")

    # Write directories first
    for file in os.listdir(path):
        if os.path.isdir(path + "/" + file):
            idx.write(getlink(path, file, True))
            listfiles(path + "/" + file)

    # ... then write files
    for file in os.listdir(path):
        if not os.path.isdir(path + "/" + file):
            if file.endswith("index.html"):
                continue
            idx.write(getlink(path, file, False))

    idx.write(footer)
    idx.close()

def main():
    listfiles(".")

if __name__=="__main__":
    main()
