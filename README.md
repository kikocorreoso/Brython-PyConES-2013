Brython-PyConES-2013
====================

My talk about Brython at PyConES 2013

The Brython repository can be found on [Bitbucket](https://bitbucket.org/olemis/brython/overview)

The talk was made using the IPython notebook, revealJS and the awesome posts by [Damian Avila](http://www.damian.oquanta.info/posts/hide-the-input-cells-from-your-ipython-slides.html).

How to create the HTML5 slides
==============================

    ipython3 nbconvert 'name of the ipynb.ipynb' --to slides --template output-toggle
    
How to run the apps
===================

    cd apps/
    python -m http.server
    

