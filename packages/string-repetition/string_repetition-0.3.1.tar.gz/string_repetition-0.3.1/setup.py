from setuptools import setup, find_packages
import os

# 读取 README.md 文件内容作为 long_description
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="string_repetition",
    version="0.3.1",
    description="一个高效的字符串重复检测算法",
    long_description=long_description, # 添加 long_description
    long_description_content_type='text/markdown', # 指定内容类型为 Markdown
    author="AdAstraAbyssoque", # 请替换为实际作者名
    author_email="bliu699@outlook.com", # 请替换为实际邮箱
    # url="https://github.com/yourusername/string-repetition", # 可选：添加项目 URL
    packages=find_packages(exclude=["tests*", "examples*"]), # 排除测试和示例目录
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)