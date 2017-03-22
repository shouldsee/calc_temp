from runipy.notebook_runner import NotebookRunner
from IPython.nbformat.current import read
import sys
from os import environ
from subprocess import call

file_ipynb='calc_temp.ipynb';
# file_ipynb='tst.ipynb';

# query = '2dntca_1cde2410a7da1cdd2db0b6a937'
# try:
query = sys.argv[1:];
# except:
query = query[0];
file_html='temp_'+query+'.html';
if not query: 
	print('query not recognised')
	quit()
print(query)
environ['query'] = query;
# call(['ls','-l'])
# ags=["runipy",'--html '+file_html];
# ags=["runipy",'--html '+file_html];
# ags=["runipy",file_ipynb,'temp.ipynb']
# ags=["runipy",
# 	"-o",'temp.ipynb',
# 	"--html",'temp.html']
# print(' '.join(ags));

ags=["runipy",file_ipynb,'temp.ipynb']
call(ags);


# notebook = read(open(file_ipynb), 'json')
# r = NotebookRunner(notebook)
# r.run_notebook()

from nbconvert import HTMLExporter
import codecs
import nbformat
exporter = HTMLExporter()
# # execfile()
# from IPython.nbformat.current import write
# write(r.nb, open("temp.ipynb", 'w'), 'json')

output_notebook = nbformat.read("temp.ipynb", as_version=4)
output, resources = exporter.from_notebook_node(output_notebook)
# output, resources = exporter.from_notebook_node(r.nb);
# output, resources = exporter.from_notebook_node(output_notebook)
codecs.open(file_html, 'w', encoding='utf-8').write(output)