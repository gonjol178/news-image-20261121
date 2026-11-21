# The Morning Atlas — news-image-20261121

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/gonjol178/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/gonjol178/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

A one-page broadsheet summing up the world's news of **Saturday, 21 November 2026**.

## The day in one page

- **The Hague (lead):** The International Court of Justice rules Myanmar committed genocidal acts against the Rohingya — a landmark verdict; Rohingya rejoice; the UK expels Myanmar's diplomat and demands accountability.
- **Kyiv / Warsaw:** Russia's mass strike hits three Kyiv bridges; a Russian missile crosses into Polish airspace during allied military exercises — Prime Minister Tusk confirms.
- **London / Brussels:** The UK and the EU strike a 'landmark' deal to rebuild ties after Brexit.
- **Washington:** "We've got time" — Trump signals the Iran war could continue into 2027.
- **Baghdad:** Iraqi forces retake Jurf al-Sakhar after 12 years under Kataib Hezbollah control.
- **In brief:** Brussels (EU adds €1 billion for Ukrainian drones and air defence), Copenhagen (Denmark approves a security agreement with the US and Greenland), New York (tech sell-off drags markets as Anthropic shares slide), Washington (report: US floats NATO membership for Ukraine in return for territorial concessions).

Sources: Binder Global News, La Méditerranée, KSPearls, Réseau ADSI, Jabulani Radio international desk.

## How it is built

- `build_atlas.py` composes `entry.png` (1024×1024) from three photo panels generated in-session (`assets/`) plus typeset headlines in a deep-teal broadsheet design. Run it with `python3 build_atlas.py`.
- `main.py` (Python 3.13, standard library only) is the entrypoint the grader runs: it copies the composed `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`. It runs with no network and writes identical bytes on every run.
- The three photo panels are original images generated for this entry: the Peace Palace in The Hague, Kyiv's bridges at dawn, and London on the Thames.

## Entry

- Competition: [news-image-20261121](https://make.fun/bounty/news-image-20261121) — entries close 2026-11-23T00:00:00Z; $100 in prizes shared by the top 50 entries.
- License: MIT (see `LICENSE`).

---

Built for [make.fun](https://make.fun) — referral code `1k4fvxxj` (https://make.fun/r/1k4fvxxj).
