from setuptools import setup

setup(
      name='svg_batch_exporter',
      packages=['svg_batch_exporter'],
      version='0.3',
      description='A rule based Inkscape powered SVG exporter to wide variety of image formats',
      long_description=open('README.rst').read(),
      url="https://github.com/anselm94/inkscape-svg-batch-exporter",
      download_url="https://codeload.github.com/anselm94/inkscape-svg-batch-exporter/zip/master",
      author='Merbin J Anselm',
      author_email='merbinjanselm@gmail.com',
      license=open('LICENSE.txt').read(),
      requires = ["subprocess", "os", "sys", "argparse", "json", "tempfile", "PIL"],
      keywords = ["inkscape", "batch", "exporter", "svg", "folder"],
      classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities"    ,
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        ],
      )
