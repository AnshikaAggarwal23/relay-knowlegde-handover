import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

# Executive Color Palette
COLOR_NAVY = colors.HexColor("#0B132B")          # Midnight Deep Slate
COLOR_ROYAL = colors.HexColor("#1D4ED8")         # Executive Royal Blue
COLOR_TEAL = colors.HexColor("#0D9488")          # Vibrant Teal
COLOR_TEXT_MAIN = colors.HexColor("#1E293B")     # Charcoal Main Body
COLOR_TEXT_MUTED = colors.HexColor("#64748B")    # Slate Grey Subtext
COLOR_BG_LIGHT = colors.HexColor("#F8FAFC")      # Crisp Off-White / Light Slate
COLOR_BG_CARD = colors.HexColor("#F1F5F9")       # Soft Card Slate
COLOR_BORDER = colors.HexColor("#CBD5E1")        # Border Grey
COLOR_ACCENT_BG = colors.HexColor("#EFF6FF")     # Soft Blue Accent Tint

class Round2NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        page_num = self._pageNumber
        
        # Running Header (Pages 2 onwards)
        if page_num > 1:
            self.setFont("Helvetica-Bold", 8.5)
            self.setFillColor(COLOR_ROYAL)
            self.drawString(40, 755, "RELAY")
            self.setFont("Helvetica-Bold", 8.5)
            self.setFillColor(COLOR_NAVY)
            self.drawString(75, 755, "•  TEAM SOLOSTACK")
            self.setFont("Helvetica", 8)
            self.setFillColor(COLOR_TEXT_MUTED)
            self.drawString(170, 755, "|  Round 2 Technical Build Documentation  •  CodersInPune Hackathon 2026")
            
            self.setStrokeColor(COLOR_BORDER)
            self.setLineWidth(0.6)
            self.line(40, 746, 572, 746)
            
        # Running Footer (All pages)
        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.6)
        self.line(40, 36, 572, 36)
        
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(COLOR_NAVY)
        self.drawString(40, 24, "Team SoloStack")
        self.setFont("Helvetica", 8)
        self.setFillColor(COLOR_TEXT_MUTED)
        self.drawString(108, 24, "|  Anshika Aggarwal (B.Tech 1st Year, ADGIPS New Delhi)  |  Round 2 Submission")
        
        page_str = f"Page {page_num} of {total_pages}"
        self.drawRightString(572, 24, page_str)
        
        self.restoreState()


def build_round2_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=42,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()

    style_cover_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=COLOR_NAVY,
        alignment=TA_LEFT
    )

    style_cover_subtitle = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=COLOR_ROYAL,
        alignment=TA_LEFT
    )

    style_sec_h1 = ParagraphStyle(
        'SecH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=COLOR_NAVY,
        spaceBefore=11,
        spaceAfter=5,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=COLOR_TEXT_MAIN,
        alignment=TA_LEFT,
        spaceAfter=4.5
    )

    style_callout_title = ParagraphStyle(
        'CalloutTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=COLOR_NAVY
    )

    style_callout_body = ParagraphStyle(
        'CalloutBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=COLOR_TEXT_MAIN
    )

    style_table_header = ParagraphStyle(
        'TableH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=11,
        textColor=colors.white,
        alignment=TA_LEFT
    )

    style_table_cell = ParagraphStyle(
        'TableC',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.2,
        textColor=COLOR_TEXT_MAIN,
        alignment=TA_LEFT
    )

    style_table_cell_bold = ParagraphStyle(
        'TableCBold',
        parent=style_table_cell,
        fontName='Helvetica-Bold',
        textColor=COLOR_NAVY
    )

    story = []

    # =========================================================================
    # HEADER BANNER & EXECUTIVE BUILD SUMMARY
    # =========================================================================
    header_data = [
        [
            Paragraph("CODERSINPUNE HACKATHON 2026 • ROUND 2 SUBMISSION DOCUMENTATION", style_cover_subtitle),
            Paragraph("TRACK: KNOWLEDGE HANDOVER", ParagraphStyle('R', parent=style_cover_subtitle, alignment=TA_RIGHT))
        ],
        [
            Paragraph("RELAY: Central Workflow & Working MVP (Round 2 — The Build)", style_cover_title),
            ""
        ],
        [
            Paragraph("<b>Project:</b> Relay (Evidence-Linked Knowledge Handover Platform)<br/>"
                      "<b>Team Name:</b> <b>SoloStack</b> (1-Member Solo Track)<br/>"
                      "<b>Author:</b> Anshika Aggarwal | B.Tech 1st Year, Dr. Akhilesh Das Gupta Institute of Professional Studies (ADGIPS), New Delhi", style_callout_body),
            Paragraph("<b>Stage:</b> Round 2 — The Build Submission<br/>"
                      "<b>Target Criteria:</b> Core Workflow Runs End-to-End (30 Pts)<br/>"
                      "<b>Evaluation Mode:</b> Autonomous Judge Quick-Start", ParagraphStyle('R2', parent=style_callout_body, alignment=TA_RIGHT))
        ]
    ]

    header_table = Table(header_data, colWidths=[355, 177])
    header_table.setStyle(TableStyle([
        ('SPAN', (0, 1), (1, 1)),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(header_table)
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_ROYAL, spaceBefore=4, spaceAfter=8))

    # Executive Build Card
    exec_card = [
        [
            Paragraph("<b>EXECUTIVE BUILD STATEMENT — ROUND 2 DELIVERABLES</b>", style_callout_title),
        ],
        [
            Paragraph(
                "For Round 2 (The Build), <b>Team SoloStack</b> has engineered a fully functioning, end-to-end knowledge handover platform. "
                "The central workflow runs seamlessly from raw source ingestion to role-tailored onboarding without requiring any external walkthrough. "
                "Judges can interact directly using the built-in <b>'1-Click Benchmark Quick-Start'</b> or by connecting custom Git logs and notes. "
                "The core application features automated pre-ingestion secret sanitization, bi-directional evidence citations, an algorithmic "
                "contradiction radar (detecting discrepancies between task boards and commit activity), and an interactive dual-pane review canvas.",
                style_callout_body
            )
        ]
    ]
    t_exec = Table(exec_card, colWidths=[532])
    t_exec.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.8, COLOR_BORDER),
        ('LINELEFT', (0, 0), (0, -1), 3.5, COLOR_ROYAL),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 9),
        ('RIGHTPADDING', (0, 0), (-1, -1), 9),
    ]))
    story.append(t_exec)
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 1: WORKING PROJECT & REPOSITORY ACCESS
    # =========================================================================
    story.append(Paragraph("1. Working Project Link & Source-Code Repository", style_sec_h1))
    story.append(Paragraph(
        "To guarantee effortless evaluation by the judging panel without setup friction, Relay is available through two deployment modes:",
        style_body
    ))

    repo_data = [
        [Paragraph("Deliverable", style_table_header), Paragraph("URL / Access Path", style_table_header), Paragraph("Evaluation Notes for Judges", style_table_header)],
        [
            Paragraph("<b>Source-Code Repository</b>", style_table_cell_bold),
            Paragraph('<a href="https://github.com/AnshikaAggarwal23/relay-knowlegde-handover" color="#1D4ED8"><u>https://github.com/AnshikaAggarwal23/relay-knowlegde-handover</u></a><br/><i>(Public GitHub Repository)</i>', style_table_cell),
            Paragraph("Complete source code including FastAPI backend, React client, automated tests, and preloaded benchmark dataset.", style_table_cell)
        ],
        [
            Paragraph("<b>Working Project Link (Live Web App)</b>", style_table_cell_bold),
            Paragraph('<a href="https://anshikaaggarwal23.github.io/relay-knowlegde-handover/" color="#1D4ED8"><u>https://anshikaaggarwal23.github.io/relay-knowlegde-handover/</u></a><br/><i>(Live Cloud Deployment via GitHub Pages)</i>', style_table_cell),
            Paragraph("Zero-install live web client. Features built-in autonomous mode and 1-Click Judge Quick-Start.", style_table_cell)
        ],
        [
            Paragraph("<b>Local 1-Command Runner</b>", style_table_cell_bold),
            Paragraph("<code>python backend/app/main.py</code><br/><i>(Runs at http://localhost:8000)</i>", style_table_cell),
            Paragraph("Unified server: FastAPI serves the interactive web client and OpenAPI Swagger documentation at <code>/docs</code>.", style_table_cell)
        ]
    ]
    t_repo = Table(repo_data, colWidths=[130, 202, 200])
    t_repo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_NAVY),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COLOR_BG_LIGHT]),
    ]))
    story.append(t_repo)
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 2: CENTRAL WORKFLOW WALKTHROUGH FOR JUDGES
    # =========================================================================
    story.append(Paragraph("2. The Central Workflow: Autonomous Judge Journey (Judging Criterion: 30 Pts)", style_sec_h1))
    story.append(Paragraph(
        "A judge can launch and evaluate the entire transition pipeline from start to finish without requiring any manual assistance:",
        style_body
    ))

    flow_data = [
        [Paragraph("Step", style_table_header), Paragraph("Workflow Stage", style_table_header), Paragraph("Judge Action & What Happens On Screen", style_table_header)],
        [
            Paragraph("<b>Step 1</b>", style_table_cell_bold),
            Paragraph("<b>Connect & Ingest</b>", style_table_cell_bold),
            Paragraph("Judge opens the app and clicks <b>'⚡ Judge Quick-Start'</b>. The system loads 6 authorized project sources (Git commits, PRs, task cards, Discord notes). The <b>Secret Redaction Radar</b> immediately flashes green, showing 2 sensitive credentials (an API key and a server password) scrubbed from the view.", style_table_cell)
        ],
        [
            Paragraph("<b>Step 2</b>", style_table_cell_bold),
            Paragraph("<b>Reconstruct State</b>", style_table_cell_bold),
            Paragraph("Judge clicks 'Proceed to Stage 2: Reconstruct'. The backend processes the telemetry, categorizing findings into Architectural Decisions, Fragile Gotchas, Ownership, and Next Actions.", style_table_cell)
        ],
        [
            Paragraph("<b>Step 3</b>", style_table_cell_bold),
            Paragraph("<b>Verify & Conflict Radar</b>", style_table_cell_bold),
            Paragraph("Judge reviews claims with confidence ratings. Relay automatically triggers an amber <b>Contradiction Alert</b>: Task card TASK-42 claimed 'Done' on Oct 24, but Git commit #9b2c3de rolled it back on Oct 26 due to Safari iOS issues. Relay highlights this conflict rather than inventing false certainty.", style_table_cell)
        ],
        [
            Paragraph("<b>Step 4</b>", style_table_cell_bold),
            Paragraph("<b>Dual-Pane Review Canvas</b>", style_table_cell_bold),
            Paragraph("The core innovation: Left pane displays raw source evidence; right pane displays editable handover cards. Clicking any card highlights the exact sentence in the source on the left. The judge can edit text, add senior tips, and click <b>'Approve & Seal Handover'</b>.", style_table_cell)
        ],
        [
            Paragraph("<b>Step 5</b>", style_table_cell_bold),
            Paragraph("<b>Role-Tailored Handover</b>", style_table_cell_bold),
            Paragraph("The sealed handover generates an actionable onboarding view. Judge toggles between <b>Developer View</b> (interactive Day-1 checklist, gotchas, SQLite setup) and <b>Lead View</b> (milestone risks, stakeholder contacts). Features 1-click Export to Markdown / PDF.", style_table_cell)
        ]
    ]
    t_flow = Table(flow_data, colWidths=[45, 120, 367])
    t_flow.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_NAVY),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COLOR_BG_LIGHT]),
    ]))
    story.append(t_flow)
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 3: LIST OF COMPLETED FEATURES
    # =========================================================================
    story.append(Paragraph("3. List of Completed Features (Working in Round 2)", style_sec_h1))
    
    feats = [
        ("1-Click Judge Quick-Start Benchmark Engine", "Loads a realistic 4-month transition dataset from 'FestFlow' (Campus Fest Web Portal) so evaluators can test immediately without hunting for files."),
        ("Pre-Ingestion Secret & PII Sanitizer", "Regex-based protection pipeline that intercepts and redacts API keys, Bearer tokens, GitHub PATs, and passwords before processing."),
        ("Structured Entity Extraction Engine", "FastAPI backend endpoint that structures unstructured Git commit messages, PRs, and chats into decisions, blockers, ownership, and next steps."),
        ("Cross-Source Temporal Contradiction Radar", "Rule pass comparing timestamps across task boards and Git commit logs to flag discrepancies (e.g. task marked closed vs commit reverted)."),
        ("Dual-Pane Interactive Review Canvas", "Side-by-side desktop UI: Raw Evidence Inspector on the left, editable Handover Cards on the right with bi-directional highlight synchronization."),
        ("Role-Tailored Output Generator", "Interactive view switcher providing tailored perspectives: Developer View (interactive checklist, gotchas) vs. Project Lead View (risks, contacts)."),
        ("Immutable Handover Manifest & Export", "Generates timestamped handover seal with one-click Markdown summary export and printer-friendly PDF dossier generation.")
    ]
    for title, desc in feats:
        story.append(Paragraph(f"&bull; <b>{title}:</b> {desc}", style_body))
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 4: TECHNOLOGY & IMPLEMENTATION DETAILS
    # =========================================================================
    story.append(Paragraph("4. Technology and Implementation Details (Depth & Reliability: 25 Pts)", style_sec_h1))
    story.append(Paragraph(
        "Relay’s implementation emphasizes technical reliability, clean separation of concerns, and zero external dependency failures:",
        style_body
    ))

    tech_details = [
        [Paragraph("Component", style_table_header), Paragraph("Technology & Implementation Architecture", style_table_header)],
        [
            Paragraph("<b>Backend API Architecture</b>", style_table_cell_bold),
            Paragraph("Built with <b>FastAPI (Python 3.11+)</b> and <b>Pydantic v2</b>. Asynchronous REST endpoints handle source parsing, secret sanitization, claim updates, and handover sealing. Automatic interactive Swagger documentation is provided at <code>/docs</code>.", style_table_cell)
        ],
        [
            Paragraph("<b>Frontend Client Architecture</b>", style_table_cell_bold),
            Paragraph("Built with <b>React 18</b> and <b>Tailwind CSS</b>. Implements a responsive 5-stage stepper, dual-pane review canvas with bi-directional citation inspection, and interactive task checklist state management. Features an autonomous browser fallback so judges can evaluate the UI even without the local Python server running.", style_table_cell)
        ],
        [
            Paragraph("<b>AI / Extraction Strategy</b>", style_table_cell_bold),
            Paragraph("Configured for <b>Google Gemini 1.5 Flash</b> with strict JSON schema enforcement. Crucially, Relay incorporates a deterministic semantic analyzer fallback that guarantees instantaneous, bug-free execution during live hackathon judging, completely immune to rate limits or API key outages.", style_table_cell)
        ],
        [
            Paragraph("<b>Security & Sanitizer Engine</b>", style_table_cell_bold),
            Paragraph("Custom regex compilation rules targeting GitHub PATs (<code>ghp_*</code>), AWS access keys, Bearer tokens, and database URI connection strings, replacing them with formatted safe tokens prior to display.", style_table_cell)
        ]
    ]
    t_tech = Table(tech_details, colWidths=[140, 392])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_NAVY),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COLOR_BG_LIGHT]),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 5: EXPLANATION OF CHANGES FROM ORIGINAL PLAN
    # =========================================================================
    story.append(Paragraph("5. Explanation of Changes Made to the Original Plan (Progress: 20 Pts)", style_sec_h1))
    story.append(Paragraph(
        "During Round 2 implementation, Team SoloStack made three justified architectural improvements to enhance reliability and judge usability:",
        style_body
    ))

    changes = [
        "<b>Addition of 1-Click Judge Quick-Start Benchmark:</b> In the original Round 1 plan, users were expected to upload custom files manually. In Round 2, we added a pre-configured benchmark project ('FestFlow Campus Portal') with realistic Git commits and chat notes, allowing judges to test the complete workflow in a single click.",
        "<b>Dual-Mode Execution (Autonomous + Backend Connected):</b> Rather than requiring judges to configure Python virtual environments and node dependencies, the React frontend operates in a dual mode: it seamlessly queries the live FastAPI backend when available, but automatically runs its built-in state engine if evaluated as a standalone web client.",
        "<b>Elevated Temporal Contradiction Flagging:</b> Rather than treating contradictions as a passive status tag, we built a dedicated high-visibility <b>Contradiction Radar Banner</b> in Stage 3 to immediately alert the evaluator when task boards disagree with Git commit history."
    ]
    for ch in changes:
        story.append(Paragraph(f"&bull; {ch}", style_body))
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 6: THREE MAJOR IMPROVEMENTS FOR ROUND 3
    # =========================================================================
    story.append(Paragraph("6. Three Substantial Improvements Committed for Round 3 (15 Pts)", style_sec_h1))
    story.append(Paragraph(
        "In strict compliance with hackathon guidelines requiring meaningful product improvements rather than cosmetic tweaks, Team SoloStack commits to delivering the following three substantial features in Round 3:",
        style_body
    ))

    r3_commitments = [
        [Paragraph("Commitment", style_table_header), Paragraph("Feature Name", style_table_header), Paragraph("Substantial Technical Scope & Impact in Round 3", style_table_header)],
        [
            Paragraph("<b>Improvement 1</b>", style_table_cell_bold),
            Paragraph("<b>Cross-Source Temporal Timeline Slider</b>", style_table_cell_bold),
            Paragraph("An interactive chronological scrub bar that displays when decisions were made across all sources on a synchronized timeline. Allows the reviewer to visually trace how a feature moved from an initial Discord chat to a Jira ticket, into a Git commit, and finally resolved or reverted.", style_table_cell)
        ],
        [
            Paragraph("<b>Improvement 2</b>", style_table_cell_bold),
            Paragraph("<b>Cryptographic Handover Seal & Tamper-Proof Audit Manifest</b>", style_table_cell_bold),
            Paragraph("Generates an immutable SHA-256 hash manifest upon handover approval. Embeds verification metadata into an encrypted, downloadable handover dossier so future maintainers can cryptographically verify that handover notes were approved by the departing lead.", style_table_cell)
        ],
        [
            Paragraph("<b>Improvement 3</b>", style_table_cell_bold),
            Paragraph("<b>Interactive Handover Q&A Agent with Strict Citation Guardrails</b>", style_table_cell_bold),
            Paragraph("An embedded conversational assistant for incoming developers that answers questions about the project (e.g., 'How do I run the ticket generator?'). Strictly constrained via RAG to cite only verified claims from the sealed handover manifest, refusing to hallucinate.", style_table_cell)
        ]
    ]
    t_r3 = Table(r3_commitments, colWidths=[90, 140, 302])
    t_r3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_NAVY),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COLOR_BG_LIGHT]),
    ]))
    story.append(t_r3)
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 7: PARTICIPANT DETAILS & INTEGRITY
    # =========================================================================
    story.append(Paragraph("7. Complete Participant Details & Submission Integrity", style_sec_h1))
    
    participant_data = [
        [Paragraph("Field", style_table_header), Paragraph("Official Record", style_table_header)],
        [Paragraph("<b>Team Name</b>", style_table_cell_bold), Paragraph("<b>SoloStack</b> (1-Member Solo Participant Track)", style_table_cell)],
        [Paragraph("<b>Participant Name</b>", style_table_cell_bold), Paragraph("Anshika Aggarwal", style_table_cell)],
        [Paragraph("<b>Academic Standing</b>", style_table_cell_bold), Paragraph("B.Tech 1st Year (Passionate Aspiring Full-Stack Developer)", style_table_cell)],
        [Paragraph("<b>Institution</b>", style_table_cell_bold), Paragraph("Dr. Akhilesh Das Gupta Institute of Professional Studies (ADGIPS), GGSIPU, New Delhi", style_table_cell)],
        [Paragraph("<b>Designated Role</b>", style_table_cell_bold), Paragraph("Solo Full-Stack Developer, Product Architect & System Integrator", style_table_cell)],
        [Paragraph("<b>Build Integrity</b>", style_table_cell_bold), Paragraph("All code developed during the official Round 2 build window in full compliance with HackWithPune fair participation rules.", style_table_cell)]
    ]
    t_part = Table(participant_data, colWidths=[140, 392])
    t_part.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_NAVY),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COLOR_BG_LIGHT]),
    ]))
    story.append(t_part)

    # Build document
    doc.build(story, canvasmaker=Round2NumberedCanvas)
    print(f"Round 2 Documentation PDF successfully generated at: {filename}")

if __name__ == "__main__":
    out_path = r"C:\Users\ANSHIKA AGGARWAL\.gemini\antigravity\scratch\relay-knowledge-handover\SoloStack_Round2_Project_Documentation.pdf"
    build_round2_pdf(out_path)
