#!/usr/bin/env python3
"""Unpack a .docx file into a directory, pretty-printing XML files."""
import argparse
import os
import shutil
import zipfile
import xml.dom.minidom


def unpack(docx_path: str, output_dir: str, merge_runs: bool = True) -> None:
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    with zipfile.ZipFile(docx_path, "r") as z:
        z.extractall(output_dir)

    # Pretty-print all XML files
    for root, dirs, files in os.walk(output_dir):
        for fname in files:
            if fname.endswith(".xml") or fname.endswith(".rels"):
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        content = f.read()
                    dom = xml.dom.minidom.parseString(content.encode("utf-8"))
                    pretty = dom.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")
                    # Remove the extra XML declaration added by toprettyxml
                    lines = pretty.split("\n")
                    if lines[0].startswith("<?xml"):
                        lines = lines[1:]
                    pretty = "\n".join(lines)
                    with open(fpath, "w", encoding="utf-8") as f:
                        f.write(pretty)
                except Exception:
                    pass  # Leave binary/non-XML files as-is

    print(f"Unpacked to: {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("docx_path")
    parser.add_argument("output_dir")
    parser.add_argument("--merge-runs", default="true")
    args = parser.parse_args()
    unpack(args.docx_path, args.output_dir, args.merge_runs.lower() != "false")
