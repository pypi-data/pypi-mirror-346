"""estats-client.

A Python client library for the e-Stat API.
"""

__version__ = "0.1.3"

from .client import (
    DataFormat,
    EstatsAPIClient,
    Language,
    MetaInfoParam,
    StatsDataParam,
    StatsListParam,
)
from .models.result import (
    Annotation as StatsDataAnnotation,
)
from .models.result import (
    Category as StatsDataCategory,
)
from .models.result import (
    Class as StatsDataClass,
)
from .models.result import (
    ClassInfo as StatsDataClassInfo,
)
from .models.result import (
    ClassObj as StatsDataClassObj,
)
from .models.result import (
    DataInfo as StatsDataDataInfo,
)
from .models.result import (
    GetStatsData,
    GetStatsDataResponse,
    StatisticalData,
)
from .models.result import (
    GovOrg as StatsDataGovOrg,
)
from .models.result import (
    Note as StatsDataNote,
)
from .models.result import (
    Parameter as StatsDataParameter,
)
from .models.result import (
    ResultInf as StatsDataResultInf,
)
from .models.result import (
    ResultInfo as StatsDataResultInfo,
)
from .models.result import (
    StatName as StatsDataStatName,
)
from .models.result import (
    TableInfo as StatsDataTableInfo,
)
from .models.result import (
    Title as StatsDataTitle,
)
from .models.result import (
    Value as StatsDataValue,
)
from .models.result_get_catalog import (
    DataCatalogInf,
    DataCatalogListInf,
    GetDataCatalog,
    GetDataCatalogResponse,
)
from .models.result_get_catalog import (
    Dataset as CatalogDataset,
)
from .models.result_get_catalog import (
    Organization as CatalogOrganization,
)
from .models.result_get_catalog import (
    Parameter as CatalogParameter,
)
from .models.result_get_catalog import (
    Resource as CatalogResource,
)
from .models.result_get_catalog import (
    Resources as CatalogResources,
)
from .models.result_get_catalog import (
    ResourceTitle as CatalogResourceTitle,
)
from .models.result_get_catalog import (
    ResultInf as CatalogResultInf,
)
from .models.result_get_catalog import (
    ResultInfo as CatalogResultInfo,
)
from .models.result_get_catalog import (
    StatName as CatalogStatName,
)
from .models.result_get_catalog import (
    Title as CatalogTitle,
)

__all__ = [
    "EstatsAPIClient",
    "StatsListParam",
    "MetaInfoParam",
    "StatsDataParam",
    "Language",
    "DataFormat",
    "GetStatsDataResponse",
    "GetStatsData",
    "StatisticalData",
    "StatsDataResultInfo",
    "StatsDataParameter",
    "StatsDataTableInfo",
    "StatsDataStatName",
    "StatsDataGovOrg",
    "StatsDataTitle",
    "StatsDataCategory",
    "StatsDataClassInfo",
    "StatsDataClassObj",
    "StatsDataClass",
    "StatsDataDataInfo",
    "StatsDataNote",
    "StatsDataAnnotation",
    "StatsDataValue",
    "StatsDataResultInf",
    "GetDataCatalogResponse",
    "GetDataCatalog",
    "DataCatalogListInf",
    "DataCatalogInf",
    "CatalogResultInfo",
    "CatalogParameter",
    "CatalogResultInf",
    "CatalogStatName",
    "CatalogOrganization",
    "CatalogTitle",
    "CatalogDataset",
    "CatalogResourceTitle",
    "CatalogResource",
    "CatalogResources",
]
