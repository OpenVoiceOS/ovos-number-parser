# Changelog

## [0.19.12a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.12a1) (2026-08-11)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.11a1...0.19.12a1)

**Merged pull requests:**

- fix: numbers\_to\_digits must not corrupt standalone digit runs \(leading zeros lost\) [\#296](https://github.com/OpenVoiceOS/ovos-number-parser/pull/296) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.11a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.11a1) (2026-08-11)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.10a1...0.19.11a1)

**Merged pull requests:**

- fix\(ar\): spaced unit+hundred parses additively \(خمس مية وثلاثين → 135 instead of 530\) [\#294](https://github.com/OpenVoiceOS/ovos-number-parser/pull/294) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.10a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.10a1) (2026-08-10)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.9a1...0.19.10a1)

**Merged pull requests:**

- fix\(en\): route numbers\_to\_digits to the English backend [\#286](https://github.com/OpenVoiceOS/ovos-number-parser/pull/286) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.9a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.9a1) (2026-08-10)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.8a2...0.19.9a1)

**Merged pull requests:**

- feat\(ar\): register-aware pronunciation and Arabic dialect code resolution [\#291](https://github.com/OpenVoiceOS/ovos-number-parser/pull/291) ([JarbasAl](https://github.com/JarbasAl))
- fix\(ar\): extract accepts colloquial and dialectal number forms [\#290](https://github.com/OpenVoiceOS/ovos-number-parser/pull/290) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.8a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.8a2) (2026-07-31)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.8a1...0.19.8a2)

**Merged pull requests:**

- docs: rewrite README in Simplified Technical English [\#284](https://github.com/OpenVoiceOS/ovos-number-parser/pull/284) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.8a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.8a1) (2026-07-22)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.7...0.19.8a1)

**Merged pull requests:**

- fix: guard non-decimal Unicode digits in number word tokenization [\#280](https://github.com/OpenVoiceOS/ovos-number-parser/pull/280) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.7](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.7) (2026-07-21)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.7a3...0.19.7)

## [0.19.7a3](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.7a3) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.7a2...0.19.7a3)

**Merged pull requests:**

- fix: drop the plural -s on French quatre-vingt/cent before mille [\#278](https://github.com/OpenVoiceOS/ovos-number-parser/pull/278) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.7a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.7a2) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.7a1...0.19.7a2)

**Merged pull requests:**

- Release 0.19.7a2 [\#277](https://github.com/OpenVoiceOS/ovos-number-parser/pull/277) ([github-actions[bot]](https://github.com/apps/github-actions))
- refactor: route French pronunciation through the shared engine [\#276](https://github.com/OpenVoiceOS/ovos-number-parser/pull/276) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.7a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.7a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.6a2...0.19.7a1)

**Merged pull requests:**

- Release 0.19.7a1 [\#275](https://github.com/OpenVoiceOS/ovos-number-parser/pull/275) ([github-actions[bot]](https://github.com/apps/github-actions))
- fix: fuse Italian cardinals into one word below a million [\#274](https://github.com/OpenVoiceOS/ovos-number-parser/pull/274) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.6a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.6a2) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.6a1...0.19.6a2)

**Merged pull requests:**

- Release 0.19.6a2 [\#273](https://github.com/OpenVoiceOS/ovos-number-parser/pull/273) ([github-actions[bot]](https://github.com/apps/github-actions))
- fix: Hebrew abstract numbers default to the feminine counting form [\#272](https://github.com/OpenVoiceOS/ovos-number-parser/pull/272) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.6a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.6a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.5a1...0.19.6a1)

**Merged pull requests:**

- Release 0.19.6a1 [\#271](https://github.com/OpenVoiceOS/ovos-number-parser/pull/271) ([github-actions[bot]](https://github.com/apps/github-actions))
- fix: Persian teens 15-18 use standard forms, not Tehrani colloquial [\#270](https://github.com/OpenVoiceOS/ovos-number-parser/pull/270) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.5a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.5a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.4a1...0.19.5a1)

**Merged pull requests:**

- Release 0.19.5a1 [\#269](https://github.com/OpenVoiceOS/ovos-number-parser/pull/269) ([github-actions[bot]](https://github.com/apps/github-actions))
- fix: accent Italian compounds of 'tre' \(ventitré, trentatré\) [\#268](https://github.com/OpenVoiceOS/ovos-number-parser/pull/268) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.4a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.4a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.3a3...0.19.4a1)

**Merged pull requests:**

- Release 0.19.4a1 [\#267](https://github.com/OpenVoiceOS/ovos-number-parser/pull/267) ([github-actions[bot]](https://github.com/apps/github-actions))
- fix: Swedish bare cardinal 1 is the neuter counting form 'ett' [\#266](https://github.com/OpenVoiceOS/ovos-number-parser/pull/266) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.3a3](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.3a3) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.3a2...0.19.3a3)

**Merged pull requests:**

- Release 0.19.3a3 [\#265](https://github.com/OpenVoiceOS/ovos-number-parser/pull/265) ([github-actions[bot]](https://github.com/apps/github-actions))

## [0.19.3a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.3a2) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.3a1...0.19.3a2)

**Merged pull requests:**

- Release 0.19.3a2 [\#264](https://github.com/OpenVoiceOS/ovos-number-parser/pull/264) ([github-actions[bot]](https://github.com/apps/github-actions))
- feat: three-way differential harness \(ICU RBNF + num2words\) [\#263](https://github.com/OpenVoiceOS/ovos-number-parser/pull/263) ([JarbasAl](https://github.com/JarbasAl))
- fix: Polish scale-word declension and spurious 'jeden' before a lone scale [\#262](https://github.com/OpenVoiceOS/ovos-number-parser/pull/262) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.3a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.3a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.2a1...0.19.3a1)

**Merged pull requests:**

- Release 0.19.3a1 [\#261](https://github.com/OpenVoiceOS/ovos-number-parser/pull/261) ([github-actions[bot]](https://github.com/apps/github-actions))
- fix: drop the leading 'een' before Dutch honderd and duizend [\#260](https://github.com/OpenVoiceOS/ovos-number-parser/pull/260) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.2a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.2a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.1a1...0.19.2a1)

**Merged pull requests:**

- Release 0.19.2a1 [\#259](https://github.com/OpenVoiceOS/ovos-number-parser/pull/259) ([github-actions[bot]](https://github.com/apps/github-actions))
- fix: Danish hundreds and thousands per Retskrivningsordbogen [\#258](https://github.com/OpenVoiceOS/ovos-number-parser/pull/258) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.1a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.1a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.0a1...0.19.1a1)

**Merged pull requests:**

- Release 0.19.1a1 [\#257](https://github.com/OpenVoiceOS/ovos-number-parser/pull/257) ([github-actions[bot]](https://github.com/apps/github-actions))
- fix: write the trema in Dutch compound numerals [\#256](https://github.com/OpenVoiceOS/ovos-number-parser/pull/256) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.0a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.20a1...0.19.0a1)

**Merged pull requests:**

- Release 0.19.0a1 [\#255](https://github.com/OpenVoiceOS/ovos-number-parser/pull/255) ([github-actions[bot]](https://github.com/apps/github-actions))
- feat: add differential harness against ICU RBNF spellout [\#254](https://github.com/OpenVoiceOS/ovos-number-parser/pull/254) ([JarbasAl](https://github.com/JarbasAl))

## [0.18.20a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.20a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.19a1...0.18.20a1)

**Merged pull requests:**

- Release 0.18.20a1 [\#253](https://github.com/OpenVoiceOS/ovos-number-parser/pull/253) ([github-actions[bot]](https://github.com/apps/github-actions))
- fix: restore the 'e' conjunction between Portuguese numeral classes [\#252](https://github.com/OpenVoiceOS/ovos-number-parser/pull/252) ([JarbasAl](https://github.com/JarbasAl))

## [0.18.19a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.19a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.18a1...0.18.19a1)

**Merged pull requests:**

- Release 0.18.19a1 [\#251](https://github.com/OpenVoiceOS/ovos-number-parser/pull/251) ([github-actions[bot]](https://github.com/apps/github-actions))
- fix: stop discarding digits, gender and ordinals for engine-backed languages [\#250](https://github.com/OpenVoiceOS/ovos-number-parser/pull/250) ([JarbasAl](https://github.com/JarbasAl))
- fix: never speak padded or unread output for oversized numbers [\#249](https://github.com/OpenVoiceOS/ovos-number-parser/pull/249) ([JarbasAl](https://github.com/JarbasAl))

## [0.18.18a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.18a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.17a1...0.18.18a1)

**Merged pull requests:**

- Release 0.18.18a1 [\#248](https://github.com/OpenVoiceOS/ovos-number-parser/pull/248) ([github-actions[bot]](https://github.com/apps/github-actions))
- fix: pronounce infinity and oversized integers without crashing [\#247](https://github.com/OpenVoiceOS/ovos-number-parser/pull/247) ([JarbasAl](https://github.com/JarbasAl))

## [0.18.17a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.17a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.16a1...0.18.17a1)

**Merged pull requests:**

- Release 0.18.17a1 [\#246](https://github.com/OpenVoiceOS/ovos-number-parser/pull/246) ([github-actions[bot]](https://github.com/apps/github-actions))
- fix: enforce descending direction on Romance additive joiners [\#245](https://github.com/OpenVoiceOS/ovos-number-parser/pull/245) ([JarbasAl](https://github.com/JarbasAl))

## [0.18.16a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.16a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.15a1...0.18.16a1)

**Merged pull requests:**

- Release 0.18.16a1 [\#244](https://github.com/OpenVoiceOS/ovos-number-parser/pull/244) ([github-actions[bot]](https://github.com/apps/github-actions))
- fix: treat hyphen, underscore and space alike in compound numerals [\#243](https://github.com/OpenVoiceOS/ovos-number-parser/pull/243) ([JarbasAl](https://github.com/JarbasAl))

## [0.18.15a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.15a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.14a1...0.18.15a1)

**Merged pull requests:**

- Release 0.18.15a1 [\#242](https://github.com/OpenVoiceOS/ovos-number-parser/pull/242) ([github-actions[bot]](https://github.com/apps/github-actions))
- fix: keep the word when a numeral is hyphen-glued to it [\#241](https://github.com/OpenVoiceOS/ovos-number-parser/pull/241) ([JarbasAl](https://github.com/JarbasAl))

## [0.18.14a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.14a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.13a1...0.18.14a1)

**Closed issues:**

- numbers\_to\_digits drops leading "one" before hundred/thousand \(generic fallback engine\) [\#238](https://github.com/OpenVoiceOS/ovos-number-parser/issues/238)

**Merged pull requests:**

- Release 0.18.14a1 [\#240](https://github.com/OpenVoiceOS/ovos-number-parser/pull/240) ([github-actions[bot]](https://github.com/apps/github-actions))
- fix: keep a leading one before a scale word in numbers\_to\_digits [\#239](https://github.com/OpenVoiceOS/ovos-number-parser/pull/239) ([JarbasAl](https://github.com/JarbasAl))
- fix\(da\): correct cardinal 11, ordinals 0-39, and is\_ordinal recognition [\#237](https://github.com/OpenVoiceOS/ovos-number-parser/pull/237) ([andlo](https://github.com/andlo))

## [0.18.13a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.13a1) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.12a1...0.18.13a1)

**Merged pull requests:**

- Release 0.18.13a1 [\#235](https://github.com/OpenVoiceOS/ovos-number-parser/pull/235) ([github-actions[bot]](https://github.com/apps/github-actions))
- fix: guard non-finite/overflow string tokens in extract\_number [\#234](https://github.com/OpenVoiceOS/ovos-number-parser/pull/234) ([JarbasAl](https://github.com/JarbasAl))

## [0.18.12a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.12a1) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.11a1...0.18.12a1)

## [0.18.11a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.11a1) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.10a1...0.18.11a1)

**Merged pull requests:**

- Release 0.18.12a1 [\#233](https://github.com/OpenVoiceOS/ovos-number-parser/pull/233) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.11a1 [\#232](https://github.com/OpenVoiceOS/ovos-number-parser/pull/232) ([github-actions[bot]](https://github.com/apps/github-actions))
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

- Release 0.18.10a1 [\#219](https://github.com/OpenVoiceOS/ovos-number-parser/pull/219) ([github-actions[bot]](https://github.com/apps/github-actions))
- fix: compose Catalan compound ordinals per the IEC normativa [\#218](https://github.com/OpenVoiceOS/ovos-number-parser/pull/218) ([JarbasAl](https://github.com/JarbasAl))

## [0.18.9a35](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a35) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a34...0.18.9a35)

## [0.18.9a34](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a34) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a33...0.18.9a34)

**Merged pull requests:**

- Release 0.18.9a34 [\#217](https://github.com/OpenVoiceOS/ovos-number-parser/pull/217) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.9a35 [\#216](https://github.com/OpenVoiceOS/ovos-number-parser/pull/216) ([github-actions[bot]](https://github.com/apps/github-actions))

## [0.18.9a33](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a33) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a32...0.18.9a33)

## [0.18.9a32](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a32) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a31...0.18.9a32)

**Merged pull requests:**

- Release 0.18.9a33 [\#215](https://github.com/OpenVoiceOS/ovos-number-parser/pull/215) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.9a32 [\#214](https://github.com/OpenVoiceOS/ovos-number-parser/pull/214) ([github-actions[bot]](https://github.com/apps/github-actions))

## [0.18.9a31](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a31) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a30...0.18.9a31)

## [0.18.9a30](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a30) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a29...0.18.9a30)

## [0.18.9a29](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a29) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a27...0.18.9a29)

## [0.18.9a27](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a27) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a26...0.18.9a27)

## [0.18.9a26](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a26) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a3...0.18.9a26)

**Merged pull requests:**

- Release 0.18.9a31 [\#213](https://github.com/OpenVoiceOS/ovos-number-parser/pull/213) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.9a30 [\#212](https://github.com/OpenVoiceOS/ovos-number-parser/pull/212) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.9a29 [\#211](https://github.com/OpenVoiceOS/ovos-number-parser/pull/211) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.9a26 [\#210](https://github.com/OpenVoiceOS/ovos-number-parser/pull/210) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.9a28 [\#209](https://github.com/OpenVoiceOS/ovos-number-parser/pull/209) ([github-actions[bot]](https://github.com/apps/github-actions))

## [0.18.9a3](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a3) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a2...0.18.9a3)

## [0.18.9a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a2) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a23...0.18.9a2)

## [0.18.9a23](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a23) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a22...0.18.9a23)

## [0.18.9a22](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a22) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a21...0.18.9a22)

## [0.18.9a21](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a21) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a20...0.18.9a21)

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

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a10...0.18.9a11)

## [0.18.9a10](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a10) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a9...0.18.9a10)

## [0.18.9a9](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a9) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a8...0.18.9a9)

## [0.18.9a8](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a8) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a24...0.18.9a8)

## [0.18.9a24](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a24) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.8a1...0.18.9a24)

## [0.18.8a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.8a1) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a1...0.18.8a1)

## [0.18.9a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a1) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a28...0.18.9a1)

## [0.18.9a28](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a28) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a7...0.18.9a28)

## [0.18.9a7](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a7) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a4...0.18.9a7)

## [0.18.9a4](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a4) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a5...0.18.9a4)

## [0.18.9a5](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a5) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a6...0.18.9a5)

## [0.18.9a6](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a6) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a25...0.18.9a6)

## [0.18.9a25](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a25) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.6a1...0.18.9a25)

**Merged pull requests:**

- Release 0.18.9a27 [\#208](https://github.com/OpenVoiceOS/ovos-number-parser/pull/208) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.9a23 [\#207](https://github.com/OpenVoiceOS/ovos-number-parser/pull/207) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.9a25 [\#206](https://github.com/OpenVoiceOS/ovos-number-parser/pull/206) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.9a24 [\#205](https://github.com/OpenVoiceOS/ovos-number-parser/pull/205) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.9a22 [\#204](https://github.com/OpenVoiceOS/ovos-number-parser/pull/204) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.9a21 [\#203](https://github.com/OpenVoiceOS/ovos-number-parser/pull/203) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.9a20 [\#202](https://github.com/OpenVoiceOS/ovos-number-parser/pull/202) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.9a19 [\#201](https://github.com/OpenVoiceOS/ovos-number-parser/pull/201) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.9a18 [\#200](https://github.com/OpenVoiceOS/ovos-number-parser/pull/200) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.9a16 [\#199](https://github.com/OpenVoiceOS/ovos-number-parser/pull/199) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.9a17 [\#198](https://github.com/OpenVoiceOS/ovos-number-parser/pull/198) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.9a15 [\#197](https://github.com/OpenVoiceOS/ovos-number-parser/pull/197) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.9a14 [\#196](https://github.com/OpenVoiceOS/ovos-number-parser/pull/196) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.9a13 [\#195](https://github.com/OpenVoiceOS/ovos-number-parser/pull/195) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.9a12 [\#194](https://github.com/OpenVoiceOS/ovos-number-parser/pull/194) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.9a11 [\#193](https://github.com/OpenVoiceOS/ovos-number-parser/pull/193) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.9a8 [\#192](https://github.com/OpenVoiceOS/ovos-number-parser/pull/192) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.9a10 [\#191](https://github.com/OpenVoiceOS/ovos-number-parser/pull/191) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.9a9 [\#190](https://github.com/OpenVoiceOS/ovos-number-parser/pull/190) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.9a7 [\#189](https://github.com/OpenVoiceOS/ovos-number-parser/pull/189) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.9a5 [\#188](https://github.com/OpenVoiceOS/ovos-number-parser/pull/188) ([github-actions[bot]](https://github.com/apps/github-actions))
- Release 0.18.9a6 [\#187](https://github.com/OpenVoiceOS/ovos-number-parser/pull/187) ([github-actions[bot]](https://github.com/apps/github-actions))

## [0.18.6a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.6a1) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.7a1...0.18.6a1)

## [0.18.7a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.7a1) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.4a1...0.18.7a1)

## [0.18.4a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.4a1) (2026-07-17)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.5a1...0.18.4a1)

## [0.18.5a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.5a1) (2026-07-17)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.3a1...0.18.5a1)

## [0.18.3a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.3a1) (2026-07-17)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.2a2...0.18.3a1)

## [0.18.2a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.2a2) (2026-07-17)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.2a1...0.18.2a2)

## [0.18.2a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.2a1) (2026-07-17)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.1a2...0.18.2a1)

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
