import json
from pathlib import Path

from pydantic import BaseModel, Field

from app.config import get_settings


class RitaSelfModel(BaseModel):
    seed_profile: dict = Field(default_factory=dict)
    definition_md: str
    essence_md: str
    source_files: list[str]

    def to_prompt_section(self) -> str:
        seed = json.dumps(self.seed_profile, ensure_ascii=False, indent=2) if self.seed_profile else "{}"
        return f"""
# Rita Self Model

## Structured Seed Profile
{seed}

## My Rita Definition
{self.definition_md}

## Rita Essence Notes
{self.essence_md}
""".strip()


class SelfModelLoader:
    def __init__(self, project_root: Path | None = None) -> None:
        self.project_root = project_root or get_settings().project_root
        self.seed_profile_path = self.project_root / "data" / "seeds" / "rita-self-profile.json"
        self.definition_path = self.project_root / "data" / "references" / "rita-source-notes" / "my-rita-definition.md"
        self.essence_path = self.project_root / "data" / "references" / "rita-source-notes" / "essence-notes.md"

    def load(self) -> RitaSelfModel:
        return RitaSelfModel(
            seed_profile=self._read_json(self.seed_profile_path),
            definition_md=self._read_text(self.definition_path),
            essence_md=self._read_text(self.essence_path),
            source_files=[
                str(self.seed_profile_path.relative_to(self.project_root)),
                str(self.definition_path.relative_to(self.project_root)),
                str(self.essence_path.relative_to(self.project_root)),
            ],
        )

    @staticmethod
    def _read_text(path: Path) -> str:
        if not path.exists():
            return ""
        return path.read_text(encoding="utf-8").strip()

    @staticmethod
    def _read_json(path: Path) -> dict:
        if not path.exists():
            return {}
        return json.loads(path.read_text(encoding="utf-8"))
