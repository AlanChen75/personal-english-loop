// Reuse the frozen v7 generator: change the institutional header and cover only.
// Research tables/charts and visible slides 2–14 stay unchanged; notes use the approved extension.
import fs from 'node:fs/promises';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { pathToFileURL, fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const sourceDir = '/Users/user/Desktop/NILM+LLM/automation2026-nilm-llm/presentation';
const sourcePath = path.join(sourceDir, 'build_automation_deck_v7.mjs');
const original = await fs.readFile(sourcePath, 'utf8');
if (createHash('sha256').update(original).digest('hex') !== 'bd05cf4fd55d1a1a003275d03b4deba2119cc1e9fac09426481006c1a98b34f1') {
  throw new Error('The v7 source changed; review it before applying the cover revision.');
}
const work = path.join(root, 'work/automation2026-v8');
const output = path.join(root, 'outputs/automation2026-v10');
const finalDeck = process.argv[2] ? path.resolve(process.argv[2]) : path.join(output, 'automation2026_13min_deck_v10.pptx');
await fs.mkdir(output, { recursive: true });
// 2026-11-06: restore the approved v7 opening after edbbc56 retained an unsolicited
// introduction. Cover identity is visual only; do not add it to narration without approval.
const extension = JSON.parse(await fs.readFile(path.join(root, 'practice-materials/automation2026/extension-v10.json'), 'utf8'));
const oldScript = await fs.readFile(path.join(sourceDir, 'automation2026_13min_script_v6.md'), 'utf8');
const oldExtension = JSON.parse(await fs.readFile(path.join(root, 'practice-materials/automation2026/extension-v7.json'), 'utf8'));
function updateApprovedPassages(source, field) {
  return oldExtension.overrides.reduce((text, previous) => {
    const current = extension.overrides.find(item => item.slide === previous.slide);
    if (!current) throw new Error(`Missing slide ${previous.slide}`);
    if (current[field] === previous[field]) return text;
    return replaceOnce(text, previous[field], current[field]);
  }, source).replaceAll('automation2026_13min_deck_v7_final.pptx', extension.source_deck);
}
const script = updateApprovedPassages(oldScript, 'spoken_transcript')
  .replace('2026-11-02', '2026-11-06');
await fs.writeFile(path.join(output, extension.source_script), script);
const display = await fs.readFile(path.join(sourceDir, 'automation2026_13min_display_script_v6.md'), 'utf8');
await fs.writeFile(path.join(output, 'automation2026_13min_display_script_v9.md'),
  updateApprovedPassages(display, 'display_transcript'));

function replaceOnce(source, from, to) {
  if (source.split(from).length !== 2) throw new Error(`Ambiguous source anchor: ${from.slice(0, 90)}`);
  return source.replace(from, to);
}
let generated = replaceOnce(original,
  "const workspaceDir = '/Users/user/Desktop/NILM+LLM/automation2026-nilm-llm';",
  `const workspaceDir = ${JSON.stringify(root)};`);
generated = replaceOnce(generated, "path.join(workspaceDir, 'tmp', 'automation-deck-v7-build')", JSON.stringify(path.join(work, 'build-v10')));
generated = replaceOnce(generated, "path.join(workspaceDir, 'presentation', 'automation2026_13min_deck_v7_final.pptx')", JSON.stringify(finalDeck));
generated = replaceOnce(generated, "path.join(workspaceDir, 'presentation', 'automation2026_13min_script_v6.md')", JSON.stringify(path.join(output, extension.source_script)));
generated = replaceOnce(generated, "text(slide,title,62,43,1130,62,35,C.navy,true);", "text(slide,title,62,78,1130,46,34,C.navy,true);");
generated = replaceOnce(generated, "rect(slide,62,114,1160,3,C.teal);", "rect(slide,62,132,1160,3,C.teal);");

const coverStart = generated.indexOf('// 1 Title');
const coverEnd = generated.indexOf('// 2 Problem');
if (coverStart < 0 || coverEnd <= coverStart) throw new Error('Cover markers missing');
const portrait = '/Users/user/Desktop/NILM+LLM/cacs2026-nilm-llm/paper/R1/presentation/assets/speaker_chung_kuang_chen.jpg';
const cover = `// 1 Title: CACS speaker identity, Automation research title
{
 const s=pres.slides.add(); s.background.fill=C.navy;
 text(s,'Engineering Bounds Constrain\\nCandidate Selection in Industrial NILM',67,110,1145,145,46,C.white,true);
 text(s,'Chung-Kuang Chen  ·  Shu-Hao Liang',67,280,1100,40,26,C.white);
 text(s,'Speaker',67,370,700,32,24,'#78C8C5',true);
 text(s,'Chung-Kuang Chen',67,412,810,48,34,C.white,true);
 text(s,'PhD Student',67,472,810,34,25,'#D5E4E7');
 text(s,'Graduate Institute of Intelligent Manufacturing Technology',67,518,855,38,24,'#D5E4E7');
 text(s,'National Taiwan University of Science and Technology',67,565,855,38,24,'#D5E4E7');
 s.images.add({blob:await fs.readFile(${JSON.stringify(portrait)}),contentType:'image/jpeg',alt:'Speaker portrait of Chung-Kuang Chen',fit:'cover',position:{left:990,top:366,width:200,height:238}});
 text(s,'The 23rd International Conference on Automation Technology',67,628,1120,30,22,'#C8D7DB');
 text(s,'Paper 1009',67,671,250,23,18,'#C8D7DB');
 text(s,'1 / 13',1125,671,95,23,15,'#C8D7DB',false,'right');
 s.speakerNotes.text=spoken[0]+'\\n\\nPortrait: presenter-supplied CACS v7 asset.';
}
`;
generated = generated.slice(0, coverStart) + cover + generated.slice(coverEnd);
generated = replaceOnce(generated, "text(s,'Future work',65,53,1100,59,36,C.white,true);rect(s,65,127,1150,3,C.teal);", "text(s,'Future work',65,78,1100,46,34,C.white,true);rect(s,65,132,1150,3,C.teal);");
generated = replaceOnce(generated, "text(s,'Q&A: How were the numbers calculated?',62,43,1130,62,35,C.navy,true);", "text(s,'Q&A: How were the numbers calculated?',62,78,1130,46,34,C.navy,true);");
generated = replaceOnce(generated, "rect(s,62,114,1160,3,C.teal);", "rect(s,62,132,1160,3,C.teal);");
const header = `
// Official wordmark remains unmodified. Reserve the top 70 px for school identity.
const headerBytes=await fs.readFile(${JSON.stringify(path.join(work, 'assets/taiwan-tech-wordmark.png'))});
for (const slide of pres.slides.items) {
 rect(slide,0,0,1280,70,C.white);
 slide.images.add({blob:headerBytes,contentType:'image/png',alt:'National Taiwan University of Science and Technology official bilingual wordmark',fit:'contain',position:{left:62,top:8,width:282,height:54}});
 text(slide,'Automation 2026',960,20,260,30,24,C.navy,true,'right');
 // Asset attribution lives in README and extension metadata, not the spoken notes.
}
`;
generated = replaceOnce(generated, 'await fs.mkdir(buildDir,{recursive:true});', header + '\nawait fs.mkdir(buildDir,{recursive:true});');
generated = generated.replace('validation-v7-final.json', `${path.basename(finalDeck, '.pptx')}.validation.json`);
const generatedPath = path.join(work, 'build-deck.mjs');
await fs.writeFile(generatedPath, generated);
await import(pathToFileURL(generatedPath).href);
