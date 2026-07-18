# Changelog

## [0.18.9a21](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a21) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.5a1...0.18.9a21)

**Merged pull requests:**

- fix: pronounce complex numbers instead of crashing [\#176](https://github.com/OpenVoiceOS/ovos-number-parser/pull/176) ([JarbasAl](https://github.com/JarbasAl))
- fix: stop pronouncing large finite numbers as infinity in Russian [\#175](https://github.com/OpenVoiceOS/ovos-number-parser/pull/175) ([JarbasAl](https://github.com/JarbasAl))
- fix: name every finite short-scale magnitude in English [\#174](https://github.com/OpenVoiceOS/ovos-number-parser/pull/174) ([JarbasAl](https://github.com/JarbasAl))
- refactor: Spanish numbers on the shared Romance extractor [\#173](https://github.com/OpenVoiceOS/ovos-number-parser/pull/173) ([JarbasAl](https://github.com/JarbasAl))
- refactor: migrate Catalan numbers onto the shared Romance engine [\#172](https://github.com/OpenVoiceOS/ovos-number-parser/pull/172) ([JarbasAl](https://github.com/JarbasAl))
- fix: parse Catalan long-scale words in extract\_number [\#171](https://github.com/OpenVoiceOS/ovos-number-parser/pull/171) ([JarbasAl](https://github.com/JarbasAl))
- fix: Basque long-scale numerals per Euskaltzaindia Araua 7 [\#170](https://github.com/OpenVoiceOS/ovos-number-parser/pull/170) ([JarbasAl](https://github.com/JarbasAl))
- fix: prevent Romance number extractor crash on large/scientific floats [\#169](https://github.com/OpenVoiceOS/ovos-number-parser/pull/169) ([JarbasAl](https://github.com/JarbasAl))
- fix: pronounce Finnish/Estonian long-scale trillions [\#168](https://github.com/OpenVoiceOS/ovos-number-parser/pull/168) ([JarbasAl](https://github.com/JarbasAl))
- fix: pronounce French long-scale billion \(10^12\) [\#167](https://github.com/OpenVoiceOS/ovos-number-parser/pull/167) ([JarbasAl](https://github.com/JarbasAl))
- fix: parse Spanish long-scale large numbers [\#166](https://github.com/OpenVoiceOS/ovos-number-parser/pull/166) ([JarbasAl](https://github.com/JarbasAl))
- fix: default number scale to each language's canonical convention [\#165](https://github.com/OpenVoiceOS/ovos-number-parser/pull/165) ([JarbasAl](https://github.com/JarbasAl))
- fix: accumulate Turkish million and thousand groups [\#164](https://github.com/OpenVoiceOS/ovos-number-parser/pull/164) ([JarbasAl](https://github.com/JarbasAl))
- fix: accumulate Azerbaijani million and thousand groups [\#163](https://github.com/OpenVoiceOS/ovos-number-parser/pull/163) ([JarbasAl](https://github.com/JarbasAl))
- test: pin Romance hundred apocopation \(cem/cen/cien vs cento/ciento\) [\#162](https://github.com/OpenVoiceOS/ovos-number-parser/pull/162) ([JarbasAl](https://github.com/JarbasAl))
- fix: accumulate Czech million and thousand groups [\#161](https://github.com/OpenVoiceOS/ovos-number-parser/pull/161) ([JarbasAl](https://github.com/JarbasAl))
- fix: preserve sign of negative fractions with zero integer part [\#160](https://github.com/OpenVoiceOS/ovos-number-parser/pull/160) ([JarbasAl](https://github.com/JarbasAl))
- fix: keep the remainder after a bare Finnish scale word [\#159](https://github.com/OpenVoiceOS/ovos-number-parser/pull/159) ([JarbasAl](https://github.com/JarbasAl))
- fix: multiply Basque hundreds inside a thousands group [\#158](https://github.com/OpenVoiceOS/ovos-number-parser/pull/158) ([JarbasAl](https://github.com/JarbasAl))
- fix: split Danish scale compounds on atoms and keep the negative sign [\#157](https://github.com/OpenVoiceOS/ovos-number-parser/pull/157) ([JarbasAl](https://github.com/JarbasAl))
- fix: Basque negative ordinal raises bare KeyError [\#156](https://github.com/OpenVoiceOS/ovos-number-parser/pull/156) ([JarbasAl](https://github.com/JarbasAl))
- fix: match Swedish fraction words case-insensitively [\#155](https://github.com/OpenVoiceOS/ovos-number-parser/pull/155) ([JarbasAl](https://github.com/JarbasAl))
- fix: accumulate Slovak million and hundred-thousand groups [\#154](https://github.com/OpenVoiceOS/ovos-number-parser/pull/154) ([JarbasAl](https://github.com/JarbasAl))
- fix: Frisian zeroth ordinal raises KeyError [\#153](https://github.com/OpenVoiceOS/ovos-number-parser/pull/153) ([JarbasAl](https://github.com/JarbasAl))
- fix: match Catalan fraction words case-insensitively [\#152](https://github.com/OpenVoiceOS/ovos-number-parser/pull/152) ([JarbasAl](https://github.com/JarbasAl))
- fix: robust Arabic numbers for Persian digits and glued punctuation [\#151](https://github.com/OpenVoiceOS/ovos-number-parser/pull/151) ([JarbasAl](https://github.com/JarbasAl))
- fix: Finnish ordinal recursion on million multiples [\#150](https://github.com/OpenVoiceOS/ovos-number-parser/pull/150) ([JarbasAl](https://github.com/JarbasAl))
- fix: match Basque fraction words case-insensitively [\#149](https://github.com/OpenVoiceOS/ovos-number-parser/pull/149) ([JarbasAl](https://github.com/JarbasAl))
- fix: reject NaN uniformly in pronounce\_number [\#148](https://github.com/OpenVoiceOS/ovos-number-parser/pull/148) ([JarbasAl](https://github.com/JarbasAl))
- fix: match Spanish fraction words case-insensitively [\#147](https://github.com/OpenVoiceOS/ovos-number-parser/pull/147) ([JarbasAl](https://github.com/JarbasAl))
- fix: sum Catalan scale groups so millions and hundred-thousands combine [\#146](https://github.com/OpenVoiceOS/ovos-number-parser/pull/146) ([JarbasAl](https://github.com/JarbasAl))
- fix: normalize Russian plural fraction endings to the singular form [\#145](https://github.com/OpenVoiceOS/ovos-number-parser/pull/145) ([JarbasAl](https://github.com/JarbasAl))
- fix: join Italian digit groups before their scale word [\#144](https://github.com/OpenVoiceOS/ovos-number-parser/pull/144) ([JarbasAl](https://github.com/JarbasAl))
- fix: pronounce English 4-digit numbers as cardinals by default [\#143](https://github.com/OpenVoiceOS/ovos-number-parser/pull/143) ([JarbasAl](https://github.com/JarbasAl))
- fix: return the no-number sentinel for non-string input across all languages [\#142](https://github.com/OpenVoiceOS/ovos-number-parser/pull/142) ([JarbasAl](https://github.com/JarbasAl))
- fix: Spanish pronounces a bare hundred as 'cien' not 'ciento' [\#141](https://github.com/OpenVoiceOS/ovos-number-parser/pull/141) ([JarbasAl](https://github.com/JarbasAl))
- fix: Polish loses the thousand and the sign in compound numbers [\#140](https://github.com/OpenVoiceOS/ovos-number-parser/pull/140) ([JarbasAl](https://github.com/JarbasAl))
- fix: Slovak minus sign applied only to the first word of a compound number [\#139](https://github.com/OpenVoiceOS/ovos-number-parser/pull/139) ([JarbasAl](https://github.com/JarbasAl))
- fix: Croatian minus sign applied only to the first word of a compound number [\#138](https://github.com/OpenVoiceOS/ovos-number-parser/pull/138) ([JarbasAl](https://github.com/JarbasAl))
- fix: Czech minus sign applied only to the first word of a compound number [\#137](https://github.com/OpenVoiceOS/ovos-number-parser/pull/137) ([JarbasAl](https://github.com/JarbasAl))
- fix: Bulgarian minus sign applied only to the first word of a compound number [\#136](https://github.com/OpenVoiceOS/ovos-number-parser/pull/136) ([JarbasAl](https://github.com/JarbasAl))
- fix: Ukrainian minus sign applied only to the first word of a compound number [\#135](https://github.com/OpenVoiceOS/ovos-number-parser/pull/135) ([JarbasAl](https://github.com/JarbasAl))
- fix: Russian minus sign applied only to the first word of a compound number [\#134](https://github.com/OpenVoiceOS/ovos-number-parser/pull/134) ([JarbasAl](https://github.com/JarbasAl))
- fix: Azerbaijani extraction — bare hundreds after a thousand, and whole-number minus sign [\#133](https://github.com/OpenVoiceOS/ovos-number-parser/pull/133) ([JarbasAl](https://github.com/JarbasAl))
- fix: Turkish extraction — bare hundreds after a thousand, and whole-number minus sign [\#132](https://github.com/OpenVoiceOS/ovos-number-parser/pull/132) ([JarbasAl](https://github.com/JarbasAl))
- fix: Catalan bare hundreds multiplied instead of added after larger numbers [\#131](https://github.com/OpenVoiceOS/ovos-number-parser/pull/131) ([JarbasAl](https://github.com/JarbasAl))
- fix: Italian bare hundreds multiplied instead of added after larger numbers [\#130](https://github.com/OpenVoiceOS/ovos-number-parser/pull/130) ([JarbasAl](https://github.com/JarbasAl))
- test: guard English "X hundred and Y" digit fusion [\#127](https://github.com/OpenVoiceOS/ovos-number-parser/pull/127) ([JarbasAl](https://github.com/JarbasAl))
- fix: return the no-number sentinel for non-string input in Romance numbers [\#123](https://github.com/OpenVoiceOS/ovos-number-parser/pull/123) ([JarbasAl](https://github.com/JarbasAl))

## [0.18.5a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.5a1) (2026-07-17)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.4a1...0.18.5a1)

## [0.18.4a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.4a1) (2026-07-17)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.3a1...0.18.4a1)

**Merged pull requests:**

- fix: index English scale words by place value for large ordinals [\#126](https://github.com/OpenVoiceOS/ovos-number-parser/pull/126) ([JarbasAl](https://github.com/JarbasAl))
- fix: correct Swedish ordinal pronunciation [\#124](https://github.com/OpenVoiceOS/ovos-number-parser/pull/124) ([JarbasAl](https://github.com/JarbasAl))
- fix: multiply the scale when a fraction precedes it in Romance numbers [\#122](https://github.com/OpenVoiceOS/ovos-number-parser/pull/122) ([JarbasAl](https://github.com/JarbasAl))

## [0.18.3a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.3a1) (2026-07-17)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.2a2...0.18.3a1)

**Merged pull requests:**

- fix: emit milijon remainder in Slovene long-scale numbers [\#121](https://github.com/OpenVoiceOS/ovos-number-parser/pull/121) ([JarbasAl](https://github.com/JarbasAl))

## [0.18.2a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.2a2) (2026-07-17)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.2a1...0.18.2a2)

**Merged pull requests:**

- docs: polish README, docs and examples for standalone + cross-domain use [\#115](https://github.com/OpenVoiceOS/ovos-number-parser/pull/115) ([JarbasAl](https://github.com/JarbasAl))

## [0.18.2a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.2a1) (2026-07-17)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.1a2...0.18.2a1)

**Merged pull requests:**

- fix: harden Arabic number extraction \(duals, article, unit lists\) [\#118](https://github.com/OpenVoiceOS/ovos-number-parser/pull/118) ([JarbasAl](https://github.com/JarbasAl))
- fix: combine compound Spanish magnitudes when extracting numbers [\#117](https://github.com/OpenVoiceOS/ovos-number-parser/pull/117) ([JarbasAl](https://github.com/JarbasAl))
- fix: correct Basque multi-scale cardinal extraction [\#116](https://github.com/OpenVoiceOS/ovos-number-parser/pull/116) ([JarbasAl](https://github.com/JarbasAl))
- test: expand Portuguese number coverage [\#114](https://github.com/OpenVoiceOS/ovos-number-parser/pull/114) ([JarbasAl](https://github.com/JarbasAl))
- fix: correct Dutch 'en een half' compound numbers [\#113](https://github.com/OpenVoiceOS/ovos-number-parser/pull/113) ([JarbasAl](https://github.com/JarbasAl))
- fix: add hundreds after thousands in Ukrainian number extraction [\#112](https://github.com/OpenVoiceOS/ovos-number-parser/pull/112) ([JarbasAl](https://github.com/JarbasAl))
- fix: Galician number vocabulary leftovers [\#111](https://github.com/OpenVoiceOS/ovos-number-parser/pull/111) ([JarbasAl](https://github.com/JarbasAl))
- fix: Czech number scale words, minus, and year pronunciation [\#110](https://github.com/OpenVoiceOS/ovos-number-parser/pull/110) ([JarbasAl](https://github.com/JarbasAl))
- fix: negate whole compound negative numbers \(en\) [\#109](https://github.com/OpenVoiceOS/ovos-number-parser/pull/109) ([JarbasAl](https://github.com/JarbasAl))
- fix\(sl\): correct compound Slovene ordinals above one hundred [\#108](https://github.com/OpenVoiceOS/ovos-number-parser/pull/108) ([JarbasAl](https://github.com/JarbasAl))
- fix: harden Swedish number extraction against non-string input [\#107](https://github.com/OpenVoiceOS/ovos-number-parser/pull/107) ([JarbasAl](https://github.com/JarbasAl))
- test: expand German number parser coverage [\#106](https://github.com/OpenVoiceOS/ovos-number-parser/pull/106) ([JarbasAl](https://github.com/JarbasAl))
- fix: parse elided and accented Italian fused numerals [\#105](https://github.com/OpenVoiceOS/ovos-number-parser/pull/105) ([JarbasAl](https://github.com/JarbasAl))
- test: expand French number coverage [\#104](https://github.com/OpenVoiceOS/ovos-number-parser/pull/104) ([JarbasAl](https://github.com/JarbasAl))
- fix: extract declined Russian один/два forms [\#103](https://github.com/OpenVoiceOS/ovos-number-parser/pull/103) ([JarbasAl](https://github.com/JarbasAl))
- fix: correct Azerbaijani large-number ordinal pronunciation [\#102](https://github.com/OpenVoiceOS/ovos-number-parser/pull/102) ([JarbasAl](https://github.com/JarbasAl))
- fix: hyphenate Hungarian thousand-group boundaries above 2000 [\#101](https://github.com/OpenVoiceOS/ovos-number-parser/pull/101) ([JarbasAl](https://github.com/JarbasAl))
- test: extend Danish number parser coverage [\#100](https://github.com/OpenVoiceOS/ovos-number-parser/pull/100) ([JarbasAl](https://github.com/JarbasAl))
- fix: gender agreement for Mirandese cardinals [\#99](https://github.com/OpenVoiceOS/ovos-number-parser/pull/99) ([JarbasAl](https://github.com/JarbasAl))
- fix: Polish singular scale words \(tysiąc/milion\) drop remainder [\#98](https://github.com/OpenVoiceOS/ovos-number-parser/pull/98) ([JarbasAl](https://github.com/JarbasAl))
- fix: Persian number scientific/underflow crashes [\#97](https://github.com/OpenVoiceOS/ovos-number-parser/pull/97) ([JarbasAl](https://github.com/JarbasAl))
- fix: complete Asturian long-scale ladder for large numbers [\#96](https://github.com/OpenVoiceOS/ovos-number-parser/pull/96) ([JarbasAl](https://github.com/JarbasAl))

## [0.18.1a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.1a2) (2026-07-17)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.1a1...0.18.1a2)

**Merged pull requests:**

- chore: migrate packaging to pyproject.toml and add LICENSE [\#94](https://github.com/OpenVoiceOS/ovos-number-parser/pull/94) ([JarbasAl](https://github.com/JarbasAl))

## [0.18.1a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.1a1) (2026-07-17)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.0a1...0.18.1a1)

**Merged pull requests:**

- fix: point the release workflows at the live gh-automations [\#92](https://github.com/OpenVoiceOS/ovos-number-parser/pull/92) ([JarbasAl](https://github.com/JarbasAl))
- test: guard indonesian and malay in the parity suite [\#91](https://github.com/OpenVoiceOS/ovos-number-parser/pull/91) ([JarbasAl](https://github.com/JarbasAl))
- feat: norwegian bokmål and nynorsk number support [\#90](https://github.com/OpenVoiceOS/ovos-number-parser/pull/90) ([JarbasAl](https://github.com/JarbasAl))
- feat: turkish, indonesian and malay number support [\#89](https://github.com/OpenVoiceOS/ovos-number-parser/pull/89) ([JarbasAl](https://github.com/JarbasAl))
- feat: greek number support [\#88](https://github.com/OpenVoiceOS/ovos-number-parser/pull/88) ([JarbasAl](https://github.com/JarbasAl))
- feat: hebrew number support [\#87](https://github.com/OpenVoiceOS/ovos-number-parser/pull/87) ([JarbasAl](https://github.com/JarbasAl))
- fix: restore the language registries and parity list [\#86](https://github.com/OpenVoiceOS/ovos-number-parser/pull/86) ([JarbasAl](https://github.com/JarbasAl))

## [0.18.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.17.0a1...0.18.0a1)

**Merged pull requests:**

- feat: bulgarian number support [\#85](https://github.com/OpenVoiceOS/ovos-number-parser/pull/85) ([JarbasAl](https://github.com/JarbasAl))
- feat: croatian number support [\#84](https://github.com/OpenVoiceOS/ovos-number-parser/pull/84) ([JarbasAl](https://github.com/JarbasAl))
- feat: slovak number support [\#83](https://github.com/OpenVoiceOS/ovos-number-parser/pull/83) ([JarbasAl](https://github.com/JarbasAl))

## [0.17.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.17.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.16.0a2...0.17.0a1)

**Merged pull requests:**

- feat: finnish and estonian number support [\#82](https://github.com/OpenVoiceOS/ovos-number-parser/pull/82) ([JarbasAl](https://github.com/JarbasAl))

## [0.16.0a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.16.0a2) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.16.0a1...0.16.0a2)

## [0.16.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.16.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.15.0a1...0.16.0a1)

**Merged pull requests:**

- feat: west frisian and aragonese number support [\#75](https://github.com/OpenVoiceOS/ovos-number-parser/pull/75) ([JarbasAl](https://github.com/JarbasAl))

## [0.15.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.15.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.14.0a1...0.15.0a1)

**Merged pull requests:**

- Release 0.15.0a1 [\#80](https://github.com/OpenVoiceOS/ovos-number-parser/pull/80) ([github-actions[bot]](https://github.com/apps/github-actions))
- feat: add Occitan \(oc\) number support [\#76](https://github.com/OpenVoiceOS/ovos-number-parser/pull/76) ([JarbasAl](https://github.com/JarbasAl))

## [0.14.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.14.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.13.0a2...0.14.0a1)

**Merged pull requests:**

- Release 0.14.0a1 [\#79](https://github.com/OpenVoiceOS/ovos-number-parser/pull/79) ([github-actions[bot]](https://github.com/apps/github-actions))
- feat\(ro\): Romanian number parsing and pronunciation [\#73](https://github.com/OpenVoiceOS/ovos-number-parser/pull/73) ([JarbasAl](https://github.com/JarbasAl))

## [0.13.0a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.13.0a2) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.13.0a1...0.13.0a2)

**Merged pull requests:**

- Release 0.13.0a2 [\#78](https://github.com/OpenVoiceOS/ovos-number-parser/pull/78) ([github-actions[bot]](https://github.com/apps/github-actions))

## [0.13.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.13.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.12.0a1...0.13.0a1)

**Merged pull requests:**

- Release 0.13.0a1 [\#77](https://github.com/OpenVoiceOS/ovos-number-parser/pull/77) ([github-actions[bot]](https://github.com/apps/github-actions))
- feat: Kabyle \(kab\) number support [\#71](https://github.com/OpenVoiceOS/ovos-number-parser/pull/71) ([JarbasAl](https://github.com/JarbasAl))

## [0.12.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.12.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.11.0a2...0.12.0a1)

**Merged pull requests:**

- Release 0.12.0a1 [\#74](https://github.com/OpenVoiceOS/ovos-number-parser/pull/74) ([github-actions[bot]](https://github.com/apps/github-actions))
- feat\(engine\): declarative knobs for scale linkers, articled scale groups and ordinal particles [\#72](https://github.com/OpenVoiceOS/ovos-number-parser/pull/72) ([JarbasAl](https://github.com/JarbasAl))

## [0.11.0a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.11.0a2) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.11.0a1...0.11.0a2)

**Merged pull requests:**

- Release 0.11.0a2 [\#70](https://github.com/OpenVoiceOS/ovos-number-parser/pull/70) ([github-actions[bot]](https://github.com/apps/github-actions))

## [0.11.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.11.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.10.0a4...0.11.0a1)

## [0.10.0a4](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.10.0a4) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.10.0a3...0.10.0a4)

## [0.10.0a3](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.10.0a3) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.10.0a2...0.10.0a3)

## [0.10.0a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.10.0a2) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.10.0a1...0.10.0a2)

## [0.10.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.10.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.9.0a1...0.10.0a1)

## [0.9.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.9.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.8.0a1...0.9.0a1)

## [0.8.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.8.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.7.0a1...0.8.0a1)

## [0.7.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.7.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.6.3a1...0.7.0a1)

## [0.6.3a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.6.3a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.6.2a1...0.6.3a1)

## [0.6.2a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.6.2a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.6.1a3...0.6.2a1)

## [0.6.1a3](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.6.1a3) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.6.1a2...0.6.1a3)

## [0.6.1a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.6.1a2) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.6.1a1...0.6.1a2)

## [0.6.1a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.6.1a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.6.0a1...0.6.1a1)

## [0.6.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.6.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.5.3a1...0.6.0a1)

## [0.5.3a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.5.3a1) (2026-06-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.5.2a4...0.5.3a1)

## [0.5.2a4](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.5.2a4) (2025-12-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.5.2a3...0.5.2a4)

## [0.5.2a3](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.5.2a3) (2025-12-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.5.2a2...0.5.2a3)

## [0.5.2a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.5.2a2) (2025-12-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.5.2a1...0.5.2a2)

## [0.5.2a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.5.2a1) (2025-10-12)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.5.1...0.5.2a1)

## [0.5.1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.5.1) (2025-10-12)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.5.1a1...0.5.1)

## [0.5.1a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.5.1a1) (2025-10-12)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.5.0a1...0.5.1a1)

## [0.5.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.5.0a1) (2025-10-04)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.4.2...0.5.0a1)

## [0.4.2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.4.2) (2025-08-04)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.4.1...0.4.2)

## [0.4.1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.4.1) (2025-08-04)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.4.1a1...0.4.1)

## [0.4.1a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.4.1a1) (2025-08-04)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.4.0...0.4.1a1)

## [0.4.0](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.4.0) (2025-08-03)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.4.0a1...0.4.0)

## [0.4.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.4.0a1) (2025-08-03)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.3.3a1...0.4.0a1)

## [0.3.3a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.3.3a1) (2025-08-03)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.3.2...0.3.3a1)

## [0.3.2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.3.2) (2025-03-25)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.3.1...0.3.2)

## [0.3.1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.3.1) (2025-02-27)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.3.0...0.3.1)

## [0.3.0](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.3.0) (2025-02-27)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.2.0a1...0.3.0)

## [0.2.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.2.0a1) (2025-02-27)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.1.0...0.2.0a1)

## [0.1.0](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.1.0) (2025-02-26)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.1.0a2...0.1.0)

## [0.1.0a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.1.0a2) (2025-02-26)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.1.0a1...0.1.0a2)

## [0.1.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.1.0a1) (2025-02-26)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.0.2...0.1.0a1)

## [0.0.2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.0.2) (2024-11-13)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.0.2a1...0.0.2)

## [0.0.2a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.0.2a1) (2024-11-13)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.0.1...0.0.2a1)

## [0.0.1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.0.1) (2024-11-07)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.0.1a2...0.0.1)

## [0.0.1a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.0.1a2) (2024-11-07)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/bc086aef8c1f18b03f6481e222a6c460f5b94962...0.0.1a2)



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
