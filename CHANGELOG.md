# Changelog

## [0.19.1a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.1a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.0a1...0.19.1a1)

**Merged pull requests:**

- fix: write the trema in Dutch compound numerals [\#256](https://github.com/OpenVoiceOS/ovos-number-parser/pull/256) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.0a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.20a1...0.19.0a1)

**Merged pull requests:**

- feat: add differential harness against ICU RBNF spellout [\#254](https://github.com/OpenVoiceOS/ovos-number-parser/pull/254) ([JarbasAl](https://github.com/JarbasAl))

## [0.18.20a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.20a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.19a1...0.18.20a1)

**Merged pull requests:**

- fix: restore the 'e' conjunction between Portuguese numeral classes [\#252](https://github.com/OpenVoiceOS/ovos-number-parser/pull/252) ([JarbasAl](https://github.com/JarbasAl))

## [0.18.19a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.19a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.18a1...0.18.19a1)

**Merged pull requests:**

- fix: stop discarding digits, gender and ordinals for engine-backed languages [\#250](https://github.com/OpenVoiceOS/ovos-number-parser/pull/250) ([JarbasAl](https://github.com/JarbasAl))
- fix: never speak padded or unread output for oversized numbers [\#249](https://github.com/OpenVoiceOS/ovos-number-parser/pull/249) ([JarbasAl](https://github.com/JarbasAl))

## [0.18.18a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.18a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.17a1...0.18.18a1)

**Merged pull requests:**

- fix: pronounce infinity and oversized integers without crashing [\#247](https://github.com/OpenVoiceOS/ovos-number-parser/pull/247) ([JarbasAl](https://github.com/JarbasAl))

## [0.18.17a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.17a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.16a1...0.18.17a1)

**Merged pull requests:**

- fix: enforce descending direction on Romance additive joiners [\#245](https://github.com/OpenVoiceOS/ovos-number-parser/pull/245) ([JarbasAl](https://github.com/JarbasAl))

## [0.18.16a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.16a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.15a1...0.18.16a1)

**Merged pull requests:**

- fix: treat hyphen, underscore and space alike in compound numerals [\#243](https://github.com/OpenVoiceOS/ovos-number-parser/pull/243) ([JarbasAl](https://github.com/JarbasAl))

## [0.18.15a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.15a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.14a1...0.18.15a1)

**Merged pull requests:**

- fix: keep the word when a numeral is hyphen-glued to it [\#241](https://github.com/OpenVoiceOS/ovos-number-parser/pull/241) ([JarbasAl](https://github.com/JarbasAl))

## [0.18.14a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.14a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.13a1...0.18.14a1)

**Closed issues:**

- numbers\_to\_digits drops leading "one" before hundred/thousand \(generic fallback engine\) [\#238](https://github.com/OpenVoiceOS/ovos-number-parser/issues/238)

**Merged pull requests:**

- fix: keep a leading one before a scale word in numbers\_to\_digits [\#239](https://github.com/OpenVoiceOS/ovos-number-parser/pull/239) ([JarbasAl](https://github.com/JarbasAl))
- fix\(da\): correct cardinal 11, ordinals 0-39, and is\_ordinal recognition [\#237](https://github.com/OpenVoiceOS/ovos-number-parser/pull/237) ([andlo](https://github.com/andlo))

## [0.18.13a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.13a1) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.11a1...0.18.13a1)

**Merged pull requests:**

- fix: guard non-finite/overflow string tokens in extract\_number [\#234](https://github.com/OpenVoiceOS/ovos-number-parser/pull/234) ([JarbasAl](https://github.com/JarbasAl))

## [0.18.11a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.11a1) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.12a1...0.18.11a1)

## [0.18.12a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.12a1) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.10a1...0.18.12a1)

**Merged pull requests:**

- fix: reject a zero denominator in Indonesian and Malay slash fractions [\#231](https://github.com/OpenVoiceOS/ovos-number-parser/pull/231) ([JarbasAl](https://github.com/JarbasAl))
- fix: extract a written slash fraction in Polish without crashing [\#230](https://github.com/OpenVoiceOS/ovos-number-parser/pull/230) ([JarbasAl](https://github.com/JarbasAl))
- fix: treat a zero denominator as not a fraction [\#229](https://github.com/OpenVoiceOS/ovos-number-parser/pull/229) ([JarbasAl](https://github.com/JarbasAl))
- fix: parse a bare 'ettusen' after a larger scale in Swedish numbers [\#228](https://github.com/OpenVoiceOS/ovos-number-parser/pull/228) ([JarbasAl](https://github.com/JarbasAl))
- fix: parse a bare scale word in Farsi numbers [\#227](https://github.com/OpenVoiceOS/ovos-number-parser/pull/227) ([JarbasAl](https://github.com/JarbasAl))
- fix: compose adjacent scale words in Greek numbers [\#226](https://github.com/OpenVoiceOS/ovos-number-parser/pull/226) ([JarbasAl](https://github.com/JarbasAl))
- fix: parse a bare 'one thousand' after a larger scale in Bulgarian numbers [\#225](https://github.com/OpenVoiceOS/ovos-number-parser/pull/225) ([JarbasAl](https://github.com/JarbasAl))
- fix: parse a bare 'one thousand' after a larger scale in Croatian numbers [\#224](https://github.com/OpenVoiceOS/ovos-number-parser/pull/224) ([JarbasAl](https://github.com/JarbasAl))
- fix: parse a bare 'one thousand' after a larger scale in Ukrainian numbers [\#223](https://github.com/OpenVoiceOS/ovos-number-parser/pull/223) ([JarbasAl](https://github.com/JarbasAl))
- fix: parse a bare 'one thousand' after a larger scale in Russian numbers [\#222](https://github.com/OpenVoiceOS/ovos-number-parser/pull/222) ([JarbasAl](https://github.com/JarbasAl))
- fix: keep the sign on negative West Frisian millions with a remainder [\#221](https://github.com/OpenVoiceOS/ovos-number-parser/pull/221) ([JarbasAl](https://github.com/JarbasAl))
- fix: keep the sign on negative Dutch millions with a remainder [\#220](https://github.com/OpenVoiceOS/ovos-number-parser/pull/220) ([JarbasAl](https://github.com/JarbasAl))

## [0.18.10a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.10a1) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a35...0.18.10a1)

**Merged pull requests:**

- fix: compose Catalan compound ordinals per the IEC normativa [\#218](https://github.com/OpenVoiceOS/ovos-number-parser/pull/218) ([JarbasAl](https://github.com/JarbasAl))

## [0.18.9a35](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a35) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a34...0.18.9a35)

## [0.18.9a34](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a34) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a32...0.18.9a34)

## [0.18.9a32](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a32) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a33...0.18.9a32)

## [0.18.9a33](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a33) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a30...0.18.9a33)

## [0.18.9a30](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a30) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a31...0.18.9a30)

## [0.18.9a31](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a31) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a29...0.18.9a31)

## [0.18.9a29](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a29) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a26...0.18.9a29)

## [0.18.9a26](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a26) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a27...0.18.9a26)

## [0.18.9a27](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a27) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a21...0.18.9a27)

## [0.18.9a21](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a21) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a25...0.18.9a21)

## [0.18.9a25](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a25) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a24...0.18.9a25)

## [0.18.9a24](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a24) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a23...0.18.9a24)

## [0.18.9a23](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a23) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a22...0.18.9a23)

## [0.18.9a22](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a22) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a28...0.18.9a22)

## [0.18.9a28](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a28) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a20...0.18.9a28)

## [0.18.9a20](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a20) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a19...0.18.9a20)

## [0.18.9a19](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a19) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a18...0.18.9a19)

## [0.18.9a18](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a18) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a17...0.18.9a18)

## [0.18.9a17](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a17) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a16...0.18.9a17)

## [0.18.9a16](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a16) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a15...0.18.9a16)

## [0.18.9a15](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a15) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a14...0.18.9a15)

## [0.18.9a14](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a14) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a13...0.18.9a14)

## [0.18.9a13](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a13) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a12...0.18.9a13)

## [0.18.9a12](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a12) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a11...0.18.9a12)

## [0.18.9a11](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a11) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.8a1...0.18.9a11)

## [0.18.8a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.8a1) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a9...0.18.8a1)

## [0.18.9a9](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a9) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a8...0.18.9a9)

## [0.18.9a8](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a8) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a7...0.18.9a8)

## [0.18.9a7](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a7) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a6...0.18.9a7)

## [0.18.9a6](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a6) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a5...0.18.9a6)

## [0.18.9a5](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a5) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a4...0.18.9a5)

## [0.18.9a4](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a4) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a3...0.18.9a4)

## [0.18.9a3](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a3) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a2...0.18.9a3)

## [0.18.9a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a2) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a1...0.18.9a2)

## [0.18.9a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a1) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a10...0.18.9a1)

## [0.18.9a10](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a10) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.7a1...0.18.9a10)

## [0.18.7a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.7a1) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.6a1...0.18.7a1)

## [0.18.6a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.6a1) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.5a1...0.18.6a1)

**Merged pull requests:**

- refactor: Italian numbers on the shared Romance extractor [\#179](https://github.com/OpenVoiceOS/ovos-number-parser/pull/179) ([JarbasAl](https://github.com/JarbasAl))
- fix: round spoken decimals instead of truncating them [\#178](https://github.com/OpenVoiceOS/ovos-number-parser/pull/178) ([JarbasAl](https://github.com/JarbasAl))
- refactor: French numbers on the shared Romance extractor [\#177](https://github.com/OpenVoiceOS/ovos-number-parser/pull/177) ([JarbasAl](https://github.com/JarbasAl))
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

## [0.18.1a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.1a2) (2026-07-17)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.1a1...0.18.1a2)

## [0.18.1a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.1a1) (2026-07-17)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.0a1...0.18.1a1)

## [0.18.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.17.0a1...0.18.0a1)

## [0.17.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.17.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.16.0a2...0.17.0a1)

## [0.16.0a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.16.0a2) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.16.0a1...0.16.0a2)

## [0.16.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.16.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.15.0a1...0.16.0a1)

## [0.15.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.15.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.14.0a1...0.15.0a1)

## [0.14.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.14.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.13.0a2...0.14.0a1)

## [0.13.0a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.13.0a2) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.13.0a1...0.13.0a2)

## [0.13.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.13.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.12.0a1...0.13.0a1)

## [0.12.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.12.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.11.0a2...0.12.0a1)

## [0.11.0a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.11.0a2) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.11.0a1...0.11.0a2)

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
