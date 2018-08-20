from distutils.core import setup

setup(
    name='PharosController',
    version='0.1',
    packages=['tests', 'pharos', 'pharos.view', 'pharos.view.GUI', 'pharos.model', 'pharos.model.daq', 'pharos.model.lib',
              'pharos.model.laser', 'pharos.model.stage', 'pharos.model.experiment', 'pharos.controller',
              'pharos.controller.santec', 'pharos.controller.keysight'],
    url='https://uetke.com',
    license='MIT',
    author='Aquiles',
    author_email='aquiles@uetke.com',
    description='Pharos Controller for Utrecht University',
)
