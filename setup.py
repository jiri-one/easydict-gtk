from setuptools import setup

with open('README.md') as f:
	long_description = ''.join(f.readlines())

setup(
	name='easydict-gtk',
	version='v0.3.6',
	description='The first open source translator which is completely open with dictionary data too.',
	long_description=long_description,
	long_description_content_type="text/markdown",
	variant="GFM",
	author='Jiří Němec',
	author_email='nemec@jiri.one',
	keywords='translator,dict',
	license='GPL3',
	url='https://github.com/jiri-one/easydict-gtk',
	include_package_data=True,
	classifiers=[
		'Intended Audience :: End Users/Desktop',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Operating System :: POSIX :: Linux',
		'Programming Language :: Python',
		'Programming Language :: Python :: Implementation :: CPython',
		'Programming Language :: Python :: 3',
		'Environment :: X11 Applications :: GTK',
		],
	python_requires=">=3.7",
	zip_safe=False,	
	install_requires=['tinydb', 'orjson', 'pycairo', 'PyGObject'],
	entry_points={
		'console_scripts': [
				'easydict-gtk = easydict.src.easydict:main',
				],
			},	
)
