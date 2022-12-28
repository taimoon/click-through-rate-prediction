import os
files = [
    "intro.ipynb",
    "file1.ipynb"
]
output_name = "final.ipynb"

cmd = "nbmerge " + " ".join(files) + " -o " + output_name
os.system(cmd)