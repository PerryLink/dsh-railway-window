# dsh-railway-window — 铁路施工天窗台账核对

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-railway-window` 读取一份铁路施工天窗台账——当日表头加每条天窗一行——核对这份台账自身的时间与算术自洽：每条天窗是否记录了作业内容或施工命令号、起止时间是否可解析且先后成立、所记天窗时长是否等于起止之差、批准时长是否不超过申请时长、天窗类型是否出自你配置的取值、天窗编号是否唯一、台账是否声明施工日期与铁路局（集团公司）。

## 实际输出长什么样

![Terminal demo of dsh-railway-window: real output over its RW-002 fixture](https://raw.githubusercontent.com/PerryLink/dsh-railway-window/main/docs/assets/dsh-railway-window-demo.png)

本插件对自己 `RW-002` 测试夹具的**真实输出**，不是示意图。规则库不伪造引文，因此每条发现都会同时写明所引条款，以及该条款原文本次未取得。

## 它回答什么问题

| 你会问 | 它怎么答 |
|---|---|
| 有一行既没填作业内容，也没填施工命令号，会被报出来吗？ | 会。`RW-001` 要求每条天窗的 `workContent` 与 `permitNo` 至少填一个，两项都缺时报出该行。它只核对是否填了其中一个，不判断该施工是否在准许范围内、是否侵入限界。 |
| 一条天窗从 `23:30` 到 `01:30`，写成两个同日时刻，为什么报结束时间早于开始时间？ | `RW-002` 只比较两个时刻，不处理跨零点，因此同日的一对时刻会被读成前后颠倒；请在时间栏补上日期，或停用本条。起止为同一时刻时视为不晚于；时间无法解析时会单独报出，不会静默跳过。 |
| 时长栏填的是分钟（`120`），而天窗是 08:00 到 10:00，为什么算术对不上？ | `RW-003` 计算的是两个时刻之间的天数，分钟口径的台账会相差 1440 倍，容差出厂为 0.01 天。请把 `daysField` 指向以天为单位的时长栏，或停用本条。它只核对算术，不判断天窗时长是否够用。 |
| 批准时长比申请时长还大，会怎么报？两栏缺一个呢？ | `RW-004` 会报出这一对数值——调度批准不会给出比申请更长的天窗，两栏通常是填反或抄错。它只在 `approvedMin` 与 `appliedMin` 都有可解析数值时执行；缺一即进 `skipped`。它不硬编码任何削减比例上限，也不判断该天窗申请是否应当批准。 |
| 天窗类型栏填了值，可这条规则从来不报任何东西，它到底跑没跑？ | 没跑。`RW-005` 出厂 `values: []`，即未配置，在你按本局办法填入分类取值之前，它只报告自己进了 `skipped`。即便配置好，它也只核对所填值是否在册，不判断该天窗应归入哪一类。 |
| 当天的台账信息不全：表头没写铁路局，同一区间的两条天窗编号还重复。会报哪些规则？ | 两条。`RW-007` 报出未声明施工日期与铁路局（集团公司）的表头——它只核对表头是否声明了这两项；若本机构表式还在表头记录天窗计划号，可把 `skylightPlanNo` 加进 `fields`。`RW-006` 报出重复的 `windowNo`，比较时忽略空白字符；同一区间同一天分多次给点属正常情形，请用不同的编号。 |

## 依据的标准

| 文件 | 文号 | 引用它的规则 |
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

| 项目 | 状态 |
|---|---|
| Harness | 对等版本范围 `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` —— 已实测同时接受 `0.2.0-rc.2` 与 `0.2.1-alpha.1`。**刻意不声明 `engines.dsh`**：它没有任何读取者，也无法拒装任何宿主 |
| Node | `^22.19.0 || >=24.0.0` |
| 平台 | 全平台（纯 ESM；无原生代码、无联网、不调用模型） |
| 工具模式 | `native` / `ptc` / `both` 均可；批量校验整个目录时建议 `ptc`，schema 成本只付一次 |

## What it does

规则表、字段说明与行为细节见 [README.md](README.md#what-it-does)（英文主版本）。本插件只列出材料与所引条款之间的字面差异，并对无法执行的检查在 `skipped` 中逐项说明。

## Install

```sh
dsh plugin --profile <name> add dsh-railway-window
dsh --profile <name> --dump-config | grep 'dsh-railway-window'
```

## Configuration

全部可调参数都在 `src/config.ts` 的 Schemastery schema 中，只改 `cordis.yml` 即可生效，无需改代码；逐条阈值在 `rules/` 下的规则库文件里。

| 键 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `rulesFile` | string | `rules/railway-window.yaml` | 规则库文件路径，相对插件包根目录 |
| `disabledRules` | string[] | `[]` | 要停用的规则 id 列表；每条都会出现在 `skipped` 中 |
| `onlyRules` | string[] | `[]` | 只执行这些规则 id；留空表示执行全部规则 |
| `skipNotes` | string | `""` | 附加到每条 `skipped` 说明后的备注 |
| `timeoutMs` | number | `120000` | 工具协作式超时预算（毫秒） |

## Material format

支持 JSON 与 YAML。完整字段示例见 [README.md](README.md#material-format)（英文主版本）。字段在读取层是可选的，由检查引擎校验，因此部分导出的材料会产生"缺项"类差异，而不是让程序崩溃。

## Rule sources

规则数据与代码分离，每条规则都带文件名、文号、按原文自身编号体系的条款号、逐字摘录与来源地址。加载期强制：摘录必须是真实引文且不少于八个字符；依据仅为原则性条款（`kind: derived-from-principle`，严重级上限 `warn`）或本机构配置（`kind: institutional-configuration`，上限 `info`）的检查不得标为 `error`。夸大依据的规则库会在加载期失败，而不会产出一份看起来很有底气的报告。

核验中确认的边界与"刻意没有作出的结论"见 [README.md](README.md#rule-sources)（英文主版本）与随包的 `rules/evidence/` 目录。

## Troubleshooting

- **插件装上了但工具不出现**：确认 `main` 指向 `lib/index.mjs` 且 `pnpm run build` 已生成该文件；`main` 写错会让加载器静默跳过该条目。
- **`dsh plugin add` 报版本不兼容**：peer 范围覆盖 `0.1.x` 与 `0.2.x`；若运行时在其之外，可显式豁免：`dsh plugin --profile <name> allow-version <包名@版本> --dsh-version <runtime> --accept-risk`
- **某条规则没有执行**：查看 `skipped` 数组，其中写明了规则 id 与原因。
- **`check` 报 `manifest-peers` 失败**：静态检查器比对的是一份早于 0.2 世代的硬编码 peer 范围；安装期的 peer 校验以运行时为准。这是 `dsh-plugin-dev` 的已知上游问题。
- **时间看起来偏移**：全部计算都是对输入字符串做墙上时钟运算，不做时区换算。

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-railway-window
```

第 4 项把 `../_shared` 的共享件同步进 `src/shared/`；每次改动共享件后都要重跑。

## License

[Apache License 2.0](LICENSE) © 2026 dsh-railway-window contributors.
