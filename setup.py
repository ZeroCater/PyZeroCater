from setuptools import setup, find_packages

version = '0.0.1'

setup(name='zerocater',
      version=version,
      description="Python interface to ZeroCater",
      long_description='',
      keywords='zerocater food delivery meal planning catering lunch',
      author='ZeroCater',
      author_email='tech@zerocater.com',
      url='https://zerocater.com',
      license='MIT',
      packages=find_packages(),
      classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
      ],
      include_package_data=True,
      zip_safe=False
  )