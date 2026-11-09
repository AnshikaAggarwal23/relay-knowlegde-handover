from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class SourceType(str, Enum):
    GIT_COMMIT = "git_commit"
    PULL_REQUEST = "pull_request"
    TASK_CARD = "task_card"
    MEETING_NOTE = "meeting_note"
    STANDUP_CHAT = "standup_chat"

class ClaimCategory(str, Enum):
    DECISION = "decision"
    BLOCKER = "blocker"
    OWNERSHIP = "ownership"
    NEXT_ACTION = "next_action"

class VerificationStatus(str, Enum):
    VERIFIED = "verified"
    UNCERTAIN = "uncertain"
    CONTRADICTION = "contradiction"

class ProjectSource(BaseModel):
    id: str
    source_type: SourceType
    title: str
    content: str
    author: str
    timestamp: str
    metadata: Dict[str, Any] = {}
    is_sanitized: bool = True
    redacted_items_count: int = 0

class Citation(BaseModel):
    source_id: str
    source_title: str
    source_type: SourceType
    author: str
    timestamp: str
    exact_quote: str

class HandoverClaim(BaseModel):
    id: str
    category: ClaimCategory
    title: str
    summary: str
    rationale: Optional[str] = None
    verification_status: VerificationStatus = VerificationStatus.VERIFIED
    confidence_score: float = 0.95
    citations: List[Citation] = []
    conflict_notes: Optional[str] = None
    is_approved: bool = True
    human_notes: Optional[str] = None

class HandoverManifest(BaseModel):
    project_id: str
    project_name: str
    departing_member: str
    target_successor_role: str
    created_at: str
    is_sealed: bool = False
    claims: List[HandoverClaim] = []
    sources: List[ProjectSource] = []
    summary_stats: Dict[str, Any] = {}
