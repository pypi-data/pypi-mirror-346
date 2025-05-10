import requests
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
import json


class Language(str, Enum):
    JAPANESE = "J"
    ENGLISH = "E"


class DataFormat(str, Enum):
    XML = "X"
    JSON = "J"
    JSONP = "P"
    CSV = "C"


class StatsListParam(BaseModel):
    surveyYears: Optional[str] = None
    openYears: Optional[str] = None
    statsField: Optional[str] = None
    statsCode: Optional[str] = None
    searchWord: Optional[str] = None
    searchKind: Optional[str] = None
    collectArea: Optional[str] = None
    explanationGetFlg: Optional[str] = None
    statsNameList: Optional[str] = None
    startPosition: Optional[int] = None
    limit: Optional[int] = None
    updatedDate: Optional[str] = None


class MetaInfoParam(BaseModel):
    statsDataId: str
    explanationGetFlg: Optional[str] = None


class StatsDataParam(BaseModel):
    dataSetId: Optional[str] = None
    statsDataId: Optional[str] = None
    lvTab: Optional[str] = None
    cdTab: Optional[str] = None
    cdTabFrom: Optional[str] = None
    cdTabTo: Optional[str] = None
    lvTime: Optional[str] = None
    cdTime: Optional[str] = None
    cdTimeFrom: Optional[str] = None
    cdTimeTo: Optional[str] = None
    lvArea: Optional[str] = None
    cdArea: Optional[str] = None
    cdAreaFrom: Optional[str] = None
    cdAreaTo: Optional[str] = None
    lvCat01: Optional[str] = None
    cdCat01: Optional[str] = None
    cdCat01From: Optional[str] = None
    cdCat01To: Optional[str] = None
    startPosition: Optional[int] = None
    limit: Optional[int] = None
    metaGetFlg: Optional[str] = None
    cntGetFlg: Optional[str] = None
    explanationGetFlg: Optional[str] = None
    annotationGetFlg: Optional[str] = None
    replaceSpChar: Optional[str] = None


class EstatsAPIClient:
    BASE_URL = "https://api.e-stat.go.jp/rest/3.0/app/json"

    def __init__(self, app_id: str):
        self.app_id = app_id
        self.session = requests.Session()
        

    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> dict:
        url = f"{self.BASE_URL}/{endpoint}"
        params["appId"] = self.app_id
        response = self.session.get(url, params=params)
        response.raise_for_status()
        res = json.loads(response.content.decode('shift-jis'))
        
        return res

    def get_stats_list(
        self,
        params: StatsListParam,
        lang: Language = Language.JAPANESE,
        data_format: DataFormat = DataFormat.JSON,
    ) -> dict:
        endpoint = "getDataCatalog"
        params_dict = params.model_dump(exclude_none=True)
        params_dict["lang"] = lang.value
        params_dict["dataFormat"] = data_format.value
        return self._make_request(endpoint, params_dict)

    def get_stats_data(
        self,
        params: StatsDataParam,
        lang: Language = Language.JAPANESE,
        data_format: DataFormat = DataFormat.JSON,
    ) -> dict:
        endpoint = "getStatsData"
        params_dict = params.model_dump(exclude_none=True)
        params_dict["lang"] = lang.value
        params_dict["dataFormat"] = data_format.value
        return self._make_request(endpoint, params_dict)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()