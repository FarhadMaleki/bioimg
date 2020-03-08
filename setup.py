import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='BioImage',
     version='0.0.1',
     scripts=['BioImage'] ,
     author="Farhad Maleki",
     description="BioImage provides a minimalistic interface for working with medical imaging modalities.",
     long_description=long_description,
     url="https://github.com/FarhadMaleki/bioimg",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
