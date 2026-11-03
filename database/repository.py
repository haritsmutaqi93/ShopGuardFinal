"""Structured Supabase data access for ShopGuard pages."""
from __future__ import annotations

from typing import Any

from .supabase_client import get_supabase_client


class ShopGuardRepository:
    """Repository for business, watermark, verification, and storage operations."""
    def __init__(self, client: Any | None = None) -> None:
        self.client = client or get_supabase_client()

    def list_businesses(self) -> list[dict]:
        return self.client.table("businesses").select("*").order("business_code").execute().data

    def create_business(self, business_code: str, business_name: str) -> dict:
        return self.client.table("businesses").insert({"business_code": business_code.strip(), "business_name": business_name.strip()}).execute().data[0]

    def dashboard_summary(self) -> dict[str, int]:
        return {
            "businesses": len(self.client.table("businesses").select("id", count="exact").execute().data),
            "watermarks": len(self.client.table("watermark_records").select("id", count="exact").eq("status", "embedded").execute().data),
            "verifications": len(self.client.table("verification_logs").select("id", count="exact").execute().data),
        }

    def create_watermark_record(self, values: dict) -> dict:
        return self.client.table("watermark_records").insert(values).execute().data[0]

    def log_verification(self, values: dict) -> dict:
        return self.client.table("verification_logs").insert(values).execute().data[0]

    def find_watermark_record(self, business_code: str, asset_id: str) -> dict | None:
        response = self.client.table("watermark_records").select("id,businesses!inner(business_code)").eq("asset_id", asset_id).eq("businesses.business_code", business_code).limit(1).execute()
        return response.data[0] if response.data else None

    def list_watermarks(self, limit: int = 100) -> list[dict]:
        return self.client.table("watermark_records").select("*,businesses(business_code,business_name)").order("created_at", desc=True).limit(limit).execute().data

    def list_verifications(self, limit: int = 100) -> list[dict]:
        return self.client.table("verification_logs").select("*").order("verified_at", desc=True).limit(limit).execute().data

    def upload_output(self, path: str, png_bytes: bytes) -> str:
        self.client.storage.from_("shopguard-images").upload(path, png_bytes, {"content-type": "image/png", "upsert": "false"})
        return path
