# From J4 to a second production without copying J4

Create a new project \`another-short-film\` while retaining the same curated shared art reference. A project's scenes, character identity, prompt choice, render budget and approvals must **never** carry over implicitly.

\`\`\`python
from studio_factory import Factory
from studio_factory.managers import manager
f=Factory(".factory/registry.sqlite3")
f.create_project("j4-async-succession")
f.create_project("another-short-film")
ref=manager("research", f).publish(
    "shared", "optical-position-reference", "sources/museum-article.md",
    {"source":"https://museum.example/reference","rights":"research-and-method-only"})
shot=manager("shot",f).publish(
    "projects/another-short-film", "opening", "shots/shot-001.json",
    {"duration_ms":3000,"visual_reference":ref})
f.reference(shot, ref, "inspired_by_method")
handoff=manager("shot",f).send(
    "another-short-film","sound",shot,"shot-opening-sound-v1",
    {"shot_digest":f.get(shot)["digest"]})
manager("sound",f).receive(handoff)
assert f.export_manifest("another-short-film")["project"]=="another-short-film"
f.close()
\`\`\`

A change in the **shared** source is a new immutable version, not an unreviewed mutation propagated to every film. Each production decides when to update its references.

Artifact provenance hierarchy:
\`source_uri → observed_source_hash → interpretation/method → prompt_revision → shot_revision → generation_id → selected_take → QC evidence → delivery receipt\`.

Maintain a separate ledger for every real generation. Reusing a reference never transfers a model license, person's likeness permission, contest eligibility or generated-output usage rights.
