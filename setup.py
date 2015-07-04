from setuptools import setup, find_packages
import dashdoord

setup(name='dashdoord',
      version=initiative_manager.__version__,
      description='A Dashboard for your Door',
      author='Greg Fertel',
      author_email='greg.fertel@gmail.com',
      url='',
      packages=find_packages(),
      classifiers=[
          'Framework :: Flask',
          'Development Status :: 1 - Alpha',
          'Environment :: Web Environment',
          'Programming Language :: Python',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Python Modules', ],
      include_package_data=True,
      zip_safe=False,
      )
