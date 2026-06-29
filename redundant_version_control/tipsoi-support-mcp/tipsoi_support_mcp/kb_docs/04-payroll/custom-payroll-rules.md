---
title: "Custom Payroll Rules"
description: "Setting up custom allowances, bonuses, deductions, and payroll rules"
category: "Payroll"
difficulty: "advanced"
tags: ["payroll", "custom", "rules", "allowances", "bonuses"]
version: "1.0"
updated_at: "2026-04-26"
---

# Custom Payroll Rules

## What are Custom Payroll Rules?

**Custom payroll rules** let you configure organization-specific allowances, bonuses, and deduction logic beyond standard salary structures. This includes:
- Variable allowances (attendance bonus, shift differentials)
- Performance-based incentives
- Department-specific rules
- Conditional deductions
- Bonus eligibility criteria

## When to Use Custom Rules

### Scenario 1: Attendance Bonus
Reward employees for perfect attendance:
- **Bonus**: ₹500/month for zero absences
- **Condition**: Absent days = 0
- **Applied to**: All employees

### Scenario 2: Shift Differentials
Extra pay for night/weekend shifts:
- **Night Shift**: +₹2,000/month
- **Weekend Shift**: +₹1,500/month
- **Applied to**: Only shift workers

### Scenario 3: Production Incentive
Bonus based on output:
- **Sales Target**: ₹100,000/month
- **Incentive**: 5% of basic salary per 20% of target achieved
- **Applied to**: Sales team only

### Scenario 4: Long Service Bonus
Loyalty reward:
- **After 5 years**: 1 month's salary bonus
- **After 10 years**: 1.5 months bonus
- **Frequency**: Annual on anniversary

## Setting Up Custom Rules

### Step 1: Define Rule Type
Choose the type of custom rule:
- **Fixed Allowance**: Same amount every month
- **Variable Allowance**: Changes based on condition
- **Performance Bonus**: Based on KPI/target
- **Deduction Rule**: Conditional deduction

### Step 2: Configure Eligibility
Who does this rule apply to?
- **All Employees**: Organization-wide
- **By Designation**: (e.g., "Sales Manager")
- **By Department**: (e.g., "Production")
- **By Grade**: (e.g., "Grade A")

### Step 3: Define Calculation Logic
How is the amount calculated?
- **Fixed amount**: ₹500 (same every month)
- **% of Basic**: 10% of basic salary
- **% of Gross**: 5% of gross salary
- **Custom formula**: (Basic × Grade Factor) + Shift Allowance

### Step 4: Set Conditions (if variable)
When does the rule apply?
- **Condition**: Attendance = 100% (zero absences)
- **Condition**: Department = Sales
- **Condition**: Hours Worked > 160
- **Operator**: AND/OR multiple conditions

### Step 5: Apply to Payroll
- **Manual**: Add per payroll run (requires approval)
- **Automatic**: Applied automatically each month
- **Review Required**: Flagged for approval before payment

## Common Custom Rules

### Rule 1: Attendance Bonus
**Name**: Perfect Attendance Bonus
**Type**: Variable Allowance
**Amount**: ₹500
**Condition**: Absent Days = 0
**Frequency**: Monthly
**Taxable**: Yes
**Applied to**: All employees

**Payroll Logic**:
```
IF Absent Days = 0 THEN
  Add ₹500 to gross salary
ELSE
  Do not add bonus
```

### Rule 2: Shift Allowance
**Name**: Night Shift Allowance
**Type**: Fixed Allowance
**Amount**: ₹2,000
**Applied to**: Employees on shift group "Night"
**Frequency**: Monthly
**Taxable**: Yes

**Payroll Logic**:
```
IF Employee Shift = "Night Shift" THEN
  Add ₹2,000 to gross salary
```

### Rule 3: Overtime Bonus (Different from OT Pay)
**Name**: Overtime Excellence Bonus
**Type**: Variable Allowance
**Amount**: ₹1,000
**Condition**: Overtime Hours > 20 in month
**Frequency**: Monthly
**Taxable**: Yes

**Payroll Logic**:
```
IF Overtime Hours > 20 THEN
  Add ₹1,000 to gross salary
ELSE
  Do not add bonus
```

### Rule 4: Performance Incentive
**Name**: Sales Commission
**Type**: Performance Bonus
**Calculation**: 5% of Basic × (Actual Sales ÷ Target)
**Applied to**: Sales Department
**Source**: External system (CRM, SalesForce)
**Frequency**: Monthly
**Taxable**: Yes

**Payroll Logic**:
```
Bonus = (₹20,000 × (₹150,000 ÷ ₹100,000)) × 5%
Bonus = (₹20,000 × 1.5) × 5% = ₹1,500
```

### Rule 5: Long Service Allowance
**Name**: Long Service Bonus
**Type**: Variable Allowance
**Amount**: Increases with tenure
  - 0-5 years: ₹0
  - 5-10 years: ₹1,000
  - 10+ years: ₹2,000
**Applied to**: All employees
**Recalculation**: On anniversary date

**Payroll Logic**:
```
Years of Service = TODAY() - Join Date
IF Years >= 10 THEN
  Add ₹2,000
ELSE IF Years >= 5 THEN
  Add ₹1,000
ELSE
  Add ₹0
```

## Advanced Rule Scenarios

### Multi-Condition Rule
**Name**: Seasonal Bonus
**Conditions**: 
- Employee Status = Active
- AND Department = Production
- AND Month IN (December, January)
- AND Attendance >= 90%

**Calculation**: 
- If all conditions met: Add 50% of basic salary

### Conditional Deduction
**Name**: Uniform Replacement Deduction
**Condition**: Uniform was issued this month
**Amount**: ₹300
**Frequency**: Once per issuance
**Tax Impact**: Non-deductible (deducted from net salary)

### Tiered Bonus
**Name**: Productivity Bonus
**Tiers**:
- 80-90% target: ₹500
- 90-100% target: ₹1,000
- 100%+ target: ₹2,000

**Calculation**:
```
IF Target Achievement 100%+ THEN
  Bonus = ₹2,000
ELSE IF Target Achievement 90-100% THEN
  Bonus = ₹1,000
ELSE IF Target Achievement 80-90% THEN
  Bonus = ₹500
ELSE
  Bonus = ₹0
```

## Testing Custom Rules

Before applying a custom rule to live payroll:

### Step 1: Test Run
1. Create the rule
2. Select test month
3. Run payroll in "draft" mode
4. Review calculations
5. Verify against manual calculation

### Step 2: Validation Checks
- ✓ Rule applies to correct employees
- ✓ Condition logic is correct
- ✓ Calculation matches expected value
- ✓ Tax treatment is correct
- ✓ No double-counting with other rules

### Step 3: Approval
- Manager reviews test results
- Confirms calculations are accurate
- Approves for live payroll

## Rule Conflict Resolution

### Scenario: Multiple Rules Apply
Employee Ali Hassan:
- Perfect Attendance Bonus: ₹500
- Night Shift Allowance: ₹2,000
- Long Service Bonus: ₹1,000

**Tipsoi combines all applicable rules**:
```
All bonuses stack: ₹500 + ₹2,000 + ₹1,000 = ₹3,500 added to gross
```

### Preventing Double-Counting
If you have overlapping rules:
- Define rule priority (Rule A overrides Rule B)
- Use exclusive conditions (Rule A applies ONLY if Condition X)
- Set rule exclusivity (Rule A excludes Rule B)

## Reporting on Custom Rules

### Monthly Report
View which employees received which custom allowances:

| Employee | Rule Applied | Amount | Month |
|---|---|---|---|
| Ali Hassan | Attendance Bonus | ₹500 | May 2026 |
| Fatima Khan | Shift Allowance | ₹2,000 | May 2026 |
| Ahmed Hassan | Sales Commission | ₹1,500 | May 2026 |

### Audit Trail
- Who created the rule
- When it was created/modified
- Which payrolls it was applied to
- Total amount disbursed per rule

## Disabling/Removing Rules

### Temporary Disable
- Rule stays configured
- Not applied to future payrolls
- Can be re-enabled anytime

### Permanent Delete
- Rule is removed
- Affects future payrolls only
- Historical payroll data unchanged

**Important**: Always verify backward impact before deleting a rule.

## Related Documents

- [Payroll Overview](./payroll-overview.md)
- [Payroll Calculation Methods](./payroll-calculation-methods.md)
- [Deductions and Allowances](./deductions-and-allowances.md)
- [Payroll Processing](./payroll-processing.md)

## FAQ

**Q: Can I apply a rule retroactively (to past months)?**
A: No, rules apply going forward. For past corrections, use manual adjustments.

**Q: What if a rule calculation results in a negative amount?**
A: Rules that calculate to negative are treated as zero (never negative bonus).

**Q: How do I track which employees received which bonus?**
A: Use the Payroll Reports section to filter by rule type and view all recipients.

**Q: Can I set an expiration date for a rule?**
A: Yes, define an "End Date" when creating the rule. It auto-disables on that date.

**Q: What happens if an employee is on leave during a bonus period?**
A: Depends on your rule setup. You can configure: "Apply regardless of leave" or "Apply only if attendance > X%"
