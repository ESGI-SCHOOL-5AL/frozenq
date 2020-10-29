from setuptools import setup

setup(
    name="frozenq",
    version="0.1.0",
    description="quantique frozen bubble like game",
    author="lustasag, akurtaliqi, System-Glitch, ulphidius, Dreamsplutox, Inarius",
    install_requires=[
        "numpy",
        "qiskit",
        "matplotlib"
    ],
    entry_points={
        "gui_scripts": [
            "frozenq = __main__:main"
        ]
    }
)
