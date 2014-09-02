#!/bin/bash

rm -f *.pyc
rm -f ~/.config/calibre/plugins/exlibris_plugin.zip
zip -r ~/.config/calibre/plugins/exlibris_plugin.zip *py *txt images/* ex_libris_examples/


