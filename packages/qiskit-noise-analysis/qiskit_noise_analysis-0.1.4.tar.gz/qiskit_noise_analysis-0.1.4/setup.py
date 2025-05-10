from setuptools import setup, find_packages

with open('README.md','r') as f:
    description = f.read() 

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()


setup(
    name = 'qiskit_noise_analysis',
    version='0.1.4',
    author = 'Mohit Joshi',
    author_email='joshimohit@bhu.ac.in',
    description='A qiskit based library to estimate resources and analyse noise in the quantum circuits.',

    packages=find_packages(),

    # entry_points={
    #     'console_scripts': [
    #         'qiskit-hello = qiskit_noise_analysis:hello'
    #     ]
    # },

    long_description=description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.13',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires= '>=3.13',
    install_requires= requirements,
    url='https://github.com/joshicoding/qiskit_noise_analysis',
    project_urls={
        'Bug Tracker': 'https://github.com/joshicoding/qiskit_noise_analysis/issues',
    },
)