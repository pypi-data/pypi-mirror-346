# setup.py
from setuptools import setup, find_packages

setup(
    name="francalc",          # nome no PyPI
    version="0.4.0",
    author="Lukydnomo",
    packages=find_packages(),       # encontra fran_calculator e fran_calculator.calculations
    include_package_data=True,
    install_requires=[              # só se você tiver deps externas
        "requests", "colorama", "pyqt5"
    ],
    entry_points={                  # se quiser criar script 'franCalc' no PATH
        "console_scripts": [
            "franCalc = fran_calc.fran_calc:main",
            "franCalc-terminal = fran_calc.fran_calc_terminal:main"
        ],
    },
)
