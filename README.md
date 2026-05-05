PDF → 2-up Booklet
===================

Overview
--------

This repository includes `pdf_to_book.py`, a small utility that rearranges a PDF into
2-up A4 pages (2 original pages per A4 sheet per side, which means 4 original pages in both-side A4 paper) suitable for duplex booklet printing.

Key features:
- Pads the input PDF to a multiple of 4 pages by adding blank A4 pages.
- Reorders pages into booklet order (4 original pages per sheet).
- Places two pages per A4 sheet in either left/right (`side`) or top/bottom (`stack`) layout.
    - Better to choose side, as the stack mode hasn't been tested.
- Supports processing in signatures (chunks) and rotates back pages for short-edge duplex alignment.

Requirements
------------

- Python 3.x
- PyMuPDF (provided in `requirements-pdf-booklet.txt`)

Installation
------------

Install the dependency from the included requirements file:

```bash
pip install -r requirements.txt
```

Usage
-----

Basic usage:

```bash
python3 pdf_to_book.py input.pdf output.pdf
```

Options:
- `--mode side|stack` — layout mode (`side` places pages left/right; `stack` places pages top/bottom). Default: `side`.
- `--signature N` — process the PDF in chunks of `N` pages and pad each chunk to a multiple of 4. `0` (default) treats the whole document as a single segment.

Example
-------

Create a side-by-side booklet with 40-page signatures:

```bash
python3 pdf_to_book.py "../book.pdf" "../book_sig40_side.pdf" --mode side --signature 40
```

How it works (brief)
--------------------

- The script opens the input PDF using PyMuPDF, computes required padding (so every segment is a multiple of 4 pages),
  and then generates A4-sized output pages.
- For each sheet the script places two source pages into predefined rectangles on the A4 canvas and emits
  both a front and a rotated back page so that duplex printing lines up as expected.

Notes & tips
-----------

- The output is sized and arranged for A4 sheets — check your printer's paper size and duplex orientation.
- If page orientation or final print alignment is off, try switching `--mode` between `side` and `stack`.
- The back pages are rotated 180° by design for short-edge duplex printers.

Files
-----

- `pdf_to_book.py` — main script that creates the booklet-imposed PDF.
- `requirements-pdf-booklet.txt` — Python dependency list (PyMuPDF).

License
-------

Add or update a `LICENSE` file in the repository to declare licensing for this project.
