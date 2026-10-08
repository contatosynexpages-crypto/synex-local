"""Kokoro local text-to-speech provider tool (kokoro-onnx).

Free, offline, multilingual (incl. Brazilian Portuguese: pm_alex, pf_dora,
pm_santa). Model files are looked up in $KOKORO_MODEL_DIR, then ./modelo,
then ~/.kokoro.

Besides the WAV, it returns per-sentence timings and word-level captions
(word timings spread across each sentence by character length), in the
WordCaption shape the Remotion Explainer composition accepts.
"""

from __future__ import annotations

import os
import re
import time
from pathlib import Path
from typing import Any

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    RetryPolicy,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    ToolTier,
)

MODEL_FILES = ("kokoro-v1.0.onnx", "voices-v1.0.bin")
MODEL_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0"


def _model_dir() -> Path | None:
    candidates = [os.environ.get("KOKORO_MODEL_DIR"), "modelo", str(Path.home() / ".kokoro")]
    for c in candidates:
        if c and all((Path(c) / f).exists() for f in MODEL_FILES):
            return Path(c)
    return None


def _espeak_config():
    """espeak-ng falls back to its compiled-in path when the data path is long
    (deep venvs) — a symlink is resolved back to the long path, so copy the
    data to a short real directory instead."""
    import shutil
    import tempfile

    import espeakng_loader
    from kokoro_onnx.config import EspeakConfig

    data = espeakng_loader.get_data_path()
    if len(data) > 90:
        short = Path(tempfile.gettempdir()) / "kokoro-espeak-data"
        if short.is_symlink():
            short.unlink()
        if not (short / "phontab").exists():
            shutil.copytree(data, short, dirs_exist_ok=True)
        data = str(short)
    return EspeakConfig(data_path=data)


class KokoroTTS(BaseTool):
    name = "kokoro_tts"
    version = "0.1.0"
    tier = ToolTier.VOICE
    capability = "tts"
    provider = "kokoro"
    stability = ToolStability.EXPERIMENTAL
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.DETERMINISTIC
    runtime = ToolRuntime.LOCAL

    dependencies = ["python:kokoro_onnx", "python:soundfile"]
    install_instructions = (
        "pip install kokoro-onnx soundfile\n"
        f"Download {MODEL_FILES[0]} and {MODEL_FILES[1]} from {MODEL_URL}\n"
        "into ~/.kokoro (or set KOKORO_MODEL_DIR)."
    )
    agent_skills = ["text-to-speech"]

    capabilities = ["text_to_speech", "offline_generation", "word_timestamps_estimated"]
    supports = {"voice_cloning": False, "multilingual": True, "offline": True, "native_audio": True}
    best_for = [
        "free offline narration in Brazilian Portuguese (pm_alex, pf_dora)",
        "zero-key productions",
    ]
    not_good_for = ["voice clone matching", "exact word-level timestamps"]

    input_schema = {
        "type": "object",
        "required": ["text"],
        "properties": {
            "text": {"type": "string", "description": "Narration. Sentences are split on . ! ?"},
            "voice": {"type": "string", "default": "pm_alex"},
            "lang": {"type": "string", "default": "pt-br"},
            "speed": {"type": "number", "default": 1.0},
            "sentence_pause": {"type": "number", "default": 0.35},
            "output_path": {"type": "string"},
        },
    }

    resource_profile = ResourceProfile(cpu_cores=2, ram_mb=1500, vram_mb=0, disk_mb=400, network_required=False)
    retry_policy = RetryPolicy(max_retries=1, retryable_errors=[])
    idempotency_key_fields = ["text", "voice", "lang", "speed"]
    side_effects = ["writes audio file to output_path"]
    user_visible_verification = ["Listen to generated audio for pronunciation and pacing"]

    def get_status(self) -> ToolStatus:
        try:
            import kokoro_onnx  # noqa: F401
            import soundfile  # noqa: F401
        except Exception:
            return ToolStatus.UNAVAILABLE
        return ToolStatus.AVAILABLE if _model_dir() else ToolStatus.UNAVAILABLE

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        return 0.0

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        if self.get_status() != ToolStatus.AVAILABLE:
            return ToolResult(success=False, error="Kokoro TTS not available. " + self.install_instructions)
        start = time.time()
        try:
            result = self._generate(inputs)
        except Exception as exc:
            return ToolResult(success=False, error=f"Kokoro generation failed: {exc}")
        result.duration_seconds = round(time.time() - start, 2)
        return result

    def _generate(self, inputs: dict[str, Any]) -> ToolResult:
        import numpy as np
        import soundfile as sf
        from kokoro_onnx import Kokoro

        md = _model_dir()
        kokoro = Kokoro(str(md / MODEL_FILES[0]), str(md / MODEL_FILES[1]), espeak_config=_espeak_config())
        voice = inputs.get("voice", "pm_alex")
        lang = inputs.get("lang", "pt-br")
        speed = float(inputs.get("speed", 1.0))
        pause = float(inputs.get("sentence_pause", 0.35))
        output_path = Path(inputs.get("output_path", "tts_output.wav"))
        output_path.parent.mkdir(parents=True, exist_ok=True)

        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", inputs["text"].strip()) if s.strip()]
        chunks, timings, captions = [], [], []
        sr, t = 24000, 0.0
        for s in sentences:
            audio, sr = kokoro.create(s, voice=voice, speed=speed, lang=lang)
            audio = np.asarray(audio, dtype=np.float32)
            # trim leading/trailing near-silence so timings are tight
            idx = np.where(np.abs(audio) > 0.01)[0]
            if idx.size:
                audio = audio[max(0, idx[0] - int(0.03 * sr)): idx[-1] + int(0.08 * sr)]
            dur = len(audio) / sr
            timings.append({"text": s, "start": round(t, 3), "end": round(t + dur, 3)})
            words = s.split()
            total = sum(len(w) + 1 for w in words)
            wt = t
            for i, w in enumerate(words):
                wd = dur * (len(w) + 1) / total
                captions.append({
                    "word": w,
                    "startMs": int(wt * 1000),
                    "endMs": int((wt + wd) * 1000),
                    **({"pageBreakAfter": True} if i == len(words) - 1 else {}),
                })
                wt += wd
            chunks += [audio, np.zeros(int(pause * sr), dtype=np.float32)]
            t += dur + pause

        sf.write(str(output_path), np.concatenate(chunks), sr)
        return ToolResult(
            success=True,
            data={
                "provider": self.provider,
                "voice": voice,
                "output": str(output_path),
                "format": "wav",
                "duration_seconds": round(t, 3),
                "sentences": timings,
                "captions": captions,
            },
            artifacts=[str(output_path)],
            model="kokoro-v1.0",
        )
