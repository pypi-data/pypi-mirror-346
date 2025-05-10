uv build --no-sources
uv build --no-sources --package ExcelMCP
uv publish --token pypi-AgEIcHlwaS5vcmcCJDhkY2U3MzFmLTZkMjAtNGM0ZC04NjJmLWM5ODM0ZTdhNTUyMwACKlszLCIzMTY3ZDdhYS0xOWQ1LTRlM2UtYTRiZC02OTE0NTMzN2VmYjUiXQAABiAPviA9JeTzCkQFkiCbgikxI1LS-c9KaiRnqxIW8do9mQuv
uv run --with excelmcp --no-project --refresh-package excelmcp -- python -c "import excelmcp"
uvx excelmcp