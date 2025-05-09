import json
from mcp.server.fastmcp import FastMCP

from mcppp.models import AssignTask, GetGshjCombination, GetPredResult, GetTptjPicture

mcp = FastMCP("try_mcp")


@mcp.tool()
def get_db_names() -> list[str]:
    """
    获取所有高熵合金数据库名称
    """

    return [
        "高熵合金基础描述符数据库",
        "高熵合金压缩塑性预测数据库",
        "高熵合金机器学习模型数据库",
    ]


@mcp.tool()
def get_gshj_combination(params: GetGshjCombination) -> str:
    """
    获取最佳的排名的高熵合金组合

    - 参数:
        - params: GetGshjCombination对象，包含查询参数
            - index: 表明第几好的高熵合金组合

    - 返回字段:
        - elements: 元素组合列表
        - con: 每个元素对应的比例，%
        - fracture strain: 塑性断裂应变，%
        - tensile strength: 1400℃下的拉伸强度，MPa
    """

    best_comb: dict[str, list[str | int] | float]
    match params.index:
        case 1:
            best_comb = {
                "elements": ["Mo", "Ti", "Nb", "Ta", "W", "Hf"],
                "con": [5, 25, 18, 16, 6, 30],
                "fracture strain": 41.42,
                "tensile strength": 432
            }
            return json.dumps(best_comb)
        case 2:
            best_comb = {
                "elements": ["Mo", "Ti", "Nb", "Ta", "W", "Hf"],
                "con": [5, 34, 30, 9, 7, 15],
                "fracture strain": 39.14,
                "tensile strength": 405
            }
            return json.dumps(best_comb)
        case 3:
            best_comb = {
                "elements": ["Mo", "Ti", "Nb", "Ta", "W", "Hf"],
                "con": [5, 35, 31, 14, 5, 10],
                "fracture strain": 38.92,
                "tensile strength": 390
            }
            return json.dumps(best_comb)
        case _:
            return "没有找到对应的高熵合金组合"


@mcp.tool()
def get_pred_result(params: GetPredResult) -> str:
    """
    获取某种高熵合金的压缩强度和拉伸强度

    - 参数:
        - params: GetPredResult对象，包含查询参数
            - elem_list: 元素列表
            - con_list: 每个元素对应的比例

    - 返回内容:
        - 拉伸强度
        - 压缩强度
    """

    if len(params.elem_list) == 6 and len(params.con_list) == 6:
        tensile_strength: int = 1143
        compression_strength: int = 1245
        return f"拉伸强度: {tensile_strength} MPa, 压缩强度: {compression_strength} MPa"
    return "参数个数错误"


@mcp.tool()
def get_tptj_picture(params: GetTptjPicture) -> str:
    """
    获取铁碳相图

    - 参数:
        - params: GetTptjPicture对象，包含查询参数
            - need_color: 是否需要彩色图片，默认不需要

    - 返回内容:
        - 图片的路径
    """


    if params.need_color:
        return "https://disc-wolido.oss-cn-beijing.aliyuncs.com/tptj/tptj-2.jpeg"
    else:
        return "https://disc-wolido.oss-cn-beijing.aliyuncs.com/tptj/tptj-1.jpg"


@mcp.tool()
def get_lab_status() -> str:
    """
    获取自驱动实验室的实时状况
    自驱动实验室也叫做无人实验室

    - 返回内容:
        - 实时状况
            - 实验室状态
            - 排队任务数
            - 短切纤维复合材料3D打印单元
                - 状态
                - 任务编号
                - 运行时间
                - 运行进度
            - 连续纤维复合材料铺贴单元
                - 状态
                - 任务编号
                - 运行时间
                - 运行进度
            - 高熵合金3D打印单元
                - 状态
                - 任务编号
                - 运行时间
                - 运行进度
            - 电磁表征单元
                - 状态
                - 任务编号
                - 运行时间
                - 运行进度
            - 力学表征单元
                - 状态
                - 任务编号
                - 运行时间
                - 运行进度
    """

    lab_status: dict = {
        "实验室状态": "运行中",
        "排队任务数": 7,
        "短切纤维复合材料3D打印单元": {
            "状态": "运行中",
            "任务编号": "xd-1415",
            "运行时间": "1小时23分",
            "运行进度": "62%",
        },
        "连续纤维复合材料铺贴单元": {
            "状态": "运行中",
            "任务编号": "xd-1329",
            "运行时间": "2小时44分",
            "运行进度": "81%",
        },
        "高熵合金3D打印单元": {
            "状态": "运行中",
            "任务编号": "xd-1416",
            "运行时间": "55分",
            "运行进度": "22%",
        },
        "电磁表征单元": {
            "状态": "等待中",
        },
        "力学表征单元": {
            "状态": "等待中",
        }
    }

    return json.dumps(lab_status)


@mcp.tool()
def get_todo_task() -> str:
    """
    获取无人实验室待下发的任务
    无人实验室也叫自驱动实验室
    """

    todo_task: dict = {
        "xd-1417": {
            "任务类型": "高熵合金3D打印",
            "元素组成": {
                "Mo": 0.05,
                "Ti": 0.34,
                "Nb": 0.3,
                "Ta": 0.09,
                "W": 0.07,
                "Hf": 0.15
            },
            "打印数量":6,
            "特殊参数": "无",
        },
        "xd-1418": {
            "任务类型": "自检",
            "自检等级": "二级",
            "特殊参数": "无"
        }
    }

    return json.dumps(todo_task)


@mcp.tool()
def assign_task(params: AssignTask) -> str:
    """
    根据id下发任务

    - 参数:
        - params: AssignTask对象，包含查询参数
            - task_id: 任务id
    """

    if params.task_id not in ("xd-1417", "xd-1418"):
        return "未找到对应的任务"

    return "任务下发成功，预计开始时间为2025年5月10日17:58，任务总时长8小时29分"



def run():
    mcp.run()

if __name__ == "__main__":
    run()
