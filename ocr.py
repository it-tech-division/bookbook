#!/usr/bin/python

try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
import sys, os, re


if not os.path.exists(sys.argv[1]):
    print("File not found : %s" % sys.argv[1])
    sys.exit(-1)

try:

    #result = pytesseract.image_to_string(Image.open(sys.argv[1]), lang='kor')
    result = pytesseract.image_to_string(Image.open(sys.argv[1]))
    title = " ".join(result.splitlines()[:3])
    print(title)
except:
    print("Usage : %s [IMAGE_FILE]" % sys.argv[0])
