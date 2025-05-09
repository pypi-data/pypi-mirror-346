from setuptools import setup, find_packages

setup(
    # Let pyproject.toml handle most metadata & dynamic versioning.
    # Explicitly find packages in 'src' layout.
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    # Ensure generated files are included.
    include_package_data=True,
    package_data={
        "perceptic_core_client": ["**/*"],
    },
)