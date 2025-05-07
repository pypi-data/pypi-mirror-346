from fastmcp import FastMCP
import httpx
import json
import os
from pydantic import Field

apiKey = os.getenv("API_KEY")

const_api_task_create = f"https://saas.zaker.cn/cms/api/similar_video/outer_build/outer_create?"
const_api_task_info = f"https://saas.zaker.cn/cms/api/similar_video/outer_build/outer_info?"


# 创建 MCP Server，指定服务名称
mcp = FastMCP("YiqijianMCPService")


@mcp.tool(description="创建生成视频任务")
async def task_create(query: str = Field(..., description="视频文案") ,category_id: str = Field("1" ,description="选填。竖屏还是横屏，1:竖屏 2:横屏")) -> dict:

    redata = {}
    try:

        # 获取参数
        # create_type = "cut_video"
        create_type = "ai_video"

        content = query

        title = ""

        # category_id = 1

        use_digital = 0

        if content is None or content == "":
            raise Exception(f"内容不能为空")



        post_data = {}
        post_data["create_type"] = create_type
        post_data["title"] = title
        post_data["content"] = content
        post_data["category_id"] = category_id
        post_data["use_digital"] = use_digital

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {apiKey}'
        }

        payload = json.dumps(post_data)


        # 调用第三方 API 接口，获得任务 id
        async with httpx.AsyncClient() as client:
            # 发起 POST 请求
            response = await client.post(const_api_task_create, headers=headers, data=payload)
            redata = response.json()

    except Exception as e:
        err = f"{e}"
        redata['status'] = "FAILURE"
        redata['errmsg'] = err

    return redata

        
    
@mcp.tool(description="查询任务进度")
async def task_info(task_id: str = Field(..., description="任务ID")) -> dict:

    debug_info = []

    redata = {}

    try:

        # 获取参数
        if task_id is None or task_id == "":
            raise Exception(f"任务id不能为空")


        api_task_query_url = f"{const_api_task_info}&task_id={task_id}"


        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {apiKey}'
        }

        redata = {}
        async with httpx.AsyncClient() as client:
            # 发起 POST 请求
            response = await client.get(api_task_query_url, headers=headers)
            redata = response.json()
            debug_info.append({"task_info": redata})

    except Exception as e:
        err = f"{e}"
        redata["status"] = "FAILURE"
        redata['errmsg'] = err

    return redata


# if __name__ == "__main__":
#     mcp.run(transport="stdio")

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()