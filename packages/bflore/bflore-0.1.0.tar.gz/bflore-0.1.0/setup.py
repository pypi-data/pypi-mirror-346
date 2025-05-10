"""
ملف إعداد مكتبة Bflore للتثبيت باستخدام pip
"""

import os
from setuptools import setup, find_packages

# قراءة ملف الوصف
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# إعداد التثبيت
setup(
    name="bflore",
    version="0.1.0",
    author="Bflore Team",
    author_email="contact@example.com",
    description="مكتبة لتوسيع إمكانيات Flask مع دعم للروابط المحلية المخصصة",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/bflore",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    python_requires=">=3.6",
    install_requires=[
        "flask>=2.0.0",
        "click>=7.0",
    ],
    entry_points={
        "console_scripts": [
            "bflore=bflore.cli:main",
        ],
    },
)