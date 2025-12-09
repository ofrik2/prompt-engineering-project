from __future__ import annotations

import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


THIS_FILE = Path(__file__).resolve()
PROJECT_ROOT = THIS_FILE.parents[2]
ANALYSIS_DIR = PROJECT_ROOT / "analysis_results"


def read_csv_rows(path: Path, max_rows: Optional[int] = None) -> List[Dict[str, str]]:
    """Read a CSV file into a list of dicts. Optionally limit to first max_rows."""
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if max_rows is not None:
        rows = rows[:max_rows]
    return rows


def html_table(rows: List[Dict[str, str]]) -> str:
    """Render a list of dicts as a simple HTML table."""
    if not rows:
        return "<p><em>No data available.</em></p>"

    cols = list(rows[0].keys())
    html = ["<table>", "<thead><tr>"]
    for c in cols:
        html.append(f"<th>{c}</th>")
    html.append("</tr></thead><tbody>")

    for r in rows:
        html.append("<tr>")
        for c in cols:
            html.append(f"<td>{r.get(c, '')}</td>")
        html.append("</tr>")

    html.append("</tbody></table>")
    return "\n".join(html)


def section_if_exists(title: str, csv_name: Optional[str], img_name: Optional[str], max_rows: int = 10) -> str:
    """Build an HTML section if at least one of CSV or image exists."""
    parts = []

    csv_path = ANALYSIS_DIR / csv_name if csv_name else None
    img_path = ANALYSIS_DIR / img_name if img_name else None

    has_csv = csv_path is not None and csv_path.exists()
    has_img = img_path is not None and img_path.exists()

    if not has_csv and not has_img:
        # Skip entire section if nothing is there
        return ""

    parts.append(f'<section class="block">')
    parts.append(f"<h2>{title}</h2>")

    if has_img:
        parts.append(f'<div class="image-wrapper"><img src="{img_path.name}" alt="{title} plot"></div>')

    if has_csv:
        rows = read_csv_rows(csv_path, max_rows=max_rows)
        parts.append("<h3>Summary (preview)</h3>")
        parts.append(html_table(rows))
        parts.append(f'<p><a href="{csv_path.name}">Download full CSV</a></p>')

    parts.append("</section>")
    return "\n".join(parts)


def main() -> None:
    ANALYSIS_DIR.mkdir(exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Try to also include method_summary.csv if it exists (might be in results/ or analysis_results/)
    method_summary_section = ""
    method_summary_paths = [
        ANALYSIS_DIR / "method_summary.csv",
        PROJECT_ROOT / "results" / "method_summary.csv",
    ]
    ms_path = next((p for p in method_summary_paths if p.exists()), None)

    if ms_path is not None:
        rows = read_csv_rows(ms_path, max_rows=20)
        method_summary_section = "\n".join(
            [
                '<section class="block">',
                "<h2>Overall Method Summary</h2>",
                html_table(rows),
                f'<p><a href="{ms_path.relative_to(ANALYSIS_DIR.parent)}">Download full CSV</a></p>'
                if ms_path.parent != ANALYSIS_DIR
                else f'<p><a href="{ms_path.name}">Download full CSV</a></p>',
                "</section>",
            ]
        )

    # Build sections using our helper (only included if files exist)
    sections = []

    # 1. Prompt variation
    sections.append(
        section_if_exists(
            title="Prompt Variation: Accuracy vs Prompt Length",
            csv_name="prompt_variation_summary.csv",
            img_name="prompt_variation_plot.png",
        )
    )

    # 2. Method disagreement / per-task comparison
    # Here we show the heatmap + the disagreement matrix CSV
    sections.append(
        section_if_exists(
            title="Method Disagreement Between Prompting Strategies",
            csv_name="method_disagreement_matrix.csv",
            img_name="method_disagreement_heatmap.png",
        )
    )

    # 3. CoT overthinking
    sections.append(
        section_if_exists(
            title="CoT Overthinking: Baseline vs CoT",
            csv_name="cot_overthinking_summary.csv",
            img_name="cot_overthinking_plot.png",
        )
    )

    # 4. Few-shot effect
    sections.append(
        section_if_exists(
            title="Few-shot Effect: Baseline vs Few-shot",
            csv_name="fewshot_effect_summary.csv",
            img_name="fewshot_effect_plot.png",
        )
    )

    # 5. Length vs correctness
    sections.append(
        section_if_exists(
            title="Answer Length vs Correctness",
            csv_name="length_correlation_summary.csv",
            img_name="length_correlation_plot.png",
        )
    )

    sections_html = "\n".join(s for s in sections if s.strip())

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>LLM Prompting Experiments – Analysis Report</title>
  <style>
    body {{
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      margin: 0;
      padding: 0;
      background: #f5f5f5;
      color: #222;
    }}
    header {{
      background: #333;
      color: #fff;
      padding: 16px 32px;
    }}
    header h1 {{
      margin: 0;
      font-size: 1.6rem;
    }}
    header p {{
      margin: 4px 0 0 0;
      font-size: 0.9rem;
      opacity: 0.8;
    }}
    main {{
      max-width: 1000px;
      margin: 24px auto 40px;
      padding: 0 16px;
    }}
    .block {{
      background: #fff;
      border-radius: 8px;
      padding: 16px 20px 20px;
      margin-bottom: 20px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }}
    h2 {{
      margin-top: 0;
      font-size: 1.3rem;
      border-bottom: 1px solid #eee;
      padding-bottom: 8px;
    }}
    h3 {{
      margin-top: 16px;
      font-size: 1.05rem;
    }}
    table {{
      border-collapse: collapse;
      width: 100%;
      margin-top: 8px;
      font-size: 0.9rem;
    }}
    th, td {{
      border: 1px solid #ddd;
      padding: 4px 6px;
      text-align: left;
    }}
    th {{
      background: #fafafa;
      font-weight: 600;
    }}
    tr:nth-child(even) td {{
      background: #fcfcfc;
    }}
    .image-wrapper {{
      text-align: center;
      margin: 8px 0 12px;
    }}
    .image-wrapper img {{
      max-width: 100%;
      height: auto;
      border: 1px solid #ddd;
      border-radius: 4px;
      background: #fdfdfd;
    }}
    a {{
      color: #0066cc;
      text-decoration: none;
    }}
    a:hover {{
      text-decoration: underline;
    }}
  </style>
</head>
<body>
  <header>
    <h1>LLM Prompting Experiments – Analysis Report</h1>
    <p>Generated: {now}</p>
  </header>
  <main>
    {method_summary_section}
    {sections_html if sections_html.strip() else '<p>No analysis files found yet. Run the analysis scripts first.</p>'}
  </main>
</body>
</html>
"""

    report_path = ANALYSIS_DIR / "report.html"
    with report_path.open("w", encoding="utf-8") as f:
        f.write(html)

    print(f"Generated HTML report → {report_path}")


if __name__ == "__main__":
    main()
