import win32com.client
import winreg
import asyncio
import pywintypes
from fastmcp import FastMCP
import os,sys
from openpyxl import Workbook

mcp = FastMCP("ExcelMCP")

class TheClass:
    def __init__(self):
        self.Excel = None
        self.TasksCount=5

global The
The = TheClass()

@mcp.tool()
def WorkBooks()->list:
    """Return Opened WorkBooks."""
    print('Tool.WorkBooks:')
    try:
        excel=Excel()
        if excel is None:
            return []
        books = []
        for book in excel.Workbooks:
            books.append({'Name': book.Name, 'FullName': book.FullName})       
        return books
    except Exception as e:
        print(e)
        return []

@mcp.tool()
def Sheets(BookPath:str)->list:
    """Return sheets of the BookPath's WorkBook."""
    print('Tool.Sheets:')
    try:
        book = BaseWorkBook(BookPath)
        if book is None:
            return []
        sheets = []
        for sheet in book.Worksheets:
            sheets.append({'Name': sheet.Name, 'FullName': sheet.FullName})
        return sheets
    except Exception as e:
        print(e)
        return []

def BaseWorkBook(BookPath: str = None):
    try:
        excel = Excel()
        if excel is None:
            return None
        if BookPath is None or BookPath.trim()=="":
            return excel.Workbooks.Add()
        else:
            for book in excel.Workbooks:
                if book.FullName.lower() == BookPath.lower():
                    book.Activate()
                    return book
            if os.path.exists(BookPath):
                book = excel.Workbooks.Open(BookPath)
                return book
            else:
                book = excel.Workbooks.Add()
                if os.path.isfile(BookPath):
                    book.SaveAs(BookPath)                
                return book
    except Exception as e:
        print(e)
        return None

@mcp.tool()
def WorkBook(BookPath: str = None) -> bool:
    """Sure Open an workbook with a workbook file path.
    Description:
        if BookPath is None, then create a new workbook.
        if BookPath is not None, then open the workbook.
        if BookPath is not None and the workbook is not opened, then create a new workbook and save to the BookPath.
    """
    print('Tool.WorkBook:')
    try:
        book = BaseWorkBook(BookPath)
        if book is None:
            return False
        else:
            return True
    except Exception as e:
        print(e)
        return False

# @mcp.tool()
# def AiTask() -> dict:
#     """Get the task from the ExcelMCP that need to be done """
#     print('Tool.AiTask:')
#     The.TasksCount-=1
#     if The.TasksCount <= 0:
#         return {'HasTask': False, 'Task': 'Call AnyAiTask() by timer 1000ms until HasTask is True.'}
#     else:
#         return {'HasTask': True, 'Task': 'Call AnyAiTask() until HasTask is False.'}

@mcp.tool()
def RunPython(PythonCode: str) -> dict:
    """Run Python codes to control office applications.
    Description:
        The MCP tools can also can be used in the Python code.
    Example:
        RunPython('The.Excel.ActiveWorkbook.SaveAs("C:\\Users\\Hasee\\Desktop\\test.xlsx")')
        RunPython('The.Excel.ActiveWorkbook.Close()')
        RunPython('The.Excel.Application.Quit()')
    Args:
        PythonCode (str): The Python code to be executed.
    """
    print('Tool.RunPython:')
    try:
        exec(PythonCode, globals())
        return {'success': True, 'output': 'Execution completed'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@mcp.tool()
def Installed() -> bool:
    """Check if the microsoft excel application is installed."""
    print('Tool.HasApplication:')
    try:
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "Excel.Application"):
            pass
        return True
    except Exception as e:        
        print(e)
        return False

def Excel():
    """Check if the microsoft excel application is installed."""
    print('Property.Excel:')
    try:
        if The.Excel is None:
            if Installed():
                excel = win32com.client.Dispatch("Excel.Application")
                #excel.Visible = True
                The.Excel = excel
            else:
                The.Excel = None
        else:
            try:
                #The.Excel.Visible = True
                name=excel.Name
            except Exception as e:
                The.Excel = None
                The.Excel = win32com.client.Dispatch("Excel.Application")
                #The.Excel.Visible = True
        return The.Excel
    except Exception as e:
        The.Excel = None
        print(e)
        return None

@mcp.tool()
def Visible(tobe: bool) -> bool:
    print('Tool.Visible:')
    """Check if the microsoft excel application is visible."""
    try:
        excel=Excel()
        excel.Visible=tobe
        name=excel.Name
        return excel.Visible
    except Exception as e:
        print(e)
        return False

@mcp.tool()
def Launch(visible: bool = True)->bool:
    """Launch the microsoft excel application."""
    print('Tool.Launch:')
    try:
        excel=Excel()
        excel.Visible=visible
        name=excel.Name
        return excel.Visible
    except Exception as e:
        print(e)
        return False

@mcp.tool()
def ActiveWorkbook() -> dict:
    """Return the active workbook."""
    print('Tool.ActiveWorkbook:')
    try:
        # excel=Excel()
        # if excel is None:
        #     return None
        book = The.Excel.ActiveWorkbook
        if book is None:
            return None
        return {'Name': book.Name, 'FullName': book.FullName}
    except Exception as e:
        print(e)
        return {'Result': "There's no active workbook."}        #return None


@mcp.tool()
def ActiveSheet() -> dict:
    """Return the active sheet."""
    print('Tool.ActiveSheet:')
    try:
        sheet=The.Excel.ActiveSheet
        if not (sheet is None):
            return {'SheetName': sheet.Name, 'WorkBook': sheet.Parent.FullName}
    except Exception as e:
        print(e)
    return {'Result': "There's no active sheet."}

@mcp.tool()
def Quit()->bool:
    """Quit the microsoft excel application."""
    print('Tool.Quit:')
    try:
        The.Excel.Quit()
        try:
            name=The.Excel.Name
            return False
        except Exception as e:
            print(e)
            The.Excel = None
            return True
    except Exception as e:
        The.Excel = None
        print(e)
        return True

@mcp.tool()
def Demostrate()->dict:
    """Demostrate for you to see some functions in this ExcelMCP server."""
    print('Tool.Demostrate:')
    try:
        excel=Excel()
        if excel is None:
            return []
        book = excel.Workbooks.Add()
        sheet = excel.ActiveSheet
        excel.Visible = True
        sheet.Cells(1, 1).Value = "Hello, World From ExcelMCP Server!"
        sheet.Cells(1, 1).Font.Size = 20
        sheet.Cells(1, 1).Font.Bold = True
        sheet.Cells(2, 1).Value = "This is a demonstration of the ExcelMCP server."
        sheet.Cells(3, 1).Value = "You can use this server to control the Microsoft Excel application."
        sheet.Cells(4, 1).Value = "For example, you can use this server to open a workbook, save a workbook, close a workbook, and so on."
        sheet.Cells(5, 1).Value = "More you can do with this ExcelMCP server: "
        sheet.Cells(6, 1).Value = " - get the active workbook, active sheet, and so on."
        sheet.Cells(7, 1).Value = " - get the tasks from the ExcelMCP that need to be done."
        sheet.Cells(8, 1).Value = " - run python codes to control office applications."
        sheet.Cells(9, 1).Value = " - get the opened workbooks, and sheets of the workbooks."
        sheet.Cells(10, 1).Value = " - get the installed office applications."
        sheet.Cells(11, 1).Value = " - launch the office applications."
        sheet.Cells(12, 1).Value = " - quit the office applications."
        sheet.Cells(13, 1).Value = "The most important thing is run python codes from Ai to control excel applications."  
        sheet.Cells(1, 1).Font.Bold = True
        return {"success": True, "output": "Demonstration completed"}
    except Exception as e:
        print(e)
        return {"success": False, "error": str(e)}

@mcp.resource("resource://Instructions")
def Instructions() -> str:
    return """
    There're some base tools for you to control the Microsoft Excel application.
    Specially you can use tool RunPython to run python codes to control Excel applications.
    openpyxl is already installed and you can use it in your uploaded python codes.
    There're an object called "The" as global, you can use it to store the objects of the Excel application.
    The.Excel is already used as the Excel application object.
    """


def main() -> None:
    """ExcelMCP server entry point with command line arguments support.
    
    Usage examples:
    1. excelmcp (stdio mode by default)
    2. excelmcp sse 8080 127.0.0.1 (SSE mode with port and host)
    3. excelmcp sse --port 8080 --host 127.0.0.1 (alternative syntax)
    """
    args = sys.argv[1:]
    transport = "stdio"
    thePort = 8000
    theHost = "127.0.0.1"

    try:
        if args:
            transport = args[0].lower()
            
            # Handle port and host arguments
            if len(args) > 1:
                # Try to parse port from arguments
                for arg in args[1:]:
                    if arg.isdigit():
                        thePort = int(arg)
                        break
                    
                # Try to find host in arguments (first non-port argument)
                for arg in args[1:]:
                    if '--host' in arg:
                        theHost = arg.split('=')[-1]
                    elif not arg.isdigit() and '--port' not in arg:
                        theHost = arg

            # Handle explicit flags (--port/--host)
            if '--port' in args:
                thePort = int(args[args.index('--port') + 1])
            if '--host' in args:
                theHost = args[args.index('--host') + 1]

        if transport == "stdio":
            print("ExcelMCP running in stdio mode")
            mcp.run("stdio")
        else:
            print(f"Starting SSE server on {theHost}:{thePort}")
            mcp.run(transport="sse", host=theHost, port=thePort)

    except ValueError as e:
        print(f"Error parsing arguments: {e}")
    except Exception as e:
        print(f"Server startup failed: {e}")
    if transport == "stdio":
        print("ExcelMCP runed on stdio mode")
        mcp.run("stdio")
    else:
        mcp.run(transport="sse", host=theHost, port=thePort)