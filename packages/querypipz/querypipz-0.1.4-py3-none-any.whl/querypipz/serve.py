# serve

class MonitorError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
class AuthenticationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
class ExistsError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Depends, Request, Response
from llama_index.core.agent import ReActAgent
from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI


from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum
import asyncio
import uuid
import time
import json
import os

from loguru import logger
import os
from datetime import datetime

# 定义日志文件路径
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"log_{datetime.now().strftime('%Y%m%d')}.log")

# 配置日志记录器
logger.configure(
    handlers=[
        {"sink": log_file, "format": "{time} - {level} - {message}", "level": "DEBUG", "rotation": "500 MB", "retention": "7 days"},
    ]
)

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #TODO 安全组配置
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


api_key = os.environ.get('bianxieai_API_KEY')
search_api_key = os.environ.get('search_api_key')
llm = OpenAI(
    model="gpt-4o",
    api_key=api_key,
    api_base='https://api.bianxieai.com/v1',
    temperature=0.1, # TODO
)
embed_model = OpenAIEmbedding(api_key=api_key,api_base='https://api.bianxieai.com/v1')
Settings.embed_model = embed_model
Settings.llm = llm

user_resources = {}
# 存储请求记录的字典，键为用户 ID，值为请求时间列表
request_records: Dict[str, list] = {}


def response_info(message:str, code:int):
    if code == 500:
        logger.error(message)
    return {"message": message, "code":code }


@app.on_event("startup")
async def startup_event():
    logger.info('Init Agent')


@app.middleware("http")
async def session_management(request: Request, call_next):
    try:
        # TODO 优化鉴权逻辑
        my_tokens = 12345
        if not request.cookies.get("tokens") or request.cookies.get("tokens") != my_tokens:
            raise AuthenticationError("Invalid token")

        # 获取请求中的会话 ID Cookie
        session_id = request.cookies.get("session_id")

        if not session_id:
            session_id = str(uuid.uuid4())
            # 将新的会话 ID 存储到 Cookie 中
            response = Response(content="Set cookie", media_type="text/plain")
            response.set_cookie(key="session_id", value=session_id)
            request.state.session_id = session_id
            # 初始化用户资源
            user_resources[session_id] = {
                "agent": "",
                "last_active": time.time()
            }
            
            return response

        if session_id not in user_resources:
            user_resources[session_id] = {
                "agent": "",
                "last_active": time.time()
            }
        user_resources[session_id]["last_active"] = time.time()

        # 继续处理请求
        response = await call_next(request)
        response.set_cookie(key="session_id", value=session_id)

        return response
    
    # except:
    #     pass
    
    except AuthenticationError as e:
        return response_info(f"Invalid token",500)
    
    except Exception as e:
        return response_info(f"session_management failed: {e}",500)
        


# 创建 Agent 实例
@app.post("/api/create_agent")
async def create_agent(request:Request):
    try:
        # tools: List[str], mcp_servers: List[str], 
        session_id = request.cookies.get("session_id")

        data = await request.json()
            
            
        # TODO
        tools = data.get("tools", [])
        mcp_servers = data.get("mcp_servers", [])

        # TODO END
        
        
        if user_resources[session_id]["agent"]:
            raise ExistsError('Agent Exists')
        
        
        user_resources[session_id]["agent"] = Work1(tools, mcp_servers)
        return response_info(f"create agent successfully",200)
        
    except ExistsError as e:
        return response_info(f"Agent exist",500)
        
    except Exception as e:
        return response_info(f"create agent failed: {e}",500)
        


# 删除 Agent 实例
@app.delete("/api/delete_agent")
async def delete_agent(request:Request):
    try:
        session_id = request.cookies.get("session_id")

        if session_id not in user_resources:
            #  TODO
            raise HTTPException(status_code=404, detail="not found")
        if not user_resources[session_id]["agent"]:
            return {"message": "failed"}

        del user_resources[session_id]
        return response_info("delete agent successfully",200)
    
    except HTTPException as e:
        return response_info(f"not found",500)
    
    except Exception as e:
        return response_info(f"delete agent failed: {e}",500)

@app.post("/api/chat")
async def chat(request: Request):
    try:
        
        data = await request.json()
        session_id = request.cookies.get("session_id")

        work1 = user_resources[session_id]["agent"]
        messages = data.get("messages", [])
        
        # 记录表
        if session_id not in request_records:
            request_records[session_id] = []
        request_records[user_id].append(datetime.now())
        
        
        prompt = messages['prompt']
        prompt2 = work1.intent_recognition(prompt)

        generate = work1.chat(prompt2)
        
        
        async def generate_response():
            try:
                for part in generate:
                    yield json.dumps({
                        "message": {
                            "content": part
                        }
                    }) + "\n"

            except Exception as e:
                yield json.dumps({
                    "message": {
                        "error": f"error: {str(e)}"
                    }
                }) + "\n"

        return StreamingResponse(
            generate_response(),
            media_type="application/json"
        )
    except Exception as e:
        return response_info(f"chat failed: {e}",500)
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)