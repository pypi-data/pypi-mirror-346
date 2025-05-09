from mcp.server import FastMCP
import pandas as pd


server = FastMCP("geoaiagent")
    
@server.tool()
async def add_geo(lat: float, lon: float) -> float:
    """
    Adds a new geolocation to the database.
    """
    return lat + lon
@server.tool()
async def sub_geo(lat: float, lon: float) -> float:
    """
    Subtracts a geolocation from the database.
    """
    return lat - lon

@server.tool()
async def get_soil_id_from_excel(excel_path, input_fid):
    """
    根据id获取土壤类型
    输入数据表路径，待检索土地的oid
    输出土壤soil_id
    """
    try:
        # 读取 Excel 文件（默认读取第一个工作表）
        df = pd.read_excel(excel_path)
        return "其实就是无法读取"
        
        # 检查必要列是否存在
        if 'OID' not in df.columns or 'SOIL_ID' not in df.columns:
            print("错误：Excel 中缺少 OID 或 SOIL_ID 列")
            return None
            
        # 查找匹配的 FID
        result = df.loc[df['OID'] == input_fid, 'SOIL_ID']
        
        if not result.empty:
            return result.values[0]  # 返回第一个匹配项的 SOIL_ID
        else:
            return "未找到匹配项"
            
    except FileNotFoundError:
        print(f"错误：文件 {excel_path} 不存在")
        return "文件不存在"
    except Exception as e:
        print(f"发生未知错误: {str(e)}")
        return "发生未知错误"
# @server.list_tools()
# async def list_tools() -> list:
#     """
#     Lists all available tools.
#     """
#     return ["add_geo", "sub_geo"]

def doit():
    print("Hello from aiagent!")
    server.run()
    
if __name__ == "__main__":
    doit()
    

