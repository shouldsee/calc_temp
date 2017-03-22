from runipy.notebook_runner import NotebookRunner
from IPython.nbformat.current import read

from os import environ
from subprocess import call

file_ipynb='calc_temp.ipynb';
# file_ipynb='tst.ipynb';
environ['input_rulestr'] = '1cde2410a7da1cdd2db0b6a937';
call(["runipy", file_ipynb])

notebook = read(open(file_ipynb), 'json')
r = NotebookRunner(notebook)
r.run_notebook()

from nbconvert import HTMLExporter
import codecs
import nbformat
exporter = HTMLExporter()
# execfile()
from IPython.nbformat.current import write
write(r.nb, open("temp.ipynb", 'w'), 'json')

output_notebook = nbformat.read("temp.ipynb", as_version=4)
# output, resources = exporter.from_notebook_node(output_notebook)
output, resources = exporter.from_notebook_node(output_notebook)
codecs.open('test.html', 'w', encoding='utf-8').write(output)