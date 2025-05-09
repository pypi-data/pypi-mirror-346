#!/bin/bash

# 配置 TestPyPI 用户名和 API Token
TEST_PYPI_USERNAME="__token__"
TEST_PYPI_API_TOKEN="pypi-AgENdGVzdC5weXBpLm9yZwIkN2NjZDU1MDMtYjIwMC00MTEzLTkxNzUtMDIzOGFjMmU1MDMxAAIqWzMsIjMxZWM3OWUwLWJjNjgtNGVkMS1iOTZkLWQ1YmQzM2JlMDIxNyJdAAAGIFYdQ2gdukYxbqdIlbd0bJqtXMoubhVQPID7z7ULqZqO"

PYPI_USERNAME="__token__"
PYPI_API_TOKEN="pypi-AgEIcHlwaS5vcmcCJGYwYzM3ZDRmLThmYTEtNDIyMy05ODU4LTg4NTk2MmYxOGQ0OQACKlszLCI1YzA4NzI0Zi1hYjFlLTQ2ZjgtOTBkZC0zMmM4MTc5MDI3NDAiXQAABiAVOTL71cay7keiThRxX21QV73SHB6gm7x7K1IBQ3YvQg"

# 清理旧的构建文件
rm -rf dist/

# 构建包
echo "Building package..."
python -m build

# 上传到 TestPyPI
echo "Uploading to TestPyPI..."
twine upload \
    --repository-url https://test.pypi.org/legacy/ \
    --username "$TEST_PYPI_USERNAME" \
    --password "$TEST_PYPI_API_TOKEN" \
    dist/*

echo "Done!"

pip uninstall xiyan-mcp-server
pip install --index-url https://test.pypi.org/simple/ --no-deps xiyan-mcp-server==0.1.7.dev0