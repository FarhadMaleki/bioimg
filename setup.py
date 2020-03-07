import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='bioimg',  
     version='0.1',
     scripts=['bioimg'] ,
     author="Farhad Maleki",
     description="Easy way to work with images in python",
     long_description=long_description,
     url="https://github.com/FarhadMaleki/bioimg",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
