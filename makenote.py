import os
files = [
    "report.ipynb",
    "EDA.ipynb",
    "preprocess and model.ipynb"
]
quote = lambda f : f'"{f}"'

output_name = 'final.ipynb'

if output_name is None:
    output_name = "ignore_" + "_".join([os.path.splitext(nm)[0] for nm in files]) + ".ipynb"

    output_name = quote(output_name)


files = [quote(f) for f in files]
cmd = "nbmerge " + " ".join(files) + " -o " + output_name
os.system(cmd)
print(output_name)
