from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, HttpUrl, ConfigDict, model_validator

# Common Models
class Location(BaseModel):
    owner: Optional[str] = None
    province_cn: Optional[str] = None
    isp: Optional[str] = None
    province_en: Optional[str] = None
    country_en: Optional[str] = None
    district_cn: Optional[str] = None
    gps: Optional[List[float]] = None # [longitude, latitude]
    street_cn: Optional[str] = None
    city_en: Optional[str] = None
    district_en: Optional[str] = None
    country_cn: Optional[str] = None
    street_en: Optional[str] = None
    city_cn: Optional[str] = None
    country_code: Optional[str] = None
    asname: Optional[str] = None
    scene_cn: Optional[str] = None
    scene_en: Optional[str] = None
    radius: Optional[float] = None

class Component(BaseModel):
    product_level: Optional[str] = None
    product_catalog: Optional[List[str]] = None
    product_vendor: Optional[str] = None
    product_name_cn: Optional[str] = None
    product_name_en: Optional[str] = None
    id: Optional[str] = None
    version: Optional[str] = None
    product_type: Optional[List[str]] = None

class ImageItem(BaseModel):
    data: Optional[str] = None
    mime: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    md5: Optional[str] = None
    s3_url: Optional[str] = None

class Favicon(BaseModel):
    hash: Optional[str] = None
    data: Optional[str] = None # Base64 encoded image data
    location: Optional[str] = None
    s3_url: Optional[str] = None

class CookieElement(BaseModel):
    order_hash: Optional[str] = None
    simhash: Optional[str] = None

class DomTreeInfo(BaseModel):
    dom_hash: Optional[str] = None
    simhash: Optional[str] = None

class LinkOtherItem(BaseModel):
    is_inner: Optional[bool] = None
    url: Optional[str] = None # Changed from HttpUrl to str to allow javascript: links

class LinkImgItem(BaseModel):
    is_inner: Optional[bool] = None
    url: Optional[str] = None
    md5: Optional[str] = None

class LinkScriptItem(BaseModel):
    is_inner: Optional[bool] = None
    url: Optional[str] = None
    md5: Optional[str] = None

class LinkInfo(BaseModel):
    other: Optional[List[LinkOtherItem]] = None
    img: Optional[List[LinkImgItem]] = None
    script: Optional[List[LinkScriptItem]] = None

class HttpServiceInfo(BaseModel):
    status_code: Optional[int] = None
    path: Optional[str] = None
    title: Optional[str] = None
    meta_keywords: Optional[str] = None
    server: Optional[str] = None
    x_powered_by: Optional[str] = None
    favicon: Optional[Favicon] = None
    host: Optional[str] = None
    html_hash: Optional[str] = None
    response_headers: Optional[str] = None
    header_order_hash: Optional[str] = None
    body: Optional[str] = None
    robots_hash: Optional[str] = None
    robots: Optional[str] = None
    sitemap_hash: Optional[str] = None
    sitemap: Optional[str] = None
    cookie_element: Optional[CookieElement] = None
    dom_tree: Optional[DomTreeInfo] = None
    script_function: Optional[List[str]] = None
    script_variable: Optional[List[str]] = None
    css_class: Optional[List[str]] = None
    css_id: Optional[List[str]] = None
    http_load_url: Optional[List[HttpUrl]] = None
    icp: Optional["ICPInfo"] = None
    copyright: Optional[str] = None
    mail: Optional[List[str]] = None
    page_type: Optional[List[str]] = None
    iframe_url: Optional[List[HttpUrl]] = None
    iframe_hash: Optional[List[str]] = None
    iframe_title: Optional[List[str]] = None
    iframe_keywords: Optional[List[str]] = None
    domain_is_wildcard: Optional[bool] = None
    is_domain: Optional[bool] = None
    icp_nature: Optional[str] = None
    icp_keywords: Optional[str] = None
    http_load_count: Optional[int] = None
    data_sources: Optional[int] = None
    page_type_keyword: Optional[List[str]] = None
    link: Optional[LinkInfo] = None


class TLSJarm(BaseModel):
    jarm_hash: Optional[str] = None
    jarm_ans: Optional[List[str]] = None


class FtpServiceInfo(BaseModel):
    is_anonymous: Optional[bool] = None

class RsyncServiceInfo(BaseModel):
    authentication: Optional[bool] = None

class SshKey(BaseModel):
    type: Optional[str] = None
    fingerprint: Optional[str] = None
    key: Optional[str] = None

class SshServiceInfo(BaseModel):
    server_keys: Optional[List[SshKey]] = None
    ciphers: Optional[List[str]] = None
    kex: Optional[List[str]] = None
    digests: Optional[List[str]] = None
    key_types: Optional[List[str]] = None
    compression: Optional[List[str]] = None

class UpnpServiceInfo(BaseModel):
    deviceType: Optional[str] = None
    friendlyName: Optional[str] = None
    manufacturer: Optional[str] = None
    manufacturerURL: Optional[HttpUrl] = None
    modelDescription: Optional[str] = None
    modelName: Optional[str] = None
    modelNumber: Optional[str] = None

class ICPInfo(BaseModel):
    licence: Optional[str] = None
    update_time: Optional[str] = None
    is_expired: Optional[bool] = None
    leader_name: Optional[str] = None
    domain: Optional[str] = None
    main_licence: Optional[Dict[str, Any]] = None
    content_type_name: Optional[str] = None
    limit_access: Optional[bool] = None

class SnmpServiceInfo(BaseModel):
    sysname: Optional[str] = None
    sysdesc: Optional[str] = None
    sysuptime: Optional[str] = None
    syslocation: Optional[str] = None
    syscontact: Optional[str] = None
    sysobjectid: Optional[str] = None

class DockerContainer(BaseModel):
    Image: Optional[str] = None
    Command: Optional[str] = None

class DockerVersionInfo(BaseModel):
    Version: Optional[str] = None
    ApiVersion: Optional[str] = None
    MinAPIVersion: Optional[str] = None
    GitCommit: Optional[str] = None
    GoVersion: Optional[str] = None
    Arch: Optional[str] = None
    KernelVersion: Optional[str] = None
    BuildTime: Optional[str] = None

class DockerServiceInfo(BaseModel):
    containers: Optional[List[DockerContainer]] = None
    version: Optional[DockerVersionInfo] = None

class DnsServiceInfo(BaseModel):
    id_server: Optional[str] = None
    version_bind: Optional[str] = None

class ElasticIndex(BaseModel):
    health: Optional[str] = None
    status: Optional[str] = None
    index: Optional[str] = None
    uuid: Optional[str] = None # Renamed field, aliased to API's "uuid"
    docs_count: Optional[Union[int,str]] = None
    store_size: Optional[str] = None
    pri: Optional[str] = None
    rep: Optional[str] = None
    pri_store_size: Optional[str] = None
    docs_deleted: Optional[str] = None

class ElasticServiceInfo(BaseModel):
    indices: Optional[List[ElasticIndex]] = None

class HiveDbTable(BaseModel):
    dbname: Optional[str] = None
    tables: Optional[List[str]] = None

class HiveServiceInfo(BaseModel):
    hive_dbs: Optional[List[HiveDbTable]] = None

class MongoOpenSSLInfo(BaseModel):
    running: Optional[str] = None
    compiled: Optional[str] = None

class MongoBuildEnvironmentInfo(BaseModel):
    distmod: Optional[str] = None
    distarch: Optional[str] = None
    cc: Optional[str] = None
    ccflags: Optional[str] = None
    cxx: Optional[str] = None
    cxxflags: Optional[str] = None
    linkflags: Optional[str] = None
    target_arch: Optional[str] = None
    target_os: Optional[str] = None
    cppdefines: Optional[str] = None

class MongoBuildInfo(BaseModel):
    version: Optional[str] = None
    gitVersion: Optional[str] = None
    openssl: Optional[MongoOpenSSLInfo] = None # 恢复类型
    sysInfo: Optional[str] = None
    allocator: Optional[str] = None
    versionArray: Optional[List[int]] = None
    javascriptEngine: Optional[str] = None
    bits: Optional[int] = None
    debug: Optional[bool] = None
    maxBsonObjectSize: Optional[int] = None
    buildEnvironment: Optional[MongoBuildEnvironmentInfo] = None # 恢复类型
    storageEngines: Optional[List[str]] = None # 恢复类型
    modules: Optional[List[str]] = None # 修改为 List[str]
    ok: Optional[float] = None # 恢复类型

class MongoConnections(BaseModel):
    current: Optional[int] = None
    available: Optional[int] = None
    totalCreated: Optional[int] = None
    rejected: Optional[int] = None
    active: Optional[int] = None
    threaded: Optional[int] = None
    exhaustIsMaster: Optional[int] = None
    exhaustHello: Optional[int] = None
    awaitingTopologyChanges: Optional[int] = None

class MongoServerStatus(BaseModel):
    host: Optional[str] = None
    process: Optional[str] = None
    pid: Optional[int] = None
    connections: Optional[MongoConnections] = None

class MongoDatabase(BaseModel):
    name: Optional[str] = None
    sizeOnDisk: Optional[Union[float,int,str]] = None
    empty: Optional[bool] = None

class MongoListDatabases(BaseModel):
    databases: Optional[List[MongoDatabase]] = None
    totalSize: Optional[Union[int,str]] = None
    totalSizeMb: Optional[int] = None

class MongoServiceInfo(BaseModel):
    authentication: Optional[bool] = None
    buildInfo: Optional[MongoBuildInfo] = None # 恢复类型
    serverStatus: Optional[MongoServerStatus] = None
    listDatabases: Optional[MongoListDatabases] = None

class EthernetIpServiceInfo(BaseModel):
    product_name: Optional[str] = None
    product_code: Optional[int] = None
    device_ip: Optional[str] = None
    vendor: Optional[str] = None
    revision: Optional[str] = None
    serial_num: Optional[str] = None
    device_type: Optional[str] = None

class ModbusProjectInfo(BaseModel):
    Project_Revision: Optional[str] = None
    ProjectLastModified: Optional[str] = None
    ProjectInformation: Optional[str] = None

class ModbusServiceInfo(BaseModel):
    UnitId: Optional[int] = None
    DeviceIdentification: Optional[str] = None
    SlaveIDdata: Optional[str] = None
    CpuModule: Optional[str] = None
    MemoryCard: Optional[str] = None
    ProjectInfo: Optional[ModbusProjectInfo] = None

class S7ServiceInfo(BaseModel):
    Module: Optional[str] = None
    Basic_Hardware: Optional[str] = None
    Basic_Firmware: Optional[str] = None
    Name_of_the_PLC: Optional[str] = None
    Name_of_the_module: Optional[str] = None
    Plant_identification: Optional[str] = None
    Reserved_for_operating_system: Optional[str] = None
    Module_type_name: Optional[str] = None
    Serial_number_of_memory_card: Optional[str] = None
    OEM_ID_of_a_module: Optional[str] = None
    Location_designation_of_a_module: Optional[str] = None
    unknown_129: Optional[str] = Field(default=None, alias="Unknown(129)")

class SmbServiceInfo(BaseModel):
    ServerDefaultDialect: Optional[str] = None
    ListDialects: Optional[List[str]] = None
    Capabilities: Optional[List[str]] = None
    Authentication: Optional[str] = None
    ServerOS: Optional[str] = None
    ServerDomain: Optional[str] = None
    ServerDNSDomainName: Optional[str] = None
    RemoteName: Optional[str] = None
    SupportNTLMv2: Optional[bool] = None  # 新增字段
    SMBv1OS: Optional[str] = None  # 新增字段
    listShares: Optional[List[Any]] = None

class TlsValidationInfo(BaseModel):
    matches_domain: Optional[bool] = None
    browser_trusted: Optional[bool] = None
    browser_error: Optional[str] = None

class TlsServiceInfo(BaseModel):
    tls_AKID: Optional[str] = None
    tls_authority_key_id: Optional[str] = None # Assuming this is the direct field if tls_AKID is the alias target
    tls_SAN: Optional[List[str]] = None
    tls_subject_alt_name: Optional[List[str]] = None # Assuming this is the direct field if tls_SAN is the alias target
    tls_SKID: Optional[str] = None
    tls_subject_key_id: Optional[str] = None # Assuming this is the direct field if tls_SKID is the alias target
    tls_md5: Optional[str] = None
    tls_sha1: Optional[str] = None
    tls_sha256: Optional[str] = None
    tls_SPKI: Optional[str] = None
    tls_subject_key_info_sha256: Optional[str] = None # Assuming this is the direct field if tls_SPKI is the alias target
    tls_SN: Optional[str] = None
    tls_serial_number: Optional[str] = None # Assuming this is the direct field if tls_SN is the alias target
    tls_issuer: Optional[str] = None
    tls_issuer_common_name: Optional[str] = None # Direct field name
    # tls_issuer_CN is removed as it was an alias for tls_issuer_common_name
    tls_issuer_country: Optional[str] = None # Direct field name
    # tls_issuer_C is removed as it was an alias for tls_issuer_country
    tls_issuer_organization: Optional[str] = None # Direct field name
    # tls_issuer_O is removed as it was an alias for tls_issuer_organization
    tls_subject: Optional[str] = None
    tls_subject_common_name: Optional[str] = None # Direct field name
    # tls_subject_CN is removed as it was an alias for tls_subject_common_name
    tls_subject_country: Optional[str] = None # Direct field name
    # tls_subject_C is removed as it was an alias for tls_subject_country
    tls_subject_organization: Optional[str] = None # Direct field name
    # tls_subject_O is removed as it was an alias for tls_subject_organization
    common_name_wildcard: Optional[bool] = None
    ja3s: Optional[str] = None
    ja4s: Optional[str] = None
    two_way_authentication: Optional[bool] = None
    handshake_log: Optional[Dict[str, Any]] = None
    version: Optional[List[str]] = None # Direct field name for versions
    validation: Optional[TlsValidationInfo] = None

    # model_config = ConfigDict(populate_by_name=True) # Not needed if aliases are removed


class IPTcpData(BaseModel):
    window: Optional[int] = None

class IPAddressData(BaseModel):
    distance: Optional[int] = None
    initial_ttl: Optional[int] = None
    tos: Optional[int] = None
    ttl: Optional[int] = None

class NetData(BaseModel):
    service_probe_name: Optional[str] = None
    tcp: Optional[IPTcpData] = None
    router_ip: Optional[str] = None
    ip: Optional[IPAddressData] = None
    port_response_time: Optional[int] = None


class ServiceSpecificData(BaseModel):
    http: Optional[HttpServiceInfo] = None
    ftp: Optional[FtpServiceInfo] = None
    rsync: Optional[RsyncServiceInfo] = None
    ssh: Optional[SshServiceInfo] = None
    upnp: Optional[UpnpServiceInfo] = None
    snmp: Optional[SnmpServiceInfo] = None
    docker: Optional[DockerServiceInfo] = None
    domain: Optional[DnsServiceInfo] = None # Changed from dns to domain
    elastic: Optional[ElasticServiceInfo] = None
    hive: Optional[HiveServiceInfo] = None
    mongodb: Optional[MongoServiceInfo] = None
    ethernetip: Optional[EthernetIpServiceInfo] = None
    modbus: Optional[ModbusServiceInfo] = None
    s7: Optional[S7ServiceInfo] = None
    smb: Optional[SmbServiceInfo] = None
    tls: Optional[TlsServiceInfo] = None


class ServiceData(BaseModel):
    product: Optional[str] = None
    components: Optional[List[Component]] = None
    port: Optional[int] = None
    service_id: Optional[str] = None
    name: str
    cert: Optional[str] = None
    transport: Optional[str] = None
    time: Optional[str] = None
    version: Optional[str] = None
    tags: Optional[List[str]] = None
    response: Optional[str] = None
    response_hash: Optional[str] = None
    net: Optional[NetData] = None

    @model_validator(mode='before')
    @classmethod
    def populate_tls_data(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        service_name = values.get('name')
        if service_name in ('tls', 'tls/ssl'):
            # 如果服务名称表明是TLS相关服务，
            # 并且原始数据中 'service' 对象下没有 'tls' 键，或者该键的值不是一个字典，
            # 我们就主动为 'tls' 键设置一个空字典。
            # 这样 Pydantic 在后续处理时，会用这个空字典去尝试创建 TlsServiceInfo 实例，
            # 结果将是一个所有字段都为 None 的 TlsServiceInfo 对象，
            # 但 ServiceData.tls 本身将不再是 None。
            if not isinstance(values.get('tls'), dict): # 包含了 'tls' 不存在或其值不是字典的情况
                values['tls'] = {} 
            
            # 'tls-jarm' 字段由其别名处理。
            # 如果原始数据中 'service' 对象下存在 'tls-jarm' 键，
            # Pydantic 会用它来填充 ServiceData 模型的 'tls_jarm' 属性。
            # 如果不存在，'tls_jarm' 将保持为 None。
            # 此处校验器无需为 'tls_jarm' 做特殊处理。
        return values

    @model_validator(mode='before')
    @classmethod
    def populate_full_mongodb_buildinfo(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        # Normalize service name first
        service_name = values.get('name')
        if service_name == 'mongodb/ssl':
            values['name'] = 'mongodb'
            service_name = 'mongodb'  # Update for current scope

        # If it's a mongodb service, try to get full buildInfo from response
        if service_name == 'mongodb':
            raw_response_str = values.get('response')
            # Ensure 'mongodb' key exists and is a dict before trying to access/modify it
            if 'mongodb' not in values or not isinstance(values.get('mongodb'), dict):
                values['mongodb'] = {} # Initialize if not present or not a dict

            mongodb_data = values.get('mongodb') # Now it's guaranteed to be a dict or newly initialized {}

            if raw_response_str and isinstance(mongodb_data, dict):
                import json # Import locally to avoid top-level import if not always needed
                try:
                    parsed_response = json.loads(raw_response_str)
                    if isinstance(parsed_response, dict):
                        full_build_info_from_response = parsed_response.get('buildInfo')

                        if isinstance(full_build_info_from_response, dict):
                            # Ensure 'buildInfo' in mongodb_data is a dict before updating
                            if not isinstance(mongodb_data.get('buildInfo'), dict):
                                mongodb_data['buildInfo'] = {}
                            
                            # Update the existing buildInfo with fields from the full_build_info_from_response
                            # This prioritizes fields from response, but keeps others if they exist in the direct mongodb.buildInfo
                            # A more robust merge might be needed if there are complex overlaps
                            # For now, let's assume full_build_info_from_response is more complete or authoritative
                            mongodb_data['buildInfo'] = full_build_info_from_response
                            
                except json.JSONDecodeError:
                    # Log or handle error if response is not valid JSON
                    pass 
        return values

    http: Optional[HttpServiceInfo] = None
    ftp: Optional[FtpServiceInfo] = None
    rsync: Optional[RsyncServiceInfo] = None
    ssh: Optional[SshServiceInfo] = None
    upnp: Optional[UpnpServiceInfo] = None
    snmp: Optional[SnmpServiceInfo] = None
    docker: Optional[DockerServiceInfo] = None
    domain: Optional[DnsServiceInfo] = None # Changed from dns to domain
    elastic: Optional[ElasticServiceInfo] = None
    hive: Optional[HiveServiceInfo] = None
    mongodb: Optional[MongoServiceInfo] = None
    ethernetip: Optional[EthernetIpServiceInfo] = None
    modbus: Optional[ModbusServiceInfo] = None
    s7: Optional[S7ServiceInfo] = None
    smb: Optional[SmbServiceInfo] = None
    tls: Optional[TlsServiceInfo] = None
    tls_jarm: Optional[TLSJarm] = Field(default=None, alias="tls-jarm")


class QuakeService(BaseModel):
    ip: str
    port: int
    hostname: Optional[str] = None
    transport: Optional[str] = None
    asn: Optional[int] = None
    org: Optional[str] = None
    service: ServiceData
    location: Optional[Location] = None
    time: Optional[str] = None
    domain: Optional[str] = None
    components: Optional[List[Component]] = None
    images: Optional[List[ImageItem]] = None
    is_ipv6: Optional[bool] = None
    is_latest: Optional[bool] = None
    app: Optional[Component] = None
    id: Optional[str] = None
    os_name: Optional[str] = None


class QuakeHost(BaseModel):
    hostname: Optional[str] = None
    org: Optional[str] = None
    ip: str
    os_version: Optional[str] = None
    os_name: Optional[str] = None
    location: Optional[Location] = None
    is_ipv6: Optional[bool] = False
    services: Optional[List[ServiceData]] = None
    time: Optional[str] = None
    asn: Optional[int] = None
    id: Optional[str] = None


# User Info Models
class UserRole(BaseModel):
    fullname: str
    priority: int
    credit: int

class EnterpriseInformation(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    status: str

class PrivacyLog(BaseModel):
    status: bool
    time: Optional[str] = None

class User(BaseModel):
    id: str
    username: str
    fullname: str
    email: str

class UserInfoData(BaseModel):
    id: str
    user: User
    baned: bool
    ban_status: str
    credit: int
    persistent_credit: int
    token: str
    mobile_phone: Optional[str] = None
    source: str
    privacy_log: PrivacyLog
    enterprise_information: EnterpriseInformation
    personal_information_status: bool
    role: List[UserRole]


# Aggregation Models
class AggregationBucket(BaseModel):
    key: Union[str, int, float]
    doc_count: int

class AggregationData(BaseModel):
    pass


# Favicon Similarity Models
class SimilarIconData(BaseModel):
    key: str
    doc_count: int
    data: Optional[str] = None


# Pagination and Metadata
class Pagination(BaseModel):
    count: Optional[int] = None
    page_index: Optional[int] = None
    page_size: Optional[int] = None
    total: Optional[Union[int, Dict[str, Any]]] = None
    pagination_id: Optional[str] = None

class Meta(BaseModel):
    pagination: Optional[Pagination] = None
    total: Optional[Union[int, Dict[str, Any]]] = None
    pagination_id: Optional[str] = None


# Generic API Response Wrapper
class QuakeResponse(BaseModel):
    code: Union[int, str]
    message: str
    data: Optional[Any] = None
    meta: Optional[Meta] = None


# Specific Response Models
class UserInfoResponse(QuakeResponse):
    data: Optional[UserInfoData] = None

class FilterableFieldsResponse(QuakeResponse):
    data: Optional[List[str]] = None

class ServiceSearchResponse(QuakeResponse):
    data: Union[Optional[List[QuakeService]], Dict[Any, Any]] = None
    meta: Meta

class ServiceScrollResponse(QuakeResponse):
    data: Optional[List[QuakeService]] = None
    meta: Meta

class ServiceAggregationResponse(QuakeResponse):
    data: Optional[Dict[str, List[AggregationBucket]]] = None
    meta: Optional[Meta] = None

class HostSearchResponse(QuakeResponse):
    data: Union[Optional[List[QuakeHost]], dict] = None
    meta: Meta

class HostScrollResponse(QuakeResponse):
    data: Union[Optional[List[QuakeHost]], dict] = None
    meta: Meta

class HostAggregationResponse(QuakeResponse):
    data: Union[Optional[Dict[str, List[AggregationBucket]]], dict] = None
    meta: Optional[Meta] = None

class SimilarIconResponse(QuakeResponse):
    data: Union[Optional[List[SimilarIconData]], dict] = None
    meta: Optional[Meta] = None


# Request Body Models
class BaseSearchQuery(BaseModel):
    query: Optional[str] = None
    ignore_cache: Optional[bool] = False
    start_time: Optional[str] = None # YYYY-MM-DD HH:MM:SS
    end_time: Optional[str] = None   # YYYY-MM-DD HH:MM:SS
    ip_list: Optional[List[str]] = None
    rule: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def check_query_or_ip_list(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if not values.get('query') and not values.get('ip_list'):
            if cls.__name__ != "AggregationQuery": # AggregationQuery always needs a query
                 raise ValueError('Either "query" or "ip_list" must be provided for search queries.')
            elif not values.get('query'): # This implies cls.__name__ == "AggregationQuery"
                 raise ValueError('"query" must be provided for aggregation queries.')
        return values

class RealtimeSearchQuery(BaseSearchQuery):
    start: Optional[int] = 0 # 用户要求添加的参数，随机1-100，但这里设置为0作为默认值，实际使用时再随机
    size: Optional[int] = 10
    include: Optional[List[str]] = None
    exclude: Optional[List[str]] = None
    latest: Optional[bool] = False # For service search
    shortcuts: Optional[List[str]] = None # For service search

class ScrollSearchQuery(BaseSearchQuery):
    size: Optional[int] = 10
    pagination_id: Optional[str] = None
    include: Optional[List[str]] = None
    exclude: Optional[List[str]] = None
    latest: Optional[bool] = False # For service scroll

class AggregationQuery(BaseSearchQuery):
    aggregation_list: List[str]
    size: Optional[int] = 5 # Per aggregation item
    latest: Optional[bool] = False # For service aggregation

class FaviconSimilarityQuery(BaseModel):
    favicon_hash: str
    similar: Optional[float] = Field(0.9, ge=0, le=1)
    size: Optional[int] = 10
    ignore_cache: Optional[bool] = False
    start_time: Optional[str] = None
    end_time: Optional[str] = None
