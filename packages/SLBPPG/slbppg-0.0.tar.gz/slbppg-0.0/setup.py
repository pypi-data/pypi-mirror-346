from setuptools import setup, find_packages

setup(name='SLBPPG',
      version='0.0',
      description='Predict stress index by ppg',
      packages=find_packages(),
      author_email='i.grishanow@gmail.com',
      install_requires=['neurokit2==0.2.10', 'catboost', 'numpy', 'pandas', 'scipy', 'opencv-python'],
      python_requires='>=3.7'
      )