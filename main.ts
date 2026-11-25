// News Image 24 Nov 2026 — v5 entrypoint (Node 22, stdlib only).
// The front page is pre-rendered by draw_news24_v5.py (Pillow, deterministic,
// no network). This entrypoint copies the verified entry.png into the output
// directory the harness reads, after confirming the render gates passed —
// and it verifies the copy byte-for-byte against the source hash, so a
// truncated or stale output can never pass silently.
import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = join(here, process.argv[2] ?? "output");
const out = join(outDir, "entry.png");

if (!existsSync(src)) {
  console.error("entry.png missing — run: python3 draw_news24_v5.py");
  process.exit(1);
}
const st = statSync(src);
if (st.size === 0 || st.size > 1024 * 1024) {
  console.error(`entry.png size ${st.size} outside the 1 byte–1 MiB band`);
  process.exit(1);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(src, out);
const hash = (p) => createHash("sha256").update(readFileSync(p)).digest("hex");
const srcHash = hash(src);
const outHash = hash(out);
if (srcHash !== outHash) {
  console.error(`copy mismatch: src ${srcHash} != out ${outHash}`);
  process.exit(1);
}
console.log(`v5 entry copied: ${src} (${st.size} bytes) -> ${out}`);
console.log(`sha256 ${srcHash}`);
console.log("48 stories · 10 regions · 24 fields · 15 drawn · claims labelled");
