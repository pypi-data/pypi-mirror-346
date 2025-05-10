from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field, field_validator


def ensure_list(v: Any) -> List[Any]:
    if isinstance(v, list):
        return v
    return [v]


class ResultInfo(BaseModel):
    status: int = Field(..., alias="STATUS")
    error_msg: str = Field(..., alias="ERROR_MSG")
    date: str = Field(..., alias="DATE")


class Parameter(BaseModel):
    lang: str = Field(..., alias="LANG")
    data_format: str = Field(..., alias="DATA_FORMAT")
    limit: int = Field(..., alias="LIMIT")


class ResultInf(BaseModel):
    from_number: int = Field(..., alias="FROM_NUMBER")
    to_number: int = Field(..., alias="TO_NUMBER")
    next_key: Optional[int] = Field(None, alias="NEXT_KEY")


class StatName(BaseModel):
    code: str = Field(..., alias="@code")
    value: str = Field(..., alias="$")


class Organization(BaseModel):
    code: str = Field(..., alias="@code")
    value: str = Field(..., alias="$")


class Title(BaseModel):
    name: str = Field(..., alias="NAME")
    tabulation_category: str = Field(..., alias="TABULATION_CATEGORY")
    tabulation_sub_category1: str = Field(..., alias="TABULATION_SUB_CATEGORY1")
    tabulation_sub_category2: str = Field(..., alias="TABULATION_SUB_CATEGORY2")
    tabulation_sub_category3: str = Field(..., alias="TABULATION_SUB_CATEGORY3")
    tabulation_sub_category4: str = Field(..., alias="TABULATION_SUB_CATEGORY4")
    tabulation_sub_category5: str = Field(..., alias="TABULATION_SUB_CATEGORY5")
    cycle: str = Field(..., alias="CYCLE")
    survey_date: str | int = Field(..., alias="SURVEY_DATE")
    collect_area: str = Field(..., alias="COLLECT_AREA")


class Dataset(BaseModel):
    stat_name: StatName = Field(..., alias="STAT_NAME")
    organization: Organization = Field(..., alias="ORGANIZATION")
    title: Title = Field(..., alias="TITLE")
    description: str = Field(..., alias="DESCRIPTION")
    publisher: str = Field(..., alias="PUBLISHER")
    contact_point: str = Field(..., alias="CONTACT_POINT")
    creator: str = Field(..., alias="CREATOR")
    release_date: str = Field(..., alias="RELEASE_DATE")
    last_modified_date: str = Field(..., alias="LAST_MODIFIED_DATE")
    frequency_of_update: str = Field(..., alias="FREQUENCY_OF_UPDATE")
    landing_page: str = Field(..., alias="LANDING_PAGE")


class ResourceTitle(BaseModel):
    name: str = Field(..., alias="NAME")
    table_category: Optional[str] = Field(None, alias="TABLE_CATEGORY")
    table_no: Optional[str | int] = Field(None, alias="TABLE_NO")
    table_name: str = Field(..., alias="TABLE_NAME")
    table_explanation: Optional[str] = Field(None, alias="TABLE_EXPLANATION")
    table_sub_category1: Optional[str] = Field(None, alias="TABLE_SUB_CATEGORY1")
    table_sub_category2: Optional[str] = Field(None, alias="TABLE_SUB_CATEGORY2")
    table_sub_category3: Optional[str] = Field(None, alias="TABLE_SUB_CATEGORY3")


class Resource(BaseModel):
    id: str = Field(..., alias="@id")
    title: ResourceTitle = Field(..., alias="TITLE")
    url: str = Field(..., alias="URL")
    description: str = Field(..., alias="DESCRIPTION")
    format: str = Field(..., alias="FORMAT")
    release_date: str = Field(..., alias="RELEASE_DATE")
    last_modified_date: str = Field(..., alias="LAST_MODIFIED_DATE")
    resource_licence_id: str = Field(..., alias="RESOURCE_LICENCE_ID")
    language: str = Field(..., alias="LANGUAGE")


class Resources(BaseModel):
    resource: List[Resource] = Field(
        alias="RESOURCE",
    )

    @field_validator("resource", mode="before")
    @classmethod
    def ensure_list(cls, v: Union[dict, list]) -> list:
        return [v] if isinstance(v, dict) else v


class DataCatalogInf(BaseModel):
    id: str = Field(..., alias="@id")
    dataset: Dataset = Field(..., alias="DATASET")
    resources: Resources = Field(..., alias="RESOURCES")


class DataCatalogListInf(BaseModel):
    number: int = Field(..., alias="NUMBER")
    result_inf: ResultInf = Field(..., alias="RESULT_INF")
    data_catalog_inf: List[DataCatalogInf] = Field(..., alias="DATA_CATALOG_INF")


class GetDataCatalog(BaseModel):
    result: ResultInfo = Field(..., alias="RESULT")
    parameter: Parameter = Field(..., alias="PARAMETER")
    data_catalog_list_inf: DataCatalogListInf = Field(
        ..., alias="DATA_CATALOG_LIST_INF"
    )


class GetDataCatalogResponse(BaseModel):
    get_data_catalog: GetDataCatalog = Field(..., alias="GET_DATA_CATALOG")
