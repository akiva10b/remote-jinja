import pathlib

from setuptools import setup

here = pathlib.Path(__file__).parent
readme_path = here / "README.md"
requirements_path = here / "requirements.txt"


with readme_path.open() as f:
    README = f.read()

setup(
    name='remote-jinja',
    version='0.1.61',
    description='Handles remote templates for ongoing projects with Jinja',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Akiva Berger',
    author_email='akiva10b@gmail.com',
    url='https://github.com/akiva10b/remote-jinja.git',
    packages=["remote_jinja"],
    classifiers=[
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=[
        'Jinja2',
    ],
    python_requires='>=3.5.3'
)