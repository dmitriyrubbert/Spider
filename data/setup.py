from distutils.core import setup
import py2exe
includes = ['Tkinter', 'ttk','tkFileDialog','threading','time','pycurl','lxml','lxml.etree', 'lxml._elementpath', 'grab','grab.ext',
	'grab.ext.text','grab.transport','grab.transport.curl','grab.tools',
	'sqlalchemy','sqlalchemy.orm','re']

packages = ['sqlalchemy.dialects.sqlite']


setup(
    windows=[{'script':'spider.py','icon_resources':[(1,'icon.ico')]}],
    options = {'py2exe': {'includes': includes, 'packages': packages }}
    )
