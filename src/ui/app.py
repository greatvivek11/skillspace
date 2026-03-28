from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
import json
import tempfile

import gradio as gr
import pandas as pd

from src.config.settings import DATA_DIR, DEFAULT_EMBEDDING_MODEL, EMBEDDINGS_DIR, HF_JOBS_PREFIX, INDEX_DIR, PROCESSED_DIR
from src.data.io import read_json, read_table
from src.data.normalize import normalize_text, split_pipe_skills
from src.embeddings.encoder import load_encoder
from src.reasoning.skill_gap import compute_skill_gap
from src.reasoning.skills import extract_skills, load_skill_catalog
from src.retrieval.index import build_index, load_index
from src.retrieval.query import search_jobs, search_jobs_by_vector


def get_runtime_mode() -> str:
    return os.getenv("SKILLSPACE_RUNTIME_MODE", "sample").strip().lower()


def has_hf_runtime_artifacts() -> bool:
    processed_path = PROCESSED_DIR / "jobs_hf_v1.parquet"
    ids_path, index_path = get_hf_artifact_paths()
    return processed_path.exists() and ids_path.exists() and index_path.exists()


def get_default_runtime_mode() -> str:
    explicit = os.getenv("SKILLSPACE_RUNTIME_MODE")
    if explicit:
        return normalize_runtime_mode(explicit)
    return "hf" if has_hf_runtime_artifacts() else "sample"


def normalize_runtime_mode(runtime_mode: str | None) -> str:
    value = (runtime_mode or get_default_runtime_mode()).strip().lower()
    return value if value in {"sample", "hf"} else "sample"


def load_sample_jobs_frame() -> pd.DataFrame:
    sample_path = DATA_DIR / "jobs_sample.csv"
    jobs = pd.read_csv(sample_path)
    jobs["skills_raw"] = jobs["skills_raw"].map(split_pipe_skills)
    jobs["retrieval_text"] = jobs["title"].fillna("") + ". " + jobs["description"].fillna("")
    return jobs


def load_hf_jobs_frame() -> pd.DataFrame:
    processed_path = PROCESSED_DIR / "jobs_hf_v1.parquet"
    if not processed_path.exists():
        raise FileNotFoundError(
            f"HF runtime mode selected but processed jobs file is missing: {processed_path}"
        )
    return read_table(processed_path)


def get_hf_artifact_paths() -> tuple[Path, Path]:
    return (
        EMBEDDINGS_DIR / f"{HF_JOBS_PREFIX}_ids.json",
        INDEX_DIR / f"{HF_JOBS_PREFIX}.faiss",
    )


def load_hf_runtime_objects() -> tuple:
    jobs_df = load_hf_jobs_frame()
    encoder = load_encoder(DEFAULT_EMBEDDING_MODEL)
    ids_path, index_path = get_hf_artifact_paths()
    if not ids_path.exists() or not index_path.exists():
        vectors = encoder.encode(
            jobs_df["retrieval_text"].fillna("").tolist(),
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        index = build_index(vectors)
        return jobs_df, encoder, index, load_skill_catalog(), False

    job_ids = read_json(ids_path)
    order = {job_id: idx for idx, job_id in enumerate(job_ids)}
    jobs_df = jobs_df[jobs_df["job_id"].isin(order)].copy()
    jobs_df["_order"] = jobs_df["job_id"].map(order)
    jobs_df = jobs_df.sort_values("_order").drop(columns="_order").reset_index(drop=True)
    index = load_index(index_path)
    return jobs_df, encoder, index, load_skill_catalog(), True


def load_jobs_frame(runtime_mode: str) -> pd.DataFrame:
    if normalize_runtime_mode(runtime_mode) == "hf":
        return load_hf_jobs_frame()
    return load_sample_jobs_frame()


@lru_cache(maxsize=2)
def get_runtime_objects(runtime_mode: str) -> tuple:
    runtime_mode = normalize_runtime_mode(runtime_mode)
    if runtime_mode == "hf":
        return load_hf_runtime_objects()
    jobs_df = load_jobs_frame(runtime_mode)
    encoder = load_encoder(DEFAULT_EMBEDDING_MODEL)
    vectors = encoder.encode(
        jobs_df["retrieval_text"].fillna("").tolist(),
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False,
    )
    index = build_index(vectors)
    skill_catalog = load_skill_catalog()
    return jobs_df, encoder, index, skill_catalog, False


def format_runtime_label(runtime_mode: str) -> str:
    return "Hugging Face dataset" if runtime_mode == "hf" else "Sample seed dataset"


def format_results(
    results: pd.DataFrame,
    resume_skills: list[str],
    runtime_mode: str,
    using_prebuilt_index: bool,
) -> tuple[pd.DataFrame, str, str, str, dict[str, object]]:
    display_rows: list[dict[str, object]] = []
    match_summaries: list[str] = []

    for _, row in results.iterrows():
        raw_skills = row.get("skills_raw", [])
        if isinstance(raw_skills, list):
            job_skills = raw_skills
        elif hasattr(raw_skills, "tolist"):
            job_skills = raw_skills.tolist()
        elif raw_skills:
            job_skills = [str(raw_skills)]
        else:
            job_skills = []
        missing_skills = compute_skill_gap(resume_skills, job_skills)
        score = round(float(row.get("score", 0.0)), 4)
        display_rows.append(
            {
                "title": row.get("title", ""),
                "domain": row.get("domain", ""),
                "location": row.get("location", ""),
                "score": score,
                "missing_skills": ", ".join(missing_skills[:5]),
            }
        )
        match_summaries.append(
            "\n".join(
                [
                    f"### {row.get('title', 'Untitled role')}",
                    f"- Score: `{score}`",
                    f"- Domain: `{row.get('domain', 'n/a') or 'n/a'}`",
                    f"- Location: `{row.get('location', 'n/a') or 'n/a'}`",
                    f"- Missing skills: {', '.join(missing_skills[:5]) if missing_skills else 'None'}",
                ]
            )
        )

    top_match = display_rows[0] if display_rows else None
    if top_match:
        hero = "\n".join(
            [
                "## Best Match",
                f"**{top_match['title']}**",
                f"Similarity score: `{top_match['score']}`",
                f"Domain: `{top_match['domain'] or 'n/a'}`",
                f"Location: `{top_match['location'] or 'n/a'}`",
                f"Missing skills: {top_match['missing_skills'] or 'None'}",
            ]
        )
    else:
        hero = "## Best Match\nNo matching jobs found."

    skills_block = "\n".join(
        [
            "## Extracted Resume Skills",
            ", ".join(resume_skills) if resume_skills else "No seed skills detected from the current catalog.",
            "",
            f"Runtime: `{format_runtime_label(runtime_mode)}`",
            f"Model: `{DEFAULT_EMBEDDING_MODEL}`",
            f"Retrieval index: `{'prebuilt artifact' if using_prebuilt_index else 'in-memory runtime build'}`",
        ]
    )
    details_block = "\n\n".join(match_summaries) if match_summaries else "No ranked matches available."
    payload = {
        "resume_skills": resume_skills,
        "runtime_mode": runtime_mode,
        "model": DEFAULT_EMBEDDING_MODEL,
        "using_prebuilt_index": using_prebuilt_index,
        "matches": display_rows,
    }
    return pd.DataFrame(display_rows), hero, skills_block, details_block, payload


def resolve_resume_text(resume_text: str, resume_file) -> str:
    text = normalize_text(resume_text)
    if text:
        return text
    if resume_file is None:
        return ""
    file_path = Path(resume_file)
    if file_path.suffix.lower() != ".txt":
        return ""
    return normalize_text(file_path.read_text(encoding="utf-8"))


def write_results_json(payload: dict[str, object]) -> str | None:
    if not payload:
        return None
    handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    json.dump(payload, handle, indent=2)
    handle.close()
    return handle.name


def analyze_resume(runtime_mode: str, resume_text: str, resume_file) -> tuple[pd.DataFrame, str, str, str, dict[str, object], str | None]:
    text = resolve_resume_text(resume_text, resume_file)
    if not text:
        message = "## Best Match\nPaste resume text or upload a `.txt` resume file."
        return pd.DataFrame(), message, "", "", {}, None

    runtime_mode = normalize_runtime_mode(runtime_mode)
    jobs_df, encoder, index, skill_catalog, using_prebuilt_index = get_runtime_objects(runtime_mode)
    resume_skills = extract_skills(text, skill_catalog)
    if runtime_mode == "hf" and using_prebuilt_index:
        vector = encoder.encode([text], normalize_embeddings=True, convert_to_numpy=True)
        results = search_jobs_by_vector(vector, index, jobs_df, top_k=5)
    else:
        results = search_jobs(text, encoder, index, jobs_df, top_k=5)
    table, hero, skills_block, details_block, payload = format_results(
        results, resume_skills, runtime_mode, using_prebuilt_index
    )
    return table, hero, skills_block, details_block, payload, write_results_json(payload)


def build_app() -> gr.Blocks:
    with gr.Blocks(title="SkillSpace", theme=gr.themes.Soft()) as app:
        gr.Markdown("# SkillSpace")
        gr.Markdown(
            "Upload or paste a candidate resume to retrieve likely-fit roles and highlight missing skills. "
            "This Phase 1 demo is designed for recruiters, hiring managers, and portfolio review."
        )
        gr.Markdown(
            "The app uses semantic embeddings for matching and lightweight rule-based skill-gap reasoning for explanations."
        )

        with gr.Row():
            runtime_mode = gr.Radio(
                choices=["sample", "hf"],
                value=get_default_runtime_mode(),
                label="Runtime mode",
                info="Use `hf` for the public Hugging Face corpus or `sample` for the tiny local demo dataset.",
            )
            run_button = gr.Button("Analyze", variant="primary")

        with gr.Row():
            resume_text = gr.Textbox(
                label="Resume text",
                lines=14,
                placeholder="Paste candidate resume text here...",
                scale=3,
            )
            resume_file = gr.File(
                label="Or upload resume text file",
                file_types=[".txt"],
                type="filepath",
                scale=1,
            )

        with gr.Row():
            hero_output = gr.Markdown(label="Best match")
            skills_output = gr.Markdown(label="Extracted skills")

        results_table = gr.Dataframe(
            label="Top job matches",
            headers=["title", "domain", "location", "score", "missing_skills"],
            interactive=False,
            wrap=True,
        )
        details_output = gr.Markdown(label="Match breakdown")
        debug_output = gr.JSON(label="Exportable results JSON")
        download_output = gr.File(label="Download JSON report")

        examples = gr.Examples(
            examples=[
                ["sample", "Python developer with Docker, PostgreSQL and API experience"],
                ["sample", "Data analyst with SQL, Excel, dashboards, and reporting skills"],
                ["hf", "Python developer with Docker, PostgreSQL and API experience"],
            ],
            inputs=[runtime_mode, resume_text],
        )

        with gr.Accordion("How To Use This Demo", open=False):
            gr.Markdown(
                "1. Paste a candidate resume or upload a `.txt` file.\n"
                "2. Choose `hf` mode for the larger public corpus.\n"
                "3. Review the best match, ranked alternatives, and missing skills.\n"
                "4. Download the JSON output if you want to save the result."
            )
            gr.Markdown(
                "Known limitations: this Phase 1 app uses a small public corpus, a compact embedding model, "
                "and deterministic skill extraction. It is a decision-support demo, not an ATS replacement."
            )

        run_button.click(
            fn=analyze_resume,
            inputs=[runtime_mode, resume_text, resume_file],
            outputs=[results_table, hero_output, skills_output, details_output, debug_output, download_output],
        )

    return app


if __name__ == "__main__":
    build_app().launch()
