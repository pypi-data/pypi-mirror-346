import asyncio
from typing import Any
import logging
import httpx
import pymysql
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
from mcp.server.fastmcp import FastMCP

# 配置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# 初始化 FastMCP server
mcp = FastMCP("query_data")

# Constants 
KK_AI_CENTER_API_BASE = "http://118.190.154.195:8099/v1" # TODO 环境变量
AES_KEY = b"kIGcDTzznnoN1a9q"  # 16 字节密钥  TODO 环境变量
AES_IV = b"xXCLkPhNkMhWb4Oc"   # 16 字节 IV   TODO 环境变量

async def getDBByPlatformkey(platformkey: str) -> dict:
    """向 NWS API 发送请求，并进行适当的错误处理。"""
    url = f"{KK_AI_CENTER_API_BASE}/getConsumerDBInfo"
    headers = {
        "api-key": platformkey
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            res = response.json()
            # host=db_info['host'], port=db_info['port'], user=db_info['user'], passwd=db_info['password'], db=db_info['database'],
            if not res or  "host" not in res or "host" not in res or "port" not in res or "user" not in res or "password" not in res or "database" not in res:
                return None
            encode_passwd = res["password"]
            try:
                res["password"] = aes_decrypt(encode_passwd, AES_KEY, AES_IV)
                return res
            except Exception as e:
                logging.debug("解密失败:", e)
                return None
        except Exception:
            return None

def aes_decrypt(ciphertext_base64, key, iv):
    """
    使用 AES-CBC 模式解密 Base64 编码的密文。

    参数:
        ciphertext_base64 (str): Base64 编码的密文。
        key (bytes): AES 密钥。
        iv (bytes): AES 初始化向量 (IV)。
    
    返回:
        str: 解密后的明文。
    """
    # Base64 解码密文
    ciphertext = base64.b64decode(ciphertext_base64)  
    # 创建 AES-CBC 解密器
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 解密数据
    decrypted_data = cipher.decrypt(ciphertext)   
    # 去除 PKCS7 填充
    unpadded_data = unpad(decrypted_data, AES.block_size)   
    # 返回解密后的明文
    return unpadded_data.decode('utf-8')

@mcp.tool()
def say_hello(name: str) -> str:
    """生成个性化问候语（中英双语版）"""
    logging.debug(f"正在生成问候语，输入参数: name={name}")
    return f"  你好 {name}! (Hello {name}!)"
@mcp.tool()
async def query_data(platformkey: str, sql: str) -> str:
    """获取某个sql的执行结果。

    Args:
        platformkey: 平台key,决定向哪个平台触发sql的执行
        sql: 需要执行的sql语句
    """
    print('query_data start')
    #  获取db的链接信息
    db_info = await getDBByPlatformkey(platformkey)
    if not db_info:
        return '没有找到对应的数据库信息'
    db = pymysql.connect(host=db_info['host'], port=db_info['port'], user=db_info['user'], passwd=db_info['password'], db=db_info['database'], charset='utf8')
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    # 查询数据
    n = cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return results


async def query_data_debug(platformkey: str, sql: str) -> str:
    #  获取db的链接信息
    db_info = await getDBByPlatformkey(platformkey)
    if not db_info:
        return '没有找到对应的数据库信息'
    db = pymysql.connect(host=db_info['host'], port=db_info['port'], user=db_info['user'], passwd=db_info['password'], db=db_info['database'], charset='utf8')
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    # 查询数据
    n = cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        print(row)
    print(results)
    cursor.close()
    db.close()
    return results

def test_01():
    ciphertext_base64 = "5wtNhDossqmuygP6KmcfgA=="
    # 解密
    try:
        decrypted_text = aes_decrypt(ciphertext_base64, AES_KEY, AES_IV)
        print("解密后的明文:", decrypted_text)
    except Exception as e:
        print("解密失败:", e)

def test_02():
    async def main():
        result = await getDBByPlatformkey('09F2918D02F1;I3FG')
        print(result)
    asyncio.run(main())
def test_03():
    async def main():
        result = await query_data("09F2918D02F1;I3FG", '''SELECT dayf AS day,accu_value AS daily_electricity_usage FROM mon202504 WHERE variantname=(SELECT sum_epf_var FROM station WHERE name='怡丰城微电网') AND dayf BETWEEN 1 AND 30 ORDER BY dayf;''')
        print(result)
    asyncio.run(main())

def main():
    # 初始化并运行 server
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()


