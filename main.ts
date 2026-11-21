// Front-page copier: the Friday 20 November 2026 newspaper image.
//
// The rendered page ships in this repository as entry.png. This program
// carries that exact file into the grading output directory, byte for
// byte, and checks the copy before it reports success. Node 22,
// standard library only. No network, no downloads, no extra files.
//
// Run it from the repository root with an output directory ready:
//   mkdir -p out && node main.ts
// The output directory comes from the environment variable named below
// and falls back to /output when that variable is unset. The program
// runs twice in grading; both runs write identical bytes because the
// source file never changes between runs. The summary line it prints
// carries the copied size, both pixel sides, and the SHA-256 hash.

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// ---------------------------------------------------------------------------
// Named constants: every literal the copier depends on lives in one place.
// ---------------------------------------------------------------------------

const PAGE_NAME = "entry.png";
const FALLBACK_OUTPUT_DIR = "/output";
const OUTPUT_ENV_KEY = "MAKEFUN_OUTPUT_DIR";
const REPO_ROOT_MARKER = "main.ts";
const MAX_PAGE_BYTES = 1048576;
const MAX_PAGE_SIDE = 1024;
const PNG_MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

// ---------------------------------------------------------------------------
// Small helpers, each carrying its answer in one named variable.
// ---------------------------------------------------------------------------

function sha256HexOf(filePath: string): string {
  const pageBytes = readFileSync(filePath);
  const hasher = createHash("sha256");
  hasher.update(pageBytes);
  const digest = hasher.digest("hex");
  return digest;
}

function envOutputDir(): string {
  const rawValue = process.env[OUTPUT_ENV_KEY];
  const trimmedValue = rawValue === undefined ? "" : rawValue.trim();
  const pickedDir = trimmedValue.length > 0 ? trimmedValue : FALLBACK_OUTPUT_DIR;
  return pickedDir;
}

function repoRootDir(): string {
  const hereFile = fileURLToPath(import.meta.url);
  const hereDir = dirname(hereFile);
  const rootDir = resolve(hereDir);
  return rootDir;
}

function firstExistingPath(candidates: string[]): string {
  let foundPath = "";
  for (const candidate of candidates) {
    const candidateExists = existsSync(candidate);
    const stillEmpty = foundPath.length === 0;
    if (candidateExists && stillEmpty) {
      foundPath = candidate;
    }
  }
  return foundPath;
}

function sourcePagePath(rootDir: string): string {
  const besideEntrypoint = join(rootDir, PAGE_NAME);
  const fromWorkingDir = join(process.cwd(), PAGE_NAME);
  const fromBotMount = join("/bot", PAGE_NAME);
  const candidates = [besideEntrypoint, fromWorkingDir, fromBotMount];
  const pickedPath = firstExistingPath(candidates);
  return pickedPath;
}

function pngSignatureOk(filePath: string): boolean {
  const headBytes = readFileSync(filePath);
  let magicOk = headBytes.length >= 8;
  for (let index = 0; index < PNG_MAGIC.length; index += 1) {
    const byteMatches = headBytes[index] === PNG_MAGIC[index];
    magicOk = magicOk && byteMatches;
  }
  return magicOk;
}

function readPngSides(filePath: string): { width: number; height: number } {
  const headBytes = readFileSync(filePath);
  const widthValue =
    headBytes[16] * 16777216 + headBytes[17] * 65536 + headBytes[18] * 256 + headBytes[19];
  const heightValue =
    headBytes[20] * 16777216 + headBytes[21] * 65536 + headBytes[22] * 256 + headBytes[23];
  const sides = { width: widthValue, height: heightValue };
  return sides;
}

// ---------------------------------------------------------------------------
// Copy step: make the directory, copy, then verify size, bytes and hash.
// ---------------------------------------------------------------------------

function copyAndVerify(sourcePath: string, targetPath: string): { bytes: number; sha256: string } {
  const targetDir = dirname(targetPath);
  mkdirSync(targetDir, { recursive: true });
  copyFileSync(sourcePath, targetPath);
  const sourceStat = statSync(sourcePath);
  const targetStat = statSync(targetPath);
  const sizeMatches = sourceStat.size === targetStat.size;
  const sizeWithinCap = targetStat.size <= MAX_PAGE_BYTES;
  const sourceHash = sha256HexOf(sourcePath);
  const targetHash = sha256HexOf(targetPath);
  const hashMatches = sourceHash === targetHash;
  const checksPass = sizeMatches && sizeWithinCap && hashMatches;
  const failureNote = checksPass
    ? ""
    : `copy check failed: size ${sourceStat.size} vs ${targetStat.size}, hash ${sourceHash} vs ${targetHash}`;
  if (checksPass === false) {
    throw new Error(failureNote);
  }
  const outcome = { bytes: targetStat.size, sha256: targetHash };
  return outcome;
}

// ---------------------------------------------------------------------------
// Main flow: resolve paths, guard the page, copy, report.
// ---------------------------------------------------------------------------

function runCopier(): number {
  const rootDir = repoRootDir();
  const entrypointPath = join(rootDir, REPO_ROOT_MARKER);
  const entrypointPresent = existsSync(entrypointPath);
  const rootNote = entrypointPresent ? rootDir : process.cwd();
  const sourcePath = sourcePagePath(rootNote);
  const sourceFound = sourcePath.length > 0;
  const missingNote = sourceFound ? "" : `page ${PAGE_NAME} not found beside ${REPO_ROOT_MARKER}`;
  if (sourceFound === false) {
    throw new Error(missingNote);
  }
  const signatureOk = pngSignatureOk(sourcePath);
  const signatureNote = signatureOk ? "" : `page ${PAGE_NAME} is not a PNG file`;
  if (signatureOk === false) {
    throw new Error(signatureNote);
  }
  const sides = readPngSides(sourcePath);
  const sidesOk =
    sides.width > 0 && sides.width <= MAX_PAGE_SIDE && sides.height > 0 && sides.height <= MAX_PAGE_SIDE;
  const sidesNote = sidesOk ? "" : `page size ${sides.width}x${sides.height} exceeds ${MAX_PAGE_SIDE}`;
  if (sidesOk === false) {
    throw new Error(sidesNote);
  }
  const outputDir = envOutputDir();
  const targetPath = join(resolve(outputDir), PAGE_NAME);
  const outcome = copyAndVerify(sourcePath, targetPath);
  const reportLine =
    `copied ${PAGE_NAME}: ${outcome.bytes} bytes ${sides.width}x${sides.height} ` +
    `sha256 ${outcome.sha256} -> ${targetPath}`;
  console.log(reportLine);
  const exitCode = 0;
  return exitCode;
}

try { const exitCode = runCopier(); process.exit(exitCode); } catch (caughtErr) {
  const errText = caughtErr instanceof Error ? caughtErr.message : String(caughtErr);
  console.error(`copier failed: ${errText}`);
  process.exit(1);
}
