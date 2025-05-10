"""
estats-client

A Python client library for the e-Stat API.
"""

__version__ = "0.1.2" # pyproject.tomlと同期させる

from .models.client import (
    EstatsAPIClient,
    StatsListParam,
    MetaInfoParam,
    StatsDataParam,
    Language,
    DataFormat,
)
from .models.result import (
    ResultInfo as StatsDataResultInfo,
    Parameter as StatsDataParameter,
    StatName as StatsDataStatName,
    GovOrg as StatsDataGovOrg,
    Title as StatsDataTitle,
    Category as StatsDataCategory,
    TableInfo as StatsDataTableInfo,
    Class as StatsDataClass,
    ClassObj as StatsDataClassObj,
    ClassInfo as StatsDataClassInfo,
    Note as StatsDataNote,
    Annotation as StatsDataAnnotation,
    Value as StatsDataValue,
    DataInfo as StatsDataDataInfo,
    ResultInf as StatsDataResultInf,
    StatisticalData,
    GetStatsData,
    GetStatsDataResponse,
)
from .models.result_get_catalog import (
    ResultInfo as CatalogResultInfo,
    Parameter as CatalogParameter,
    ResultInf as CatalogResultInf,
    StatName as CatalogStatName,
    Organization as CatalogOrganization,
    Title as CatalogTitle,
    Dataset as CatalogDataset,
    ResourceTitle as CatalogResourceTitle,
    Resource as CatalogResource,
    Resources as CatalogResources,
    DataCatalogInf,
    DataCatalogListInf,
    GetDataCatalog,
    GetDataCatalogResponse,
)

# catalog.py の関数は、クライアントのメソッドとして再設計するか、
# 別途ユーティリティとして提供するか検討後のため、一旦コメントアウト
# from .models.catalog import get_all_catalog, get_stats_list_with_retry


__all__ = [
    # client models
    "EstatsAPIClient",
    "StatsListParam",
    "MetaInfoParam",
    "StatsDataParam",
    "Language",
    "DataFormat",
    # result (getStatsData) models
    "GetStatsDataResponse",
    "GetStatsData",
    "StatisticalData",
    "StatsDataResultInfo",
    "StatsDataParameter",
    "StatsDataTableInfo",
    "StatsDataStatName", # result.py由来のStatName
    "StatsDataGovOrg",
    "StatsDataTitle",    # result.py由来のTitle
    "StatsDataCategory",
    "StatsDataClassInfo",
    "StatsDataClassObj",
    "StatsDataClass",
    "StatsDataDataInfo",
    "StatsDataNote",
    "StatsDataAnnotation",
    "StatsDataValue",
    "StatsDataResultInf", # result.py由来のResultInf
    # result_get_catalog (getStatsList/getDataCatalog) models
    "GetDataCatalogResponse",
    "GetDataCatalog",
    "DataCatalogListInf",
    "DataCatalogInf",
    "CatalogResultInfo",
    "CatalogParameter",
    "CatalogResultInf", # result_get_catalog.py由来のResultInf
    "CatalogStatName",  # result_get_catalog.py由来のStatName
    "CatalogOrganization",
    "CatalogTitle",     # result_get_catalog.py由来のTitle
    "CatalogDataset",
    "CatalogResourceTitle",
    "CatalogResource",
    "CatalogResources",
    # "get_all_catalog",
    # "get_stats_list_with_retry",
]