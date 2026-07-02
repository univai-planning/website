---
name: edit-notebook
description: Atomic tools for reading and editing Jupyter notebook cells in Univ.AI content.
---

# Edit Notebook Cells

Use `_scripts/notebook_tools.py` instead of inline JSON rewrites when inspecting
or editing notebooks.

## Commands

```bash
python3 _scripts/notebook_tools.py list <notebook> [--type code|markdown|raw] [--lines N]
python3 _scripts/notebook_tools.py read <notebook> <cell_index>
python3 _scripts/notebook_tools.py find <notebook> <pattern> [--type code|markdown|raw] [-C N] [-i]
python3 _scripts/notebook_tools.py edit <notebook> <cell_index> --old OLD --new NEW [--replace-all]
python3 _scripts/notebook_tools.py replace <notebook> <cell_index> --source SOURCE [--type code|markdown|raw]
python3 _scripts/notebook_tools.py add <notebook> <cell_index> --position above|below --type code|markdown|raw --source SOURCE
python3 _scripts/notebook_tools.py delete <notebook> <cell_index> [<cell_index2> ...]
```

## Rules

- Read or list cells before editing.
- Re-run `list` after adding or deleting cells because indices shift.
- Use `edit` for targeted string replacements and `replace` only when the full
  cell source is known.
- For multi-line replacements, prefer a temp file or careful shell quoting over
  ad hoc Python.
- After edits, validate JSON:

  ```bash
  python3 -m json.tool <notebook> >/dev/null
  ```

## Notes

- PEP 723 injection inserts a cell at index 1, shifting later indices.
- For pymc3 ports, pair this skill with `port-pymc3`.
