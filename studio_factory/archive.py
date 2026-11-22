"""Restore archived conversation text files without needing external services.

Archive records preserve exact extracted text, NOT original binary bytes.
The source file IDs and public/restricted classifications remain in manifest.
"""
import argparse
import json
from pathlib import Path

class ArchiveError(ValueError):
    pass

def unpack(source: Path, dest: Path, *, overwrite: bool = False) -> int:
    obj=json.loads(source.read_text(encoding="utf-8"))
    if obj.get("format") not in {"J4_VERSION_TEXT_ARCHIVE","HIGGSFIELD_STUDIO_LOSSLESS_TEXT_REPRESENTATION"}:
        raise ArchiveError("unsupported archive format")
    files=obj.get("files")
    if not isinstance(files,list):
        raise ArchiveError("missing files")
    dest.mkdir(parents=True,exist_ok=True)
    for f in files:
        name=f.get("filename")
        if not isinstance(name,str) or Path(name).name!=name or name in (".",".."):
            raise ArchiveError("unsafe archive entry")
        if not isinstance(f.get("content"),str):
            raise ArchiveError("non-text archive entry")
        target=dest/name
        if target.exists() and not overwrite:
            raise ArchiveError(f"refusing to overwrite {target}")
    for f in files:
        (dest/f["filename"]).write_text(f["content"],encoding="utf-8")
    return len(files)

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("archive",type=Path)
    p.add_argument("output_directory",type=Path)
    p.add_argument("--overwrite",action="store_true")
    args=p.parse_args(argv)
    print(f"restored {unpack(args.archive,args.output_directory,overwrite=args.overwrite)} files")

if __name__=="__main__":
    main()
