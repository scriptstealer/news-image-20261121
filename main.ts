// THE WORLD TODAY — 21 November 2026 (round 2 entrypoint).
//
// The front page itself is the PNG sitting next to this file; this program
// only carries it to the grader's output directory. It uses nothing but
// the Node standard library, so it runs in a bare container with no
// packages installed and no network.
//
// Run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const IMAGE_NAME = "entry.png";
const FALLBACK_OUTPUT_DIR = "/output";

function fail(message) {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

// The image lives beside this script, wherever the repo was checked out.
const here = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(here, IMAGE_NAME);

if (!existsSync(sourcePath)) {
  fail(`could not find ${IMAGE_NAME} next to main.ts (${sourcePath})`);
}

const pixels = readFileSync(sourcePath);
if (pixels.length === 0) {
  fail(`${IMAGE_NAME} is empty, refusing to write a blank entry`);
}

// The gate tells PNG from JPEG by the first bytes; make sure the file we
// are about to hand it really is the PNG we drew, not a truncated copy.
const PNG_MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
const looksLikePng = PNG_MAGIC.every((byte, i) => pixels[i] === byte);
if (!looksLikePng) {
  fail(`${IMAGE_NAME} does not start with a PNG signature, refusing to copy it`);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? FALLBACK_OUTPUT_DIR;
mkdirSync(outDir, { recursive: true });

const targetPath = join(outDir, IMAGE_NAME);
writeFileSync(targetPath, pixels);

const written = statSync(targetPath);
if (written.size !== pixels.length) {
  fail(`wrote ${written.size} bytes but the source is ${pixels.length}`);
}

// Read the copy back and compare it byte for byte: the two grader runs
// must produce identical bytes, and a half-written file must fail loudly
// here instead of reaching the judge.
const roundTrip = readFileSync(targetPath);
if (!roundTrip.equals(pixels)) {
  fail(`the copy at ${targetPath} differs from the source image`);
}

console.log(`wrote ${targetPath} (${written.size} bytes)`);
