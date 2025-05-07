from typing import Optional, List, Dict
from enum import Enum

from pydantic import BaseModel, TypeAdapter


class GAM(BaseModel):
    network_id: int


class XANDR(BaseModel):
    member_id: int
    aws_region: str


class ActivationChannels(BaseModel):
    gam: Optional[GAM] = None
    xandr: Optional[XANDR] = None


class Features(BaseModel):
    sso_data: bool = False
    enterprise: bool = False
    dcr: bool = False
    byok: bool = False
    gotom: bool = False
    coops: bool = False


class Prediction(BaseModel):
    name: str
    params_path: str


class CustomAttributeType(str, Enum):
    training = "training"
    direct = "direct"
    external_id = "external_id"


class CustomAttributeRawDataFormat(str, Enum):
    parquet = "parquet"
    json = "json"


class CustomAttribute(BaseModel):
    name: str
    target_external_id_name: str | None = None
    display_name: str | None = None
    category: str | None = None
    active: bool
    external_id_name: str
    raw_data_format: CustomAttributeRawDataFormat
    incremental: bool
    type: CustomAttributeType
    id_pii: bool | None = False
    value_pii: bool | None = False
    s3_predictions_params_path: str | None = None


class Taxonomies(BaseModel):
    name: str
    score: float


class CanonicalIdExtraction(BaseModel):
    uri_provider: str
    id_regex: str | None = None
    use_uri_path_hash_as_extracted_id: bool | None = None


class ScmiSiteType(str, Enum):
    SPA = "SPA"
    STATIC = "STATIC"


class ContentProvider(BaseModel):
    name: str
    section_prefixes: List[str]
    source_system: str | None = None
    content_id_extraction_query: str | None = None
    hardcoded_taxonomies: List[Taxonomies] | None = None
    canonical_id_extraction: CanonicalIdExtraction | None = None
    is_uri_extracted_id_external_id: bool | None = None
    uri_prefixes: List[str]
    scmi_site_id: str | None = None
    scmi_site_type: ScmiSiteType | None = None
    tracking_based_crawler: bool = False


class TrackingProvider(BaseModel):
    tracker: str
    logical_paths: List[str]


class TenantConfig(BaseModel):
    name: str
    timezone: str | None = None
    activation_channels: ActivationChannels
    features: Features
    predictions: List[Prediction]
    kropka_tenants: List[str]
    content_providers: List[ContentProvider]
    tracking_providers: List[TrackingProvider] | None = None
    custom_attributes: List[CustomAttribute] | None = None
    is_test_tenant: bool = False
    cron_schedule: Dict[str, str] | None = None


def get_json_schema():
    adapter = TypeAdapter(List[TenantConfig])
    return adapter.json_schema()
