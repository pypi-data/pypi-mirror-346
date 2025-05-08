from fastapi import FastAPI, HTTPException, File, UploadFile, Header, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from contextlib import asynccontextmanager
from typing import List, Dict, AsyncGenerator, Any, Tuple, TypedDict, Optional
from uuid import uuid4
import json
import asyncio

from .models import ChatRequest, Message, FileInfo
from .file_handler import handle_batch_file_upload
from .chat_handler import process_messages, generate_chat_response, get_file_references, validate_and_fix_messages, collect_stream_content, LANGUAGE_CODE_TO_ENGLISH, ToolCall
from .utils import async_generator_to_json_stream
from .state import cleanup_inactive_sessions, store_file_info, get_qa_state, set_qa_state, get_openai_client, get_session_history, set_session_history, append_session_history
from .tasks import tool_tasks_aggregate_async
from .config import Config
from .tools import get_tools

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    Args:
        app: FastAPI应用实例
    """
    # 应用启动时的初始化
    yield
    # 应用关闭时的清理
    cleanup_inactive_sessions()

# 创建FastAPI应用
app = FastAPI(title="LightPDF Agent API", lifespan=lifespan)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root() -> dict:
    """
    API根路径
    Returns:
        dict: API启动信息
    """
    return {"message": "LightPDF Agent API已启动"}

@app.post("/api/upload")
async def upload_file(
    files: List[UploadFile] = File(None),
    session_id: Optional[str] = Header(None, alias="Session-ID"),
    extends: Optional[str] = None
) -> JSONResponse:
    """
    处理文件上传请求
    Args:
        files: 要上传的文件列表
        session_id: 会话ID
        extends: 可选的文件信息列表JSON字符串，用于直接保存并返回文件信息
    Returns:
        JSONResponse: 文件信息列表
    """
    # 准备响应头
    headers = {
        "Cache-Control": "no-cache, no-transform",
        "X-Accel-Buffering": "no"  # 禁用Nginx缓冲
    }

    # 如果没有session_id，创建新的
    if not session_id:
        session_id = str(uuid4())
        headers["Set-Session-ID"] = session_id
    
    # 处理extends参数 - 如果提供了extends参数，直接解析并返回
    if extends:
        try:
            file_info_list = json.loads(extends)
            # 转换为FileInfo对象
            results = []
            for info in file_info_list:
                file_info = FileInfo(
                    file_id=info.get("file_id"),
                    filename=info.get("filename"),
                    content_type=info.get("content_type"),
                    path=info.get("path")
                )
                # 存储文件信息到会话
                store_file_info(session_id, file_info)
                results.append(file_info)
            
            # 将FileInfo对象转换为字典
            results_dict = [result.model_dump() for result in results]
            
            return JSONResponse(
                content=results_dict,
                headers=headers
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"解析extends参数失败: {str(e)}")
    
    # 如果没有extends参数，执行常规的文件上传处理
    if not files or len(files) == 0:
        raise HTTPException(status_code=400, detail="未提供文件且未提供extends参数")
        
    # 使用批量处理函数处理所有文件
    results = await handle_batch_file_upload(files, session_id)
    
    # 将FileInfo对象转换为字典
    results_dict = [result.model_dump() for result in results]
    
    return JSONResponse(
        content=results_dict,
        headers=headers
    )

@app.post("/api/chat1")
async def chat1(
    request: ChatRequest,
    session_id: Optional[str] = Header(None, alias="Session-ID")
):
    """处理聊天请求"""
    try:
        # 准备响应头
        headers = {
            "Cache-Control": "no-cache, no-transform",
            "X-Accel-Buffering": "no"  # 禁用Nginx缓冲
        }
        
        # 如果没有session_id，创建新的
        if not session_id:
            session_id = str(uuid4())
            headers["Set-Session-ID"] = session_id
        
        # 创建一个用户消息
        user_message = Message(
            role="user",
            content=request.content,
            file_ids=request.file_ids,
            file_infos=request.file_infos
        )
        
        # 处理消息
        processed_messages = await process_messages(session_id, [user_message])
        
        # 生成响应
        return StreamingResponse(
            async_generator_to_json_stream(generate_chat_response(session_id, processed_messages, instructions=request.instructions, language=request.language)),
            media_type="application/x-ndjson",
            headers=headers
        )
    except Exception as e:
        error_msg = str(e)
        raise HTTPException(status_code=500, detail=f"LightPDF Agent处理错误: {error_msg}") 

# 新增：统一ndjson流式输出工具

def ndjson_stream(generator_func):
    async def wrapper(*args, **kwargs):
        """
        将异步生成器输出转为ndjson流
        Yields:
            bytes: ndjson流
        """
        async for item in generator_func(*args, **kwargs):
            if isinstance(item, (dict, list)):
                yield (json.dumps(item, ensure_ascii=False) + "\n").encode("utf-8")
            elif isinstance(item, str):
                yield (item.rstrip('\n') + "\n").encode("utf-8")
            else:
                yield str(item).encode("utf-8") + b"\n"
    return wrapper

async def process_message(session_id: str, msg: Message) -> List[Dict]:
    """处理消息列表，包括文件处理和格式转换
    
    Args:
        session_id: 用户会话ID
        message: 消息
        
    Returns:
        List[Dict]: 处理后的消息列表
    """
    # 转换消息并处理文件
    processed_messages = []
    
    # 定义一个内部函数来处理添加文件链接
    def add_file_links_to_message(message_dict: Dict, files: List[Dict[str, str]]) -> Dict:
        """将文件信息添加到消息中，使用JSON格式
        
        Args:
            message_dict: 消息字典
            files: 文件信息列表，每个文件包含path和可选的name、password
            
        Returns:
            Dict: 更新后的消息字典
        """
        if files:
            # 直接添加files字段，与MCP工具结构兼容
            message_dict["content"] += "\n\n---\n\n" + json.dumps(files, ensure_ascii=False)
        return message_dict
    
    # 定义一个内部函数来处理直接的文件信息，返回JSON格式
    def get_file_info_json(file_infos: List) -> List[Dict[str, str]]:
        """从直接文件信息获取JSON格式的文件列表
        
        Args:
            file_infos: 文件信息列表
            
        Returns:
            List[Dict[str, str]]: 文件信息列表，JSON格式
        """
        files = []
        for file_info in file_infos:
            file_data = {
                "path": file_info.path,
                "name": file_info.filename
            }
            # 如果文件信息中包含密码，添加到结果中
            if hasattr(file_info, 'password') and file_info.password:
                file_data["password"] = file_info.password
            
            files.append(file_data)
        return files

    # 基本消息结构
    message_dict = {"role": msg.role, "content": msg.content}
    
    # 处理assistant角色的工具调用
    if msg.role == "assistant" and msg.tool_calls:
        message_dict["tool_calls"] = msg.tool_calls
        # 当有工具调用时，content可以为空字符串
        if not message_dict["content"]:
            message_dict["content"] = ""
    
    # 处理tool角色的工具响应
    if msg.role == "tool":
        if msg.tool_call_id:
            message_dict["tool_call_id"] = msg.tool_call_id
        if msg.name:
            message_dict["name"] = msg.name
        # 确保tool角色必须有tool_call_id和name
        if "tool_call_id" not in message_dict or "name" not in message_dict:
            return []
    
    # 如果消息包含文件ID
    if msg.file_ids:
        file_urls = get_file_references(msg.file_ids, session_id)
        message_dict = add_file_links_to_message(message_dict, file_urls)
    
    # 如果消息包含直接的文件信息
    if msg.file_infos:
        file_urls = get_file_info_json(msg.file_infos)
        message_dict = add_file_links_to_message(message_dict, file_urls)
    
    processed_messages.append(message_dict)
    
    # 返回完整的会话历史
    return validate_and_fix_messages(processed_messages)

# 合并后的通用LLM流式推理生成器
async def llm_stream_generator(qa_id: str, session_id: str, first_round: bool = False, instructions: Optional[str] = None, language: Optional[str] = None) -> AsyncGenerator:
    """
    通用LLM流式推理生成器。
    Args:
        qa_id: 问答ID
        session_id: 会话ID
        first_round: 是否为首轮
    Yields:
        dict: 流式输出内容
    """
    try:
        if first_round:
            yield {"type": "task", "id": qa_id}

        openai_client = get_openai_client()
        tools = await get_tools()

        # 完全依赖流式响应
        while True:
            # 使用流式请求 - 异步客户端
            from openai.types.chat import ChatCompletionStreamOptionsParam
            
            # 准备发送给API的消息
            request_messages = get_session_history(session_id).copy()
            print("\n", request_messages)
            
            # 获取指令：优先使用前端传递的指令，否则使用配置文件中的默认指令
            if not instructions:
                instructions = Config.get_default_instructions() or ""

            if language:
                language_instruction = f"- If the user does not specify a language, respond in {LANGUAGE_CODE_TO_ENGLISH.get(language, f"{language} language")}."
                instructions = f"{instructions}\n{language_instruction}" if instructions else language_instruction
            
            # 如果有指令则添加系统提示词
            if instructions:
                request_messages.insert(0, {"role": "system", "content": instructions})
            
            response = await openai_client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                temperature=0.5,
                messages=request_messages,
                tools=tools,
                parallel_tool_calls=False,
                stream=True,
                stream_options=ChatCompletionStreamOptionsParam(include_usage=True)  # 使用类型化对象
            )
            
            full_content = ""
            finish_reason = None
            tool_calls_data = []
            yield_content = False
            usage_info = None  # 初始化usage_info变量，用于存储token统计信息
            
            # 收集流式响应内容
            async for item in collect_stream_content(response):
                if isinstance(item, tuple):
                    if len(item) == 4:
                        full_content, finish_reason, tool_calls_data, usage_info = item
                else:
                    if not yield_content:
                        # 第一次消息通知
                        yield {
                            "type": "stream_start",
                            "content": ""
                        }
                        yield_content = True
                    
                    yield item
            
            # 如果需要调用工具
            if finish_reason == 'tool_calls' and tool_calls_data:
                if yield_content:
                    # 停止当前流
                    yield {
                        "type": "stream_end",
                        "content": full_content
                    }
                
                # 转换工具调用格式并创建消息
                tool_calls = []
                for tc_data in tool_calls_data:
                    tc_function = tc_data["function"]
                    if tc_data["id"] and tc_function["name"]:
                        tool_calls.append({
                            'id': tc_data["id"],
                            'function': {
                                'name': tc_function["name"],
                                'arguments': tc_function["arguments"]
                            }
                        })
                
                # 创建助手消息
                append_session_history(session_id, {
                    "role": "assistant",
                    "content": full_content or "",
                    "tool_calls": [
                        {
                            "id": tc["id"],
                            "type": "function", 
                            "function": {
                                "name": tc["function"]["name"],
                                "arguments": tc["function"]["arguments"]
                            }
                        } for tc in tool_calls
                    ]
                })

                tool_call = tool_calls[0]
                yield {
                    "type": "tool_call",
                    "step_type": "start",
                    "content": json.dumps({
                        "id": tool_call["id"],
                        "function": {
                            "name": tool_call["function"]["name"],
                            "arguments": json.loads(tool_call["function"]["arguments"])
                        }
                    })
                }

                
                set_qa_state(qa_id, {"status": "tool_calling", "tool_call_args": tool_calls, "session_id": session_id})
                # 异步调度工具调用（改为聚合调度）
                asyncio.create_task(tool_tasks_aggregate_async(qa_id, session_id, tool_calls))
                return
                
            else:
                # 如果不需要调用工具，直接结束流
                stream_end_data = {
                    "type": "stream_end",
                    "content": full_content
                }
                
                # 如果有使用统计信息，添加到输出中
                if usage_info:
                    stream_end_data["usage"] = usage_info
                
                set_qa_state(qa_id, {"status": "finished", "content": full_content, "session_id": session_id, "usage": usage_info})
                yield stream_end_data
                
                # 更新会话历史
                append_session_history(session_id, {
                    "role": "assistant",
                    "content": full_content
                })

                break

    except Exception as e:
        set_qa_state(qa_id, {"status": "finished", "content": f"LLM异常: {str(e)}", "session_id": session_id})
        yield {"type": "error", "content": f"LLM异常: {str(e)}"}

@app.post("/api/chat")
async def chat(
    request: ChatRequest,
    session_id: Optional[str] = Header(None, alias="Session-ID")
):
    """
    首次发起多轮LLM+工具调用流程。
    - 只负责初始化会话、写入首轮状态、流式输出LLM内容。
    - 遇到工具调用时断流，状态写入redis，celery异步处理工具。
    - 后续全部通过/api/chat/{id}轮询接口自动衔接。
    """
    try:
        headers = {
            "Cache-Control": "no-cache, no-transform",
            "X-Accel-Buffering": "no"
        }
        if not session_id:
            session_id = str(uuid4())
            headers["Set-Session-ID"] = session_id
        qa_id = str(uuid4())
        # 取session_id下的完整history，追加本轮user消息
        history = get_session_history(session_id) or []
        # 创建一个用户消息
        user_message = Message(
            role="user",
            content=request.content,
            file_ids=request.file_ids,
            file_infos=request.file_infos
        )
        # 处理消息
        processed_messages = await process_message(session_id, user_message)
        history.extend(processed_messages)
        set_session_history(session_id, history)
        # 只调用llm_stream_generator
        return StreamingResponse(
            ndjson_stream(llm_stream_generator)(qa_id, session_id, True),
            media_type="application/x-ndjson",
            headers=headers
        )
    except Exception as e:
        error_msg = str(e)
        raise HTTPException(status_code=500, detail=f"LightPDF Agent处理错误: {error_msg}")

@app.get("/api/chat/{id}")
async def chat_poll(id: str = Path(..., description="问答ID（celery任务ID）")):
    """
    轮询接口，自动衔接工具调用和LLM流式输出，支持多轮嵌套。
    状态机说明：
    - waiting_tool：工具调用中，返回tool_calling。
    - tool_call_end_ready：工具调用完成，先返回tool_call/end，再继续LLM流式输出。
    - finished：流程结束，返回stream_end。
    - 任何异常均写入finished并输出error。
    """
    try:
        async def poll_result():
            try:
                state = get_qa_state(id)
                if state:
                    session_id = state.get("session_id")
                    if state.get("status") == "tool_call_end_ready":
                        tool_result = state.get("tool_call_end_message", {})
                        if tool_result.get("type") == "error":
                            yield tool_result
                            return

                        yield tool_result if tool_result else {"type": "tool_call", "step_type": "end"}

                        async for chunk in llm_stream_generator(id, session_id, False):
                            yield chunk
                    elif state.get("status") == "finished":
                        usage = state.get("usage", {})
                        content = state.get("content", "LLM全部输出完毕")
                        yield {"type": "stream_end", "content": content, "usage": usage}
                    else:
                        yield {"type": "tool_calling"}
                else:
                    yield {"type": "tool_calling"}
            except Exception as e:
                set_qa_state(id, {"status": "finished", "content": f"轮询异常: {str(e)}"})
                yield {"type": "error", "content": f"轮询异常: {str(e)}"}
        return StreamingResponse(
            ndjson_stream(poll_result)(),
            media_type="application/x-ndjson"
        )
    except Exception as e:
        error_msg = str(e)
        raise HTTPException(status_code=500, detail=f"轮询问答任务时出错: {error_msg}") 