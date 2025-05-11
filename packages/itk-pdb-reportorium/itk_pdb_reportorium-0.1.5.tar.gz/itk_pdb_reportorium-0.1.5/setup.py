from setuptools import setup, find_packages

setup(
    name="itk-pdb-reportorium",
    version="0.1.5",
    packages=find_packages(where=".") + ["metadata"],
    include_package_data=True,
    description="This package is specialized for the module-qc-statistical-tools (MQST) and aims to send the output MQST reports to EOS using the SendFileToEOS.py script.",
    author="kenneth wraight,Omar Istaitia, Doyeong Kim, Dimitris Varouchas",
    author_email='kenneth.wraight@glasgow.ac.uk, omar.istaitia@cern.ch, doyeong.kim@cern.ch, dimitris.varouchas@cern.ch',    install_requires=[
        "randomname",
        "scp",
        "paramiko",
    ],
)

