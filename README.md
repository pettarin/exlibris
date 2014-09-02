# exlibris

**exlibris** is a tool for adding an ex libris to EPUB eBooks, available as a CLI tool, a GUI tool, and Calibre plugin.

* Version: 1.0.19
* Date: 2014-09-02
* Developer: [Alberto Pettarin](http://www.albertopettarin.it/) ([contact](http://www.albertopettarin.it/contact.html))
* License: the GNU General Public License Version 3 (GPLv3), see LICENSE

There are three main usage cases:

1. a CLI script, useful for batch processing;
2. a GUI tool, useful if you prefer a graphical interface; and
3. a plugin for Calibre.


### Important updates

* 2014-09-02 Please note that exlibris needs substantial code refactoring. Unfortunately, I no longer have time to develop or maintain exlibris. **Please fork and improve.** If you are willing to take it over, please let me know.


## Main library

Look inside the `lib/` directory.


## CLI

Look inside the `cli/` directory.

To get its usage, run it without arguments:

```
$ python exlibris-cli.py
```


## GUI

Look inside the `gui/` directory.

To run it:

```
$ python exlibris-gui.py
```

To get the Italian version:

```
$ python exlibris-gui.py it
```


## Plugin for Calibre

Look inside the `plugin_calibre/` directory.

To compile it locally:

```
$ bash compile_plugin.sh
```

Note that you can get this plugin directly using the Plugin manager inside Calibre.


## License

**exlibris** is released under the GNU General Public License Version 3 (GPLv3).


## Limitations and Missing Features

* Perform real EPUB parsing using an XML parser
* Code clean-up: remove replicated code
* Let the user insert an image as the ex libris (e.g., by building a suitable XHTML page around it)
* Better command line parsing (e.g., by using `argparse`)
* (Plugin Calibre only) Expose shortcut to the Calibre shortcut manager
* (Plugin Calibre only) When using the "Copy EPUB" function, mark the new EPUB (with the ex libris) to distinguish it from the original one 


[![Analytics](https://ga-beacon.appspot.com/UA-52776738-1/exlibris)](http://www.albertopettarin.it)

