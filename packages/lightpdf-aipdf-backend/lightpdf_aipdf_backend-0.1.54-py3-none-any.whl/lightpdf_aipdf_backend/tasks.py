import asyncio
from .state import set_qa_state

def format_tool_call_aggregate_result(yield_messages: list) -> dict:
    """
    聚合多个工具调用的yield_message，返回统一格式。
    Args:
        yield_messages: 所有工具的yield_message列表
    Returns:
        dict: 聚合后的主消息
    """
    if len(yield_messages) == 1:
        return yield_messages[0]
    return {
        "type": "tool_call",
        "step_type": "end",
        "results": yield_messages
    }

# 异步工具调用任务（单工具版）
async def tool_task_async(qa_id: str, session_id: str, tool_call: dict) -> tuple:
    """
    工具调用任务（异步版，单工具）。
    Args:
        qa_id: 问答ID
        session_id: 会话ID
        tool_call: 单个工具调用参数
    Returns:
        tuple: (tool_response_message, yield_message)
    """
    from .chat_handler import handle_tool_call
    from .state import append_session_history, get_session_history
    try:
        history = get_session_history(session_id)
        api_messages = history.copy()
        from .chat_handler import ToolCall, ToolCallFunction
        tc_obj = ToolCall(
            id=tool_call.get("id"),
            function=ToolCallFunction(
                name=tool_call["function"]["name"],
                arguments=tool_call["function"]["arguments"]
            )
        )
        tool_response_message, yield_message = await handle_tool_call(tc_obj, api_messages)
        append_session_history(session_id, tool_response_message)
        return tool_response_message, yield_message
    except Exception as e:
        error_result = {"type": "error", "step_type": "end", "content": f"工具调用异常: {str(e)}"}
        set_qa_state(qa_id, {"status": "finished", "tool_call_end_message": error_result, "session_id": session_id})
        return None, error_result

# 新增：聚合多个工具调用，全部完成后统一写入状态
async def tool_tasks_aggregate_async(qa_id: str, session_id: str, tool_calls: list) -> None:
    """
    并发调度所有tool_task_async，全部完成后统一set_qa_state为tool_call_end_ready。
    Args:
        qa_id: 问答ID
        session_id: 会话ID
        tool_calls: 工具调用参数列表
    Returns:
        None
    """
    try:
        tasks = [tool_task_async(qa_id, session_id, tool_call) for tool_call in tool_calls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        # 聚合所有yield_message
        yield_messages = []
        for res in results:
            if isinstance(res, tuple) and len(res) == 2:
                _, yield_message = res
                yield_messages.append(yield_message)
            elif isinstance(res, dict):
                yield_messages.append(res)
            else:
                yield_messages.append({"type": "error", "content": str(res)})
        main_result = format_tool_call_aggregate_result(yield_messages)
        set_qa_state(qa_id, {"status": "tool_call_end_ready", "tool_call_end_message": main_result, "session_id": session_id})
    except Exception as e:
        error_result = {"type": "error", "step_type": "end", "content": f"工具调用聚合异常: {str(e)}"}
        set_qa_state(qa_id, {"status": "finished", "tool_call_end_message": error_result, "session_id": session_id})