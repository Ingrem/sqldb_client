from setuptools import setup

setup(
    name='db_contractor',
    version="1.0.0",
    packages=[
        'db_contractor',
    ],
    install_requires=[
        'sqlalchemy',
        'psycopg2-binary',
    ]
)
