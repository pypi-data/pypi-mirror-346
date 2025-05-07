from setuptools import setup, find_packages

setup(
    name="PyThinkDesign",          # 包名（pip install 时用的名称）
    version="0.1.11",            # 版本号
    author="cscad",
    author_email="cscad@cscad.com",
    description="python sdk for thinkdesign",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),   # 自动发现所有包
    package_data={  # 关键配置：指定要包含的非 Python 文件
        "PyThinkDesign": ["*.pyd", "*.dll"]
    },
    install_requires=[          # 依赖的其他包（可选）
        "requests>=2.25.1",
        "pywin32",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",    # Python 版本要求
)