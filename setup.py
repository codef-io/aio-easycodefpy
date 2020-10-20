import ast
from setuptools import setup, find_packages


def get_metadata(resource):
    filename = 'aio_easycodefpy/__init__.py'
    with open(filename, 'r') as f:
        tree = ast.parse(f.read(), filename)
    for node in tree.body:
        if (isinstance(node, ast.Assign) and
                node.targets[0].id == resource):
            return ast.literal_eval(node.value)

    raise ValueError(f'could not find {resource}')


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()


requires = [
    'aiofile>=3.1.1',
    'aiohttp>=3.6.3',
    'cchardet>=2.1.6',
    'pycryptodome>=3.9.8',
    'typing_extensions>=3.7.4.3',
]


setup(
    name=get_metadata('__title__'),
    version=get_metadata('__version__'),
    author=get_metadata('__author__'),
    author_email='codef.io.dev@gmail.com',
    description='Easily develop codef api',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/codef-io/aio-easycodefpy.git',
    packages=find_packages(exclude=['cmd']),
    keywords=[
        'easycodef',
        'codef',
        'codef-api',
        'codef-py',
        'codef-python'
    ],
    python_requires='>=3.5',
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    install_requires=requires
)