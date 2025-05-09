from distutils.core import setup
import sys

# Manually manage the test dependency
install_requires = []

if {'pytest', 'test', 'ptr'}.intersection(sys.argv):
    install_requires.append('pytest-runner')

# Read the README file manually
with open('README.md', 'r') as f:
    long_description = f.read()

# Set up the package using distutils
setup(
    description="nustar-pipeline",
    long_description=long_description,
    version='0.2.26',
    include_package_data=True,
    install_requires=install_requires,  # Manually handle dependencies
)

