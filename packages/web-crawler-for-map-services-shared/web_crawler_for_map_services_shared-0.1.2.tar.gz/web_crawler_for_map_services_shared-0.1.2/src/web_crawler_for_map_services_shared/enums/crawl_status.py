from enum import Enum

class CrawlStatus(Enum):
    QUEUED = 0
    PROCESSING = 1
    COMPLETED = 2
    FAILED = 3