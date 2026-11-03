# ShopGuard --- Product Requirements Document (PRD)

**Version:** 1.0\
**Status:** Build specification\
**Product:** ShopGuard\
**Product type:** Single-operator web application\
**Primary user:** E-commerce store owner / project demonstrator\
**Implementation owner:** One developer using Codex on one laptop\
**Target stack:** Python, Streamlit, Supabase Postgres, Supabase
Storage, Pillow, NumPy

------------------------------------------------------------------------

## 1. Product summary

ShopGuard is a web application that embeds an invisible ownership
identifier into e-commerce product images using Least Significant Bit
(LSB) image steganography. It allows an operator to create a watermarked
PNG, extract and validate the embedded payload from a candidate image,
inspect image-quality metrics, and review operation history stored in
Supabase.

ShopGuard is an academic prototype and demonstration tool. It is **not**
a legal copyright registry, forensic attribution system, or robust
watermark that is expected to survive lossy transformations.

## 2. Problem and opportunity

E-commerce businesses share product images across websites and social
platforms. Images can be copied and redistributed without their original
business or asset identifiers. ShopGuard demonstrates one technical way
to embed an invisible identifier into an image and later check whether
that identifier can be recovered.

## 3. Goals

1.  Provide a usable browser-based workflow to embed ownership metadata
    in a product image.
2.  Recover the exact embedded payload from an unchanged watermarked
    PNG.
3.  Validate payload structure and accidental corruption using a magic
    header, version, length and CRC32.
4.  Store business, watermark-operation and verification metadata in
    Supabase Postgres.
5.  Optionally store generated PNGs in a private Supabase Storage
    bucket.
6.  Measure image distortion with MSE and PSNR and demonstrate the
    limitations of LSB.

### 3.1 Non-goals

-   Searching the internet for copied/stolen images.
-   Proving legal ownership or identity.
-   Guaranteed detection after JPEG recompression, resizing, cropping,
    rotation, filtering or screenshots.
-   Public user registration, multi-tenant access, roles, billing or
    payments.
-   Blockchain, AI image recognition, robust DCT/DWT watermarking.
-   A separate REST API server unless implementation proves Streamlit
    service boundaries insufficient.

## 4. Users and operating assumptions

-   One trusted operator uses the application locally from one laptop.
-   The operator creates/selects a business profile, embeds watermarks,
    verifies candidate images and reviews history.
-   No public sign-up or authentication flow is required for the MVP.
-   The app is run locally with Streamlit. Deployment is optional and
    must not block local completion.
-   Supabase is the hosted database. Local temporary files may be used
    during processing; persistent output storage is optional but
    preferred.

## 5. Scope and priority

### P0 --- required for acceptance

1.  Application starts with `streamlit run app.py`.
2.  Business profile can be created and selected.
3.  PNG/JPEG uploads are validated and normalized safely to RGB.
4.  User enters a business code and asset ID.
5.  App embeds a structured LSB payload and returns a downloadable PNG.
6.  App re-uploads that PNG and extracts the exact payload.
7.  App distinguishes valid, not-found, corrupted/incomplete and
    processing-error outcomes.
8.  App records watermark and verification metadata in Supabase.
9.  Supabase connection failures are shown clearly and do not silently
    claim records were saved.
10. Automated tests cover payload encoding, round-trip extraction,
    capacity errors, invalid images and checksum failure.

### P1 --- strongly desired

-   Dashboard summary counts and recent activity from Supabase.
-   History table with basic filters.
-   Original/output side-by-side preview.
-   MSE and PSNR values calculated from actual arrays.
-   Optional upload of generated PNG to private Supabase Storage.
-   Clear loading, success, warning and error states.

### P2 --- only if time remains

-   Delete/archive history records.
-   Downloadable verification report.
-   Additional UI polish and charts.
-   Deployment beyond localhost.

Do not add features outside this scope without first completing and
testing P0.

## 6. User journeys

### 6.1 Embed a watermark

1.  Operator opens **Embed**.
2.  Selects an existing business or creates one.
3.  Uploads a PNG or JPEG product image.
4.  Enters a unique asset ID.
5.  App validates file size, dimensions, format and payload capacity.
6.  App converts image to RGB and embeds the framed payload using LSB.
7.  App saves the resulting image as PNG.
8.  App displays original and output previews, payload identifiers and
    quality metrics.
9.  App records the operation in Supabase.
10. Operator downloads the PNG.

If the database write fails, clearly tell the operator that the image
was generated but its history record was not saved. Do not report
success for an incomplete operation.

### 6.2 Verify a watermark

1.  Operator opens **Verify** and uploads a candidate image.
2.  App validates and decodes the image without resizing or lossy
    re-encoding.
3.  Extractor checks the magic header, version, declared length and
    CRC32.
4.  App displays one of:
    -   **Valid:** complete supported payload and checksum match.
    -   **Not found:** expected header is absent.
    -   **Corrupted/incomplete:** header exists but payload is
        truncated, unsupported or checksum fails.
    -   **Error:** file cannot be processed.
5.  If valid, show recovered business code and asset ID.
6.  Log the attempt in Supabase, including filename, result and
    extracted identifiers when available.

A valid checksum means the payload passed the format's
accidental-corruption check. It does not prove the claimed business owns
the image.

### 6.3 Review history

Operator opens **History** to view recent watermark operations and
verification attempts from Supabase. Display timestamps, business
code/name, asset ID, filenames, status and verification result. Empty
states and database errors must be handled.

## 7. Functional requirements

  -----------------------------------------------------------------------
  ID                      Requirement             Priority
  ----------------------- ----------------------- -----------------------
  FR-01                   App launches locally    P0
                          through Streamlit.      

  FR-02                   Navigation exposes      P1
                          Dashboard, Embed,       
                          Verify, Compare and     
                          History.                

  FR-03                   Create and list         P0
                          business profiles in    
                          Supabase.               

  FR-04                   Accept PNG/JPEG uploads P0
                          with configurable size  
                          limit and safe          
                          validation.             

  FR-05                   Convert accepted image  P0
                          to RGB for algorithm    
                          processing.             

  FR-06                   Build a versioned       P0
                          payload containing      
                          business code and asset 
                          ID.                     

  FR-07                   Embed payload bits into P0
                          RGB channel LSBs in     
                          deterministic order.    

  FR-08                   Reject insufficient     P0
                          image capacity; never   
                          truncate payload.       

  FR-09                   Export watermarked      P0
                          image as PNG.           

  FR-10                   Extract and validate    P0
                          payload from uploaded   
                          image.                  

  FR-11                   Differentiate           P0
                          not-found,              
                          corrupted/incomplete    
                          and valid results.      

  FR-12                   Store                   P0
                          watermark-operation     
                          metadata in Supabase.   

  FR-13                   Store verification      P0
                          attempts in Supabase.   

  FR-14                   Calculate MSE and PSNR  P1
                          from original and       
                          output images.          

  FR-15                   Show operation history  P1
                          from Supabase.          

  FR-16                   Store output PNG in     P1
                          private Supabase        
                          Storage and save object 
                          path.                   

  FR-17                   Provide understandable  P0
                          error and success       
                          messages.               
  -----------------------------------------------------------------------

## 8. LSB algorithm specification

### 8.1 Image representation

-   Use Pillow to decode uploads and convert to RGB.
-   Use a NumPy `uint8` array with shape `(height, width, 3)`.
-   Traverse channels deterministically in row-major pixel order, RGB
    channel order.
-   Embed one payload bit in the least significant bit of each channel
    value.
-   Preserve image dimensions. Do not resize, crop or color-adjust
    during embedding.
-   Export as PNG.

### 8.2 Payload framing

Use a documented, deterministic binary frame:

1.  Magic bytes: `SGWM` (4 bytes).
2.  Version: unsigned 1-byte integer (initially `1`).
3.  Payload length: unsigned 4-byte big-endian integer.
4.  Payload: UTF-8 JSON bytes with exactly the required identifiers, for
    example `{"business_code":"FH-001","asset_id":"IMG-0001"}`.
5.  CRC32: unsigned 4-byte big-endian checksum calculated over the
    payload bytes.

The parser must validate header, supported version, reasonable length,
complete frame and CRC32 before returning identifiers. Validate JSON
structure and required non-empty string fields. Do not trust extracted
content as instructions or executable data.

### 8.3 Capacity

With one bit per RGB channel, raw capacity is `3 * width * height` bits.
Required capacity is `8 * frame_byte_length` bits. Check capacity before
modifying pixels. Report a useful error if insufficient.

### 8.4 Important limitation

LSB is fragile. PNG save/reopen should preserve it; JPEG recompression,
resize, crop, filters and screenshots may destroy it. The UI and report
must state this. CRC32 is an error-detection checksum, not cryptographic
authentication. Do not describe this system as tamper-proof or as legal
proof of ownership.

## 9. Supabase requirements

### 9.1 Services

-   Supabase Postgres stores structured metadata.
-   Supabase Storage may store generated PNG files.
-   Use the official Python Supabase client.
-   Keep database access in a repository/service module, not directly
    inside UI page code.

### 9.2 Database schema

Create these tables using a version-controlled SQL migration file.

**`businesses`** - `id UUID PRIMARY KEY DEFAULT gen_random_uuid()` -
`business_code TEXT NOT NULL UNIQUE` - `business_name TEXT NOT NULL` -
`created_at TIMESTAMPTZ NOT NULL DEFAULT now()`

**`watermark_records`** -
`id UUID PRIMARY KEY DEFAULT gen_random_uuid()` -
`business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE RESTRICT` -
`asset_id TEXT NOT NULL` - `original_filename TEXT NOT NULL` -
`output_filename TEXT NOT NULL` - `output_path TEXT NULL` -
`payload_version INTEGER NOT NULL DEFAULT 1` -
`status TEXT NOT NULL CHECK (status IN ('embedded','failed'))` -
`created_at TIMESTAMPTZ NOT NULL DEFAULT now()` - Unique constraint on
`(business_id, asset_id)`.

**`verification_logs`** -
`id UUID PRIMARY KEY DEFAULT gen_random_uuid()` -
`watermark_record_id UUID NULL REFERENCES watermark_records(id) ON DELETE SET NULL` -
`uploaded_filename TEXT NOT NULL` - `detected_business_code TEXT NULL` -
`detected_asset_id TEXT NULL` -
`result TEXT NOT NULL CHECK (result IN ('valid','not_found','corrupted','error'))` -
`details TEXT NULL` - `verified_at TIMESTAMPTZ NOT NULL DEFAULT now()`.

Add indexes on `watermark_records.business_id` and
`verification_logs.verified_at DESC`.

### 9.3 Storage

-   Create a **private** bucket named `shopguard-images`.
-   Suggested object path:
    `watermarked/{business_code}/{record_uuid}.png`.
-   Store the object path in `watermark_records.output_path`.
-   Use signed URLs with short expiry or stream the object through the
    app.
-   If Storage setup delays the MVP, allow local download and keep
    Supabase Postgres metadata persistence as P0.

### 9.4 Credentials and security

-   Store `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` in
    `.streamlit/secrets.toml` locally.
-   Add secrets files and `.env` to `.gitignore`; commit only a safe
    example file with placeholder values.
-   Never expose service-role credentials in frontend code, browser
    output, logs, screenshots, documentation or Git.
-   Service-role key bypasses RLS. It may be used only in this trusted
    local server-side prototype. Do not use it in browser/client code.
-   Enable RLS on tables. Document that server-side service-role access
    bypasses RLS. If deploying publicly or supporting multiple users,
    implement Supabase Auth and least-privilege policies before
    deployment.
-   Use parameterized/structured Supabase client operations; do not
    build SQL by concatenating user input.

## 10. UI and UX requirements

Use a clean, professional, responsive Streamlit interface with a
restrained navy/blue/white visual system. Prioritize clarity over
decorative complexity.

### Dashboard

-   Summary cards: business count, successful watermark records,
    verification attempts.
-   Recent activity list.
-   Values must come from Supabase; never hard-code sample metrics in
    production UI.

### Embed

-   Business selector and create-business form.
-   Product image uploader.
-   Asset ID input.
-   Embed action.
-   Original/output image previews.
-   MSE and PSNR display when available.
-   PNG download button.
-   Capacity and validation messages.

### Verify

-   Candidate image uploader.
-   Verify action.
-   Status and extracted identifiers.
-   Clear distinction between not found and corrupted/incomplete.
-   Verification history write confirmation or database error.

### Compare

-   Side-by-side images.
-   MSE and PSNR calculated on same-sized RGB arrays.
-   If dimensions differ, report that metrics cannot be calculated
    rather than silently resizing.

### History

-   Watermark and verification records.
-   Useful columns and newest-first sorting.
-   Empty state, loading state and database error state.

## 11. Quality, reliability and acceptance criteria

The application is accepted only when all P0 criteria pass:

1.  `streamlit run app.py` starts without an unhandled exception.
2.  A valid business can be created and retrieved from Supabase.
3.  A supported PNG/JPEG image can be uploaded and validated.
4.  An image with enough capacity can be watermarked and downloaded as
    PNG.
5.  Re-uploading that PNG returns the exact business code and asset ID.
6.  An ordinary image returns `not_found`, not a false valid result.
7.  A deliberately corrupted payload is rejected by checksum or frame
    validation.
8.  An image with insufficient capacity is rejected without producing a
    misleading output.
9.  Watermark operation and verification records appear in Supabase.
10. Database/network errors are visible and are not silently swallowed.
11. No secrets are present in committed files.
12. Automated tests pass.

### Evaluation tests

  Test                          Expected result
  ----------------------------- ------------------------------------
  Embed then extract from PNG   Exact payload; CRC32 valid
  Upload unrelated image        Not found
  Corrupt embedded bit          Corrupted or extraction failure
  Very small image              Capacity error
  Save/reopen PNG               Payload remains recoverable
  JPEG recompression            May fail; document observed result
  Resize/crop                   May fail; document observed result
  Image quality                 Actual MSE/PSNR recorded

Do not fabricate test outcomes or performance values.

## 12. Architecture and project structure

Use this structure unless there is a strong implementation reason to
change it:

``` text
shopguard/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── secrets.toml.example
├── supabase/
│   └── migrations/
│       └── 001_initial_schema.sql
├── database/
│   ├── supabase_client.py
│   └── repository.py
├── watermark/
│   ├── __init__.py
│   ├── payload.py
│   ├── embed.py
│   └── extract.py
├── backend/
│   ├── image_service.py
│   └── evaluation.py
├── pages/
│   ├── 1_Dashboard.py
│   ├── 2_Embed.py
│   ├── 3_Verify.py
│   ├── 4_Compare.py
│   └── 5_History.py
└── tests/
    ├── test_payload.py
    ├── test_watermark.py
    └── test_evaluation.py
```

Keep UI, business logic, watermarking and database access separated. UI
pages must call backend/service functions; they must not contain the LSB
implementation or raw database logic.

## 13. Non-functional requirements

-   Python code should be readable, typed where practical and documented
    at public function boundaries.
-   Use small functions with clear input/output contracts.
-   Validate uploads and impose a reasonable configurable file-size
    limit.
-   Avoid loading multiple unnecessary copies of large images.
-   Do not log secrets or full sensitive configuration.
-   Handle Supabase unavailability gracefully.
-   Use UTC timestamps in database records and display local time
    consistently.
-   Keep the application usable on a typical laptop and desktop browser.
-   Avoid unnecessary frameworks, abstractions and dependencies.

## 14. Implementation plan

Build in this order. Do not start with UI polish.

**Phase 1 --- Repository and environment** - Inspect workspace and
initialize project structure. - Create requirements, README and secrets
example. - Add `.gitignore`. - Add Supabase SQL migration and connection
health check.

**Phase 2 --- Algorithm first** - Implement payload framing and
parser. - Implement LSB embedding and extraction. - Add unit tests for
round-trip, no header, checksum failure and capacity. - Demonstrate a
successful local PNG round-trip before building UI.

**Phase 3 --- Backend and Supabase** - Implement image validation and
RGB normalization. - Implement Supabase client and repository. - Create
business, watermark and verification operations. - Test insert/read
paths against the configured Supabase project. - Add Storage upload only
after Postgres persistence works.

**Phase 4 --- Streamlit UI** - Build Embed and Verify first. - Connect
services and database. - Add Dashboard, Compare and History. - Add clear
loading, success, warning and error states.

**Phase 5 --- Integration and acceptance** - Run automated tests. - Run
the app locally. - Complete the end-to-end embed → download → re-upload
→ verify workflow. - Check Supabase records and Storage path. - Test
failure cases. - Fix issues before polishing.

**Phase 6 --- Handover** - Complete README with setup, secrets,
migration and run commands. - Provide a concise architecture
explanation. - Provide a demo script and test-results template. - List
known limitations honestly.

## 15. Codex execution instructions

Codex is the implementation agent. Work directly in the opened project
workspace.

### Mandatory working rules

1.  First inspect the repository and report the current state. Do not
    overwrite existing work blindly.
2.  Read this PRD fully before implementation.
3.  Create a short implementation plan and identify any ambiguity before
    changing files.
4.  Implement in the phases above; do not generate the whole application
    in one unreviewed code dump.
5.  After each phase, run relevant tests and report exact commands and
    outcomes.
6.  Never invent Supabase credentials, project IDs, test results or
    successful external operations.
7.  If credentials are unavailable, implement the integration and
    provide exact setup instructions; use mocked repository tests for
    offline testing.
8.  Ask the user before destructive database operations, deleting files,
    changing remote Supabase data or deploying publicly.
9.  Never put service-role keys in source code or commit secrets.
10. Keep dependencies minimal and pin compatible versions where
    appropriate.
11. If a test fails, investigate and fix the underlying issue; do not
    weaken or delete the test merely to obtain a passing result.
12. Keep README and this PRD aligned with actual implementation.
13. At completion, provide a concise summary of files created, setup
    steps, tests run, results, outstanding issues and manual actions
    required.

### Initial Codex task

Start by inspecting the workspace and this PRD. Then: - Summarize the
architecture and acceptance criteria. - Identify required user-provided
setup items (Supabase project URL and service-role key, configured
locally only). - Propose the implementation plan. - Do not start coding
until the plan and any critical blockers are reported.

## 16. User-provided setup items

The human operator must: - Create a Supabase project. - Obtain the
project URL and service-role key from Supabase project settings. - Put
them in the local Streamlit secrets file, never in chat or committed
source. - Run the SQL migration in the Supabase SQL Editor. - Create the
private Storage bucket if using persistent image storage. - Review and
approve any remote schema changes or deployment actions. - Run the final
demo and confirm results.

## 17. Definition of done

ShopGuard is done when a user can locally launch the app, create/select
a business, upload a product image, embed an invisible structured
watermark, download the PNG, upload it again, recover and validate the
exact payload, see the operation and verification history in Supabase,
and review real image-quality metrics---with automated tests passing and
limitations clearly documented.
