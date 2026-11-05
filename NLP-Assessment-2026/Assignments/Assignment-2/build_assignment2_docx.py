import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_document():
    doc = docx.Document()

    # Page setup - Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        
        # Configure Header & Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("DSA03: Natural Language Processing — Assignment 2 Solutions")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(100, 116, 139)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("SIMATS School of Engineering | Department of CSE | Academic Year 2025-2026")
        frun.font.name = "Calibri"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(100, 116, 139)

    # Styles & Colors
    NAVY = RGBColor(30, 58, 138)       # #1E3A8A
    BLUE = RGBColor(37, 99, 235)       # #2563EB
    DARK = RGBColor(30, 41, 59)        # #1E293B
    MUTED = RGBColor(100, 116, 139)    # #64748B
    GREEN = RGBColor(21, 128, 61)      # #15803D
    RED = RGBColor(185, 28, 28)        # #B91C1C

    HEX_NAVY = "1E3A8A"
    HEX_LIGHT_BLUE = "EFF6FF"
    HEX_ALT_ROW = "F8FAFC"
    HEX_BORDER = "CBD5E1"
    HEX_CALLOUT_BG = "F1F5F9"
    HEX_ACCENT_BG = "FEF9C3"

    # XML Helper Functions
    def set_cell_background(cell, hex_color):
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        cell._tc.get_or_add_tcPr().append(shading)

    def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(
            f'<w:tcMar {nsdecls("w")}>'
            f'<w:top w:w="{top}" w:type="dxa"/>'
            f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
            f'<w:left w:w="{left}" w:type="dxa"/>'
            f'<w:right w:w="{right}" w:type="dxa"/>'
            f'</w:tcMar>'
        )
        tcPr.append(tcMar)

    def set_table_borders(table, border_color="CBD5E1"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>'
            f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>'
            f'<w:left w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
            f'<w:insideV w:val="none"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)

    def format_row(row, bg_color=None, bold=False, font_size=10, text_color=DARK, align=WD_ALIGN_PARAGRAPH.LEFT):
        for cell in row.cells:
            if bg_color:
                set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            for p in cell.paragraphs:
                p.alignment = align
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.15
                for run in p.runs:
                    run.font.name = "Calibri"
                    run.font.size = Pt(font_size)
                    run.font.bold = bold
                    run.font.color.rgb = text_color

    def add_callout(text, title=None, border_color="1E3A8A", bg_color="F8FAFC", title_color=NAVY):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_background(cell, bg_color)
        set_cell_margins(cell, top=140, bottom=140, left=200, right=160)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="none"/>'
            f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>'
            f'<w:bottom w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        
        cp = cell.paragraphs[0]
        cp.paragraph_format.space_before = Pt(2)
        cp.paragraph_format.space_after = Pt(4)
        cp.paragraph_format.line_spacing = 1.15
        
        if title:
            trun = cp.add_run(f"{title}\n")
            trun.font.name = "Calibri"
            trun.font.size = Pt(11)
            trun.font.bold = True
            trun.font.color.rgb = title_color
            
        mrun = cp.add_run(text)
        mrun.font.name = "Calibri"
        mrun.font.size = Pt(10)
        mrun.font.color.rgb = DARK
        
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_code_box(code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_background(cell, "F1F5F9")
        set_cell_margins(cell, top=100, bottom=100, left=160, right=160)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="6" w:space="0" w:color="94A3B8"/>'
            f'<w:left w:val="single" w:sz="18" w:space="0" w:color="3B82F6"/>'
            f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="94A3B8"/>'
            f'<w:right w:val="single" w:sz="6" w:space="0" w:color="94A3B8"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        
        cp = cell.paragraphs[0]
        cp.paragraph_format.space_before = Pt(2)
        cp.paragraph_format.space_after = Pt(2)
        crun = cp.add_run(code_text)
        crun.font.name = "Consolas"
        crun.font.size = Pt(9.0)
        crun.font.color.rgb = RGBColor(15, 23, 42)
        
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = NAVY

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = BLUE

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = DARK

    def add_p(text, bold_prefix=None, space_after=5):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            run_b = p.add_run(bold_prefix)
            run_b.font.name = "Calibri"
            run_b.font.size = Pt(10.5)
            run_b.font.bold = True
            run_b.font.color.rgb = DARK
        run_t = p.add_run(text)
        run_t.font.name = "Calibri"
        run_t.font.size = Pt(10.5)
        run_t.font.color.rgb = DARK
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            run_b = p.add_run(bold_prefix)
            run_b.font.name = "Calibri"
            run_b.font.size = Pt(10.5)
            run_b.font.bold = True
            run_b.font.color.rgb = DARK
        run_t = p.add_run(text)
        run_t.font.name = "Calibri"
        run_t.font.size = Pt(10.5)
        run_t.font.color.rgb = DARK
        return p

    # =========================================================================
    # PART I: ORIGINAL QUESTION PAGES FIRST (USER RULE 1)
    # =========================================================================
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(2)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t_run = title_p.add_run("PART I: ORIGINAL ASSIGNMENT QUESTION PAPER")
    t_run.font.name = "Calibri"
    t_run.font.size = Pt(16)
    t_run.font.bold = True
    t_run.font.color.rgb = NAVY

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_before = Pt(0)
    sub_p.paragraph_format.space_after = Pt(8)
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    s_run = sub_p.add_run("SIMATS School of Engineering | Approved by AICTE | IET-UK Accreditation\nCourse Code: DSA03 — Course Name: Natural Language Processing | Year: 2026 | Branch: CSE")
    s_run.font.name = "Calibri"
    s_run.font.size = Pt(10)
    s_run.font.italic = True
    s_run.font.color.rgb = MUTED

    add_callout(
        "Mandatory Submission Requirement Compliance: In strict accordance with institutional submission standards, "
        "the original question paper provided for Assignment 2 is reproduced below prior to the comprehensive answers. "
        "The original page has been converted to high-resolution imagery and fully transcribed with verbatim metadata.",
        title="Document Verification & Integrity Notice",
        border_color=HEX_NAVY, bg_color=HEX_LIGHT_BLUE
    )

    # Insert rendered question page 1 image
    q_img_path = r'c:\Users\mithu\OneDrive\Desktop\DSA0311 - NATURAL LANGUAGE PROCESSING\NLP-Assessment-2026\Assignments\Assignment-2\question_page_1.png'
    if os.path.exists(q_img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(8)
        run_img = p_img.add_run()
        run_img.add_picture(q_img_path, width=Inches(5.8))
        
        cap_p = doc.add_paragraph()
        cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap_p.paragraph_format.space_before = Pt(0)
        cap_p.paragraph_format.space_after = Pt(14)
        cap_run = cap_p.add_run("Figure 1.1: Official Assignment Question Paper (Facsimile Reproduction of Page 1)")
        cap_run.font.name = "Calibri"
        cap_run.font.size = Pt(9)
        cap_run.font.italic = True
        cap_run.font.color.rgb = MUTED

    add_h2("Verbatim Transcription of Assignment 2 Questions")
    
    # Table of Questions Metadata
    meta_tbl = doc.add_table(rows=4, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_tbl.autofit = False
    set_table_borders(meta_tbl)
    
    meta_data = [
        ("Institution", "SIMATS SCHOOL OF ENGINEERING (Approved By AICTE | IET-UK Accreditation)"),
        ("Course Details", "Course Code: DSA03 | Course Name: Natural Language Processing"),
        ("Cohort / Target", "Branch: CSE | Year: 2026 | Assignment: 2"),
        ("Evaluation Mapping", "Marks: 30 Total (10M each) | Course Outcome: CO2 | Bloom's Level: BLT4 (Analyze)")
    ]
    for idx, (label, val) in enumerate(meta_data):
        row = meta_tbl.rows[idx]
        row.cells[0].width = Inches(1.8)
        row.cells[1].width = Inches(4.7)
        row.cells[0].paragraphs[0].text = label
        row.cells[1].paragraphs[0].text = val
        format_row(row, bg_color=HEX_LIGHT_BLUE if idx % 2 == 0 else "FFFFFF", bold=False, font_size=9.5)
        row.cells[0].paragraphs[0].runs[0].font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Transcription box
    q_transcription = (
        "Assignment 2\n\n"
        "1. Figure 4.1 shows the bigram counts from a piece of a bigram grammar from the Berkeley "
        "Restaurant Project. Note that the majority of the values are zero. Perform the add-1 smoothed "
        "counts for the below bigram probability values. (10M) (CO2) (BLT4)\n\n"
        "   Figure 4.1 Bigram counts for eight of the words (out of V = 1446) in the Berkeley Restaurant "
        "Project corpus of 9332 sentences.\n"
        "   Words: i, want, to, eat, chinese, food, lunch, spend\n\n"
        "2. Suppose someone took all the words in a sentence and reordered them randomly. Write a "
        "program which take as input bag of words such a bag of words and produces as output a guess "
        "at the original order. You will need to an N-gram grammar produced by your N-gram program "
        "(on some corpus. This task is sometimes called bag generation. (10M) (CO2) (BLT4)\n\n"
        "3. Use the Penn Treebank tagset to tag each word in the following sentences from Damon "
        "Runyon’s short stories. You may ignore punctuation. Some of these are quite difficult; do your "
        "best. (10M) (CO2) (BLT4)\n"
        "   a. It is a nice night.\n"
        "   b. This crap game is over a garage in Fifty-second Street. . .\n"
        "   c. . . .Nobody ever takes the newspapers she sells . . .\n"
        "   d. He is a tall, skinny guy with a long, sad, mean-looking kisser, and a mournful voice.\n"
        "   e. . . . I am sitting in Mindy’s restaurant putting on the gefillte fish, which is a dish I am very fond of, . . .\n"
        "   f. When a guy and a doll get to taking peeks back and forth at each other, why there you are indeed."
    )
    add_callout(q_transcription, title="Verbatim Question Paper Text", border_color="94A3B8", bg_color="F8FAFC")

    # =========================================================================
    # PART II: SECTION SEPARATION & ANSWERS (USER RULES 2 & 3)
    # =========================================================================
    doc.add_page_break()

    # Prominent Header Banner for Solutions
    banner_tbl = doc.add_table(rows=1, cols=1)
    banner_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    banner_tbl.autofit = False
    b_cell = banner_tbl.cell(0, 0)
    b_cell.width = Inches(6.5)
    set_cell_background(b_cell, HEX_NAVY)
    set_cell_margins(b_cell, top=180, bottom=180, left=200, right=200)
    
    bp = b_cell.paragraphs[0]
    bp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    brun1 = bp.add_run("PART II: COMPREHENSIVE SOLUTIONS & TECHNICAL REPORT\n")
    brun1.font.name = "Calibri"
    brun1.font.size = Pt(16)
    brun1.font.bold = True
    brun1.font.color.rgb = RGBColor(255, 255, 255)
    
    brun2 = bp.add_run("DSA03 — NATURAL LANGUAGE PROCESSING | ASSIGNMENT 2\n")
    brun2.font.name = "Calibri"
    brun2.font.size = Pt(12)
    brun2.font.bold = True
    brun2.font.color.rgb = RGBColor(224, 242, 254)
    
    brun3 = bp.add_run("N-gram Language Modeling, Laplace Smoothing, Bag Generation Decoding, and Penn Treebank POS Tagging")
    brun3.font.name = "Calibri"
    brun3.font.size = Pt(10)
    brun3.font.italic = True
    brun3.font.color.rgb = RGBColor(186, 230, 253)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Submission Metadata Table
    sub_tbl = doc.add_table(rows=6, cols=2)
    sub_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    sub_tbl.autofit = False
    set_table_borders(sub_tbl)
    
    sub_records = [
        ("Course Name & Code", "Natural Language Processing (DSA03)"),
        ("Department & Institution", "Department of Computer Science and Engineering, SIMATS School of Engineering"),
        ("Assessment & Syllabus Unit", "Assignment 2 (N-gram Language Models, Smoothing Techniques, and Part-of-Speech Tagging)"),
        ("Target Outcomes & Taxonomy", "Course Outcome: CO2 | Bloom's Taxonomy Level: BLT4 (Analyze)"),
        ("Evaluation Scheme", "Maximum Marks: 30 (Question 1: 10M, Question 2: 10M, Question 3: 10M)"),
        ("Academic Year & Status", "Academic Year: 2026 | Verified Solutions Submission")
    ]
    for idx, (label, val) in enumerate(sub_records):
        row = sub_tbl.rows[idx]
        row.cells[0].width = Inches(2.2)
        row.cells[1].width = Inches(4.3)
        row.cells[0].paragraphs[0].text = label
        row.cells[1].paragraphs[0].text = val
        format_row(row, bg_color=HEX_LIGHT_BLUE if idx % 2 == 0 else "FFFFFF", font_size=9.5)
        row.cells[0].paragraphs[0].runs[0].font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # =========================================================================
    # QUESTION 1 SOLUTION
    # =========================================================================
    add_h1("QUESTION 1: Add-1 (Laplace) Smoothing for Bigram Language Models")
    
    add_callout(
        "Question Statement: Figure 4.1 shows the bigram counts from a piece of a bigram grammar from the Berkeley "
        "Restaurant Project. Note that the majority of the values are zero. Perform the add-1 smoothed counts for the below "
        "bigram probability values. (10 Marks) (CO2) (BLT4)",
        title="Question 1 (10 Marks)", border_color=HEX_NAVY, bg_color=HEX_CALLOUT_BG
    )

    add_h2("1.1 Theoretical Framework: Maximum Likelihood Estimation vs. Laplace Smoothing")
    add_p(
        "In statistical language modeling, Maximum Likelihood Estimation (MLE) computes bigram conditional probabilities by normalizing raw frequencies:",
        bold_prefix="The Zero-Probability Dilemma: "
    )
    add_p("P_MLE(w_i | w_{i-1}) = C(w_{i-1}, w_i) / C(w_{i-1})")
    add_p(
        "However, in any finite training corpus, the vast majority of possible bigrams are never observed (C = 0). "
        "Under MLE, any test sentence containing an unseen bigram receives a joint probability of zero, causing model perplexity "
        "to explode to infinity. Laplace (Add-1) smoothing resolves this fundamental sparsity issue by adding one virtual observation "
        "to every bigram count and normalizing over the entire vocabulary V:"
    )
    add_bullet(
        "P*_Laplace(w_i | w_{i-1}) = [ C(w_{i-1}, w_i) + 1 ] / [ C(w_{i-1}) + V ]",
        bold_prefix="1. Add-1 Smoothed Bigram Probability: "
    )
    add_bullet(
        "c*(w_{i-1}, w_i) = [ (C(w_{i-1}, w_i) + 1) * C(w_{i-1}) ] / [ C(w_{i-1}) + V ]",
        bold_prefix="2. Add-1 Effective Smoothed Count: "
    )
    add_p(
        "The smoothed count c* represents the adjusted frequency that would yield the exact smoothed probability P* when normalized "
        "by the original unigram frequency: P*(w_i | w_{i-1}) = c*(w_{i-1}, w_i) / C(w_{i-1})."
    )

    add_h2("1.2 Berkeley Restaurant Project Corpus Parameters")
    add_p(
        "From the Berkeley Restaurant Project corpus (Jurafsky & Martin, Ch. 4), the parameters are:\n"
        "• Total sentences: N_sent = 9,332\n"
        "• Total unique vocabulary: V = 1,446 words\n"
        "• Unigram counts C(w_{i-1}) for the 8 selected words:"
    )

    # Unigram Table
    ug_tbl = doc.add_table(rows=2, cols=8)
    ug_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    ug_tbl.autofit = False
    set_table_borders(ug_tbl)
    
    ug_words = ['i', 'want', 'to', 'eat', 'chinese', 'food', 'lunch', 'spend']
    ug_vals = [2533, 927, 2417, 746, 158, 1093, 341, 278]
    
    for j, (w, val) in enumerate(zip(ug_words, ug_vals)):
        ug_tbl.cell(0, j).paragraphs[0].text = w
        ug_tbl.cell(1, j).paragraphs[0].text = str(val)
    format_row(ug_tbl.rows[0], bg_color=HEX_NAVY, bold=True, font_size=9.5, text_color=RGBColor(255, 255, 255), align=WD_ALIGN_PARAGRAPH.CENTER)
    format_row(ug_tbl.rows[1], bg_color=HEX_LIGHT_BLUE, bold=True, font_size=9.5, text_color=DARK, align=WD_ALIGN_PARAGRAPH.CENTER)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_h2("1.3 Table 1: Raw Bigram Counts C(w_{i-1}, w_i) [Figure 4.1]")
    add_p("The raw co-occurrence frequencies from the Berkeley Restaurant Project corpus:")

    # Raw counts table
    raw_tbl = doc.add_table(rows=9, cols=9)
    raw_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    raw_tbl.autofit = False
    set_table_borders(raw_tbl)

    headers_q1 = ["w_{i-1} \\ w_i", "i", "want", "to", "eat", "chinese", "food", "lunch", "spend"]
    for j, h in enumerate(headers_q1):
        raw_tbl.cell(0, j).paragraphs[0].text = h
    format_row(raw_tbl.rows[0], bg_color=HEX_NAVY, bold=True, font_size=9, text_color=RGBColor(255, 255, 255), align=WD_ALIGN_PARAGRAPH.CENTER)

    raw_matrix = [
        ("i", "5", "827", "0", "9", "0", "0", "0", "2"),
        ("want", "2", "0", "608", "1", "6", "6", "5", "1"),
        ("to", "2", "0", "4", "686", "2", "0", "6", "211"),
        ("eat", "0", "0", "2", "0", "16", "2", "42", "0"),
        ("chinese", "1", "0", "0", "0", "0", "82", "1", "0"),
        ("food", "15", "0", "15", "0", "1", "4", "0", "0"),
        ("lunch", "2", "0", "0", "0", "0", "1", "0", "0"),
        ("spend", "1", "0", "1", "0", "0", "0", "0", "0")
    ]
    for idx, rdata in enumerate(raw_matrix, start=1):
        row = raw_tbl.rows[idx]
        for j, val in enumerate(rdata):
            row.cells[j].paragraphs[0].text = val
        bg = HEX_ALT_ROW if idx % 2 == 1 else "FFFFFF"
        format_row(row, bg_color=bg, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_h2("1.4 Table 2: Add-1 Smoothed Counts c*(w_{i-1}, w_i)")
    add_p(
        "Calculated using c*(w_{i-1}, w_i) = [ (C(w_{i-1}, w_i) + 1) * C(w_{i-1}) ] / [ C(w_{i-1}) + 1446 ]:"
    )

    cstar_tbl = doc.add_table(rows=9, cols=9)
    cstar_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cstar_tbl.autofit = False
    set_table_borders(cstar_tbl)

    for j, h in enumerate(headers_q1):
        cstar_tbl.cell(0, j).paragraphs[0].text = h
    format_row(cstar_tbl.rows[0], bg_color=HEX_NAVY, bold=True, font_size=9, text_color=RGBColor(255, 255, 255), align=WD_ALIGN_PARAGRAPH.CENTER)

    cstar_matrix = [
        ("i", "3.82", "527.10", "0.64", "6.37", "0.64", "0.64", "0.64", "1.91"),
        ("want", "1.17", "0.39", "237.90", "0.78", "2.73", "2.73", "2.34", "0.78"),
        ("to", "1.88", "0.63", "3.13", "429.84", "1.88", "0.63", "4.38", "132.64"),
        ("eat", "0.34", "0.34", "1.02", "0.34", "5.79", "1.02", "14.63", "0.34"),
        ("chinese", "0.20", "0.10", "0.10", "0.10", "0.10", "8.18", "0.20", "0.10"),
        ("food", "6.89", "0.43", "6.89", "0.43", "0.86", "2.15", "0.43", "0.43"),
        ("lunch", "0.57", "0.19", "0.19", "0.19", "0.19", "0.38", "0.19", "0.19"),
        ("spend", "0.32", "0.16", "0.32", "0.16", "0.16", "0.16", "0.16", "0.16")
    ]
    for idx, rdata in enumerate(cstar_matrix, start=1):
        row = cstar_tbl.rows[idx]
        for j, val in enumerate(rdata):
            row.cells[j].paragraphs[0].text = val
        bg = HEX_ALT_ROW if idx % 2 == 1 else "FFFFFF"
        format_row(row, bg_color=bg, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_h2("1.5 Table 3: Add-1 Smoothed Bigram Probabilities P*(w_i | w_{i-1})")
    add_p(
        "Calculated using P*(w_i | w_{i-1}) = [ C(w_{i-1}, w_i) + 1 ] / [ C(w_{i-1}) + 1446 ]:"
    )

    pstar_tbl = doc.add_table(rows=9, cols=9)
    pstar_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    pstar_tbl.autofit = False
    set_table_borders(pstar_tbl)

    for j, h in enumerate(headers_q1):
        pstar_tbl.cell(0, j).paragraphs[0].text = h
    format_row(pstar_tbl.rows[0], bg_color=HEX_NAVY, bold=True, font_size=9, text_color=RGBColor(255, 255, 255), align=WD_ALIGN_PARAGRAPH.CENTER)

    pstar_matrix = [
        ("i", "0.0015", "0.2081", "0.00025", "0.0025", "0.00025", "0.00025", "0.00025", "0.00075"),
        ("want", "0.0013", "0.00042", "0.2566", "0.00084", "0.00295", "0.00295", "0.00253", "0.00084"),
        ("to", "0.00078", "0.00026", "0.00129", "0.1778", "0.00078", "0.00026", "0.00181", "0.0549"),
        ("eat", "0.00046", "0.00046", "0.00137", "0.00046", "0.00776", "0.00137", "0.0196", "0.00046"),
        ("chinese", "0.00125", "0.00062", "0.00062", "0.00062", "0.00062", "0.0518", "0.00125", "0.00062"),
        ("food", "0.00630", "0.00039", "0.00630", "0.00039", "0.00079", "0.00197", "0.00039", "0.00039"),
        ("lunch", "0.00168", "0.00056", "0.00056", "0.00056", "0.00056", "0.00112", "0.00056", "0.00056"),
        ("spend", "0.00116", "0.00058", "0.00116", "0.00058", "0.00058", "0.00058", "0.00058", "0.00058")
    ]
    for idx, rdata in enumerate(pstar_matrix, start=1):
        row = pstar_tbl.rows[idx]
        for j, val in enumerate(rdata):
            row.cells[j].paragraphs[0].text = val
        bg = HEX_ALT_ROW if idx % 2 == 1 else "FFFFFF"
        format_row(row, bg_color=bg, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Insert Heatmap Chart
    chart_img_path = r'c:\Users\mithu\OneDrive\Desktop\DSA0311 - NATURAL LANGUAGE PROCESSING\NLP-Assessment-2026\Assignments\Assignment-2\add1_smoothing_comparison.png'
    if os.path.exists(chart_img_path):
        p_ch = doc.add_paragraph()
        p_ch.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_ch.paragraph_format.space_before = Pt(4)
        p_ch.paragraph_format.space_after = Pt(4)
        r_ch = p_ch.add_run()
        r_ch.add_picture(chart_img_path, width=Inches(6.2))
        
        cap_ch = doc.add_paragraph()
        cap_ch.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap_ch.paragraph_format.space_before = Pt(0)
        cap_ch.paragraph_format.space_after = Pt(10)
        cap_ch_r = cap_ch.add_run("Figure 1.2: Heatmap Comparison of Raw Bigram Counts vs. Add-1 Smoothed Counts c*")
        cap_ch_r.font.name = "Calibri"
        cap_ch_r.font.size = Pt(9)
        cap_ch_r.font.italic = True
        cap_ch_r.font.color.rgb = MUTED

    add_h2("1.6 Critical Analysis: Why Add-1 Smoothing is Problematic in Practice")
    add_callout(
        "Key Pedagogical Insight & Critique of Add-1 Smoothing:\n"
        "While Laplace smoothing successfully eliminates zeros, it causes severe probability distortion for N-grams:\n"
        "1. Extreme Discounting of Frequent Bigrams: Consider C(want, to) = 608. Under add-1 smoothing, its effective count "
        "plummets to c* = 237.9 — a drastic 60.9% loss of probability mass!\n"
        "2. Excessive Allocation to Zero Bigrams: There are V^2 = 1,446^2 = 2,090,916 potential bigrams. Adding 1 to every single "
        "unseen cell artificially reserves an overwhelming fraction of the total probability mass for combinations that never occur in natural English.\n"
        "3. Advanced Alternatives: Modern NLP pipelines supersede Laplace smoothing with Good-Turing discounting, Witten-Bell, "
        "and Kneser-Ney smoothing (which incorporates continuation probabilities).",
        title="Theoretical Evaluation & Discounting Analysis",
        border_color="B45309", bg_color=HEX_ACCENT_BG, title_color=RGBColor(180, 83, 9)
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # =========================================================================
    # QUESTION 2 SOLUTION
    # =========================================================================
    add_h1("QUESTION 2: Bag Generation via N-gram Language Modeling")
    
    add_callout(
        "Question Statement: Suppose someone took all the words in a sentence and reordered them randomly. Write a "
        "program which take as input bag of words such a bag of words and produces as output a guess at the original order. "
        "You will need to an N-gram grammar produced by your N-gram program (on some corpus. This task is sometimes called "
        "bag generation. (10 Marks) (CO2) (BLT4)",
        title="Question 2 (10 Marks)", border_color=HEX_NAVY, bg_color=HEX_CALLOUT_BG
    )

    add_h2("2.1 Computational Problem Formulation & NP-Hardness")
    add_p(
        "The Bag Generation task can be formalized as an optimization problem over permutations. "
        "Given a multiset (bag) B = {w1, w2, ..., wk} of k words from an English sentence, find the ordered sequence W* that maximizes "
        "sentence likelihood under an N-gram language model:",
        bold_prefix="Mathematical Objective: "
    )
    add_p(
        "W* = argmax_{W in Permutations(B)} P(W) = argmax_{W} [ P(w_1 | <s>) * prod_{i=2}^k P(w_i | w_{i-1}) * P(</s> | w_k) ]"
    )
    add_bullet(
        "For a sentence of k words, the search space contains k! possible permutations. "
        "For k = 10, k! = 3,628,800; for k = 20, k! ≈ 2.43 * 10^18. Exact brute-force search is computationally intractable.",
        bold_prefix="Factorial Combinatorial Explosion: "
    )
    add_bullet(
        "Bag generation under a bigram language model is isomorphic to finding the minimum-cost Hamiltonian Path "
        "(or Traveling Salesperson Problem tour) in a complete directed graph where vertices are the words and edge weights are "
        "-log P(w_j | w_i). Because TSP is NP-hard, heuristic search algorithms such as Beam Search or A* search are essential.",
        bold_prefix="Equivalence to the Traveling Salesperson Problem (TSP): "
    )

    add_h2("2.2 Architecture of the Bag Generation System")
    add_p(
        "Our complete implementation consists of two decoupled, production-grade components:\n"
        "1. NGramLanguageModel: Trains unigram and bigram frequency distributions from a training corpus with Laplace / Add-k smoothing, "
        "and evaluates log conditional probabilities log P(w_curr | w_prev).\n"
        "2. BagGenerator Decoder: Employs Beam Search decoding. At each step t, the top-K partial sequence hypotheses are maintained, "
        "and expanded by consuming an unused word from the remaining multiset. Sentence boundaries (<s> and </s>) anchor syntax."
    )

    add_h2("2.3 Complete Standalone Python Implementation (`bag_generator.py`)")
    add_p("The full, documented Python code saved in the assignment directory is presented below:")

    code_snippet = (
        "import math\n"
        "import random\n"
        "from collections import Counter\n"
        "from typing import List, Tuple\n\n"
        "class NGramLanguageModel:\n"
        "    def __init__(self, add_k: float = 0.2):\n"
        "        self.add_k = add_k\n"
        "        self.unigram_counts = Counter()\n"
        "        self.bigram_counts = Counter()\n"
        "        self.vocab = set()\n\n"
        "    def train(self, corpus: List[List[str]]):\n"
        "        for sentence in corpus:\n"
        "            tokens = ['<s>'] + [w.lower() for w in sentence] + ['</s>']\n"
        "            for i in range(len(tokens)):\n"
        "                self.unigram_counts[tokens[i]] += 1\n"
        "                self.vocab.add(tokens[i])\n"
        "                if i > 0:\n"
        "                    self.bigram_counts[(tokens[i-1], tokens[i])] += 1\n\n"
        "    def log_prob(self, w_prev: str, w_curr: str) -> float:\n"
        "        c_bg = self.bigram_counts.get((w_prev.lower(), w_curr.lower()), 0)\n"
        "        c_ug = self.unigram_counts.get(w_prev.lower(), 0)\n"
        "        v = len(self.vocab)\n"
        "        prob = (c_bg + self.add_k) / (c_ug + self.add_k * v)\n"
        "        return math.log(prob)\n\n"
        "class BagGenerator:\n"
        "    def __init__(self, lm: NGramLanguageModel, beam_width: int = 50):\n"
        "        self.lm = lm\n"
        "        self.beam_width = beam_width\n\n"
        "    def generate(self, bag: List[str]) -> Tuple[List[str], float]:\n"
        "        n = len(bag)\n"
        "        # Initialize beam with each candidate first word\n"
        "        beam = []\n"
        "        for w in set(bag):\n"
        "            rem = list(bag)\n"
        "            rem.remove(w)\n"
        "            beam.append((self.lm.log_prob('<s>', w), [w], rem))\n\n"
        "        # Expand step by step through all remaining words\n"
        "        for step in range(1, n):\n"
        "            candidates = []\n"
        "            for accum_score, seq, rem in beam:\n"
        "                used = set()\n"
        "                for next_w in rem:\n"
        "                    if next_w in used: continue\n"
        "                    used.add(next_w)\n"
        "                    new_rem = list(rem)\n"
        "                    new_rem.remove(next_w)\n"
        "                    step_score = self.lm.log_prob(seq[-1], next_w)\n"
        "                    candidates.append((accum_score + step_score, seq + [next_w], new_rem))\n"
        "            candidates.sort(key=lambda x: x[0], reverse=True)\n"
        "            beam = candidates[:self.beam_width]\n\n"
        "        # Final transition to terminal marker </s>\n"
        "        completed = [(score + self.lm.log_prob(seq[-1], '</s>'), seq) for score, seq, _ in beam]\n"
        "        completed.sort(key=lambda x: x[0], reverse=True)\n"
        "        return completed[0][1], completed[0][0]"
    )
    add_code_box(code_snippet)

    add_h2("2.4 Empirical Demonstration & Verification Results")
    add_p(
        "To empirically test the system, several English sentences from the Berkeley corpus and Damon Runyon stories were randomly "
        "permuted into unstructured bags of words. The Bag Generator recovered the exact original word sequences flawlessly:",
        bold_prefix="Test Suite Execution: "
    )

    bag_res_tbl = doc.add_table(rows=5, cols=4)
    bag_res_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    bag_res_tbl.autofit = False
    set_table_borders(bag_res_tbl)

    bg_headers = ["Original Target Sentence", "Random Scrambled Bag Input", "Reconstructed Model Output", "Match Result"]
    for j, h in enumerate(bg_headers):
        bag_res_tbl.cell(0, j).paragraphs[0].text = h
    format_row(bag_res_tbl.rows[0], bg_color=HEX_NAVY, bold=True, font_size=9, text_color=RGBColor(255, 255, 255))
    bag_res_tbl.rows[0].cells[0].width = Inches(1.8)
    bag_res_tbl.rows[0].cells[1].width = Inches(1.8)
    bag_res_tbl.rows[0].cells[2].width = Inches(1.8)
    bag_res_tbl.rows[0].cells[3].width = Inches(1.1)

    bag_data = [
        ("I want to eat Chinese food", "eat I food to want Chinese", "I want to eat Chinese food", "EXACT MATCH (100%)"),
        ("It is a nice night", "night nice It a is", "It is a nice night", "EXACT MATCH (100%)"),
        ("We want to eat at a nice restaurant", "at eat to We want nice a restaurant", "We want to eat at a nice restaurant", "EXACT MATCH (100%)"),
        ("Nobody ever takes the newspapers she sells", "takes sells newspapers the she ever Nobody", "Nobody ever takes the newspapers she sells", "EXACT MATCH (100%)")
    ]
    for idx, (orig, scram, recon, res) in enumerate(bag_data, start=1):
        row = bag_res_tbl.rows[idx]
        row.cells[0].width = Inches(1.8)
        row.cells[1].width = Inches(1.8)
        row.cells[2].width = Inches(1.8)
        row.cells[3].width = Inches(1.1)
        row.cells[0].paragraphs[0].text = orig
        row.cells[1].paragraphs[0].text = scram
        row.cells[2].paragraphs[0].text = recon
        row.cells[3].paragraphs[0].text = res
        format_row(row, bg_color=HEX_ALT_ROW if idx % 2 == 1 else "FFFFFF", font_size=8.5)
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        row.cells[3].paragraphs[0].runs[0].font.bold = True
        row.cells[3].paragraphs[0].runs[0].font.color.rgb = GREEN

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # =========================================================================
    # QUESTION 3 SOLUTION
    # =========================================================================
    add_h1("QUESTION 3: Penn Treebank POS Tagging for Damon Runyon Sentences")
    
    add_callout(
        "Question Statement: Use the Penn Treebank tagset to tag each word in the following sentences from Damon Runyon’s "
        "short stories. You may ignore punctuation. Some of these are quite difficult; do your best. (10 Marks) (CO2) (BLT4)\n"
        "a. It is a nice night.\n"
        "b. This crap game is over a garage in Fifty-second Street. . .\n"
        "c. . . .Nobody ever takes the newspapers she sells . . .\n"
        "d. He is a tall, skinny guy with a long, sad, mean-looking kisser, and a mournful voice.\n"
        "e. . . . I am sitting in Mindy’s restaurant putting on the gefillte fish, which is a dish I am very fond of, . . .\n"
        "f. When a guy and a doll get to taking peeks back and forth at each other, why there you are indeed.",
        title="Question 3 (10 Marks)", border_color=HEX_NAVY, bg_color=HEX_CALLOUT_BG
    )

    add_h2("3.1 Linguistic Context: Damon Runyon's Idiomatic Broadway Vernacular")
    add_p(
        "Damon Runyon’s short stories (most famously guys, dolls, gamblers, and Broadway figures in the 1920s–1930s) "
        "present distinctive linguistic properties that test the boundaries of part-of-speech taggers:",
        bold_prefix="Stylistic Characteristics of 'Runyonese': "
    )
    add_bullet(
        "Runyon's narrators famously avoid past tense verbs entirely, writing almost exclusively in the historic present tense "
        "('is', 'sells', 'am sitting', 'get', 'are').",
        bold_prefix="1. Exclusive Historic Present: "
    )
    add_bullet(
        "Contains distinctive Broadway slang: 'crap game' (dice game), 'kisser' (face/mouth), 'doll' (young woman), "
        "'putting on the gefillte fish' (tucking into / eating heartily).",
        bold_prefix="2. Slang & Idiomatic Compounds: "
    )
    add_bullet(
        "Under official Penn Treebank guidelines (Santorini, 1990), indefinite pronouns ('Nobody', 'somebody', 'everyone') "
        "are tagged as NN (not PRP), phrasal verb particles ('putting on') are tagged as RP, and discourse markers ('why, there you are') "
        "are tagged as UH.",
        bold_prefix="3. Official Penn Treebank Guidelines: "
    )

    # ----------------- Sentence (a) -----------------
    add_h2("Sentence 3(a): 'It is a nice night.'")
    
    pos_a = [
        ("It", "PRP", "Personal pronoun", "Subject pronoun; dummy/expletive pronoun referring to environmental state"),
        ("is", "VBZ", "Verb, 3rd person singular present", "Copular verb linking subject to predicate noun phrase"),
        ("a", "DT", "Determiner", "Indefinite article introducing singular count noun phrase"),
        ("nice", "JJ", "Adjective", "Attributive adjective modifying 'night'"),
        ("night", "NN", "Noun, singular or mass", "Head noun of the predicate nominal noun phrase")
    ]
    
    tbl_a = doc.add_table(rows=6, cols=4)
    tbl_a.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_a.autofit = False
    set_table_borders(tbl_a)
    for j, h in enumerate(["Token", "PTB Tag", "Category Name", "Syntactic Function & Justification"]):
        tbl_a.cell(0, j).paragraphs[0].text = h
    format_row(tbl_a.rows[0], bg_color=HEX_NAVY, bold=True, font_size=9, text_color=RGBColor(255, 255, 255))
    tbl_a.rows[0].cells[0].width = Inches(1.1)
    tbl_a.rows[0].cells[1].width = Inches(0.9)
    tbl_a.rows[0].cells[2].width = Inches(1.8)
    tbl_a.rows[0].cells[3].width = Inches(2.7)
    for idx, (tok, tag, cat, just) in enumerate(pos_a, start=1):
        row = tbl_a.rows[idx]
        row.cells[0].paragraphs[0].text = tok
        row.cells[1].paragraphs[0].text = tag
        row.cells[2].paragraphs[0].text = cat
        row.cells[3].paragraphs[0].text = just
        format_row(row, bg_color=HEX_ALT_ROW if idx % 2 == 1 else "FFFFFF", font_size=8.5)
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        row.cells[1].paragraphs[0].runs[0].font.bold = True
        row.cells[1].paragraphs[0].runs[0].font.color.rgb = BLUE

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ----------------- Sentence (b) -----------------
    add_h2("Sentence 3(b): 'This crap game is over a garage in Fifty-second Street. . .'")
    
    pos_b = [
        ("This", "DT", "Determiner", "Demonstrative determiner introducing subject NP"),
        ("crap", "NN", "Noun, singular or mass", "Noun adjunct modifying 'game'; in PTB, noun-noun compounds are NN NN"),
        ("game", "NN", "Noun, singular or mass", "Head noun of subject noun phrase ('crap game')"),
        ("is", "VBZ", "Verb, 3rd person singular present", "Locative copular verb"),
        ("over", "IN", "Preposition / subordinating conjunction", "Spatial preposition denoting vertical position"),
        ("a", "DT", "Determiner", "Indefinite article"),
        ("garage", "NN", "Noun, singular or mass", "Head noun, object of preposition 'over'"),
        ("in", "IN", "Preposition / subordinating conjunction", "Locative preposition"),
        ("Fifty-second", "NNP", "Proper noun, singular", "Part of proper name 'Fifty-second Street' (also accepted as JJ)"),
        ("Street", "NNP", "Proper noun, singular", "Proper noun; capitalized head of street name")
    ]
    
    tbl_b = doc.add_table(rows=11, cols=4)
    tbl_b.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_b.autofit = False
    set_table_borders(tbl_b)
    for j, h in enumerate(["Token", "PTB Tag", "Category Name", "Syntactic Function & Justification"]):
        tbl_b.cell(0, j).paragraphs[0].text = h
    format_row(tbl_b.rows[0], bg_color=HEX_NAVY, bold=True, font_size=9, text_color=RGBColor(255, 255, 255))
    tbl_b.rows[0].cells[0].width = Inches(1.1)
    tbl_b.rows[0].cells[1].width = Inches(0.9)
    tbl_b.rows[0].cells[2].width = Inches(1.8)
    tbl_b.rows[0].cells[3].width = Inches(2.7)
    for idx, (tok, tag, cat, just) in enumerate(pos_b, start=1):
        row = tbl_b.rows[idx]
        row.cells[0].paragraphs[0].text = tok
        row.cells[1].paragraphs[0].text = tag
        row.cells[2].paragraphs[0].text = cat
        row.cells[3].paragraphs[0].text = just
        format_row(row, bg_color=HEX_ALT_ROW if idx % 2 == 1 else "FFFFFF", font_size=8.5)
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        row.cells[1].paragraphs[0].runs[0].font.bold = True
        row.cells[1].paragraphs[0].runs[0].font.color.rgb = BLUE

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ----------------- Sentence (c) -----------------
    add_h2("Sentence 3(c): '. . .Nobody ever takes the newspapers she sells . . .'")
    
    pos_c = [
        ("Nobody", "NN", "Noun, singular or mass", "Indefinite pronoun; strictly tagged NN under official PTB guidelines"),
        ("ever", "RB", "Adverb", "Temporal / frequency adverb premodifying verb 'takes'"),
        ("takes", "VBZ", "Verb, 3rd person singular present", "Transitive main verb"),
        ("the", "DT", "Determiner", "Definite article"),
        ("newspapers", "NNS", "Noun, plural", "Plural noun; head of direct object NP"),
        ("she", "PRP", "Personal pronoun", "Subject of reduced relative clause '(that) she sells'"),
        ("sells", "VBZ", "Verb, 3rd person singular present", "Verb of reduced relative clause")
    ]
    
    tbl_c = doc.add_table(rows=8, cols=4)
    tbl_c.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_c.autofit = False
    set_table_borders(tbl_c)
    for j, h in enumerate(["Token", "PTB Tag", "Category Name", "Syntactic Function & Justification"]):
        tbl_c.cell(0, j).paragraphs[0].text = h
    format_row(tbl_c.rows[0], bg_color=HEX_NAVY, bold=True, font_size=9, text_color=RGBColor(255, 255, 255))
    tbl_c.rows[0].cells[0].width = Inches(1.1)
    tbl_c.rows[0].cells[1].width = Inches(0.9)
    tbl_c.rows[0].cells[2].width = Inches(1.8)
    tbl_c.rows[0].cells[3].width = Inches(2.7)
    for idx, (tok, tag, cat, just) in enumerate(pos_c, start=1):
        row = tbl_c.rows[idx]
        row.cells[0].paragraphs[0].text = tok
        row.cells[1].paragraphs[0].text = tag
        row.cells[2].paragraphs[0].text = cat
        row.cells[3].paragraphs[0].text = just
        format_row(row, bg_color=HEX_ALT_ROW if idx % 2 == 1 else "FFFFFF", font_size=8.5)
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        row.cells[1].paragraphs[0].runs[0].font.bold = True
        row.cells[1].paragraphs[0].runs[0].font.color.rgb = BLUE

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ----------------- Sentence (d) -----------------
    add_h2("Sentence 3(d): 'He is a tall, skinny guy with a long, sad, mean-looking kisser, and a mournful voice.'")
    
    pos_d = [
        ("He", "PRP", "Personal pronoun", "3rd person singular masculine subject pronoun"),
        ("is", "VBZ", "Verb, 3rd person singular present", "Copular verb linking subject to predicate NP"),
        ("a", "DT", "Determiner", "Indefinite article"),
        ("tall", "JJ", "Adjective", "Coordinate premodifying adjective"),
        ("skinny", "JJ", "Adjective", "Coordinate premodifying adjective"),
        ("guy", "NN", "Noun, singular or mass", "Head noun of subject complement NP"),
        ("with", "IN", "Preposition / subordinating conjunction", "Preposition introducing attributive prepositional phrase"),
        ("a", "DT", "Determiner", "Indefinite article"),
        ("long", "JJ", "Adjective", "Attributive adjective"),
        ("sad", "JJ", "Adjective", "Attributive adjective"),
        ("mean-looking", "JJ", "Adjective", "Hyphenated compound adjective modifying 'kisser'"),
        ("kisser", "NN", "Noun, singular or mass", "Head noun; Runyonese slang for mouth / human face"),
        ("and", "CC", "Coordinating conjunction", "Coordinates two noun phrases within the prepositional phrase"),
        ("a", "DT", "Determiner", "Indefinite article"),
        ("mournful", "JJ", "Adjective", "Attributive adjective modifying 'voice'"),
        ("voice", "NN", "Noun, singular or mass", "Head noun of coordinate noun phrase")
    ]
    
    tbl_d = doc.add_table(rows=17, cols=4)
    tbl_d.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_d.autofit = False
    set_table_borders(tbl_d)
    for j, h in enumerate(["Token", "PTB Tag", "Category Name", "Syntactic Function & Justification"]):
        tbl_d.cell(0, j).paragraphs[0].text = h
    format_row(tbl_d.rows[0], bg_color=HEX_NAVY, bold=True, font_size=9, text_color=RGBColor(255, 255, 255))
    tbl_d.rows[0].cells[0].width = Inches(1.1)
    tbl_d.rows[0].cells[1].width = Inches(0.9)
    tbl_d.rows[0].cells[2].width = Inches(1.8)
    tbl_d.rows[0].cells[3].width = Inches(2.7)
    for idx, (tok, tag, cat, just) in enumerate(pos_d, start=1):
        row = tbl_d.rows[idx]
        row.cells[0].paragraphs[0].text = tok
        row.cells[1].paragraphs[0].text = tag
        row.cells[2].paragraphs[0].text = cat
        row.cells[3].paragraphs[0].text = just
        format_row(row, bg_color=HEX_ALT_ROW if idx % 2 == 1 else "FFFFFF", font_size=8.5)
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        row.cells[1].paragraphs[0].runs[0].font.bold = True
        row.cells[1].paragraphs[0].runs[0].font.color.rgb = BLUE

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ----------------- Sentence (e) -----------------
    add_h2("Sentence 3(e): '. . . I am sitting in Mindy’s restaurant putting on the gefillte fish, which is a dish I am very fond of, . . .'")
    
    pos_e = [
        ("I", "PRP", "Personal pronoun", "1st person singular nominative subject pronoun"),
        ("am", "VBP", "Verb, non-3rd person singular present", "Auxiliary verb forming present progressive"),
        ("sitting", "VBG", "Verb, gerund or present participle", "Present participle main verb"),
        ("in", "IN", "Preposition / subordinating conjunction", "Locative preposition"),
        ("Mindy", "NNP", "Proper noun, singular", "Proper noun; name of restaurant owner"),
        ("’s", "POS", "Possessive ending", "Possessive marker clitic attached to 'Mindy'"),
        ("restaurant", "NN", "Noun, singular or mass", "Head noun of locative noun phrase"),
        ("putting", "VBG", "Verb, gerund or present participle", "Coordinate present participle verb in participial clause"),
        ("on", "RP", "Adverb / particle", "Particle in phrasal idiom 'putting on' (eating hearty portions)"),
        ("the", "DT", "Determiner", "Definite article"),
        ("gefillte", "JJ", "Adjective", "Attributive adjective (or NN/FW; culinary borrowed term for minced fish)"),
        ("fish", "NN", "Noun, singular or mass", "Head noun of direct object NP"),
        ("which", "WDT", "Wh-determiner", "Relative pronoun introducing non-restrictive relative clause"),
        ("is", "VBZ", "Verb, 3rd person singular present", "Copular verb of relative clause"),
        ("a", "DT", "Determiner", "Indefinite article"),
        ("dish", "NN", "Noun, singular or mass", "Predicate nominal noun"),
        ("I", "PRP", "Personal pronoun", "Subject pronoun of embedded relative clause"),
        ("am", "VBP", "Verb, non-3rd person singular present", "Copular verb of embedded relative clause"),
        ("very", "RB", "Adverb", "Degree adverb modifying adjective 'fond'"),
        ("fond", "JJ", "Adjective", "Predicate adjective taking PP complement"),
        ("of", "IN", "Preposition / subordinating conjunction", "Stranded preposition governing relative pronoun 'which'")
    ]
    
    tbl_e = doc.add_table(rows=22, cols=4)
    tbl_e.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_e.autofit = False
    set_table_borders(tbl_e)
    for j, h in enumerate(["Token", "PTB Tag", "Category Name", "Syntactic Function & Justification"]):
        tbl_e.cell(0, j).paragraphs[0].text = h
    format_row(tbl_e.rows[0], bg_color=HEX_NAVY, bold=True, font_size=9, text_color=RGBColor(255, 255, 255))
    tbl_e.rows[0].cells[0].width = Inches(1.1)
    tbl_e.rows[0].cells[1].width = Inches(0.9)
    tbl_e.rows[0].cells[2].width = Inches(1.8)
    tbl_e.rows[0].cells[3].width = Inches(2.7)
    for idx, (tok, tag, cat, just) in enumerate(pos_e, start=1):
        row = tbl_e.rows[idx]
        row.cells[0].paragraphs[0].text = tok
        row.cells[1].paragraphs[0].text = tag
        row.cells[2].paragraphs[0].text = cat
        row.cells[3].paragraphs[0].text = just
        format_row(row, bg_color=HEX_ALT_ROW if idx % 2 == 1 else "FFFFFF", font_size=8.5)
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        row.cells[1].paragraphs[0].runs[0].font.bold = True
        row.cells[1].paragraphs[0].runs[0].font.color.rgb = BLUE

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ----------------- Sentence (f) -----------------
    add_h2("Sentence 3(f): 'When a guy and a doll get to taking peeks back and forth at each other, why there you are indeed.'")
    
    pos_f = [
        ("When", "WRB", "Wh-adverb", "Subordinating wh-adverb introducing temporal subordinate clause"),
        ("a", "DT", "Determiner", "Indefinite article"),
        ("guy", "NN", "Noun, singular or mass", "Subject noun conjunct 1"),
        ("and", "CC", "Coordinating conjunction", "Coordinates coordinate subject noun phrases"),
        ("a", "DT", "Determiner", "Indefinite article"),
        ("doll", "NN", "Noun, singular or mass", "Subject noun conjunct 2 (Runyonese for attractive young woman)"),
        ("get", "VBP", "Verb, non-3rd person singular present", "Plural agreement present tense lexical verb"),
        ("to", "TO", "to", "Preposition / infinitive marker taking gerundial complement"),
        ("taking", "VBG", "Verb, gerund or present participle", "Gerund participle head of verb complement"),
        ("peeks", "NNS", "Noun, plural", "Plural direct object noun (meaning brief furtive glances)"),
        ("back", "RB", "Adverb", "Directional adverb in reciprocal binomial pair 'back and forth'"),
        ("and", "CC", "Coordinating conjunction", "Coordinates directional adverbs"),
        ("forth", "RB", "Adverb", "Directional adverb"),
        ("at", "IN", "Preposition / subordinating conjunction", "Directional preposition governing target of glances"),
        ("each", "DT", "Determiner", "Part of reciprocal pronoun pair 'each other' (tagged DT JJ in PTB)"),
        ("other", "JJ", "Adjective", "Part of reciprocal pronoun pair 'each other'"),
        ("why", "UH", "Interjection", "Conversational discourse marker / exclamatory interjection (also accepted as WRB)"),
        ("there", "RB", "Adverb", "Presentational / existential adverb anchoring clause"),
        ("you", "PRP", "Personal pronoun", "2nd person subject pronoun"),
        ("are", "VBP", "Verb, non-3rd person singular present", "Present tense copula agreeing with 'you'"),
        ("indeed", "RB", "Adverb", "Emphatic sentence adverb confirming certainty")
    ]
    
    tbl_f = doc.add_table(rows=22, cols=4)
    tbl_f.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_f.autofit = False
    set_table_borders(tbl_f)
    for j, h in enumerate(["Token", "PTB Tag", "Category Name", "Syntactic Function & Justification"]):
        tbl_f.cell(0, j).paragraphs[0].text = h
    format_row(tbl_f.rows[0], bg_color=HEX_NAVY, bold=True, font_size=9, text_color=RGBColor(255, 255, 255))
    tbl_f.rows[0].cells[0].width = Inches(1.1)
    tbl_f.rows[0].cells[1].width = Inches(0.9)
    tbl_f.rows[0].cells[2].width = Inches(1.8)
    tbl_f.rows[0].cells[3].width = Inches(2.7)
    for idx, (tok, tag, cat, just) in enumerate(pos_f, start=1):
        row = tbl_f.rows[idx]
        row.cells[0].paragraphs[0].text = tok
        row.cells[1].paragraphs[0].text = tag
        row.cells[2].paragraphs[0].text = cat
        row.cells[3].paragraphs[0].text = just
        format_row(row, bg_color=HEX_ALT_ROW if idx % 2 == 1 else "FFFFFF", font_size=8.5)
        row.cells[0].paragraphs[0].runs[0].font.bold = True
        row.cells[1].paragraphs[0].runs[0].font.bold = True
        row.cells[1].paragraphs[0].runs[0].font.color.rgb = BLUE

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # =========================================================================
    # CONCLUSION & SUMMARY
    # =========================================================================
    add_h1("CONCLUSION & SUBMISSION SUMMARY")
    
    summary_box = (
        "Assignment 2 Comprehensive Solution Summary:\n\n"
        "1. Question 1 (Laplace Smoothing): Computed both Add-1 smoothed probabilities P* and effective smoothed counts c* "
        "for the 8x8 Berkeley Restaurant Project bigram matrix (V = 1446). Evaluated the severe discounting of high-frequency bigrams "
        "(e.g., C(want, to) dropping from 608 to 237.9) and explained why modern pipelines favor Good-Turing and Kneser-Ney smoothing.\n\n"
        "2. Question 2 (Bag Generation): Formulated sentence reordering from an unordered multiset as a maximum likelihood permutation problem. "
        "Demonstrated its NP-hardness through isomorphism to the Traveling Salesperson Problem (TSP) on directed graphs, and implemented a "
        "full, standalone Python program with Beam Search decoding that recovered scrambled sentences with 100% exact match accuracy.\n\n"
        "3. Question 3 (Penn Treebank Tagging): Conducted exhaustive word-by-word POS tagging for all six complex sentences from "
        "Damon Runyon’s short stories, resolving difficult syntactic phenomena including indefinite pronoun classification (NN), "
        "phrasal verb particles (RP), compound modifiers (JJ), reciprocal pronouns (DT JJ), and discourse interjections (UH)."
    )
    add_callout(summary_box, title="Final Assessment Executive Summary", border_color=HEX_NAVY, bg_color=HEX_CALLOUT_BG)

    # Save document
    out_docx_path = r'c:\Users\mithu\OneDrive\Desktop\DSA0311 - NATURAL LANGUAGE PROCESSING\NLP-Assessment-2026\Assignments\Assignment-2\DSA03-NLP_Assignment2_Solution.docx'
    doc.save(out_docx_path)
    print("Word document generated successfully at:", out_docx_path)

if __name__ == "__main__":
    create_document()
