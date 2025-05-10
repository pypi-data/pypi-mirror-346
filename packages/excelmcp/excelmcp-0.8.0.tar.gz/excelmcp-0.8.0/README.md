# ExcelMCP

ExcelMCP server is for AI to Automation Microsoft Excel Application

## Installation
```bash
uvx excelmcp
```

## Usage
```python
import excelmcp as mcp

# Check Excel installation
if mcp.Installed():
    mcp.Launch(visible=False)
    
    # Workbook operations
    if mcp.WorkBook(r"D:\test.xlsx"):
        print(f"Active Workbook: {mcp.ActiveWorkbook()}")
        print(f"Sheets: {mcp.Sheets(r'D:\\test.xlsx')}")

    # Python automation
    mcp.RunPython('''
    The.Excel.ActiveWorkbook.SaveAs("D:\\processed.xlsx")
    The.Excel.Application.Quit()
    ''')
```

## API Reference
### `WorkBook(path: str)`
- Opens/Creates specified workbook
- Returns: True if successful

### `Visible(state: bool)`
- Toggles Excel visibility

### `RunPython(code: str)`
- Executes Python code in Excel context
- Returns: Dict with success status and output/error

## Error Handling
```python
try:
    mcp.WorkBook("invalid_path.xlsx")
except Exception as e:
    print(f"Error: {e}")
finally:
    mcp.Quit()
```

## Development
```bash
git clone https://github.com/yourrepo/excelmcp
pip install -e .
```