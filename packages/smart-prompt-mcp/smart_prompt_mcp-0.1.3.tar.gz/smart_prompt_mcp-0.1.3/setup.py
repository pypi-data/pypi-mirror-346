from setuptools import setup, find_packages

setup(
    name="smart_prompt_mcp",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        "fastmcp",
    ],
    entry_points={
        'console_scripts': [
            'smart-prompt-mcp=smart_prompt_mcp:main',
        ],
    },
    author="MuJiayi",
    description="一个智能提示词MCP服务器",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords="mcp, prompt, template",
    python_requires=">=3.6",
)
