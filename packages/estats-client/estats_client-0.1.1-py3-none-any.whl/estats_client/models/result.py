from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any, Union

class ResultInfo(BaseModel):
    status: int = Field(..., alias="STATUS")
    error_msg: str = Field(..., alias="ERROR_MSG")
    date: str = Field(..., alias="DATE")

class Parameter(BaseModel):
    lang: str = Field(..., alias="LANG")
    stats_data_id: str = Field(..., alias="STATS_DATA_ID")
    data_format: str = Field(..., alias="DATA_FORMAT")
    start_position: int = Field(..., alias="START_POSITION")
    limit: Optional[int] = Field(None, alias="LIMIT")
    metaget_flg: str = Field(..., alias="METAGET_FLG")
    cnt_get_flg: Optional[str] = Field(None, alias="CNT_GET_FLG")

class StatName(BaseModel):
    code: str = Field(..., alias="@code")
    value: str = Field(..., alias="$")

class GovOrg(BaseModel):
    code: str = Field(..., alias="@code")
    value: str = Field(..., alias="$")

class Title(BaseModel):
    no: str = Field(..., alias="@no")
    value: str = Field(..., alias="$")

class Category(BaseModel):
    code: str = Field(..., alias="@code")
    value: str = Field(..., alias="$")

class TableInfo(BaseModel):
    id: str = Field(..., alias="@id")
    stat_name: StatName = Field(..., alias="STAT_NAME")
    gov_org: GovOrg = Field(..., alias="GOV_ORG")
    statistics_name: str = Field(..., alias="STATISTICS_NAME")
    title: Title = Field(..., alias="TITLE")
    cycle: str = Field(..., alias="CYCLE")
    survey_date: Union[str, int] = Field(..., alias="SURVEY_DATE")
    open_date: str = Field(..., alias="OPEN_DATE")
    small_area: Union[str, int] = Field(..., alias="SMALL_AREA")
    collect_area: str = Field(..., alias="COLLECT_AREA")
    main_category: Category = Field(..., alias="MAIN_CATEGORY")
    sub_category: Category = Field(..., alias="SUB_CATEGORY")
    overall_total_number: int = Field(..., alias="OVERALL_TOTAL_NUMBER")
    updated_date: str = Field(..., alias="UPDATED_DATE")

class Class(BaseModel):
    code: str = Field(..., alias="@code")
    name: str = Field(..., alias="@name")
    level: str = Field(..., alias="@level")
    unit: Optional[str] = Field(None, alias="@unit")
    parent_code: Optional[str] = Field(None, alias="@parentCode")

class ClassObj(BaseModel):
    id: str = Field(..., alias="@id")
    name: str = Field(..., alias="@name")
    class_: Union[List[Class], Class] = Field(..., alias="CLASS")

class ClassInfo(BaseModel):
    class_obj: List[ClassObj] = Field(..., alias="CLASS_OBJ")

class Note(BaseModel):
    char: str = Field(..., alias="@char")
    value: str = Field(..., alias="$")

class Annotation(BaseModel):
    annotation: str = Field(..., alias="@annotation")
    value: str = Field(..., alias="$")

class Value(BaseModel):
    tab: Optional[str] = Field(None, alias="@tab")
    cat01: Optional[str] = Field(None, alias="@cat01")
    cat02: Optional[str] = Field(None, alias="@cat02")
    cat03: Optional[str] = Field(None, alias="@cat03")
    cat04: Optional[str] = Field(None, alias="@cat04")
    cat05: Optional[str] = Field(None, alias="@cat05")
    cat06: Optional[str] = Field(None, alias="@cat06")
    cat07: Optional[str] = Field(None, alias="@cat07")
    cat08: Optional[str] = Field(None, alias="@cat08")
    cat09: Optional[str] = Field(None, alias="@cat09")
    cat10: Optional[str] = Field(None, alias="@cat10")
    cat11: Optional[str] = Field(None, alias="@cat11")
    cat12: Optional[str] = Field(None, alias="@cat12")
    cat13: Optional[str] = Field(None, alias="@cat13")
    cat14: Optional[str] = Field(None, alias="@cat14")
    cat15: Optional[str] = Field(None, alias="@cat15")
    area: Optional[str] = Field(None, alias="@area")
    time: str = Field(..., alias="@time")
    unit: str = Field(..., alias="@unit")
    value: str = Field(..., alias="$")


class DataInfo(BaseModel):
    note: List[Note] = Field(..., alias="NOTE")
    annotation: Optional[List[Annotation]] = Field(None, alias="ANNOTATION")
    value: List[Value] = Field(..., alias="VALUE")
    @field_validator("note", mode="before")
    @classmethod
    def ensure_list(cls, v: Union[dict, list]) -> list:
        return [v] if isinstance(v, dict) else v
    
class ResultInf(BaseModel):
    total_number: int = Field(..., alias="TOTAL_NUMBER")
    from_number: int = Field(..., alias="FROM_NUMBER")
    to_number: int = Field(..., alias="TO_NUMBER")
    next_key: Optional[int] = Field(None, alias="NEXT_KEY")

class StatisticalData(BaseModel):
    result_inf: ResultInf = Field(..., alias="RESULT_INF")
    table_inf: TableInfo = Field(..., alias="TABLE_INF")
    class_inf: ClassInfo = Field(..., alias="CLASS_INF")
    data_inf: DataInfo = Field(..., alias="DATA_INF")

class GetStatsData(BaseModel):
    result: ResultInfo = Field(..., alias="RESULT")
    parameter: Parameter = Field(..., alias="PARAMETER")
    statistical_data: StatisticalData = Field(..., alias="STATISTICAL_DATA")

class GetStatsDataResponse(BaseModel):
    get_stats_data: GetStatsData = Field(..., alias="GET_STATS_DATA")
