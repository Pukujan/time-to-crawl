from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from ttc.domain.receipts import RunReceipt


class ReceiptLog:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if not self._path.exists():
            self._path.write_text("", encoding="utf-8")

    def append(self, receipt: RunReceipt) -> None:
        import json

        with self._path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(asdict(receipt)) + "\n")

    def load(self) -> tuple[dict[str, object], ...]:
        import json

        rows: list[dict[str, object]] = []
        for line in self._path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
        return tuple(rows)
