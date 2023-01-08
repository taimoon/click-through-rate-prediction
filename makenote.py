import os
files = [
    "intro.ipynb",
    "EDA.ipynb",
    "preprocess and model.ipynb"
]
output_name = "final.ipynb"

cmd = "nbmerge " + " ".join(files) + " -o " + output_name
os.system(cmd)