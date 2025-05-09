from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="linkmanager-plugin-base",  
    version="0.1", 
    author="Razzery",  
    author_email="karamelkafe23@gmail.com",  
    description="Базовый класс для создания и использования плагинов Link Manager",  
    long_description=long_description,  
    long_description_content_type="text/markdown",  
    url="https://t.me/news_about_link_manager",  
    packages=find_packages(),  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  
    
)