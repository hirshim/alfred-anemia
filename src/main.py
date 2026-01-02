"""貧血鑑別スクリプト - Script Filter用にすべてのコードを1ファイルに統合"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# 性別ごとの貧血基準値（g/dL）
ANEMIA_THRESHOLD_MALE = 13.0
ANEMIA_THRESHOLD_FEMALE = 12.0


def check_anemia(gender: str, hb: float) -> dict[str, str]:
    """貧血を鑑別する

    Args:
        gender: 性別（'m' または 'f'）
        hb: ヘモグロビン値（g/dL）

    Returns:
        辞書形式の結果:
        - title: タイトル文字列
        - subtitle: サブタイトル文字列
    """
    gender_lower = gender.lower().strip()

    # 性別の検証
    if gender_lower not in ("m", "f"):
        return {
            "title": "性別: (m or f)",
            "subtitle": "性別: (m or f)",
        }

    # 性別が有効な場合
    threshold = (
        ANEMIA_THRESHOLD_MALE if gender_lower == "m" else ANEMIA_THRESHOLD_FEMALE
    )

    title = f"性別: {gender_lower}, Hb: {hb:.1f}"
    subtitle = f"Hb: < {threshold:.1f} g/dL → 貧血"

    return {
        "title": title,
        "subtitle": subtitle,
    }


def parse_arguments() -> argparse.Namespace:
    """コマンドライン引数を解析する

    Returns:
        解析された引数の名前空間
    """
    parser = argparse.ArgumentParser(
        description="貧血の鑑別を行うスクリプト",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version="alfred-anemia 0.1.0",
    )

    parser.add_argument(
        "--input",
        "-i",
        type=str,
        help="入力ファイルのパス（JSON形式）",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="出力ファイルのパス",
    )

    parser.add_argument(
        "gender",
        nargs="?",
        type=str,
        help="性別（m: 男性, f: 女性）",
    )

    parser.add_argument(
        "hb",
        nargs="?",
        type=float,
        help="ヘモグロビン値（g/dL）",
    )

    return parser.parse_args()


def validate_inputs(gender: str | None, hb: float | None) -> tuple[str, float]:
    """入力を検証する

    Args:
        gender: 性別
        hb: ヘモグロビン値

    Returns:
        検証済みの性別とヘモグロビン値のタプル

    Raises:
        SystemExit: 入力が無効な場合（エラーコード2）
    """
    if gender is None or hb is None:
        print("エラー: 性別とヘモグロビン値が必要です", file=sys.stderr)
        print("使用方法: python -m src.main <gender> <hb>", file=sys.stderr)
        sys.exit(2)

    try:
        hb_float = float(hb)
    except (ValueError, TypeError):
        print(f"エラー: ヘモグロビン値が無効です: {hb}", file=sys.stderr)
        sys.exit(2)

    if hb_float < 0:
        msg = f"エラー: ヘモグロビン値は0以上である必要があります: {hb_float}"
        print(msg, file=sys.stderr)
        sys.exit(2)

    return gender, hb_float


def format_output(result: dict[str, str], output_format: str = "text") -> str:
    """結果をフォーマットする

    Args:
        result: 結果の辞書
        output_format: 出力形式（'text' または 'json'）

    Returns:
        フォーマットされた文字列
    """
    if output_format == "json":
        return json.dumps(result, ensure_ascii=False, indent=2)
    else:
        return f"{result['title']}\n{result['subtitle']}"


def read_input_file(file_path: str) -> dict[str, Any]:
    """入力ファイルを読み込む

    Args:
        file_path: 入力ファイルのパス

    Returns:
        読み込んだデータの辞書

    Raises:
        SystemExit: ファイル読み込みエラー（エラーコード3）
    """
    path = Path(file_path)

    if not path.exists():
        print(f"エラー: ファイルが見つかりません: {file_path}", file=sys.stderr)
        sys.exit(3)

    try:
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError as e:
        print(f"エラー: JSONの解析に失敗しました: {e}", file=sys.stderr)
        sys.exit(3)
    except Exception as e:
        print(f"エラー: ファイルの読み込みに失敗しました: {e}", file=sys.stderr)
        sys.exit(3)


def write_output_file(file_path: str, content: str) -> None:
    """出力ファイルに書き込む

    Args:
        file_path: 出力ファイルのパス
        content: 書き込む内容

    Raises:
        SystemExit: ファイル書き込みエラー（エラーコード3）
    """
    path = Path(file_path)

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"エラー: ファイルの書き込みに失敗しました: {e}", file=sys.stderr)
        sys.exit(3)


def main() -> int:
    """メイン関数

    Returns:
        終了コード（0: 正常終了、1-3: エラー）
    """
    try:
        try:
            args = parse_arguments()
        except SystemExit as e:
            # --help や --version の場合は正常終了として扱う
            return 0 if e.code == 0 else 1

        # 入力ファイルから読み込む場合
        if args.input:
            try:
                data = read_input_file(args.input)
                gender = data.get("gender")
                hb = data.get("hb")
            except SystemExit:
                return 3
        else:
            # コマンドライン引数から取得
            gender = args.gender
            hb = args.hb

        # 入力の検証
        try:
            gender, hb = validate_inputs(gender, hb)
        except SystemExit:
            return 2

        # 貧血鑑別の実行
        result = check_anemia(gender, hb)

        # 出力形式の決定（出力ファイルの拡張子から判断）
        output_format = (
            "json" if args.output and args.output.endswith(".json") else "text"
        )

        # 結果のフォーマット
        output = format_output(result, output_format)

        # 出力
        if args.output:
            write_output_file(args.output, output)
        else:
            print(output)

        return 0

    except KeyboardInterrupt:
        print("\n中断されました", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"エラー: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
