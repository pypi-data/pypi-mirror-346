from setuptools import setup
from pathlib import Path

this_dir = Path(__file__).parent
long_desc = (this_dir / "README.md").read_text(encoding="utf-8")

setup(
    name="trustlint",
    version="1.0.3",
    packages=["trustlint"],
    package_dir={"trustlint": "."},
    package_data={"trustlint": ["index.ts"]},
    include_package_data=True,
    python_requires=">=3.7",
    long_description=long_desc,
    long_description_content_type="text/markdown",
)
