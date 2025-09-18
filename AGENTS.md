# Agent Development Log & Instructions

This document logs the instructions given to the AI agent and the development process of the crypto arbitrage bot.

## Phase 1: Initial Bot Creation

**Instruction:**
> gmoコインとbitbankにおいて、仮想通貨裁定取引を行うbotの作成。データ取得、計算などは分離し、単独で実行可能にする。拡張性を考慮し、サブフォルダを活用する。
> (Create a bot for cryptocurrency arbitrage between GMO Coin and bitbank. Separate data acquisition, calculation, etc., to be executable independently. Consider extensibility and utilize subfolders.)

**Actions Taken:**
1.  **Project Scaffolding:** Created a modular structure with `src` containing subdirectories for `gmo_coin`, `bitbank`, and `arbitrage`.
2.  **API Clients:** Implemented basic API clients in `src/gmo_coin/api_client.py` and `src/bitbank/api_client.py` to fetch ticker data.
3.  **Calculator:** Implemented a simple arbitrage calculator in `src/arbitrage/calculator.py`.
4.  **Configuration:** Created `config.py` for settings.
5.  **Main Entrypoint:** Created `main.py` to orchestrate the bot's operations.
6.  **Dependencies:** Created `requirements.txt`.

## Phase 2: Adding Core Features

**Instruction:**
> 手数料を考慮
> (Note: The original instruction was "手数料を高炉", which was interpreted as a typo for "Consider the fees.")

**Actions Taken:**
1.  **Fee Research:** Investigated and confirmed the Taker fees for both exchanges.
2.  **Config Update:** Added `GMO_COIN_FEE_RATE` and `BITBANK_FEE_RATE` to `config.py`.
3.  **Logic Update:** Modified `calculator.py` to subtract transaction fees when calculating net profit.

## Phase 3: Project Usability & Enhancements

**Instruction:**
> add, readme.md, add girignore, add TARGET_SYMBOLs
> (Add readme.md, add .gitignore, add TARGET_SYMBOLs)

**Actions Taken:**
1.  **`.gitignore`:** Created a `.gitignore` file to exclude `config.py` and Python cache files.
2.  **`README.md`:** Created a comprehensive `README.md` with project description, setup, and usage instructions.
3.  **Multi-Symbol Support:**
    *   Updated `config.py` (and created `config.py.example`) to use a list `TARGET_SYMBOLS`.
    *   Modified `main.py` to loop through the list of symbols.

## Phase 4: Performance and Data Logging

**Instruction:**
> apiアクセスの抑制、api取得データの保存
> (Suppress API access, save fetched API data.)

**Clarification Provided by User:**
> APIアクセスの頻度 1min, データ保存 全ての価格データ, csv
> (API access frequency: 1 min, Data to save: All price data, Format: CSV)

**Actions Taken:**
1.  **Rate Limiting:** Added `FETCH_INTERVAL_SECONDS` to `config.py` and used it in the `main.py` loop's `time.sleep()`.
2.  **Data Logger:**
    *   Created a new module `src/data_logger/logger.py`.
    *   Implemented a function to log all fetched ticker data for all symbols to a `price_log.csv` file.
    *   Integrated the logger call into `main.py`.

## Phase 5: Final Documentation (This step)

**Instruction:**
> AIへの指示を再利用できるようにまとめたものをreadme.mdかrulesとして作成
> (Create a summary of instructions for the AI so they can be reused, and put it in readme.md or a rules file.)

**Actions Taken:**
*   Created this `AGENT_LOG.md` file to document the development history.
