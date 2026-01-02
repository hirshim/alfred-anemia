"""mainモジュールのテスト"""

import json
import sys
from pathlib import Path

import pytest

from src.main import main


def test_main_function_exists() -> None:
    """main関数が存在することを確認"""
    assert callable(main)


def test_main_with_valid_args_male(capsys: pytest.CaptureFixture[str]) -> None:
    """男性の有効な引数でのテスト"""
    sys.argv = ["main", "m", "14.0"]
    result = main()
    captured = capsys.readouterr()
    assert result == 0
    assert "性別: m, Hb: 14.0" in captured.out
    assert "Hb: < 13.0 g/dL → 貧血" in captured.out


def test_main_with_valid_args_female(capsys: pytest.CaptureFixture[str]) -> None:
    """女性の有効な引数でのテスト"""
    sys.argv = ["main", "f", "11.0"]
    result = main()
    captured = capsys.readouterr()
    assert result == 0
    assert "性別: f, Hb: 11.0" in captured.out
    assert "Hb: < 12.0 g/dL → 貧血" in captured.out


def test_main_with_invalid_gender(capsys: pytest.CaptureFixture[str]) -> None:
    """無効な性別でのテスト"""
    sys.argv = ["main", "x", "14.0"]
    result = main()
    captured = capsys.readouterr()
    assert result == 0
    assert "性別: (m or f)" in captured.out


def test_main_with_missing_args(capsys: pytest.CaptureFixture[str]) -> None:
    """引数が不足している場合のテスト"""
    sys.argv = ["main"]
    result = main()
    captured = capsys.readouterr()
    assert result == 2
    assert "エラー" in captured.err or "必要" in captured.err


def test_main_with_output_file(tmp_path: Path) -> None:
    """出力ファイル指定のテスト"""
    output_file = tmp_path / "output.txt"
    sys.argv = ["main", "m", "14.0", "--output", str(output_file)]
    result = main()
    assert result == 0
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert "性別: m, Hb: 14.0" in content


def test_main_with_json_output(tmp_path: Path) -> None:
    """JSON形式での出力テスト"""
    output_file = tmp_path / "output.json"
    sys.argv = ["main", "m", "14.0", "--output", str(output_file)]
    result = main()
    assert result == 0
    assert output_file.exists()
    content = json.loads(output_file.read_text(encoding="utf-8"))
    assert content["title"] == "性別: m, Hb: 14.0"
    assert content["subtitle"] == "Hb: < 13.0 g/dL → 貧血"


def test_main_with_input_file(tmp_path: Path) -> None:
    """入力ファイルからの読み込みテスト"""
    input_file = tmp_path / "input.json"
    input_data = {"gender": "f", "hb": 11.5}
    input_file.write_text(json.dumps(input_data), encoding="utf-8")

    sys.argv = ["main", "--input", str(input_file)]
    result = main()
    assert result == 0
