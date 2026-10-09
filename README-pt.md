# dsh-railway-window — Verificação de tempos e aritmética do registo de janelas de trabalho ferroviário

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-railway-window` lê um registo ferroviário de janelas de trabalho —o cabeçalho do dia mais uma linha por janela— e verifica a coerência temporal e aritmética desse próprio registo: se cada janela regista o seu conteúdo de trabalho ou o seu número de ordem de controlo de tráfego, se o início e o fim são analisáveis e sucessivos, se a duração registada é igual ao intervalo, se a duração aprovada não excede a solicitada, se o tipo de janela vem do seu vocabulário, se os números de janela não se repetem e se o registo declara a sua data de trabalho e a administração ferroviária (grupo empresarial).

## Como é a saída

![Terminal demo of dsh-railway-window: real output over its RW-002 fixture](https://raw.githubusercontent.com/PerryLink/dsh-railway-window/main/docs/assets/dsh-railway-window-demo.png)

Saída real deste plugin sobre o seu próprio fixture de teste `RW-002` — não é uma simulação. O pacote de regras não inventa citações, por isso cada achado nomeia a cláusula aplicada e avisa que o seu texto não foi obtido.

## O que ele responde

| Você pergunta | O que ele responde |
|---|---|
| Uma linha não regista nem o conteúdo de trabalho nem o número da ordem de controlo de tráfego. Isso é reportado? | Sim. `RW-001` exige que em cada janela esteja preenchido pelo menos um dos dois, `workContent` ou `permitNo`, e reporta a linha em que faltam ambos. Verifica apenas que um deles está preenchido; não julga se a obra se manteve dentro do âmbito autorizado nem se algo invadiu o gabarito de circulação. |
| Uma janela vai de `23:30` a `01:30` e está escrita como duas horas do mesmo dia. Porque é reportado que o fim é anterior ao início? | `RW-002` compara os dois instantes e não modela a passagem da meia-noite, pelo que um par do mesmo dia é lido invertido; registe a data dos dois lados ou desative a regra. Se o início e o fim coincidirem, considera-se que o início não é posterior, e uma hora que não se consegue analisar é reportada à parte em vez de ser omitida em silêncio. |
| A coluna da duração está em minutos (`120`) e a janela foi das 08:00 às 10:00. Porque é que a aritmética não bate certo? | `RW-003` mede o intervalo em dias, pelo que um registo em minutos difere por um fator de 1440; a tolerância de fábrica é de 0,01 dia. Aponte `daysField` para uma coluna de duração expressa em dias ou desative a regra. Verifica apenas a aritmética, nunca se a janela foi suficientemente longa para a obra. |
| A duração aprovada é maior do que a solicitada. O que é reportado, e o que acontece se faltar uma das duas colunas? | `RW-004` reporta esse par, porque um despachante não concede mais do que foi solicitado e o habitual é as duas colunas estarem trocadas. Só é executada quando `approvedMin` e `appliedMin` são analisáveis; se faltar um, reporta que entrou em `skipped`. Não inclui qualquer tecto de redução da aprovação e não conclui se a janela devia ser concedida. |
| A coluna do tipo de janela tem valor, mas a regra nunca reporta nada. Está a ser executada? | Não. `RW-005` vem com `values: []`, ou seja, por configurar, e reporta que entrou em `skipped` até indicar as classificações usadas pelas medidas da sua administração. Mesmo configurada, verifica apenas se o valor consta da sua lista; não decide em que classe uma janela deve ser enquadrada. |
| O registo do dia está incompleto: o cabeçalho não nomeia a administração e duas janelas do mesmo troço repetem número. Que regras disparam? | Duas. `RW-007` reporta um cabeçalho que não declara a data de trabalho e a administração ferroviária (grupo empresarial) — verifica apenas que o cabeçalho as declare, e pode acrescentar `skylightPlanNo` aos seus `fields` se o seu formulário também registar um número de plano. `RW-006` reporta o `windowNo` repetido, comparando com os espaços em branco ignorados; um troço com várias janelas no mesmo dia é normal, pelo que deve numerá-las de forma distinta. |

## Normas que segue

| Documento | Número | Regras que o citam |
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

| Superfície | Estado |
|---|---|
| Harness | Faixa de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificada para aceitar tanto `0.2.0-rc.2` quanto `0.2.1-alpha.1`. **`engines.dsh` não é declarado**: não tem leitor e não pode recusar nenhum host |
| Node | `^22.19.0 || >=24.0.0` |
| Plataformas | Todas (ESM puro; sem código nativo, sem rede, sem chamada ao modelo) |
| Modo de ferramenta | Funciona em `native`, `ptc` e `both`; para um diretório inteiro use `ptc` |

## What it does

A tabela de regras, os campos e o comportamento detalhado estão em [README.md](README.md#what-it-does) (versão principal em inglês). O plugin apenas lista divergências literais frente às cláusulas citadas e indica em `skipped` cada verificação que não pôde ser executada.

## Install

```sh
dsh plugin --profile <name> add dsh-railway-window
dsh --profile <name> --dump-config | grep 'dsh-railway-window'
```

## Configuration

Todos os parâmetros ajustáveis ficam no esquema Schemastery de `src/config.ts`, portanto mudam pelo `cordis.yml` sem editar código; os limites por regra ficam no pacote de regras sob `rules/`.

| Chave | Tipo | Padrão | Descrição |
|---|---|---|---|
| `rulesFile` | string | `rules/railway-window.yaml` | Caminho do pacote de regras, relativo à raiz do pacote |
| `disabledRules` | string[] | `[]` | Ids de regras a desativar; cada uma aparece em `skipped` |
| `onlyRules` | string[] | `[]` | Executar apenas estas regras; vazio executa todas |
| `skipNotes` | string | `""` | Nota acrescentada a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Orçamento de tempo limite cooperativo da ferramenta |

## Material format

Aceita JSON ou YAML. O exemplo completo de campos está em [README.md](README.md#material-format) (versão principal em inglês). Os campos são opcionais na camada de leitura e validados pelo motor, de modo que uma exportação parcial gera achados sobre o que falta em vez de falhar.

## Rule sources

Os dados das regras ficam separados do código: cada regra traz documento, número, cláusula na numeração própria da fonte, trecho literal e URL de origem. O carregador impõe que o trecho seja citação real de pelo menos oito caracteres e que uma verificação baseada apenas em princípio geral (`kind: derived-from-principle`, teto `warn`) ou em política local (`kind: institutional-configuration`, teto `info`) nunca seja declarada `error`.

Os limites verificados e as conclusões deliberadamente **não** afirmadas estão em [README.md](README.md#rule-sources) (versão principal em inglês) e em `rules/evidence/`.

## Troubleshooting

- **O plugin instala mas a ferramenta não aparece**: confirme que `main` resolve para `lib/index.mjs` e que `pnpm run build` o gerou.
- **`dsh plugin add` recusa o pacote**: a faixa de peers cobre `0.1.x` e `0.2.x`; fora dela, conceda isenção explícita com `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`.
- **Uma regra não executou**: leia o arranjo `skipped`.
- **`check` informa `manifest-peers` como falha**: problema conhecido do `dsh-plugin-dev`; o runtime aplica a compatibilidade na instalação.
- **Os horários parecem deslocados**: toda a aritmética é de hora local sobre as cadeias fornecidas.

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-railway-window
```

O último comando copia o kit compartilhado de `../_shared` para `src/shared/`; execute-o novamente após cada alteração compartilhada.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-railway-window contributors.
