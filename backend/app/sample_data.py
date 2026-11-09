from app.models import ProjectSource, SourceType, HandoverClaim, ClaimCategory, VerificationStatus, Citation
from app.sanitizer import sanitize_content

RAW_SAMPLE_SOURCES = [
    {
        "id": "SRC-GIT-01",
        "source_type": SourceType.GIT_COMMIT,
        "title": "commit #8a1f4c: switch to sqlite for local dev",
        "author": "Aryan Sharma <aryan@adgips.ac.in>",
        "timestamp": "2026-10-15T14:32:00Z",
        "content": (
            "commit 8a1f4cd582b9e671234e6f\n"
            "Author: Aryan Sharma <aryan@adgips.ac.in>\n"
            "Date:   Tue Oct 15 14:32:00 2026 +0530\n\n"
            "    refactor(db): replace PostgreSQL docker with SQLite for local development\n\n"
            "    Decision rationale: Many 1st-year juniors at ADGIPS had Docker Desktop crashes "
            "    on Windows 11 machines. SQLite requires zero installation, eliminates connection "
            "    pool timeouts, and runs seamlessly out-of-the-box. Production will use Supabase Postgres."
        ),
        "metadata": {"sha": "8a1f4cd", "branch": "main"}
    },
    {
        "id": "SRC-GIT-02",
        "source_type": SourceType.GIT_COMMIT,
        "title": "commit #9b2c3d: rollback safari auth cookie",
        "author": "Aryan Sharma <aryan@adgips.ac.in>",
        "timestamp": "2026-10-26T18:15:00Z",
        "content": (
            "commit 9b2c3de14567a9881234bc\n"
            "Author: Aryan Sharma <aryan@adgips.ac.in>\n"
            "Date:   Sat Oct 26 18:15:00 2026 +0530\n\n"
            "    revert(auth): rollback httpOnly refresh cookie for Safari iOS\n\n"
            "    CRITICAL GOTCHA: Safari ITP (Intelligent Tracking Prevention) drops cross-site "
            "    cookies on iOS when fest subdomains are accessed. Sticking with in-memory Bearer token "
            "    and localStorage fallback until Safari bug #4092 is resolved. "
            "    Temp test key was api_key = 'AIzaSyD-TEST-LEAKED-KEY-9876543210' - DO NOT COMMIT."
        ),
        "metadata": {"sha": "9b2c3de", "branch": "main"}
    },
    {
        "id": "SRC-PR-14",
        "source_type": SourceType.PULL_REQUEST,
        "title": "PR #14: Refactor ticket QR generation",
        "author": "Aryan Sharma <aryan@adgips.ac.in>",
        "timestamp": "2026-10-20T11:45:00Z",
        "content": (
            "Pull Request #14: Optimized QR Code Generation for Registrations\n"
            "State: Merged | Reviewer: Prof. Gupta (Faculty Coordinator)\n\n"
            "Architecture Decision: Switched from generating server-side PDF passes to rendering client-side "
            "SVG QR codes. This reduced server RAM usage from 1.2GB down to 180MB during ticket release crunch. "
            "The QR generator uses the qrcode.react library."
        ),
        "metadata": {"pr_number": 14, "status": "merged"}
    },
    {
        "id": "SRC-TASK-42",
        "source_type": SourceType.TASK_CARD,
        "title": "TASK-42: Safari Auth Fix",
        "author": "Aryan Sharma",
        "timestamp": "2026-10-24T09:00:00Z",
        "content": (
            "Task: TASK-42 - Fix Safari Session Logout\n"
            "Board: FestFlow Sprint 3 | Column: DONE\n"
            "Description: Implemented standard secure cookie header for mobile Safari users. "
            "Tested and closed."
        ),
        "metadata": {"task_id": "TASK-42", "status": "done"}
    },
    {
        "id": "SRC-CHAT-01",
        "source_type": SourceType.STANDUP_CHAT,
        "title": "Discord Standup Log (Oct 28)",
        "author": "Aryan Sharma",
        "timestamp": "2026-10-28T10:30:00Z",
        "content": (
            "Discord #general-dev-updates (Oct 28, 10:30 AM):\n"
            "Aryan: 'Hey team, for whoever takes over deployment: the automated GitHub Action deploy "
            "webhook is located in the college GitHub organization under secret FEST_DEPLOY_SECRET. "
            "Password to the staging server is password = 'FestAdmin2026!SecureKey'. "
            "Ping the club president to add you as an admin before I leave next week!'"
        ),
        "metadata": {"channel": "general-dev-updates"}
    },
    {
        "id": "SRC-TASK-55",
        "source_type": SourceType.TASK_CARD,
        "title": "TASK-55: Automated S3 DB Backup",
        "author": "Aryan Sharma",
        "timestamp": "2026-11-02T16:00:00Z",
        "content": (
            "Task: TASK-55 - Setup Automated Nightly Database Backup\n"
            "Board: FestFlow Sprint 4 | Column: IN PROGRESS (BLOCKED)\n"
            "Blocker Note: Cron job script is written at scripts/backup_db.py, but fails because "
            "AWS S3 credentials from college IT department are still pending approval."
        ),
        "metadata": {"task_id": "TASK-55", "status": "blocked"}
    }
]

def get_sanitized_sample_sources():
    sources = []
    for item in RAW_SAMPLE_SOURCES:
        clean_content, red_count, red_types = sanitize_content(item["content"])
        source = ProjectSource(
            id=item["id"],
            source_type=item["source_type"],
            title=item["title"],
            content=clean_content,
            author=item["author"],
            timestamp=item["timestamp"],
            metadata=item["metadata"],
            is_sanitized=True,
            redacted_items_count=red_count
        )
        sources.append(source)
    return sources

def get_sample_handover_claims():
    return [
        HandoverClaim(
            id="CLM-01",
            category=ClaimCategory.DECISION,
            title="Local Database Standardized on SQLite (Zero-Config)",
            summary="Replaced PostgreSQL Docker container with SQLite for local development to prevent Docker crashes on junior developer machines.",
            rationale="Junior 1st/2nd years at ADGIPS faced Docker Desktop installation and memory issues on Windows 11. SQLite requires zero configuration while remaining ACID compliant.",
            verification_status=VerificationStatus.VERIFIED,
            confidence_score=0.98,
            citations=[
                Citation(
                    source_id="SRC-GIT-01",
                    source_title="commit #8a1f4c: switch to sqlite for local dev",
                    source_type=SourceType.GIT_COMMIT,
                    author="Aryan Sharma",
                    timestamp="2026-10-15T14:32:00Z",
                    exact_quote="refactor(db): replace PostgreSQL docker with SQLite for local development... Decision rationale: Many 1st-year juniors had Docker crashes."
                )
            ],
            is_approved=True,
            human_notes="Keep this SQLite setup for local dev; connect to Supabase Postgres only when building production releases."
        ),
        HandoverClaim(
            id="CLM-02",
            category=ClaimCategory.BLOCKER,
            title="Safari iOS Authentication Cookie Dropping Bug",
            summary="Authentication cookies are dropped on Safari iOS due to Apple's Intelligent Tracking Prevention (ITP).",
            rationale="Safari prevents cross-subdomain cookies. Reverted to in-memory Bearer tokens with localStorage fallback.",
            verification_status=VerificationStatus.CONTRADICTION,
            confidence_score=0.95,
            conflict_notes="CONFLICT DETECTED: Task Card TASK-42 marked 'Done' on Oct 24, but Git commit #9b2c3de on Oct 26 rolled it back due to live Safari failures.",
            citations=[
                Citation(
                    source_id="SRC-GIT-02",
                    source_title="commit #9b2c3d: rollback safari auth cookie",
                    source_type=SourceType.GIT_COMMIT,
                    author="Aryan Sharma",
                    timestamp="2026-10-26T18:15:00Z",
                    exact_quote="revert(auth): rollback httpOnly refresh cookie for Safari iOS... CRITICAL GOTCHA: Safari ITP drops cross-site cookies."
                ),
                Citation(
                    source_id="SRC-TASK-42",
                    source_title="TASK-42: Safari Auth Fix",
                    source_type=SourceType.TASK_CARD,
                    author="Aryan Sharma",
                    timestamp="2026-10-24T09:00:00Z",
                    exact_quote="Task: TASK-42 - Fix Safari Session Logout... Status: DONE."
                )
            ],
            is_approved=True,
            human_notes="High priority for incoming dev: do not mark this fixed until tested on real iPhone Safari."
        ),
        HandoverClaim(
            id="CLM-03",
            category=ClaimCategory.DECISION,
            title="Ticket Generation Renders Client-Side SVG Over PDFs",
            summary="Passes and QR codes are generated client-side as SVG base64 strings instead of server-side PDF files.",
            rationale="Generating server-side PDFs spiked server RAM to 1.2GB during peak registration spikes. Client-side SVG reduced memory to 180MB.",
            verification_status=VerificationStatus.VERIFIED,
            confidence_score=0.96,
            citations=[
                Citation(
                    source_id="SRC-PR-14",
                    source_title="PR #14: Refactor ticket QR generation",
                    source_type=SourceType.PULL_REQUEST,
                    author="Aryan Sharma",
                    timestamp="2026-10-20T11:45:00Z",
                    exact_quote="Switched from generating server-side PDF passes to rendering client-side SVG QR codes. Reduced server RAM from 1.2GB to 180MB."
                )
            ],
            is_approved=True
        ),
        HandoverClaim(
            id="CLM-04",
            category=ClaimCategory.OWNERSHIP,
            title="Deployment Webhooks & GitHub Org Permissions",
            summary="Automated deployment is controlled via GitHub Organization secret FEST_DEPLOY_SECRET.",
            rationale="Only the College Tech Club President holds admin rights to re-assign or regenerate this key.",
            verification_status=VerificationStatus.VERIFIED,
            confidence_score=0.94,
            citations=[
                Citation(
                    source_id="SRC-CHAT-01",
                    source_title="Discord Standup Log (Oct 28)",
                    source_type=SourceType.STANDUP_CHAT,
                    author="Aryan Sharma",
                    timestamp="2026-10-28T10:30:00Z",
                    exact_quote="automated GitHub Action deploy webhook is located under secret FEST_DEPLOY_SECRET... Ping the club president to add you as an admin."
                )
            ],
            is_approved=True,
            human_notes="Anshika: Talk to Prof. Gupta or the club president during Week 1 to receive GitHub Org Maintainer role."
        ),
        HandoverClaim(
            id="CLM-05",
            category=ClaimCategory.NEXT_ACTION,
            title="Day-1 Setup & Unblock S3 Nightly Backups (TASK-55)",
            summary="1. Verify local SQLite environment. 2. Follow up with college IT department for AWS S3 bucket credentials for TASK-55.",
            rationale="The backup script at scripts/backup_db.py is ready but blocked on cloud credentials.",
            verification_status=VerificationStatus.UNCERTAIN,
            confidence_score=0.89,
            conflict_notes="Uncertain: College IT coordinator response pending since Nov 2.",
            citations=[
                Citation(
                    source_id="SRC-TASK-55",
                    source_title="TASK-55: Automated S3 DB Backup",
                    source_type=SourceType.TASK_CARD,
                    author="Aryan Sharma",
                    timestamp="2026-11-02T16:00:00Z",
                    exact_quote="Cron job script is written at scripts/backup_db.py, but fails because AWS S3 credentials from college IT department are still pending."
                )
            ],
            is_approved=True,
            human_notes="Priority checklist item for new maintainer."
        )
    ]
