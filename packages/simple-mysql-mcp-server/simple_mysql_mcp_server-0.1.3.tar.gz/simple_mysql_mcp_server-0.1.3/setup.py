from setuptools import setup, find_packages

setup(
    name="simple-mysql-mcp-server",
    version="0.1.3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "sqlalchemy",
        "pymysql",
        "cryptography"
    ],
    entry_points={
        "console_scripts": [
            "simple-mcp-server = simple_mysql_mcp_server.main:main"
        ]
    },
    author="Rehan Tariq",
    license="MIT",
    description="A MySQL-compatible MCP server for GitHub Copilot and LLMs.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ]
)
