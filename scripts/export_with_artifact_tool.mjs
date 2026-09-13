// Optional Codex authoring/round-trip check. The portable Python build produces
// the same CSV without requiring this package or Node.js.
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { Workbook } from '@oai/artifact-tool';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const matrix = JSON.parse(await fs.readFile(path.join(root, 'data/csv_matrix.json'), 'utf8'));
const wb = Workbook.create();
const sheet = wb.worksheets.add('ヒジャブの出現率');
const range = sheet.getRange(`A1:M${matrix.length}`);
range.values = matrix;
const values = range.values;
if (JSON.stringify(values) !== JSON.stringify(matrix)) throw new Error('Cell round-trip mismatch');
const quote = value => /[",\r\n]/.test(value) ? '"' + value.replaceAll('"','""') + '"' : value;
const csv = '\uFEFF' + values.map(row => row.map(quote).join(',')).join('\r\n') + '\r\n';
const output = path.join(root,'output/ヒジャブの出現率.csv');
const previous = await fs.readFile(output,'utf8');
if (csv !== previous) throw new Error('Portable build differs from artifact-tool authoring');
await fs.writeFile(output, csv);
const report = await wb.inspect({kind:'region',sheetId:sheet.name,range:'A1:F4',maxChars:1800,tableMaxRows:4,tableMaxCols:6});
console.log(report.ndjson ?? report);
console.log(`${values.length - 1} rows authored and identical to the portable CSV build.`);
