from distutils.core import setup
setup(name='pygtkspellchecker',
      version='1.0',
      packages=['gtkspellcheck', 'pylocale'],
      package_data={'pylocale' : ['locales.db', 'locales/*/*/*']})
