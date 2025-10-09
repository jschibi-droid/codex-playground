# codex-playground

## Agent Mode

Agent mode provides a quick smoke test to confirm the CLI setup.

```bash
python src/agent_test.py
```

## Competitor Analysis (Automated)

This project includes an automated pipeline for MarketCheck dealership competitor analysis. The workflow pulls active inventory, generates Markdown + CSV traceability, and builds a presentation deck that mirrors our template sections.

- **API key setup**
  - Windows (PowerShell): `setx MARKETCHECK_API_KEY "your-key-value"`
  - macOS/Linux (bash/zsh): `export MARKETCHECK_API_KEY="your-key-value"`
  - For development convenience you can copy `.env.example` to `.env` and load it with your shell or tooling; never commit the `.env` file.
- **GitHub Actions secret**
  - Navigate to *Settings → Secrets and variables → Actions* and add a repository secret named `MARKETCHECK_API_KEY` with the same key value.
- **Local runs**
  - Single target: `python scripts/competitor_report.py --year 2023 --make "Hyundai" --model "Ioniq 6" --zip 19064`
  - Batch targets via config: `python scripts/competitor_report.py --config config/targets.yml`
  - Build presentation from latest CSV: `python scripts/build_presentation.py --config config/targets.yml --markdown-link "https://example.com/reports/..."`
- **Outputs**
  - Markdown reports: `reports/competitors_{make}_{model}_{year}_{YYYYMMDD}.md`
  - Data CSVs (gitignored by default): `reports/data/{make}_{model}_{year}_{YYYYMMDD}.csv`
  - PowerPoint decks: `reports/presentations/{make}_{model}_{year}_{YYYYMMDD}.pptx`
- **Market endpoints**
  - Inventory search uses `/v2/search/car/active` with the `api_key` supplied via query string.
  - Market endpoints are plan-dependent; when unavailable the automation falls back to summaries derived from the inventory listings.
- **References**
  - MarketCheck API docs: https://www.marketcheck.com/developers/docs/
  - MarketCheck pricing: https://www.marketcheck.com/developers/pricing/
