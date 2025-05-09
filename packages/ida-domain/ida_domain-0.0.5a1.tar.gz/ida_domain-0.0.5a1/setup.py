from setuptools import setup, find_packages

setup(
    name="ida-domain",
    version="0.0.5-alpha.1",
    author="Hex-Rays SA",
    author_email="support@hex-rays.com",
    description="IDA Domain API",
    long_description="""
# IDA Domain API
\n**⚠️ This is a alpha pre-release version. APIs may change without notice.**


## The IDA Domain API provides a Domain Model on top of IDA SDK

## Usage example:

```python
import ida_domain

db = ida_domain.Database()
if db.open("program.exe")
  for s in db.segments.get_all()
    print(f"Segment {s.start_ea} - {s.end_ea}")

  for f in db.functions.get_all()
    print(f"Function {f.name}")
```
""",
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
      "Development Status :: 3 - Alpha",
      "License :: OSI Approved :: MIT License",
      "Programming Language :: Python :: 3",
      "Operating System :: OS Independent",
      "Topic :: Software Development :: Disassemblers",
    ],
    packages=["ida_domain", "ida_domain.windows", "ida_domain.macos", "ida_domain.linux"],
    package_dir={
        "ida_domain": "ida_domain",
        "ida_domain.windows": "ida_domain/windows",
        "ida_domain.macos": "ida_domain/macos",
        "ida_domain.linux": "ida_domain/linux",
    },
    include_package_data=True,
    package_data={
        "ida_domain": ["*.py"],
        "ida_domain.windows": ["*.py", "*.pyd", "*.dll"],
        "ida_domain.macos": ["*.py", "*.so", "*.dylib"],
        "ida_domain.linux": ["*.py", "*.so"],
    },
    zip_safe=False,
)
