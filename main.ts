// Entry point for the news-image-20261120 submission, third entry.
//
// The deliverable image is entry.png beside this file: a one-page
// newspaper of Friday 20 November 2026, drawn entirely in code by
// the Python program in this repository (render.py, scenes.py,
// draw.py, data.py). This program's only job is to place those
// exact bytes where the grader expects them: /output/entry.png,
// or MAKEFUN_OUTPUT_DIR/entry.png when that variable is set
// outside the grader's container. Standard library only, no
// network, same bytes on every run.

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const sourceImageUrl = new URL('./entry.png', import.meta.url);
const targetImagePath = join(outputDir, 'entry.png');

const pngSignature = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

const sourcePresent = existsSync(sourceImageUrl);
if (sourcePresent === false) {
  console.error('entry.png missing beside main.ts');
  process.exit(1);
}

const sourceBytes = readFileSync(sourceImageUrl);
const signatureMatches = sourceBytes.subarray(0, 8).equals(pngSignature);
if (signatureMatches === false) {
  console.error('entry.png is not a PNG file');
  process.exit(1);
}

mkdirSync(outputDir, { recursive: true });
copyFileSync(sourceImageUrl, targetImagePath);

const writtenBytes = readFileSync(targetImagePath);
const writtenSignatureMatches = writtenBytes.subarray(0, 8).equals(pngSignature);
if (writtenSignatureMatches === false) {
  console.error('copied entry.png lost its PNG signature');
  process.exit(1);
}

const writtenSize = statSync(targetImagePath).size;
const sizeLimit = 1024 * 1024;
if (writtenSize > sizeLimit) {
  console.error(`entry.png is ${writtenSize} bytes, over the 1048576 byte cap`);
  process.exit(1);
}
console.log(`wrote ${targetImagePath} ${writtenSize} bytes`);
