/**
 * dsh-railway-window — table shape and material contract.
 *
 * The plugin is data-only: this file declares which columns the material may use
 * and how they map onto canonical field names; the shared kit supplies the reader
 * and the check engine, and the rule pack declares every check. Adding a check
 * that fits an existing kind is a rule-pack edit, not a code change.
 */

import { canonicaliseRow, parseTable, type TableSpec } from './shared/table.ts'
import { runTableCheck, type TableCheckOptions, type TableInput } from './shared/rows.ts'
import type { Ruleset } from './shared/rules.ts'

/** Tool id exposed to the model, and the row id in `cordis.patch.yml`. */
export const TOOL_NAME = 'railway_window'

/** The register's column aliases, declared once so both the spec and the guard see them. */
const COLUMNS = {
  windowNo: ['序号', '天窗编号', '编号', 'windowNo'],
  windowType: ['天窗类型', '施工类型', '类型', 'windowType'],
  line: ['线别', '线路', '行别', 'line'],
  section: ['区间', '施工地点', '里程', 'section'],
  startAt: ['开始时间', '天窗开始', '起始时间', 'startAt'],
  endAt: ['结束时间', '天窗结束', '终止时间', 'endAt'],
  durationMin: ['天窗时长', '时长分钟', '历时', 'durationMin'],
  appliedMin: ['申请时长', '计划时长', 'appliedMin'],
  approvedMin: ['批准时长', '实际批准', 'approvedMin'],
  workContent: ['作业内容', '施工内容', '作业项目', 'workContent'],
  permitNo: ['施工命令号', '调度命令号', '准许号', 'permitNo'],
  applicant: ['申请单位', '施工单位', '作业单位', 'applicant'],
  approver: ['批准人', '调度员', 'approver'],
  status: ['状态', '天窗状态', 'status'],
} as const

/** How the material declares its table. */
export const SPEC: TableSpec = {
  rowKeys: ['rows', 'items', 'windows', '天窗'],
  columns: COLUMNS,
  header: {
  date: ['date', '施工日期', '天窗日期'],
  bureau: ['bureau', '铁路局', '集团公司'],
  skylightPlanNo: ['skylightPlanNo', '天窗计划号', '计划编号'],
  checkedAt: ['checkedAt', '核对日期'],
  },
}

/** Fields the material must carry somewhere for the reader to accept it. */
export const REQUIRE_ANY_OF = [
  '天窗编号',
  'windowNo',
  '开始时间',
  'startAt',
  '结束时间',
  'endAt',
  '作业内容',
  'workContent',
]

/**
 * Parse the material and attach its canonical field names.
 * @param source - JSON or YAML text.
 * @param target - description of where the material came from.
 * @returns the normalized table, with each row's aliases resolved to field names.
 */
export function parseMaterial(source: string, target: string): TableInput {
  const table = parseTable(source, target, {
    ...SPEC,
    ...(REQUIRE_ANY_OF === undefined ? {} : { requireAnyOf: REQUIRE_ANY_OF }),
  })
  for (const row of table.rows) canonicaliseRow(row, SPEC)
  return table
}

/**
 * Run the rule pack against the material.
 * @param input - normalized table.
 * @param ruleset - validated rule pack.
 * @param options - plugin identity, clock value, rule selection and overrides.
 * @returns the report.
 */
export function runCheck(input: TableInput, ruleset: Ruleset, options: TableCheckOptions) {
  return runTableCheck(input, ruleset, options)
}

export type { TableCheckOptions, TableInput }
