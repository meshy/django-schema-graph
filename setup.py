from setuptools import find_packages, setup


version = '0.0.1'


setup(
    author='Charlie Denton',
    author_email='charlie@meshy.co.uk',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Database',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    description='An interactive graph of your Django model structure.',
    include_package_data=True,
    license='MIT',
    name='django-schema-graph',
    packages=find_packages(),
    url='https://github.com/meshy/django-schema-graph',
    version=version,
)
