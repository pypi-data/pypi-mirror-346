from enum import Enum
from typing import TYPE_CHECKING, Optional, TypedDict, Literal, Dict, List, Any

from typing_extensions import NotRequired

from aiob2.models.archetypes import B2Object

if TYPE_CHECKING:
    from aiob2.http import HTTPClient


class CORSRules(TypedDict):
    corsRuleName: str
    allowedOrigins: List[str]
    allowedOperations: List[Literal['b2_download_file_by_name', 'b2_download_file_by_id', 'b2_upload_file', 'b2_upload_part']]
    allowedHeaders: NotRequired[List[str]]
    exposeHeaders: NotRequired[List[str]]
    maxAgeSeconds: int    


LifeCycleRules = TypedDict('LifeCycleRules', {
    'daysFromHidingToDeleting': Optional[int],
    'daysFromUploadingToHiding': Optional[int],
    'fileNamePrefix': str
})


class BucketType(str, Enum):
    PUBLIC = 'allPublic'
    PRIVATE = 'allPrivate'
    RESTRICTED = 'restricted'
    SNAPSHOT = 'snapshot'
    SHARED = 'shared'


class BucketPayload(TypedDict):
    accountId: str
    bucketId: str
    bucketName: str
    bucketType: Literal['allPublic', 'allPrivate', 'restricted', 'snapshot', 'shared']
    bucketInfo: Dict[Any, Any]
    corsRules: List[CORSRules]
    fileLockConfiguration: Dict[Any, Any]
    defaultServerSideEncryption: Dict[Any, Any]
    lifecycleRules: LifeCycleRules
    replicationConfiguration: Dict[Any, Any]
    revision: int
    options: List[str]


class ListBucketPayload(TypedDict):
    buckets: List[BucketPayload]


class EventNotificationRule(TypedDict):
    eventTypes: List[str]
    isEnabled: bool
    isSuspended: bool
    name: str
    objectNamePrefix: str
    suspensionReason: str
    targetConfiguration: Dict[Any, Any]


class Bucket(B2Object):
    """Represents a Backblaze B2 bucket
    
    Attributes
    ----------
        account_id: :class:`str`
            The ID of the account the bucket belongs to
        id: :class:`str`
            The bucket's ID
        name: :class:`str`
            The bucket's name
        type: :class:`str`
        info: Dict[:class:`str`, :class:`str`]
        cors_rules: :class:`CORSRules`
        file_lock_config: Dict[Any, Any]
        default_sse: Dict[Any, Any]
        lifecycle_rules: Dict[Any, Any]
        replication_config: Dict[Any, Any]
        revision: :class:`str`
        options: :class:`str`
    """

    __slots__ = (
        'account_id',
        'id',
        'name',
        'type',
        'info',
        'cors_rules',
        'file_lock_config',
        'default_sse',
        'lifecycle_rules',
        'replication_config',
        'revision',
        'options',
        '_http'
    )

    def __init__(self, data: BucketPayload, _http: 'HTTPClient'):
        self.account_id: str = data['accountId']
        self.id: str = data['bucketId']
        self.name: str = data['bucketName']
        self.type: BucketType = BucketType(data['bucketType'])
        self.info: Dict[Any, Any] = data['bucketInfo']
        self.cors_rules: List[CORSRules] = data['corsRules']
        self.file_lock_config: Dict[Any, Any] = data['fileLockConfiguration']
        self.default_sse: Dict[Any, Any] = data['defaultServerSideEncryption']
        self.lifecycle_rules: LifeCycleRules = data['lifecycleRules']
        self.replication_config: Dict[Any, Any] = data['replicationConfiguration']
        self.revision: int = data['revision']
        self.options: List[str] = data['options']

        self._http = _http

    async def delete(self) -> None:
        """Deletes the bucket from your account. The target bucket must be empty."""
        await self._http.delete_bucket(self.id)

    # async def get_notification_rules(self) -> List[NotificationRule]
