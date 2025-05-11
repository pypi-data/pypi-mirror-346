from setuptools import setup, find_packages
from gsdriver import __version__

REQUIRES = [
    "tqdm>=4.64.0",
    "asyncio>=3.4.3",
    "python-dateutil>=2.8.2",
    "pandas>=1.4.2",
    "openpyxl>=3.1.2",
    "bs4>=0.0.1",
    "requests>=2.31.1",
    "aiohttp>=3.9.1",
    "lxml>=4.9.4",
    "PyJWT>=2.9.0",
    "selenium>=4.8.2",
    "selenium-wire>=5.1.0",
    "blinker==1.7.0",
    "webdriver_manager>=4.0.1",
    "pyperclip>=1.8.2",
    "gspread>=5.6.2",
    "google-cloud-bigquery>=3.4.0",
    "holidays>=0.43",
    "workalendar>=17.0.0",
]

setup(
    name="gcp-webdriver",
    version=__version__,
    description="Selenium WebDriver utils with GCP functions",
    url="https://github.com/minyeamer/gsdriver.git",
    author="minyeamer",
    author_email="minyeamer@gmail.com",
    license="minyeamer",
    install_requires=REQUIRES,
    packages=find_packages(),
    keywords=["gcp-webdriver", "webdriver", "gcp"],
    python_requires=">=3.7",
)