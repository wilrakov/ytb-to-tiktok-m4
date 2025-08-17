from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ytb-to-tiktok",
    version="1.0.0",
    author="Votre Nom",
    author_email="votre.email@example.com",
    description="Outil pour télécharger des vidéos YouTube et les découper en segments pour TikTok",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/votre-username/ytb-to-tiktok",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Video",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ytb-to-tiktok=ytb_to_tiktok.cli:main",
        ],
    },
    keywords="youtube, video, download, split, tiktok, social media",
    project_urls={
        "Bug Reports": "https://github.com/votre-username/ytb-to-tiktok/issues",
        "Source": "https://github.com/votre-username/ytb-to-tiktok",
    },
)
