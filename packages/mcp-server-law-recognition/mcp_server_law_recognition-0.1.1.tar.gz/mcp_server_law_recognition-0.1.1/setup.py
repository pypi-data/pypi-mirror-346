from setuptools import setup, find_packages

# 读取 README.md
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# 读取 LICENSE （仅在 dynamic = ["license"] 时需要）
with open("LICENSE", "r", encoding="utf-8") as f:
    license_text = f.read().strip()

setup(
    name="mcp_server_law_recognition",
    version="0.1.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    # license=license_text,

)