from pathlib import Path

from pydantic import BaseModel

from app.config import get_settings


class RitaMemoryContext(BaseModel):
    long_term_memory_md: str
    interaction_samples_md: str
    source_files: list[str]

    def to_prompt_section(self) -> str:
        return f"""
# Rita Long-term Memory
{self.long_term_memory_md}

# Rita Interaction Samples
{self.interaction_samples_md}
""".strip()


class MemoryLoader:
    def __init__(self, project_root: Path | None = None) -> None:
        self.project_root = project_root or get_settings().project_root
        self.long_term_memory_path = self.project_root / "data" / "memories" / "processed" / "rita-long-term-memory.md"
        self.interaction_samples_path = self.project_root / "data" / "references" / "rita-source-notes" / "interaction-samples.md"

    def load(self) -> RitaMemoryContext:
        return RitaMemoryContext(
            long_term_memory_md=self._read_text(self.long_term_memory_path),
            interaction_samples_md=self._read_text(self.interaction_samples_path),
            source_files=[
                str(self.long_term_memory_path.relative_to(self.project_root)),
                str(self.interaction_samples_path.relative_to(self.project_root)),
            ],
        )

    @staticmethod
    def _read_text(path: Path) -> str:
        if not path.exists():
            return ""
        return path.read_text(encoding="utf-8").strip()
