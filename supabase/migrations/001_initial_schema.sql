-- Run this once in the Supabase SQL Editor after reviewing it.
create extension if not exists pgcrypto;

create table if not exists public.businesses (
  id uuid primary key default gen_random_uuid(),
  business_code text not null unique,
  business_name text not null,
  created_at timestamptz not null default now()
);

create table if not exists public.watermark_records (
  id uuid primary key default gen_random_uuid(),
  business_id uuid not null references public.businesses(id) on delete restrict,
  asset_id text not null,
  original_filename text not null,
  output_filename text not null,
  output_path text null,
  payload_version integer not null default 1,
  status text not null check (status in ('embedded', 'failed')),
  created_at timestamptz not null default now(),
  unique (business_id, asset_id)
);

create table if not exists public.verification_logs (
  id uuid primary key default gen_random_uuid(),
  watermark_record_id uuid null references public.watermark_records(id) on delete set null,
  uploaded_filename text not null,
  detected_business_code text null,
  detected_asset_id text null,
  result text not null check (result in ('valid', 'not_found', 'corrupted', 'error')),
  details text null,
  verified_at timestamptz not null default now()
);

create index if not exists watermark_records_business_id_idx on public.watermark_records(business_id);
create index if not exists verification_logs_verified_at_idx on public.verification_logs(verified_at desc);
alter table public.businesses enable row level security;
alter table public.watermark_records enable row level security;
alter table public.verification_logs enable row level security;
-- The local server uses a service-role key, which bypasses RLS. Add least-privilege policies before public deployment.
