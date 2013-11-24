Brython-PyConES-2013
====================

My talk about Brython at PyConES 2013

The Brython repository can be found on [Bitbucket](https://bitbucket.org/olemis/brython/overview)

The talk was made using the IPython notebook, revealJS and the awesome posts by [Damian Avila](http://www.damian.oquanta.info/posts/hide-the-input-cells-from-your-ipython-slides.html).

How to create the HTML5 slides
==============================

    ipython3 nbconvert 'Brython talk PyConEs 2013.ipynb' --to slides --template output-toggle
    

How to see the slides and the apps working
==========================================

Change to the location where the html files are placed and run

    python -m http.server
    
and then open a browser at `http://0.0.0.0:8000/`

Apps running on Gdrive
======================

Shared folder is [here](https://drive.google.com/folderview?id=0B4OEtv-kAaTBUlE2OU9QcHVpT3c&usp=sharing).

* [colors](https://googledrive.com/host/0B4OEtv-kAaTBSllJM19hdkpCeTQ/colors_bootstrapped.html)

* [table](https://googledrive.com/host/0B4OEtv-kAaTBSllJM19hdkpCeTQ/table_bootstrapped.html)

* [puzzle](https://googledrive.com/host/0B4OEtv-kAaTBSllJM19hdkpCeTQ/puzzle_bootstrapped.html)

* [jsonp](https://googledrive.com/host/0B4OEtv-kAaTBSllJM19hdkpCeTQ/jsonp_bootstrapped.html)

* [hangman](https://googledrive.com/host/0B4OEtv-kAaTBSllJM19hdkpCeTQ/hangman_bootstrapped.html)

* [to-do](https://googledrive.com/host/0B4OEtv-kAaTBSllJM19hdkpCeTQ/todo_bootstrapped.html)
