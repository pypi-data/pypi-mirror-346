from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ruspython_translator", # Уникальное имя для PyPI
    version="0.1.0", # Версия твоей библиотеки
    author="Твое Имя или Никнейм",
    author_email="твой@email.com",
    description="Библиотека для выполнения Python кода с русскими ключевыми словами",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/твой_ник/ruspython_translator", # Ссылка на репозиторий, если есть
    py_modules=["ruspython"], # Указываем наш модуль
    # Если бы ruspython.py был в папке, например, src/ruspython_translator/ruspython.py,
    # то использовали бы packages=find_packages(where="src"), package_dir={"": "src"}
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", # Выбери лицензию
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Interpreters",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Natural Language :: Russian",
    ],
    python_requires='>=3.6', # Минимальная версия Python
    keywords='russian python, python на русском, транслятор, интерпретатор',
)