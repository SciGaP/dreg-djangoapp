import setuptools

setuptools.setup(
    name="dreg-djangoapp",
    version="0.0.1",
    description="dREG Django app for UI customizations",
    packages=setuptools.find_packages(),
    install_requires=[
        'django>=1.11.16'
    ],
    entry_points="""
[airavata.djangoapp]
dreg_djangoapp = dreg_djangoapp.apps:DregDjangoappConfig
""",
)
