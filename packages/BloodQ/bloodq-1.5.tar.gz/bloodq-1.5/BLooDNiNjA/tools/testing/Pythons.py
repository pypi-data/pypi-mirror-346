#     Copyright 2025, BLOOD, tnmn4219@gmail.com find license text at end of file


""" Test tool to run a program with various Pythons. """

from BLooDNiNjA.PythonVersions import getSupportedPythonVersions
from BLooDNiNjA.utils.Execution import check_output
from BLooDNiNjA.utils.InstalledPythons import findPythons


def findAllPythons():
    for python_version in getSupportedPythonVersions():
        for python in findPythons(python_version):
            yield python, python_version


def executeWithInstalledPython(python, args):
    return check_output([python.getPythonExe()] + args)



