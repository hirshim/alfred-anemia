"""貧血鑑別ロジックのテスト"""

import pytest

from src.main import check_anemia


class TestAnemiaChecker:
    """貧血鑑別関数のテスト"""

    def test_check_anemia_male_valid(self) -> None:
        """男性の有効な入力のテスト"""
        result = check_anemia("m", 14.0)
        assert result["title"] == "性別: m, Hb: 14.0"
        assert result["subtitle"] == "Hb: < 13.0 g/dL → 貧血"

    def test_check_anemia_female_valid(self) -> None:
        """女性の有効な入力のテスト"""
        result = check_anemia("f", 11.0)
        assert result["title"] == "性別: f, Hb: 11.0"
        assert result["subtitle"] == "Hb: < 12.0 g/dL → 貧血"

    def test_check_anemia_invalid_gender(self) -> None:
        """無効な性別のテスト"""
        result = check_anemia("x", 14.0)
        assert result["title"] == "性別: (m or f)"
        assert result["subtitle"] == "性別: (m or f)"

    def test_check_anemia_case_insensitive(self) -> None:
        """大文字小文字を区別しないテスト"""
        result_m = check_anemia("M", 14.0)
        result_f = check_anemia("F", 11.0)
        assert result_m["title"] == "性別: m, Hb: 14.0"
        assert result_f["title"] == "性別: f, Hb: 11.0"

    def test_check_anemia_with_whitespace(self) -> None:
        """空白を含む性別のテスト"""
        result = check_anemia(" m ", 14.0)
        assert result["title"] == "性別: m, Hb: 14.0"

    def test_check_anemia_decimal_hb(self) -> None:
        """小数点を含むヘモグロビン値のテスト"""
        result = check_anemia("m", 13.5)
        assert result["title"] == "性別: m, Hb: 13.5"
