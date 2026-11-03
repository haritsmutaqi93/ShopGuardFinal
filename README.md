# ShopGuard

ShopGuard is a local Streamlit academic prototype that embeds a small, invisible ownership identifier into RGB product images. It uses one least-significant bit (LSB) of each RGB channel and exports the result as PNG.

## What it does

- Creates and selects business profiles stored in Supabase Postgres.
- Frames `business_code` and `asset_id` in a deterministic `SGWM` v1 binary payload: magic bytes, version, big-endian length, UTF-8 JSON, and CRC32.
- Embeds/extracts that frame in deterministic row-major RGB LSBs.
- Rejects insufficient capacity and differentiates valid, not found, and corrupted payloads.
- Calculates MSE/PSNR on equal-size RGB images, shows histories, and optionally supports private Storage through `ShopGuardRepository.upload_output`.

## Local setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .streamlit\secrets.toml.example .streamlit\secrets.toml
streamlit run app.py
```

## Supabase setup

1. Create a Supabase project.
2. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and place the project URL and **service-role key** there only. Never commit or paste that key into chat.
3. Review and run `supabase/migrations/001_initial_schema.sql` in the Supabase SQL Editor. This creates the three tables, indexes, and enables RLS. It does not create broad browser policies because this local server uses the service role.
4. Optional Storage: create a **private** bucket named `shopguard-images`. The repository exposes a storage upload method; the MVP keeps local PNG download as the primary workflow.

Without credentials, local image embedding, extraction, and comparison still work where reachable; business creation and history persistence deliberately report that they are unavailable.

## Tests

```powershell
pytest -q
```

Tests cover frame round trips, CRC failure, capacity rejection, not-found detection, corrupted bits, and MSE/PSNR. They do not call Supabase.

## Limits

LSB data is fragile: JPEG recompression, resize, crop, filtering, color conversion, and screenshots may break recovery. CRC32 detects accidental corruption only; it is not authentication, legal proof, or tamper resistance. Always retain the generated PNG unchanged for the demonstration.
