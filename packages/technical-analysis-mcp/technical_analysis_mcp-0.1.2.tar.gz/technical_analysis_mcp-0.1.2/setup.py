from setuptools import setup, find_packages

setup(
    name='technical-analysis-mcp',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
    ],
    author='Li Bin',
    author_email='binlish81@qq.com',
    description='Technical analysis tools for investment advisory',
    entry_points={
        'console_scripts': [
            'technical-analysis-mcp=technical_analysis.main:main',
            'stock_mcp=technical_analysis.main:main'
        ]
    }
)