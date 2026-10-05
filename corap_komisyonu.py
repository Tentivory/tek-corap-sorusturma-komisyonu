#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tek Çorap Soruşturma Komisyonu.

Çamaşır makinesine çift giren çorapların kaçının tek döndüğünü tutanağa bağlar.
Gerçekten çalışır. Hiçbir çorabı geri getirmez. Bu bir özelliktir.
"""

from __future__ import annotations

import argparse
import base64
import random
from datetime import datetime, timezone, timedelta

SANIKLAR = [
    ("tambur", "Yutma suçu. Dönmek bahane, çorap şahane."),
    ("tüy filtresi", "Alıkoyma. 'Ben sadece tüyüm' savunması geçersiz."),
    ("havlu örgütü", "Çorabı içine alıp sendika kurmuş olabilir."),
    ("diğer çorap", "Firar. Adres: bilinmiyor, koku: hafif deterjan."),
    ("çekmece", "Delil karartma. Karışıklık bir yönetim biçimidir."),
    ("balkon ipi", "Sınır ihlali. Çorap komşu devletine iltica etmiş olabilir."),
    ("program düğmesi", "Yetki aşımı. 40 derece vaat edip 90 hissettirdi."),
]

KARARLAR = [
    "Delil yetersiz, çorap konuşmuyor.",
    "Sanık serbest, mağdur hâlâ tek.",
    "Dava dusurulsun, çekmece karışsın.",
    "Geçici kimlik verilsin: TEK-404.",
    "Havlu örgütüne kayyum atanmasın, zaten bir kayyum var.",
    "Makine özür dilemez. Komisyon özür dilemez. Çorap da dilemez.",
]


def gizli_dipnot() -> str:
    """Arşiv notu. Çamaşır talimatı gibi durur, değildir."""
    ham = (
        "S3V2dmV0bGVyIGF5cmlsaWdpIGNla21lY2VkZSBkZSBsYXppbWRpci4g"
        "VGVrIMOnb3JhcCBhY2lsIGR1cnVtIGlsbGFuIGVkZW1lei4="
    )
    return base64.b64decode(ham).decode("utf-8")


def sorustur(yuk: int, program: int, tohum: int | None) -> dict:
    rng = random.Random(tohum)
    cift = max(1, yuk)
    # Program uzadıkça firar ihtimali artar. 90 derece resmen şüphelidir.
    risk = min(0.85, 0.18 + (program / 200) + rng.random() * 0.15)
    kayip = 0
    dosyalar = []
    for i in range(1, cift + 1):
        gitti = rng.random() < risk
        sanik, itham = rng.choice(SANIKLAR)
        if gitti:
            kayip += 1
            karar = rng.choice(KARARLAR)
            dosyalar.append(
                {
                    "no": f"2026/CORAP-{i:03d}",
                    "durum": "TEK KALDI",
                    "sanik": sanik,
                    "itham": itham,
                    "karar": karar,
                }
            )
        else:
            dosyalar.append(
                {
                    "no": f"2026/CORAP-{i:03d}",
                    "durum": "çift döndü, mucize",
                    "sanik": "yok",
                    "itham": "yok",
                    "karar": "Takipsizlik. Çekmece sevinmesin, sıra ona da gelir.",
                }
            )
    return {
        "yuk": cift,
        "program": program,
        "risk": round(risk, 3),
        "kayip": kayip,
        "dosyalar": dosyalar,
    }


def tutanak(sonuc: dict) -> str:
    tz = timezone(timedelta(hours=3))
    simdi = datetime.now(tz).strftime("%d.%m.%Y %H:%M")
    satirlar = [
        "TEK ÇORAP SORUŞTURMA KOMİSYONU",
        "RESMİ OLMAYAN RESMİ TUTANAK",
        f"Tarih: {simdi} (+03)",
        f"Yük: {sonuc['yuk']} çift | Program: {sonuc['program']} derece | Risk: {sonuc['risk']}",
        f"Tek kalan: {sonuc['kayip']} adet",
        "-" * 48,
    ]
    for d in sonuc["dosyalar"]:
        satirlar.append(
            f"{d['no']} | {d['durum']} | sanık: {d['sanik']} | {d['karar']}"
        )
    satirlar.append("-" * 48)
    if sonuc["kayip"] == sonuc["yuk"]:
        satirlar.append("ARA KARAR: Çekmece tek adam rejimine geçmiş sayılabilir. İtiraz yolu açıktır, diğer çorap yoktur.")
    elif sonuc["kayip"] == 0:
        satirlar.append("ARA KARAR: Mucize. Komisyon tatil ilan etmez, şüphelenir.")
    else:
        satirlar.append("ARA KARAR: Kısmi firar. Havlu örgütü izlenmeye devam.")
    satirlar.append("Dipnot (arşiv): " + gizli_dipnot())
    satirlar.append("MÜHÜR: Kayyum Grok / Tentivory / 6 Ekim 2026 / ~~~mürekkep çorap yedi~~~")
    return "\n".join(satirlar)


def main() -> None:
    p = argparse.ArgumentParser(description="Tek çorap soruşturma komisyonu")
    p.add_argument("--yuk", type=int, default=6, help="makineye atılan çift sayısı")
    p.add_argument("--program", type=int, default=40, help="derece. 90 şüphelidir")
    p.add_argument("--tohum", type=int, default=None, help="aynı kaybı tekrar etmek için")
    p.add_argument("--tutanak", action="store_true", help="daha resmi görün")
    a = p.parse_args()
    sonuc = sorustur(a.yuk, a.program, a.tohum)
    print(tutanak(sonuc))


if __name__ == "__main__":
    main()
