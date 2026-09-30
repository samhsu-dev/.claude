#!/usr/bin/env node
/* Pre-highlight code in a rendered HTML page, in place.
 *
 * Rewrites the text of every <code class="language-X"> element, inline or inside
 * <pre>, into span-wrapped tokens. Highlighting happens at render time so the
 * page ships no script and fetches no highlighter.
 *
 * Usage: node highlight.mjs <page.html>...
 */

import { readFileSync, writeFileSync } from 'node:fs';

const KEYWORDS = {
  js: 'await async await break case catch class const continue default delete do else export extends finally for from function if import in instanceof let new of return static super switch this throw try typeof var void while yield',
  ts: 'abstract any as asserts async await boolean break case catch class const continue declare default delete do else enum export extends finally for from function if implements import in instanceof interface keyof let namespace never new number of private protected public readonly return static string super switch this throw try type typeof undefined unknown var void while yield',
  py: 'and as assert async await break class continue def del elif else except finally for from global if import in is lambda none nonlocal not or pass raise return true false try while with yield',
  sh: 'case do done elif else esac fi for function if in then until while export local return source',
};
KEYWORDS.javascript = KEYWORDS.js;
KEYWORDS.typescript = KEYWORDS.ts;
KEYWORDS.python = KEYWORDS.py;
KEYWORDS.bash = KEYWORDS.sh;
KEYWORDS.shell = KEYWORDS.sh;

const LITERALS = new Set(['true', 'false', 'null', 'undefined', 'None', 'True', 'False', 'NaN', 'Infinity']);

function rulesFor(lang) {
  const words = new Set((KEYWORDS[lang] ?? '').split(' ').filter(Boolean));
  const lineComment = lang.startsWith('py') || lang === 'python' || KEYWORDS[lang] === KEYWORDS.sh ? /^#[^\n]*/ : /^\/\/[^\n]*/;
  return [
    ['com', /^\/\*[\s\S]*?\*\//],
    ['com', lineComment],
    ['str', /^(?:"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|`(?:\\.|[^`\\])*`)/],
    ['num', /^(?:0[xX][0-9a-fA-F]+|\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\b/],
    ['dec', /^@[A-Za-z_$][\w$.]*/],
    [
      'word',
      /^[A-Za-z_$][\w$]*/,
      (t) => (words.has(t) || words.has(t.toLowerCase()) ? 'kw' : LITERALS.has(t) ? 'lit' : null),
    ],
    ['pun', /^[{}()[\].,;:?!<>=+\-*/%&|^~]+/],
  ];
}

function escapeHtml(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function decodeHtml(s) {
  return s
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#0?39;/g, "'")
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&');
}

function tokenize(source, lang) {
  const rules = rulesFor(lang);
  let rest = source;
  let out = '';
  let guard = 0;

  while (rest.length > 0) {
    if (++guard > source.length * 4 + 1000) throw new Error('tokenizer failed to advance');

    const ws = /^\s+/.exec(rest);
    if (ws) {
      out += escapeHtml(ws[0]);
      rest = rest.slice(ws[0].length);
      continue;
    }

    let matched = false;
    for (const [cls, re, refine] of rules) {
      const m = re.exec(rest);
      if (!m) continue;
      const text = m[0];
      const finalClass = refine ? refine(text) : cls;
      out += finalClass ? `<span class="tok-${finalClass}">${escapeHtml(text)}</span>` : escapeHtml(text);
      rest = rest.slice(text.length);
      matched = true;
      break;
    }
    if (!matched) {
      out += escapeHtml(rest[0]);
      rest = rest.slice(1);
    }
  }
  return out;
}

const files = process.argv.slice(2);
if (files.length === 0) {
  console.error('usage: highlight.mjs <page.html>...');
  process.exit(1);
}

for (const file of files) {
  const html = readFileSync(file, 'utf8');
  let count = 0;

  const next = html.replace(
    /<code([^>]*\bclass="[^"]*\blanguage-([a-zA-Z]+)\b[^"]*"[^>]*)>([\s\S]*?)<\/code>/g,
    (whole, attrs, lang, body) => {
      if (body.includes('<span class="tok-')) return whole;
      count += 1;
      return `<code${attrs}>${tokenize(decodeHtml(body), lang.toLowerCase())}</code>`;
    },
  );

  writeFileSync(file, next);
  console.log(`${file}: highlighted ${count} block${count === 1 ? '' : 's'}`);
}
