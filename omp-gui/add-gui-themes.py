#!/usr/bin/python3
"""Add extra built-in themes to the omp-gui renderer bundle inside app.asar.

Usage: add-gui-themes.py APP_ASAR THEMES_JSON

THEMES_JSON maps a theme id to {label, description, scheme, tokens}. Each theme
must define exactly the token keys of the bundle's THEME_TOKEN_KEYS. Dark themes
are listed after the last upstream dark theme, light themes at the end, so the
picker keeps its dark-then-light order. Any unexpected bundle layout fails the
build instead of shipping an unpatched GUI.
"""

import hashlib
import json
import re
import struct
import sys

BLOCK_SIZE = 4 * 1024 * 1024
RENDERER_DIR = ("out", "renderer", "assets")


def fail(message):
    sys.exit(f"add-gui-themes: {message}")


def read_asar(path):
    with open(path, "rb") as f:
        data = f.read()
    # Chromium pickles: a uint32 size pickle, then the header pickle holding one string.
    header_size = struct.unpack_from("<I", data, 4)[0]
    json_size = struct.unpack_from("<i", data, 12)[0]
    header = json.loads(data[16 : 16 + json_size])
    return header, data[8 + header_size :]


def write_asar(path, header, payload):
    header_json = json.dumps(header, separators=(",", ":"), ensure_ascii=False).encode()
    padding = (-len(header_json)) % 4
    header_pickle = (
        struct.pack("<Ii", 4 + len(header_json) + padding, len(header_json))
        + header_json
        + b"\0" * padding
    )
    with open(path, "wb") as f:
        f.write(struct.pack("<II", 4, len(header_pickle)))
        f.write(header_pickle)
        f.write(payload)


def integrity(content):
    blocks = [
        hashlib.sha256(content[i : i + BLOCK_SIZE]).hexdigest()
        for i in range(0, max(len(content), 1), BLOCK_SIZE)
    ]
    return {
        "algorithm": "SHA256",
        "hash": hashlib.sha256(content).hexdigest(),
        "blockSize": BLOCK_SIZE,
        "blocks": blocks,
    }


def find_bundle(header, payload):
    node = header
    for part in RENDERER_DIR:
        node = node.get("files", {}).get(part)
        if node is None:
            fail(f"missing {'/'.join(RENDERER_DIR)} in app.asar")
    matches = []
    for name, entry in node["files"].items():
        if not re.fullmatch(r"index-[\w-]+\.js", name) or "offset" not in entry:
            continue
        start = int(entry["offset"])
        source = payload[start : start + entry["size"]].decode()
        if "\nconst THEMES = {\n" in source:
            matches.append((entry, source))
    if len(matches) != 1:
        fail(f"expected one renderer bundle defining THEMES, found {len(matches)}")
    return matches[0]


def theme_schemes(source, names):
    schemes = {}
    for name in names:
        match = re.search(
            rf"\nconst {name} = \{{\n  label: [^\n]+\n  description: [^\n]+\n  scheme: \"(dark|light)\",\n",
            source,
        )
        if not match:
            fail(f"cannot read the scheme of upstream theme {name!r}")
        schemes[name] = match.group(1)
    return schemes


def patch_source(source, themes):
    keys_match = re.search(r"\nconst THEME_TOKEN_KEYS = \[\n(.*?)\n\];\n", source, re.S)
    if not keys_match:
        fail("THEME_TOKEN_KEYS not found")
    token_keys = re.findall(r'"(--omp-[a-z0-9-]+)"', keys_match.group(1))
    if not token_keys:
        fail("THEME_TOKEN_KEYS is empty")

    block = re.search(r"\nconst THEMES = \{\n((?:  \w+,?\n)+)\};\n", source)
    if not block:
        fail("THEMES literal has an unexpected shape")
    names = re.findall(r"\w+", block.group(1))
    already = [theme_id for theme_id in themes if theme_id in names]
    if already:
        fail(f"themes already present in the bundle: {already}")
    schemes = theme_schemes(source, names)
    anchor = names[-1]

    definitions = []
    for theme_id, theme in themes.items():
        if not re.fullmatch(r"[a-zA-Z]\w*", theme_id):
            fail(f"theme id {theme_id!r} is not a valid identifier")
        if theme_id in names or re.search(rf"\b(const|let|var|function|class) {theme_id}\b", source):
            fail(f"theme id {theme_id!r} already exists in the bundle")
        if theme.get("scheme") not in ("dark", "light"):
            fail(f"theme {theme_id!r} needs scheme dark or light")
        tokens = theme.get("tokens", {})
        missing = [key for key in token_keys if key not in tokens]
        extra = [key for key in tokens if key not in token_keys]
        if missing or extra:
            fail(f"theme {theme_id!r} tokens mismatch: missing {missing}, unknown {extra}")
        entry = {
            "label": theme["label"],
            "description": theme["description"],
            "scheme": theme["scheme"],
            "tokens": {key: tokens[key] for key in token_keys},
        }
        definitions.append(f"const {theme_id} = {json.dumps(entry, indent=2, ensure_ascii=False)};\n")
        if theme["scheme"] == "dark":
            last_dark = max((i for i, n in enumerate(names) if schemes.get(n) == "dark"), default=-1)
            names.insert(last_dark + 1, theme_id)
        else:
            names.append(theme_id)
        schemes[theme_id] = theme["scheme"]

    new_block = "\n" + "".join(definitions) + "const THEMES = {\n" + ",\n".join(f"  {n}" for n in names) + "\n};\n"
    source = source[: block.start()] + new_block + source[block.end() :]
    return add_picker_strings(source, themes, anchor)


def add_picker_strings(source, themes, anchor):
    """The theme picker shows themePicker.theme.<id>.* strings from every locale table."""
    strings = "".join(
        f"  {json.dumps(f'themePicker.theme.{theme_id}.{field}')}: {json.dumps(theme[field], ensure_ascii=False)},\n"
        for theme_id, theme in themes.items()
        for field in ("label", "description")
    )
    pattern = re.compile(rf'\n  "themePicker\.theme\.{anchor}\.description": "(?:[^"\\\n]|\\.)*",\n')
    source, count = pattern.subn(lambda m: m.group(0) + strings, source)
    if count == 0:
        fail(f"no locale table defines themePicker.theme.{anchor}.description")
    return source


def main():
    if len(sys.argv) != 3:
        fail("usage: add-gui-themes.py APP_ASAR THEMES_JSON")
    asar_path, themes_path = sys.argv[1:]
    with open(themes_path, encoding="utf-8") as f:
        themes = json.load(f)

    header, payload = read_asar(asar_path)
    entry, source = find_bundle(header, payload)
    patched = patch_source(source, themes).encode()

    # Append the patched bundle; the original bytes stay as unreferenced padding.
    entry["offset"] = str(len(payload))
    entry["size"] = len(patched)
    if "integrity" in entry:
        entry["integrity"] = integrity(patched)
    write_asar(asar_path, header, payload + patched)
    print(f"add-gui-themes: added {', '.join(themes)}")


if __name__ == "__main__":
    main()
