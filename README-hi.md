# dsh-railway-window — रेलवे कार्य-विंडो रजिस्टर की समय और अंकगणितीय जाँच

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-railway-window` एक रेलवे कार्य-विंडो रजिस्टर पढ़ता है — दिन का हेडर और प्रत्येक विंडो की एक पंक्ति — और उसी रजिस्टर की समय तथा अंकगणितीय संगति जाँचता है: क्या प्रत्येक विंडो अपनी कार्य-सामग्री या अपना यातायात-नियंत्रण आदेश क्रमांक दर्ज करती है, क्या आरंभ और समाप्ति के समय पढ़े जा सकते हैं और क्रम में हैं, क्या दर्ज अवधि ठीक अंतराल के बराबर है, क्या स्वीकृत अवधि आवेदित अवधि से अधिक नहीं है, क्या विंडो का प्रकार आपकी शब्दावली से आता है, क्या विंडो क्रमांक दोहराए नहीं गए हैं, और क्या रजिस्टर अपनी कार्य-तिथि तथा रेलवे प्रशासन (समूह कंपनी) घोषित करता है।

## आउटपुट कैसा दिखता है

![Terminal demo of dsh-railway-window: real output over its RW-002 fixture](https://raw.githubusercontent.com/PerryLink/dsh-railway-window/main/docs/assets/dsh-railway-window-demo.png)

इस प्लगइन का अपने ही `RW-002` टेस्ट फ़िक्स्चर पर वास्तविक आउटपुट — कोई नकली चित्र नहीं। नियम-पैक उद्धरण नहीं गढ़ता, इसलिए हर निष्कर्ष लागू किए गए खंड का नाम और यह भी बताता है कि उसका मूल पाठ इस बार प्राप्त नहीं हुआ।

## यह किन सवालों का जवाब देता है

| आपका सवाल | इसका जवाब |
|---|---|
| एक पंक्ति में न कार्य-सामग्री दर्ज है और न यातायात-नियंत्रण आदेश क्रमांक। क्या यह दर्ज होता है? | हाँ। `RW-001` हर विंडो में `workContent` या `permitNo` में से कम से कम एक भरा होने की अपेक्षा करता है और जिस पंक्ति में दोनों न हों उसे दर्ज करता है। यह केवल देखता है कि इनमें से एक भरा है; यह नहीं आँकता कि वह कार्य अनुमत दायरे के भीतर रहा या क्लीयरेंस गेज (clearance gauge) में दख़ल हुआ। |
| एक विंडो `23:30` से `01:30` तक है और उसे एक ही दिन के दो समयों के रूप में लिखा गया है। समाप्ति को आरंभ से पहले क्यों बताया जाता है? | `RW-002` दोनों क्षणों की तुलना करता है और मध्यरात्रि पार होने की स्थिति को नहीं समझता, इसलिए एक ही दिन का यह जोड़ा उलटा पढ़ा जाता है; दोनों ओर तिथि लिखें या इस नियम को बंद कर दें। यदि आरंभ और समाप्ति एक ही क्षण हों तो आरंभ को बाद का नहीं माना जाता, और जो समय पढ़ा न जा सके वह चुपचाप छोड़े जाने के बजाय अलग से दर्ज होता है। |
| अवधि कॉलम में मिनट (`120`) लिखे हैं और विंडो 08:00 से 10:00 तक थी। अंकगणित क्यों मेल नहीं खाता? | `RW-003` अंतराल को दिनों में नापता है, इसलिए मिनटों में लिखा रजिस्टर 1440 गुना भिन्न होता है; डिफ़ॉल्ट सहनशीलता 0.01 दिन है। `daysField` को दिनों में लिखी अवधि वाले कॉलम पर लगाएँ या इस नियम को बंद कर दें। यह केवल अंकगणित जाँचता है, यह नहीं कि विंडो उस कार्य के लिए पर्याप्त लंबी थी। |
| स्वीकृत अवधि आवेदित अवधि से बड़ी है। क्या दर्ज होता है, और यदि इनमें से एक कॉलम खाली हो तो? | `RW-004` उस जोड़े को दर्ज करता है, क्योंकि नियंत्रण कक्ष आवेदन से अधिक नहीं देता और सामान्यतः दोनों कॉलम उलटे भरे होते हैं। यह तभी चलता है जब `approvedMin` और `appliedMin` दोनों पढ़े जा सकें; एक न हो तो यह बताता है कि वह `skipped` में गया। इसमें स्वीकृति घटाने की कोई ऊपरी सीमा नहीं है और यह नहीं तय करता कि वह विंडो मंज़ूर होनी चाहिए थी या नहीं। |
| विंडो प्रकार कॉलम में मान भरा है, पर यह नियम कभी कुछ दर्ज नहीं करता। क्या यह चल रहा है? | नहीं। `RW-005` में `values: []` है, अर्थात् कॉन्फ़िगर नहीं किया गया, और जब तक आप अपने प्रशासन के नियमों में प्रयुक्त वर्गीकरण दर्ज नहीं करते, यह बताता है कि वह `skipped` में गया। कॉन्फ़िगर होने पर भी यह केवल देखता है कि मान आपकी सूची में है; यह तय नहीं करता कि विंडो किस वर्ग में रखी जानी चाहिए। |
| उस दिन का रजिस्टर अधूरा है: हेडर में रेलवे प्रशासन नहीं लिखा और एक ही खंड की दो विंडो का क्रमांक दोहराया गया है। कौन से नियम चलेंगे? | दो। `RW-007` ऐसे हेडर को दर्ज करता है जो कार्य-तिथि और रेलवे प्रशासन (समूह कंपनी) घोषित नहीं करता — यह केवल देखता है कि हेडर इन्हें घोषित करता है, और यदि आपके फ़ॉर्म में विंडो योजना क्रमांक भी दर्ज होता है तो `skylightPlanNo` को उसके `fields` में जोड़ा जा सकता है। `RW-006` दोहराए गए `windowNo` को दर्ज करता है और तुलना करते समय श्वेत स्थान छोड़ देता है; एक ही खंड को एक दिन में कई विंडो मिलना सामान्य है, इसलिए क्रमांक अलग-अलग रखें। |

## यह किन मानकों पर आधारित है

| दस्तावेज़ | संख्यांक | इन्हें उद्धृत करने वाले नियम |
|---|---|---|
| 《铁路营业线施工安全管理办法》 | 现行版本与条号本次未核实 | RW-001, RW-002, RW-003, RW-006, RW-007 |
| 各铁路局集团公司施工天窗管理办法（本机构配置） | 无统一标准（本条依据为台账的申请与批准两栏） | RW-004 |
| 各铁路局集团公司施工天窗管理办法（本机构配置） | 无统一标准（本条依据为本机构分类口径） | RW-005 |

**Boundary:** this plugin checks a **铁路施工天窗台账** for time and arithmetic self-consistency — that each window
records its work content or its traffic-control order number, that the start and end times parse and follow each
other, that the recorded duration equals the span, that the approved duration does not exceed the applied
duration, that the window type comes from your vocabulary, that window numbers are unique, and that the register
names its working date and railway bureau. It does **not** decide whether a window should be granted, whether
work encroached on the clearance gauge, whether it was an unsafe act, or whether it affected traffic safety.

> ### ⚠️ Read this before trusting a citation in the report
>
> **Every `excerpt` in this plugin's rule pack says, in so many words, that the clause text was not
> obtained.** The regime lives in 《铁路营业线施工安全管理办法》 and in each railway bureau's own work-window
> and traffic-control-order measures. The verification pass could not retrieve verbatim clause text, so rather
> than paraphrase a quotation the pack states the gap in the `excerpt` field itself and puts the honest
> reasoning in `note`. Every rule is therefore `warn` or `info`, and a test asserts that no rule claims a
> quotation it does not have. **When the texts are in hand, replace each `excerpt` with the real clause and
> raise `kind` to `direct`.**
>
> Three limits matter before trusting a finding:
>
> - **The plugin ships no window classification and no status vocabulary.** How windows are classified and how
>   their states are worded varies by bureau, so `RW-005` reports itself in `skipped` until you configure them.
> - **No approval-ratio ceiling is built in.** Whether an approved window may be shorter than applied for, and
>   by how much, is the bureau's rule; `RW-004` only checks that the approved figure does not exceed the
>   applied one, which is a data-entry property rather than a substantive one.
> - **The duration unit is days, and the rule says so.** `RW-003` measures the span in minutes internally and
>   expresses it in days, so a window that starts and ends on the same calendar day is measured correctly. A
>   register that records durations in minutes differs by a factor of 1440 — repoint `daysField` at a
>   day-denominated column, or disable the rule.
>
> The plugin also **does not handle crossing midnight**: a window written as two same-day times
> (`23:30` to `01:30`) will read as a reversed pair. Record the date on both sides, or disable that rule.

## Compatibility

| सतह | स्थिति |
|---|---|
| Harness | peer रेंज `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — `0.2.0-rc.2` और `0.2.1-alpha.1` दोनों को स्वीकार करने के लिए सत्यापित। **`engines.dsh` जानबूझकर घोषित नहीं**: इसका कोई पाठक नहीं और यह किसी होस्ट को अस्वीकार नहीं कर सकता |
| Node | `^22.19.0 || >=24.0.0` |
| प्लेटफ़ॉर्म | सभी (शुद्ध ESM; कोई नेटिव कोड नहीं, कोई नेटवर्क नहीं, कोई मॉडल कॉल नहीं) |
| टूल मोड | `native`, `ptc` और `both` में काम करता है; पूरे फ़ोल्डर के लिए `ptc` चुनें |

## What it does

नियम-सूची, फ़ील्ड और विस्तृत व्यवहार [README.md](README.md#what-it-does) (अंग्रेज़ी मुख्य संस्करण) में हैं। यह प्लगइन केवल उद्धृत धाराओं के सामने शाब्दिक अंतर सूचीबद्ध करता है और हर न चल पाई जाँच को `skipped` में बताता है।

## Install

```sh
dsh plugin --profile <name> add dsh-railway-window
dsh --profile <name> --dump-config | grep 'dsh-railway-window'
```

## Configuration

सभी समायोज्य पैरामीटर `src/config.ts` की Schemastery स्कीमा में हैं, इसलिए कोड बदले बिना `cordis.yml` से बदले जा सकते हैं; प्रति-नियम सीमाएँ `rules/` के नियम-पैक में हैं।

| कुंजी | प्रकार | डिफ़ॉल्ट | विवरण |
|---|---|---|---|
| `rulesFile` | string | `rules/railway-window.yaml` | नियम-पैक का पथ, पैकेज रूट के सापेक्ष |
| `disabledRules` | string[] | `[]` | बंद करने वाले नियम id; प्रत्येक `skipped` में दिखता है |
| `onlyRules` | string[] | `[]` | केवल ये नियम चलाएँ; खाली होने पर सभी नियम चलते हैं |
| `skipNotes` | string | `""` | हर `skipped` कारण के आगे जोड़ी जाने वाली टिप्पणी |
| `timeoutMs` | number | `120000` | उपकरण का सहकारी समय-सीमा बजट |

## Material format

JSON या YAML स्वीकार्य है। पूरा फ़ील्ड उदाहरण [README.md](README.md#material-format) (अंग्रेज़ी मुख्य संस्करण) में है। पढ़ने की परत में फ़ील्ड वैकल्पिक हैं और जाँच इंजन उन्हें सत्यापित करता है, इसलिए आंशिक निर्यात पर क्रैश के बजाय "अनुपस्थित" श्रेणी के निष्कर्ष मिलते हैं।

## Rule sources

नियम-डेटा कोड से अलग है: प्रत्येक नियम में दस्तावेज़, संख्या, स्रोत की अपनी क्रमांकन-प्रणाली के अनुसार धारा, शब्दशः उद्धरण और स्रोत URL होता है। लोडर लागू करता है कि उद्धरण कम से कम आठ अक्षरों का वास्तविक उद्धरण हो, और जिस जाँच का आधार केवल सामान्य सिद्धांत (`kind: derived-from-principle`, अधिकतम `warn`) या स्थानीय नीति (`kind: institutional-configuration`, अधिकतम `info`) हो, उसे कभी `error` घोषित न किया जाए।

सत्यापित सीमाएँ और जान-बूझकर **न** कहे गए निष्कर्ष [README.md](README.md#rule-sources) (अंग्रेज़ी मुख्य संस्करण) और `rules/evidence/` में हैं।

## Troubleshooting

- **प्लगइन इंस्टॉल हो गया पर टूल दिखता नहीं**: जाँचें कि `main` `lib/index.mjs` पर जाता है और `pnpm run build` ने उसे बनाया है।
- **`dsh plugin add` असंगत बताकर मना करता है**: peer range `0.1.x` और `0.2.x` दोनों को कवर करती है; बाहर होने पर स्पष्ट छूट दें: `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`।
- **कोई नियम नहीं चला**: `skipped` सरणी देखें।
- **`check` में `manifest-peers` विफल दिखता है**: यह `dsh-plugin-dev` की ज्ञात अपस्ट्रीम समस्या है; रनटाइम इंस्टॉल के समय अनुकूलता लागू करता है।
- **समय खिसका हुआ लगता है**: सारी गणना दिए गए स्ट्रिंग पर वॉल-क्लॉक है।

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-railway-window
```

अंतिम कमांड `../_shared` का साझा किट `src/shared/` में कॉपी करता है; हर साझा बदलाव के बाद इसे दोबारा चलाएँ।

## License

[Apache License 2.0](LICENSE) © 2026 dsh-railway-window contributors.
