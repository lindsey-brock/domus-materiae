#!/usr/bin/env python3
"""Wrap the artifact source (page content only) into a complete HTML document.

The Artifact runtime supplies <!doctype>, <head> and the reset at publish time, so
the source deliberately has none. Served raw, that means quirks mode - which breaks
svh units and changes compositing. This reproduces the wrapper for local use."""
import io, sys

SRC = "domus-materiae-style-guide.artifact.html"
OUT = "domus-materiae-style-guide.html"

s = io.open(SRC, encoding="utf-8").read()
cut = s.index("</style>") + len("</style>")
head, body = s[:cut], s[cut:]

doc = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  :root{{color-scheme:light dark}}
  body{{margin:0}}
  img{{max-width:100%}}
  [hidden]{{display:none!important}}
</style>
{head}
</head>
<body>
{body.lstrip()}
</body>
</html>
"""
io.open(OUT, "w", encoding="utf-8").write(doc)
print(f"{OUT}: {len(doc)} bytes")
