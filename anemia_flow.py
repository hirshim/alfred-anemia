#!/usr/bin/env python3
"""
貧血鑑別診断ワークフロー - ステップバイステップ入力方式

入力形式: anemia [Hb] [WBC] [PLT/Retic] [MCV] ...
フローチャートに基づき、入力値から次のステップまたは診断結果を返す。
"""

import json
import sys
from typing import List, Optional, Dict, Any


# 判定基準
THRESHOLDS = {
    "hb_low_male": 13.0,    # 男性: Hb < 13 で貧血
    "hb_low_female": 12.0,  # 女性: Hb < 12 で貧血 (簡略化のため12を使用)
    "hb_anemia": 12.0,      # 簡略化: Hb < 12 で貧血と判定
    "wbc_low": 4000,        # WBC < 4000 で低値
    "plt_low": 10,          # PLT < 10万 で低値
    "retic_high": 2.0,      # Retic ≥ 2% で増加
    "mcv_low": 80,          # MCV < 80 で小球性
    "mcv_high": 101,        # MCV ≥ 101 で大球性
}


def create_alfred_item(title: str, subtitle: str, arg: str = "", valid: bool = True, icon: str = "icon.png") -> Dict[str, Any]:
    """Alfred用のアイテムを生成する"""
    return {
        "title": title,
        "subtitle": subtitle,
        "arg": arg,
        "valid": valid,
        "icon": {"path": icon}
    }


def create_prompt_item(prompt: str, example: str, current_values: str = "") -> Dict[str, Any]:
    """次の入力を促すアイテムを生成する"""
    return create_alfred_item(
        title=prompt,
        subtitle=f"例: anemia {current_values} {example}".strip(),
        arg="",
        valid=False
    )


def create_result_item(title: str, diagnoses: List[str]) -> Dict[str, Any]:
    """診断結果アイテムを生成する"""
    diagnosis_text = ", ".join(diagnoses)
    return create_alfred_item(
        title=f"🔍 {title}",
        subtitle=f"疑われる疾患: {diagnosis_text}",
        arg=diagnosis_text,
        valid=True
    )


def parse_values(query: str) -> List[float]:
    """入力文字列から数値リストを抽出する"""
    values = []
    for part in query.strip().split():
        try:
            values.append(float(part))
        except ValueError:
            continue
    return values


def diagnose(values: List[float]) -> Dict[str, Any]:
    """
    入力値に基づいて診断フローを実行する。
    
    フロー:
    0. Hb → 貧血の有無を確認
    1. WBC → 低値なら PLT へ、正常なら Retic へ
    2. PLT → WBC/PLT両方低値なら「汎血球減少→骨髄検査」
    3. Retic → 増加なら溶血/出血、なければ MCV へ
    4. MCV → 大球性/正球性/小球性 で分岐
    """
    items = []
    
    # Step 0: Hb入力がない → Hb入力を促す
    if len(values) == 0:
        items.append(create_prompt_item(
            "Hb(g/dL)を入力してください",
            "10.5",
            ""
        ))
        return {"items": items}
    
    hb = values[0]
    
    # Step 0.5: 貧血かどうかチェック
    if hb >= THRESHOLDS["hb_anemia"]:
        items.append(create_alfred_item(
            f"✅ Hb {hb:.1f} g/dL - 貧血なし",
            "WHO基準: 男性<13, 女性<12 で貧血",
            "",
            valid=False
        ))
        return {"items": items}
    
    # 貧血あり → WBC入力へ
    if len(values) < 2:
        items.append(create_prompt_item(
            f"Hb {hb:.1f} (貧血)。WBCを入力してください",
            "4500",
            f"{hb:.1f}"
        ))
        return {"items": items}
    
    wbc = values[1]
    
    # Step 1: WBC評価
    if wbc < THRESHOLDS["wbc_low"]:
        # WBC低値 → PLTを確認
        if len(values) < 3:
            items.append(create_prompt_item(
                f"Hb {hb:.1f}, WBC {wbc:.0f} (低値)。PLT(万)を入力",
                "8",
                f"{hb:.1f} {wbc:.0f}"
            ))
            return {"items": items}
        
        plt = values[2]
        if plt < THRESHOLDS["plt_low"]:
            # 汎血球減少
            items.append(create_result_item(
                "汎血球減少 → 骨髄検査を検討",
                ["再生不良性貧血", "骨髄異形成症候群", "骨髄線維症", 
                 "巨赤芽球性貧血", "白血病", "肝疾患・脾機能亢進症"]
            ))
        else:
            # WBC低値だがPLT正常 → Reticへ
            if len(values) < 4:
                items.append(create_prompt_item(
                    f"Hb {hb:.1f}, WBC {wbc:.0f} (低値), PLT {plt:.0f}万。Retic(%)を入力",
                    "1.5",
                    f"{hb:.1f} {wbc:.0f} {plt:.0f}"
                ))
                return {"items": items}
            retic = values[3]
            return evaluate_retic_and_mcv(values, hb, wbc, retic, 4)
        return {"items": items}
    
    # Step 2: WBC正常 → Retic確認
    if len(values) < 3:
        items.append(create_prompt_item(
            f"Hb {hb:.1f}, WBC {wbc:.0f} (正常)。Retic(%)を入力",
            "1.5",
            f"{hb:.1f} {wbc:.0f}"
        ))
        return {"items": items}
    
    retic = values[2]
    return evaluate_retic_and_mcv(values, hb, wbc, retic, 3)


def evaluate_retic_and_mcv(values: List[float], hb: float, wbc: float, retic: float, mcv_index: int) -> Dict[str, Any]:
    """網赤血球とMCVを評価する"""
    items = []
    values_str = " ".join(f"{v:.1f}" if v < 100 else f"{v:.0f}" for v in values[:mcv_index])
    
    # Step 3: Retic評価
    if retic >= THRESHOLDS["retic_high"]:
        # Retic増加 → 溶血か出血
        items.append(create_result_item(
            "網赤血球増加 → 溶血または出血性貧血",
            ["溶血性貧血（溶血所見あり）", "出血性貧血（溶血所見なし）"]
        ))
        items.append(create_alfred_item(
            "💡 溶血所見を確認",
            "間接Bil↑, LDH↑, ハプトグロビン↓, ヘモジデリン尿",
            "",
            valid=False
        ))
        return {"items": items}
    
    # Step 4: Retic正常 → MCV確認
    if len(values) < mcv_index + 1:
        items.append(create_prompt_item(
            f"Retic {retic:.1f}% (正常)。MCVを入力",
            "85",
            values_str
        ))
        return {"items": items}
    
    mcv = values[mcv_index]
    
    # Step 5: MCV評価で分岐
    if mcv >= THRESHOLDS["mcv_high"]:
        # 大球性貧血
        items.append(create_result_item(
            f"大球性貧血 (MCV {mcv:.0f})",
            ["巨赤芽球性貧血 (VitB12/葉酸欠乏)", "骨髄異形成症候群", 
             "肝疾患", "甲状腺機能低下症", "アルコール性"]
        ))
        items.append(create_alfred_item(
            "💡 VitB12・葉酸を測定してください",
            "欠乏があれば巨赤芽球性貧血、なければ他疾患を検討",
            "",
            valid=False
        ))
    elif mcv <= THRESHOLDS["mcv_low"]:
        # 小球性貧血
        items.append(create_result_item(
            f"小球性貧血 (MCV {mcv:.0f})",
            ["鉄欠乏性貧血", "慢性炎症に伴う貧血 (ACI)", 
             "サラセミア", "鉄芽球性貧血"]
        ))
        items.append(create_alfred_item(
            "💡 Fe, TIBC, フェリチンを測定",
            "Fe↓TIBC↑Fer↓→鉄欠乏 / Fe↓TIBC正常〜↓Fer正常〜↑→ACI",
            "",
            valid=False
        ))
    else:
        # 正球性貧血
        items.append(create_result_item(
            f"正球性貧血 (MCV {mcv:.0f})",
            ["腎性貧血 (EPO低下)", "慢性炎症に伴う貧血", 
             "溶血性貧血", "赤芽球癆"]
        ))
        items.append(create_alfred_item(
            "💡 EPO・フェリチン・CRPを測定",
            "EPO低値→腎性貧血 / 炎症所見あり→ACI",
            "",
            valid=False
        ))
    
    return {"items": items}


def main():
    """メイン処理"""
    query = ""
    if len(sys.argv) > 1:
        query = sys.argv[1].strip()
    
    values = parse_values(query)
    result = diagnose(values)
    
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
