#!/usr/bin/env python3
"""
Create a 2-up booklet-imposed PDF suitable for duplex printing (long-edge flip).

Usage:
    python3 pdf_to_book.py input.pdf output.pdf [--mode side|stack] [--signature int_number]

e.g.:  python3 pdf_to_book.py   "../book.pdf"   "../book_sig40_side.pdf"   --mode side --signature 40

This script:
 - Pads the input PDF to a multiple of 4 pages by adding blank pages.
 - Reorders pages into booklet order (4 original pages per A4 sheet).
 - Places two pages per A4 sheet; default is side-by-side (left/right). Use
     `--mode stack` to place pages top/bottom (suitable for books flipped up/down).
 - Produces front/back pages; the back side is rotated 180° for short-edge duplex.

Requires: PyMuPDF (install with `pip install PyMuPDF`)
"""

import sys
import argparse
import fitz  # PyMuPDF


def pad_to_multiple_of_4(doc):
    extra = (4 - (doc.page_count % 4)) % 4
    for _ in range(extra):
        doc.new_page(width=595, height=842)  # A4 portrait blank page


def make_booklet_shortedge(in_path, out_path, mode="side", signature=0):
    src = fitz.open(in_path)
    total_pages = src.page_count

    out = fitz.open()

    def impose_segment(start_idx, seg_count):
        # seg_count: number of pages in this segment (before padding)
        # pad to multiple of 4 locally
        padded = seg_count
        extra = (4 - (padded % 4)) % 4
        padded += extra

        if mode == "side":
            A4_w, A4_h = 842, 595
            first_rect = fitz.Rect(0, 0, A4_w / 2, A4_h)
            second_rect = fitz.Rect(A4_w / 2, 0, A4_w, A4_h)
        else:
            A4_w, A4_h = 595, 842
            first_rect = fitz.Rect(0, 0, A4_w, A4_h / 2)
            second_rect = fitz.Rect(0, A4_h / 2, A4_w, A4_h)

        sheets = padded // 4

        for k in range(sheets):
            # local 1-based page numbers inside the segment
            lp1 = padded - 2 * k
            lp2 = 1 + 2 * k
            lp3 = 2 + 2 * k
            lp4 = padded - 1 - 2 * k

            # convert local to global indices; if local > seg_count, treat as blank
            def global_index(local):
                if local <= seg_count:
                    return start_idx + (local - 1)
                return None

            g1 = global_index(lp1)
            g2 = global_index(lp2)
            g3 = global_index(lp3)
            g4 = global_index(lp4)

            # FRONT
            page = out.new_page(width=A4_w, height=A4_h)
            if g1 is not None:
                page.show_pdf_page(first_rect, src, g1)
            if g2 is not None:
                page.show_pdf_page(second_rect, src, g2)

            # BACK
            page_b = out.new_page(width=A4_w, height=A4_h)
            if mode == "stack":
                # swap halves so after 180° rotation pages align upright
                if g3 is not None:
                    page_b.show_pdf_page(second_rect, src, g3)
                if g4 is not None:
                    page_b.show_pdf_page(first_rect, src, g4)
            else:
                if g3 is not None:
                    page_b.show_pdf_page(first_rect, src, g3)
                if g4 is not None:
                    page_b.show_pdf_page(second_rect, src, g4)

            page_b.set_rotation(180)

    # If signature==0 use the whole book as one segment; otherwise split
    if not signature or signature >= total_pages:
        impose_segment(0, total_pages)
    else:
        start = 0
        remaining = total_pages
        while remaining > 0:
            seg = min(signature, remaining)
            impose_segment(start, seg)
            start += seg
            remaining -= seg

    out.save(out_path)
    out.close()
    src.close()


def main():
    p = argparse.ArgumentParser(description="Create 2-up booklet PDF (short-edge duplex)")
    p.add_argument("input", help="input PDF path")
    p.add_argument("output", help="output PDF path")
    p.add_argument("--mode", choices=("side", "stack"), default="side", help="layout mode: side (left/right) or stack (top/bottom)")
    p.add_argument("--signature", type=int, default=0, help="signature size: group pages into chunks of this many pages (pad each to multiple of 4). 0 => whole book")
    args = p.parse_args()
    try:
        make_booklet_shortedge(args.input, args.output, mode=args.mode, signature=args.signature)
        print(f"Wrote booklet PDF suitable for short-edge duplex: {args.output}")
    except Exception as e:
        print("Error:", e)
        sys.exit(1)


if __name__ == '__main__':
    main()
