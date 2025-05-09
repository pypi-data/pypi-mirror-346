from pydantic import BaseModel


class GetGshjCombination(BaseModel):
    index: int = 1


class GetPredResult(BaseModel):
    elem_list: list[str]
    con_list: list[float]


class GetTptjPicture(BaseModel):
    need_color: bool = False


class AssignTask(BaseModel):
    task_id: str