---
title: "Payroll Overview"
description: "Complete guide to payroll management, calculation, and processing"
category: "Payroll"
difficulty: "intermediate"
tags: ["payroll", "salary", "processing", "finance", "compensation"]
version: "1.0"
updated_at: "2026-04-26"
---

# Payroll Overview

## What is Payroll?

**Payroll** is the process of calculating, processing, and disbursing employee salaries and wages. In Tipsoi, payroll is a comprehensive module that handles:
- Salary structure setup
- Attendance-based deductions
- Overtime calculations
- Tax and statutory deductions
- Leave encashment
- Bonus and incentive processing
- Payment distribution and reporting

Tipsoi automates the entire payroll cycle, ensuring accuracy and compliance with local labor laws.

## Why Payroll Management Matters

Payroll is critical because it:
- **Ensures timely payment** — Employees paid on schedule
- **Maintains compliance** — Follows tax laws, labor regulations, social security
- **Reduces errors** — Automated calculations prevent manual mistakes
- **Provides transparency** — Clear salary breakdowns for employees
- **Enables reporting** — Audits, tax filings, statutory reports
- **Improves morale** — Accurate, on-time payments boost employee satisfaction

## Key Payroll Concepts

### Salary Structure
The breakdown of employee compensation:
- **Basic Salary** — Fixed monthly base pay
- **Allowances** — Housing, travel, special allowances (fixed or variable)
- **Deductions** — Tax, insurance, loans, penalties
- **Gross Salary** — Basic + all allowances before deductions
- **Net Salary** — Gross - all deductions (amount employee receives)

### Pay Cycle
The frequency of payroll processing:
- **Monthly** — Most common (1st to last day of month)
- **Bi-weekly** — Every 2 weeks
- **Weekly** — Every week
- **Custom** — Any schedule configured by organization

### Attendance Impact
How attendance affects salary:
- **Full attendance** — Paid 100% salary
- **Partial attendance** — Salary deducted based on absent days
- **Leave taken** — Deducted or covered by leave balance (depends on leave type)
- **Overtime** — Added pay for hours beyond scheduled shift

### Overtime (OT)
Extra hours worked beyond the standard shift:
- **OT Rate** — Typically 1.5x or 2x the hourly rate
- **OT Limit** — Some countries cap OT per month
- **OT Eligibility** — Depends on designation (hourly workers usually eligible)
- **OT Calculation** — Hours × hourly rate × multiplier

### Statutory Deductions
Mandatory deductions as per law:
- **Income Tax** — Tax on salary (depends on annual income)
- **Social Security** — Pension/provident fund contributions
- **Health Insurance** — Employer + employee contributions
- **Unemployment Insurance** — As per local law

### Leave Encashment
Payout for unused leave days:
- Triggered when employee leaves or at year-end carry-forward limit
- Amount = Daily salary × unused days
- Subject to company policy and local law

## Payroll Phases in Tipsoi

### Phase 1: Setup
- Configure salary structures for different roles
- Define overtime rules and rates
- Set up tax calculations
- Configure statutory deduction rules

### Phase 2: Monthly Processing
- Validate attendance data
- Calculate gross salary
- Apply deductions (statutory + voluntary)
- Calculate overtime (if applicable)
- Generate payslips

### Phase 3: Review & Approval
- Manager/Admin reviews salary calculations
- Address any anomalies (zero attendance, salary spikes, missing data)
- Approve final payroll

### Phase 4: Disbursement
- Generate payment file for bank
- Disburse salaries to employee accounts
- Generate payroll reports and documentation

## Payroll Workflow

```
┌─────────────────┐
│  Month Begins   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Validate Attendance Data       │
│  - Check for missing punches    │
│  - Verify device sync           │
│  - Flag anomalies               │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Calculate Gross Salary         │
│  - Basic + allowances           │
│  - Apply attendance deductions  │
│  - Calculate overtime           │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Apply Deductions               │
│  - Statutory taxes              │
│  - Insurance premiums           │
│  - Loan repayments              │
│  - Other voluntary deductions   │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Calculate Net Salary           │
│  (Gross - Deductions)           │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Review & Approve               │
│  - Check for errors             │
│  - Verify bank details          │
│  - Approve final amounts        │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Disburse Salaries              │
│  - Generate payment file        │
│  - Submit to bank               │
│  - Send payslips to employees   │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Archive & Report               │
│  - Generate payroll reports     │
│  - Tax documentation            │
│  - Audit trail creation         │
└─────────────────────────────────┘
```

## How to Access Payroll

1. **Log in** to Tipsoi admin dashboard
2. Go to **Payroll** from the main menu
3. Choose your task:
   - **Setup** → Configure salary structures
   - **Monthly Run** → Execute payroll
   - **Reports** → View payroll analytics
   - **Payslips** → Employee salary documents

## Key Features

### Automated Calculations
- Attendance-based pro-rata salary
- Overtime calculations
- Statutory deductions (tax, insurance)
- Leave encashment

### Validation & Anomaly Detection
- Detects zero-attendance employees
- Flags salary anomalies
- Validates bank account details
- Confirms leave balance consistency

### Multi-Currency Support
- Configure currency for each organization
- Display all amounts in organization currency
- Exchange rate handling for international transfers

### Compliance & Audit Trail
- Complete audit log of all payroll actions
- User approval tracking (who approved what, when)
- Export for regulatory compliance
- Tax documentation generation

### Self-Service Payslips
- Employees access their payslips anytime
- View salary breakdown
- Download for tax filing
- Historical records

## Payroll Security

All payroll operations follow strict security:
- **Role-based access** — Only authorized personnel can run payroll
- **Approval workflow** — Payroll requires manager/admin approval
- **Secondary authentication** — 2FA/PIN for final execution
- **Encryption** — All payroll data encrypted in transit and at rest
- **Audit logging** — Every action logged with user, timestamp, changes

## Common Payroll Scenarios

### Scenario 1: New Employee (Mid-Month Hire)
- Pro-rata salary for partial month
- No full-month deductions
- Standard calculation from join date

### Scenario 2: Employee on Long Leave
- Unpaid leave: salary deducted for leave days
- Paid leave: salary unchanged (leave balance deducted)
- Partial leave: pro-rata calculation

### Scenario 3: Overtime-Heavy Month
- Overtime hours added to gross salary
- OT multiplier applied (typically 1.5x)
- Appears as separate line item in payslip

### Scenario 4: Resignation With Encashment
- Final payslip includes unused leave payout
- Calculated as daily rate × remaining days
- Subject to company policy limits

## Troubleshooting Common Issues

**Q: Payroll shows 0 for an employee even though they worked**
- Check attendance data (missing punches)
- Verify employee is active
- Check salary structure assignment

**Q: Overtime not calculating correctly**
- Verify OT eligibility in employee profile
- Check shift configuration
- Confirm OT rate setting in salary structure

**Q: Cannot approve payroll (button grayed out)**
- Ensure you have payroll admin role
- Check for data validation errors
- See validation report for anomalies

## Related Documents

- [Payroll Calculation Methods](./payroll-calculation-methods.md)
- [Custom Payroll Rules](./custom-payroll-rules.md)
- [Overtime Management](./overtime-management.md)
- [Deductions and Allowances](./deductions-and-allowances.md)
- [Payroll Processing](./payroll-processing.md)
- [Payroll Reports](./payroll-reports.md)

## Next Steps

1. **For Setup**: [Configure salary structures](./payroll-calculation-methods.md)
2. **For Monthly Run**: [Process payroll](./payroll-processing.md)
3. **For Analysis**: [View payroll reports](./payroll-reports.md)

**Need more help?** Contact support or check the FAQ section below.

## Frequently Asked Questions

**Q: How often should I run payroll?**
A: Standard is monthly, but you can configure bi-weekly or weekly cycles in your organization settings.

**Q: Can I run payroll manually?**
A: Yes, but Tipsoi recommends using the automated monthly schedule. Manual runs are possible with manager approval.

**Q: What if I made a mistake in payroll?**
A: Contact your admin. Previous payrolls cannot be edited, but they can create an adjustment entry for the next month.

**Q: How is tax calculated?**
A: Tax depends on annual income and your country's tax slabs. Configure these in the tax settings section.

**Q: Can employees see their payslips?**
A: Yes, after payroll is finalized, employees can access their payslips in their dashboard under "My Payslips."

**Q: What happens to unused leave during payroll?**
A: Depends on your leave policy. Unused leave can be carried forward to next year (if policy allows) or encashed (paid out).
