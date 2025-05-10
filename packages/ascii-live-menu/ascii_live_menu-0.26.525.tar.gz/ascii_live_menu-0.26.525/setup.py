from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    page_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="ascii_live_menu",
    version="0.26.525",
    author="Kelven Vilela",
    author_email="kelvenserejo@gmail.com",
    description="Description",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KelvenVS/ASCII_Live_Menu.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.1',
        entry_points={
        "console_scripts": [
            "ascii_menu=ascii_live_menu.main:menu"
        ]
    },
)