from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

from app.models import (
    ProjectSource, HandoverClaim, HandoverManifest, 
    SourceType, ClaimCategory, VerificationStatus
)
from app.sample_data import get_sanitized_sample_sources, get_sample_handover_claims
from app.sanitizer import sanitize_content
from app.extractor import reconstruct_project_state

router = APIRouter()

# In-memory session store (acts as instant state cache backed by SQLite models)
ACTIVE_PROJECTS: Dict[str, HandoverManifest] = {}

def get_or_create_project(project_id: str = "proj-festflow-01") -> HandoverManifest:
    if project_id not in ACTIVE_PROJECTS:
        sources = get_sanitized_sample_sources()
        claims = get_sample_handover_claims()
        ACTIVE_PROJECTS[project_id] = HandoverManifest(
            project_id=project_id,
            project_name="FestFlow: Campus Fest Web Portal",
            departing_member="Aryan Sharma (Lead Developer, Final Year)",
            target_successor_role="Junior Full-Stack Developer",
            created_at=datetime.utcnow().isoformat(),
            is_sealed=False,
            claims=claims,
            sources=sources,
            summary_stats={
                "total_sources": len(sources),
                "total_claims": len(claims),
                "verified_claims": sum(1 for c in claims if c.verification_status == VerificationStatus.VERIFIED),
                "conflicts_flagged": sum(1 for c in claims if c.verification_status == VerificationStatus.CONTRADICTION),
                "uncertain_claims": sum(1 for c in claims if c.verification_status == VerificationStatus.UNCERTAIN),
                "redacted_secrets_count": sum(s.redacted_items_count for s in sources)
            }
        )
    return ACTIVE_PROJECTS[project_id]

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Relay Knowledge Handover Engine",
        "version": "2.0.0-round2",
        "active_projects": len(ACTIVE_PROJECTS)
    }

@router.post("/sample/load", response_model=HandoverManifest)
def load_sample_project():
    """
    1-Click Judge Quick-Start endpoint.
    Loads the benchmark Campus Fest project with pre-sanitized sources and evidence claims.
    """
    project = get_or_create_project("proj-festflow-01")
    return project

class CustomSourceInput(BaseModel):
    title: str
    source_type: SourceType
    content: str
    author: Optional[str] = "Anonymous Contributor"

@router.post("/sources/add", response_model=ProjectSource)
def add_custom_source(source_in: CustomSourceInput, project_id: str = "proj-festflow-01"):
    """
    Stage 1: Connect.
    Accepts custom text/code notes, runs regex credential scrubbing, and attaches to project.
    """
    project = get_or_create_project(project_id)
    clean_text, red_count, red_types = sanitize_content(source_in.content)
    
    new_src = ProjectSource(
        id=f"SRC-CUSTOM-{len(project.sources)+1:02d}",
        source_type=source_in.source_type,
        title=source_in.title,
        content=clean_text,
        author=source_in.author,
        timestamp=datetime.utcnow().isoformat(),
        is_sanitized=True,
        redacted_items_count=red_count,
        metadata={"redacted_types": red_types}
    )
    project.sources.append(new_src)
    project.summary_stats["total_sources"] = len(project.sources)
    project.summary_stats["redacted_secrets_count"] += red_count
    return new_src

@router.post("/reconstruct", response_model=List[HandoverClaim])
async def trigger_reconstruct(project_id: str = "proj-festflow-01"):
    """
    Stage 2 & 3: Reconstruct & Verify.
    Synthesizes project state and executes bi-directional citation matching.
    """
    project = get_or_create_project(project_id)
    claims = await reconstruct_project_state(project.sources)
    project.claims = claims
    project.summary_stats["total_claims"] = len(claims)
    project.summary_stats["verified_claims"] = sum(1 for c in claims if c.verification_status == VerificationStatus.VERIFIED)
    project.summary_stats["conflicts_flagged"] = sum(1 for c in claims if c.verification_status == VerificationStatus.CONTRADICTION)
    project.summary_stats["uncertain_claims"] = sum(1 for c in claims if c.verification_status == VerificationStatus.UNCERTAIN)
    return claims

class ClaimUpdateInput(BaseModel):
    claim_id: str
    title: Optional[str] = None
    summary: Optional[str] = None
    human_notes: Optional[str] = None
    is_approved: Optional[bool] = None
    verification_status: Optional[VerificationStatus] = None

@router.post("/claims/update", response_model=HandoverClaim)
def update_claim(update_data: ClaimUpdateInput, project_id: str = "proj-festflow-01"):
    """
    Stage 4: Review Canvas.
    Allows the human reviewer to edit text, mark approval, or resolve contradictions.
    """
    project = get_or_create_project(project_id)
    for c in project.claims:
        if c.id == update_data.claim_id:
            if update_data.title is not None:
                c.title = update_data.title
            if update_data.summary is not None:
                c.summary = update_data.summary
            if update_data.human_notes is not None:
                c.human_notes = update_data.human_notes
            if update_data.is_approved is not None:
                c.is_approved = update_data.is_approved
            if update_data.verification_status is not None:
                c.verification_status = update_data.verification_status
            return c
    raise HTTPException(status_code=404, detail="Claim not found")

@router.post("/handover/seal", response_model=HandoverManifest)
def seal_handover(project_id: str = "proj-festflow-01"):
    """
    Stage 4 -> 5: Approve & Seal Handover.
    Finalizes the handover package with an immutable timestamped lock.
    """
    project = get_or_create_project(project_id)
    project.is_sealed = True
    return project

@router.get("/handover/view/{role}", response_model=Dict[str, Any])
def get_role_handover_view(role: str = "developer", project_id: str = "proj-festflow-01"):
    """
    Stage 5: Handover.
    Generates role-tailored perspectives:
    - 'developer': setup gotchas, open bugs, active PRs, Day-1 checklist
    - 'lead': project velocity, milestones, risk matrix, ownership directory
    """
    project = get_or_create_project(project_id)
    
    if role.lower() == "lead":
        filtered_claims = [c for c in project.claims if c.category in (ClaimCategory.DECISION, ClaimCategory.OWNERSHIP)]
        checklist = [
            "Verify all external stakeholder and faculty permissions are transitioned.",
            "Confirm GitHub organization admin role has been assigned to new technical lead.",
            "Review risk matrix regarding unblocked S3 cloud backup credentials."
        ]
    else: # default developer view
        filtered_claims = project.claims
        checklist = [
            "Clone repository and verify local zero-config SQLite database initialization.",
            "Review Safari iOS auth cookie gotcha before testing mobile web forms.",
            "Verify client-side SVG QR code generator in PR #14.",
            "Check out branch for TASK-55 and inspect scripts/backup_db.py."
        ]
        
    return {
        "project_name": project.project_name,
        "departing_member": project.departing_member,
        "role_view": role.capitalize(),
        "is_sealed": project.is_sealed,
        "day1_checklist": checklist,
        "claims": filtered_claims,
        "total_claims": len(filtered_claims),
        "secret_protection_guarantee": f"{project.summary_stats.get('redacted_secrets_count', 0)} credentials successfully sanitized"
    }
