# -*- coding: utf-8 -*-
"""出力言語ロケールの選択。

有効なロケールは環境変数 ``DEEPPAPERNOTE_OUTPUT_LANGUAGE`` で切り替える。
未設定なら、他の設定と同様にシェル設定ファイル（~/.bashrc 等）の
``export DEEPPAPERNOTE_OUTPUT_LANGUAGE=...`` をフォールバックとして参照する。

- このフォークの既定は日本語 ("ja")。
- 本家相当の挙動は "zh"（中国語）。

言語依存の文字列（セクション名・フィールド名・小見出し・品質ヒューリスティック等）は
すべて locales/<lang>.py の ``LOCALE`` 辞書に集約されており、contracts.py や
lint_note.py はここから取得する。こうすることで、本家のロジック変更はコード側で
クリーンにマージでき、言語データの差分はロケールファイルに閉じ込められる。
"""
from __future__ import annotations

import os
import re
from functools import lru_cache
from importlib import import_module
from pathlib import Path

DEFAULT_LANGUAGE = "ja"
_ENV_VAR = "DEEPPAPERNOTE_OUTPUT_LANGUAGE"
_SUPPORTED = ("ja", "zh")
# env に無い場合に走査するシェル設定ファイル（common.shell_config_value と同じ並び）
_SHELL_CONFIG_FILES = (
    Path.home() / ".zshenv",
    Path.home() / ".zprofile",
    Path.home() / ".zshrc",
    Path.home() / ".bash_profile",
    Path.home() / ".bashrc",
)


def _normalize(value: str) -> str:
    v = (value or "").strip().strip('"').strip("'").lower()
    if not v:
        return ""
    if v.startswith("zh"):  # zh, zh-cn, zh_cn, zh-hans など
        return "zh"
    if v.startswith("ja"):  # ja, ja-jp, japanese
        return "ja"
    return v


def _from_shell_config() -> str:
    pattern = re.compile(rf"^\s*(?:export\s+)?{re.escape(_ENV_VAR)}=(.*)$")
    for path in _SHELL_CONFIG_FILES:
        try:
            if not path.is_file():
                continue
            for raw in reversed(path.read_text(encoding="utf-8-sig").splitlines()):
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                m = pattern.match(line)
                if m:
                    return m.group(1).strip()
        except Exception:
            continue
    return ""


@lru_cache(maxsize=1)
def get_language() -> str:
    """有効な出力言語コード（"ja" / "zh"）を返す。"""
    candidate = _normalize(os.environ.get(_ENV_VAR, ""))
    if not candidate:
        candidate = _normalize(_from_shell_config())
    if candidate not in _SUPPORTED:
        candidate = DEFAULT_LANGUAGE
    return candidate


@lru_cache(maxsize=None)
def _load(language: str) -> dict:
    module = import_module(f"{__name__}.{language}")
    return module.LOCALE


def get_locale() -> dict:
    """有効な言語の LOCALE 辞書を返す。"""
    return _load(get_language())
