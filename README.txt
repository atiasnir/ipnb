==============================
IPython Notebook Utilities
==============================

IPython notebook are great for development and visualzing data,
however, in terms of code sharing and reusing they're quite bad.

If you want to reuse your notebook as a program or import functionality
into other modules, you have a problem. Yes, you can move your 
code into a separate module but then you loose then notebook interface 
and the ability to change it. 

This package contains several utilities to reuse the code in your 
notebook without the need to export/convert it everytime. 


To import a notebook into another module do the following:

	import ipnb.importer
	import my_notebook

	my_notebook.some_cool_method()


You can also run a notebook directly from the command line:

	python -m ipnb.run /path/to/my_notebook.ipynb

Optionally specify '-s' to print the source code to stderr before execution 
starts and '-d' to debug the notebook. Currently the implementation 
will try to use PuDB and fallback to pdb
