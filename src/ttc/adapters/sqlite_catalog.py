from __future__ import annotations

import sqlite3
from pathlib import Path

from ttc.domain.models import TypedRecord


class SqliteCatalog:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS records (
                    record_id TEXT PRIMARY KEY,
                    profile_id TEXT NOT NULL,
                    record_type TEXT NOT NULL,
                    identity_key TEXT NOT NULL,
                    evidence_id TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    observed_at INTEGER NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    identity_key TEXT NOT NULL,
                    record_id TEXT NOT NULL,
                    evidence_id TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                )
                """
            )

    def persist(self, records: tuple[TypedRecord, ...]) -> None:
        import json

        with self._connect() as conn:
            for record in records:
                payload = json.dumps(record.payload)
                conn.execute(
                    """
                    INSERT INTO records(
                        record_id, profile_id, record_type, identity_key,
                        evidence_id, payload_json, observed_at
                    ) VALUES (?, ?, ?, ?, ?, ?, strftime('%s','now'))
                    ON CONFLICT(record_id) DO UPDATE SET
                        evidence_id=excluded.evidence_id,
                        payload_json=excluded.payload_json
                    """,
                    (
                        record.record_id,
                        record.profile_id,
                        record.record_type,
                        record.identity_key,
                        record.evidence_id,
                        payload,
                    ),
                )
                conn.execute(
                    "DELETE FROM records WHERE identity_key = ? AND record_id != ?",
                    (record.identity_key, record.record_id),
                )
                conn.execute(
                    """
                    INSERT INTO history(identity_key, record_id, evidence_id, payload_json)
                    VALUES (?, ?, ?, ?)
                    """,
                    (record.identity_key, record.record_id, record.evidence_id, payload),
                )

    def list_by_profile(self, profile_id: str) -> tuple[TypedRecord, ...]:
        import json

        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT record_id, profile_id, record_type, identity_key, evidence_id, payload_json
                FROM records WHERE profile_id = ?
                """,
                (profile_id,),
            ).fetchall()
        return tuple(
            TypedRecord(
                record_id=row[0],
                profile_id=row[1],
                record_type=row[2],
                payload=json.loads(row[5]),
                evidence_id=row[4],
                identity_key=row[3],
            )
            for row in rows
        )

    def history_for(self, identity_key: str) -> tuple[str, ...]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT evidence_id FROM history WHERE identity_key = ? ORDER BY id",
                (identity_key,),
            ).fetchall()
        return tuple(row[0] for row in rows)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
