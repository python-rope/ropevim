from setuptools import find_packages, setup


def get_long_description():
    lines = open("README.rst").read().splitlines(False)
    end = lines.index("Installation")
    return "\n" + "\n".join(lines[:end]) + "\n"


setup(
    name="ropevim",
    version="0.8.1",
    description="A vim plugin for using rope python refactoring library",
    long_description=get_long_description(),
    maintainer="Matej Cepl",
    maintainer_email="mcepl@cepl.eu",
    author="Ali Gholami Rudi",
    author_email="aligrudi@users.sourceforge.net",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    url="https://github.com/python-rope/ropevim",
    license="GNU GPL",
    classifiers=[
        "Development Status :: 6 - Mature",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Topic :: Software Development",
    ],
    install_requires=["ropemode"],
)
