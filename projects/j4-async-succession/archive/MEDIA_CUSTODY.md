# Media custody, rights and completeness — J4

The GitHub repository is **public** and explicitly keeps rendered video/audio, user refs and personal footage out of Git. This document accounts for the actual uploads without silently publishing sensitive originals.

| Raw file | Bytes | SHA-256 | Repo media upload |
| --- | ---: | --- | --- |
| IMG_7835.mp4 | 36071278 | 2bafa5fe49906c07d7c362de42924b0ba57f71b43c9257bc78512a8c4508e698 | EXTERNAL_ONLY |
| IMG_7836.mp4 | 8882046 | a743ab5b79ce40413e9111346211f3ab8c912160bc989a461d2951b3215d83ef | EXTERNAL_ONLY |
| IMG_7876.mp4 | 17788016 | 8fd10c2e692fea97b6d79530be9972790cc2e280d1ffcdca4dec0ad2ec04b97d | EXTERNAL_ONLY |
| IMG_7870.jpeg | 332874 | 3cc06d6e55eeb086fd6cc8aae1c85b0d4e33975cd30d3f3a2573559e7c844798 | EXTERNAL_ONLY |
| IMG_7899.jpeg | 242787 | 42defe3b9dbbf101170a761c2c1ad18c7a58e03fbec259bfecff84ad9d8268d1 | EXTERNAL_ONLY |

## Complete available local handoff

Locally created: \`j4_factory_handoff_20261122/j4_all_available_resources_lossless.zip\`. It retains **267** available mounted files, including version folders v2.6–v4.0, auxiliary code, screenshot evidence, original five uploads and existing ZIP releases; the bundle has passed ZIP CRC checking. ZIP byte size: **76,407,296**. ZIP SHA-256: \`4efe79aa309c193382a82e6c4c56654881df5dbba66df7cfc45df84f0ca3011e\`.

This local archive has not been uploaded to GitHub and is not independently persisted in an object store. The user must download or place it in private persistent storage. The repository references it only by digest to avoid falsely claiming preservation. Future upload should use a **private, access-controlled, encrypted asset store** with object versioning and retention before pointing the registry at persistent URIs. No provider-specific address is invented.

The archive manifest tracks original sizes and SHA-256, plus whether each source is text/code or restricted media. Do not upload user-identifiable footage or third-party copyrighted reference imagery into a public repository without a separate rights review.

## Public Git text coverage

- \`archive/v2_6/\` includes eight individual source-derived text artifacts (canonical prompts, shot and sound IR, QA/provenance).
- \`archive/v2_7/\` through \`archive/v4_0/\` include 14 JSON text archives with the final surfaced file contents for each version.
- The 15-version set currently contains **132 restored text-file slots**. The JSON text archives include filename and conversation-file references; use \`studio_factory.archive\` to restore them as individual files.
- This is not a verbatim reproduction of every intermediate revision or every user/assistant message. See \`conversation_attachment_index.json\` for every surfaced file record, including older revisions.

## Explicit outstanding gaps

1. Full verbatim transcript export of the entire ChatGPT conversation — **NOT_AVAILABLE**. Standardized v2.6 prompt book is **not** a replacement for exact turns.
2. Earlier same-named intermediate generated text versions — indexed, not all independently archived on Git.
3. Build helpers and other unsurfaced generated source files — in the offline handoff but not yet individually published to Git.
4. Original videos, photos, generated screenshots, and historical ZIPs — held in the offline handoff, **not** uploaded to this public GitHub repository.
5. Persistent external storage URI, licence/consent records and encrypted access policy — **NOT_CONFIGURED**.
6. Original legacy \`pipeline/build_animatic.py\` input schema — **NOT_TESTED**; cannot promise adapter compatibility.

No task is complete solely because an index exists: status remains \`PARTIAL_ARCHIVED\` until every required original has a verified durable URI, a matching digest, and a rights disposition.
