from setuptools import setup
from glob import glob

with open("progression_qc/VERSION") as f:
    version = f.read()[8:]

setup(
    name="progression_qc",
    version=version,
    description="progression_qc est un compilateur/validateur pour la production de d'exercices pour Progression. progression_qc reçoit sur l'entrée standard ou en paramètre un fichier YAML contenant la description d'une question et reproduit sur la sortie standard le résultat traité et validé.",
    url="https://git.dti.crosemont.quebec/progression/validateur",
    author="Patrick Lafrance",
    author_email="plafrance@crosemont.qc.ca",
    license='GPLv3+',
    packages=["progression_qc", "schemas"],
    data_files=[("schemas", glob("schemas/*.json"))],
    include_package_data=True,
    package_data={"progression_qc": ["VERSION"]},
    install_requires=["jsonschema", "pyyaml-include==1.4.1", "werkzeug"],
    classifiers=['Programming Language :: Python :: 3'],
)
