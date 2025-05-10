uv build --no-sources
uv build --no-sources --package ExcelMCP
uv publish --token pypi-AgEIcHlwaS5vcmcCJGRmOGY1YzFhLTEyMTMtNDg3MS05Yzg0LTNjYjg2NzIyMTlmNAACKlszLCIzMTY3ZDdhYS0xOWQ1LTRlM2UtYTRiZC02OTE0NTMzN2VmYjUiXQAABiB8t90RJlg00nBSUAnu2xkEaArXVruvoOwnjpHvJ44SQw
uv run --with excelmcp --no-project --refresh-package excelmcp -- python -c "import excelmcp"
uvx excelmcp