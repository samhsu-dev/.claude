#!/usr/bin/env node
// Mechanical checks over rendered prompt text. Emits JSON on stdout, never throws.
// Usage: scan.mjs <rendered.txt> [more.txt ...] [--corpus <path>] [--budget <n>]

import { readFileSync } from "node:fs";

const STOP = new Set(
  ("a an the and or of to in on is are it its that this you your with as at by for not no be" +
    " been from than then so one there their they we our what which when where how all any")
    .split(" "),
);
const EMPHASIS = /\b(CRITICAL|IMPORTANT|MUST|ALWAYS|NEVER|REQUIRED|MANDATORY)\b/g;
const GRAM = 4;

function contentWords(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9 ]/g, " ")
    .split(/\s+/)
    .filter((w) => w && !STOP.has(w));
}

// A section header is a short line with no terminal punctuation, preceded by a blank line.
function sections(lines) {
  const found = [];
  lines.forEach((line, i) => {
    const t = line.trim();
    if (!t || t.length > 60 || /[.:,;?]$/.test(t) || t.startsWith("-")) return;
    if (i > 0 && lines[i - 1].trim() !== "") return;
    if (t.split(/\s+/).length > 7) return;
    found.push({ title: t, line: i + 1 });
  });
  return found.map((s, i) => ({
    ...s,
    words: lines
      .slice(s.line, found[i + 1] ? found[i + 1].line - 1 : lines.length)
      .join(" ")
      .split(/\s+/)
      .filter(Boolean).length,
  }));
}

function repeatedGrams(lines) {
  const seen = new Map();
  lines.forEach((line, i) => {
    const w = contentWords(line);
    for (let k = 0; k + GRAM <= w.length; k++) {
      const g = w.slice(k, k + GRAM).join(" ");
      const at = seen.get(g) ?? [];
      if (at[at.length - 1] !== i + 1) at.push(i + 1);
      seen.set(g, at);
    }
  });
  return [...seen]
    .filter(([, at]) => at.length > 1)
    .map(([gram, at]) => ({ gram, lines: at }));
}

// Tokens that could bind an example to a specific corpus row: paths, dotted filenames,
// and file:line references.
function concreteTokens(text) {
  const pats = [
    /\b[\w./-]+\.(?:ts|tsx|js|jsx|py|go|rb|php|java|yml|yaml|json|env|md|sql|sh)\b(?::\d+(?:-\d+)?)?/g,
    /\b(?:Dockerfile|docker-compose)[\w.-]*/g,
    /\b[\w-]+\/[\w./-]+\b/g,
  ];
  const hits = new Map();
  for (const p of pats) {
    for (const m of text.matchAll(p)) {
      const tok = m[0];
      if (tok.length < 4) continue;
      hits.set(tok, (hits.get(tok) ?? 0) + 1);
    }
  }
  return [...hits].map(([token, count]) => ({ token, count }));
}

function corpusHits(tokens, corpusPath) {
  let corpus;
  try {
    corpus = readFileSync(corpusPath, "utf8");
  } catch (err) {
    return { error: `corpus unreadable: ${err.message}` };
  }
  return {
    path: corpusPath,
    tokens: tokens.map(({ token }) => ({
      token,
      corpusOccurrences: corpus.split(token).length - 1,
    })),
  };
}

// Proxy for the ~20-instruction attention budget: one directive per bullet or standalone rule
// line. Example bodies are demonstrations of rules already counted, so they are excluded.
function directiveCount(lines, secs) {
  const exampleRanges = secs
    .filter((s) => /example/i.test(s.title))
    .map((s) => [s.line, s.line + s.words]);
  let n = 0;
  let inExamples = false;
  lines.forEach((line, i) => {
    const t = line.trim();
    if (/^<\/?examples?>/.test(t)) inExamples = /^<examples>/.test(t);
    if (inExamples || exampleRanges.some(([a]) => i + 1 === a)) return;
    if (!t || t.startsWith("<")) return;
    if (secs.some((s) => s.line === i + 1)) return;
    n += 1;
  });
  return n;
}

function scan(path, opts) {
  let text;
  try {
    text = readFileSync(path, "utf8");
  } catch (err) {
    return { file: path, error: err.message };
  }
  const lines = text.split("\n");
  const tokens = concreteTokens(text);
  const secs = sections(lines);
  const directives = directiveCount(lines, secs);
  const out = {
    file: path,
    size: {
      chars: text.length,
      words: text.split(/\s+/).filter(Boolean).length,
      lines: lines.length,
    },
    sections: secs,
    directiveCount: directives,
    directiveBudget: opts.budget,
    overBudget: directives > opts.budget,
    repeatedGrams: repeatedGrams(lines),
    emphasisWords: [...text.matchAll(EMPHASIS)].map((m) => m[0]),
    concreteTokens: tokens,
  };
  if (opts.corpus) out.corpusLeakage = corpusHits(tokens, opts.corpus);
  return out;
}

function main() {
  const argv = process.argv.slice(2);
  const files = [];
  const opts = { corpus: null, budget: 20 };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === "--corpus") opts.corpus = argv[++i];
    else if (argv[i] === "--budget") opts.budget = Number(argv[++i]) || 20;
    else files.push(argv[i]);
  }
  if (files.length === 0) {
    process.stdout.write(
      JSON.stringify({ error: "usage: scan.mjs <rendered.txt> [--corpus p] [--budget n]" }),
    );
    return;
  }
  process.stdout.write(JSON.stringify(files.map((f) => scan(f, opts)), null, 2));
}

main();
