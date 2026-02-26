#!/usr/bin/env python3
"""Repack an unpacked docx directory back into a .docx file."""
import argparse
import os
import zipfile


def pack(input_dir: str, output_path: str, original: str = None) -> None:
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(input_dir):
            for fname in files:
                fpath = os.path.join(root, fname)
                arcname = os.path.relpath(fpath, input_dir)
                # Normalize path separators
                arcname = arcname.replace("\\", "/")
                zf.write(fpath, arcname)
    print(f"Packed to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir")
    parser.add_argument("output_path")
    parser.add_argument("--original", default=None)
    parser.add_argument("--validate", default="true")
    args = parser.parse_args()
    pack(args.input_dir, args.output_path, args.original)
