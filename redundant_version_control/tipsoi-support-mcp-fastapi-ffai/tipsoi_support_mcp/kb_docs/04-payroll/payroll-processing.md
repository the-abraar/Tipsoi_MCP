---
title: "Payroll Processing"
description: "Step-by-step guide to running and processing monthly payroll"
category: "Payroll"
difficulty: "intermediate"
tags: ["payroll", "processing", "monthly", "execution", "approval"]
version: "1.0"
updated_at: "2026-04-26"
---

# Payroll Processing

## Payroll Processing Checklist

Before running payroll, ensure:
- ✓ All employees have salary structures assigned
- ✓ Leave and attendance data is complete
- ✓ No pending corrections or manual entries
- ✓ Overtime calculations are finalized
- ✓ Custom rules are configured
- ✓ Bank account details are verified for all employees

## Step-by-Step Payroll Processing

### Step 1: Validate Attendance Data

**Purpose**: Ensure all punch data is complete and accurate.

**Actions**:
1. Go to **Payroll → Monthly Run → Validate Attendance**
2. Review system report:
   - Missing punch-in or punch-out records
   - Device synchronization issues
   - Manual entry overrides pending
3. Address anomalies:
   - Missing punches: Manually enter or request from employee
   - Device errors: Sync biometric device, re-pull data
   - Overrides: Review manager's notes, approve if valid

**Expected Result**: All employees have complete attendance for the month.

### Step 2: Validate Leave Data

**Purpose**: Ensure leave balance and usage are correct.

**Actions**:
1. Go to **Payroll → Monthly Run → Validate Leave**
2. Check:
   - Pending leave approvals (approve or reject)
   - Leave balance consistency (no employee over-used)
   - Leave encashment eligibility (resignation, year-end)
3. Resolve issues:
   - Approve pending leave requests
   - Adjust leave balance if needed
   - Calculate encashment for eligible employees

**Expected Result**: No pending leave issues, all balances correct.

### Step 3: Run Payroll Calculation

**Purpose**: Auto-calculate gross, deductions, and net salary.

**Actions**:
1. Go to **Payroll → Monthly Run → Start Payroll**
2. Select month and year
3. Select employees:
   - All active employees (default)
   - Specific department
   - Specific designation
   - Custom filter
4. Click "Calculate Payroll"
5. System will:
   - Calculate gross salary (basic + allowances - attendance deductions)
   - Apply overtime (if any)
   - Calculate deductions (tax, EPF, ESI, etc.)
   - Calculate net salary
   - Generate payslips

**Duration**: Usually 1-5 minutes depending on employee count.

### Step 4: Review Payroll Validation Report

**Purpose**: Identify anomalies and issues before approval.

**Report shows**:
- Employees with 0 attendance (check if on leave)
- Unusually high or low payroll amounts
- Missing bank account details
- Salary structure inconsistencies
- Overtime beyond caps
- Deduction errors

**Actions for Each Anomaly**:

| Anomaly | Action |
|---|---|
| 0 Attendance | Verify employee is on leave or resigned |
| Salary 50% below normal | Check for unpaid leave or absence |
| Missing bank account | Add/verify bank details |
| OT exceeds cap | Review OT legitimacy, may need approval |
| Negative net salary | Review deductions, fix errors |

**Resolution**:
1. Fix issues in system
2. Recalculate payroll
3. Re-review validation report
4. Repeat until no critical issues

### Step 5: Payroll Approval

**Who can approve**: HR Manager, Finance Manager, Payroll Admin

**Steps**:
1. Go to **Payroll → Monthly Run → Approve**
2. Review payroll summary:
   - Total payroll amount
   - Number of employees
   - Breakdown by department/designation
3. Check for approval signatures (workflow shows):
   - Calculated by: (date/time, user name)
   - Reviewed by: (optional, if configured)
   - Approved by: (you are approving)
4. Add comments (optional): "Approved for May 2026 payroll"
5. Click "Approve Payroll"

**System will lock payroll** - No further changes allowed (except by admin).

### Step 6: Generate Payment File

**Purpose**: Create bank transfer instruction file for salary disbursement.

**Steps**:
1. Go to **Payroll → Monthly Run → Generate Payment File**
2. Select file format:
   - Bank-specific format (e.g., NEFT for India)
   - CSV/Excel for manual processing
   - API direct to bank (if connected)
3. Verify:
   - Employee count
   - Total amount to be disbursed
   - Bank account details
4. Click "Generate File"
5. Download file
   - File includes: Employee name, account number, amount, remarks
   - Ready to submit to bank

**Security**: File is encrypted, password-protected.

### Step 7: Submit to Bank

**Manual Process**:
1. Log into bank portal
2. Upload payment file from Tipsoi
3. Verify:
   - Employee count matches
   - Total amount matches
   - No duplicate entries
4. Approve in bank system
5. Bank processes and credits salaries (usually same/next day)

**Automated Process** (if bank integration enabled):
1. Tipsoi auto-submits to bank
2. Confirmation email received
3. Check confirmation in Tipsoi

### Step 8: Send Payslips to Employees

**Purpose**: Provide employees with salary statement.

**Method 1: Email**
1. Go to **Payroll → Payslips**
2. Select month
3. Click "Send Payslips via Email"
4. Payslips sent to all employees
5. Employees can download from their dashboard

**Method 2: Print**
1. Go to **Payroll → Payslips**
2. Select month
3. Click "Print Payslips"
4. Print physical copies for distribution

**Method 3: Self-Service**
- Employees log in and download from **My Payslips**
- Available after payroll is finalized

**Payslip includes**:
- Basic salary
- Allowances (itemized)
- Deductions (itemized)
- Gross salary
- Net salary (take-home)
- Year-to-date totals
- Bank account details

### Step 9: Archive Payroll

**Purpose**: Complete the payroll cycle and prepare for next month.

**Actions**:
1. Go to **Payroll → Monthly Run → Finalize**
2. Generate final report:
   - Payroll summary
   - Department breakdown
   - Designation breakdown
   - Bank submission confirmation
3. Click "Archive Payroll"
   - Status changes from "Draft" to "Finalized"
   - No further editing allowed
   - Data locked for audit trail

## Payroll Status Lifecycle

```
Draft → Validated → Calculated → Approved → Disbursed → Finalized
```

| Status | Meaning | Editable? | Action |
|---|---|---|---|
| Draft | Not started | Yes | Add employees, configure |
| Validated | Attendance/leave checked | Yes | Fix issues |
| Calculated | Salaries computed | Yes | Review report |
| Approved | Locked for disbursal | No | Generate payment file |
| Disbursed | Paid to employees | No | Archive payroll |
| Finalized | Closed, archived | No | None |

## Common Scenarios & Solutions

### Scenario 1: Late Attendance Data
**Problem**: Critical punch data arrives after payroll calculated.
**Solution**:
1. Go to **Payroll → Monthly Run**
2. Select payroll status "Approved"
3. Click "Undo Approval"
4. Update attendance data
5. Recalculate
6. Re-approve

**Time window**: Before payment file submitted to bank.

### Scenario 2: Employee Joins Mid-Month
**Problem**: New employee should be on pro-rata salary.
**Solution**:
1. Ensure salary structure assigned (effective from join date)
2. In validation, pro-rata is calculated automatically
3. Payroll includes correct pro-rata amount
4. Process normally

### Scenario 3: Correction After Payroll Approved
**Problem**: Error found after payroll approved (e.g., wrong tax amount).
**Solution**: Cannot edit approved payroll. Instead:
1. Create **Adjustment Payroll** for next month:
   - Add deduction/allowance to fix error
   - Mark as "Correction for May"
2. Process adjustment in next payroll
3. Document in audit trail

### Scenario 4: Employee Resignation Mid-Month
**Problem**: Final salary calculation needs encashment.
**Solution**:
1. Mark employee as "Resigned" with last date
2. In payroll validation, system flags for encashment
3. Calculate pro-rata + unused leave encashment
4. Process final payroll
5. Archive once paid

### Scenario 5: Multiple Payroll Cycles
**Problem**: Organization has bi-weekly payroll for some, monthly for others.
**Solution**:
1. Create payroll cycles in organization settings
2. Filter employees by payroll cycle
3. Run separate payroll for each cycle
4. Submit separate bank files

## Payroll Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| Validation showing 0 attendance for all | Attendance data not synced | Sync biometric device, pull fresh data |
| Cannot approve (button grayed out) | Not enough permissions | Contact admin, ensure Payroll Admin role |
| Negative net salary | Too many deductions | Review and adjust deductions |
| OT not calculating | Employee not eligible | Add to OT eligible list in settings |
| Payslips not sent | Email addresses missing | Add/update email in employee profiles |
| Bank file format error | Wrong bank format selected | Select correct bank and regenerate |

## Audit Trail

All payroll actions are logged:
- Calculated by: User name, timestamp
- Validated by: (if required in workflow)
- Approved by: User name, timestamp, approval date
- Any undo/redo actions
- Any manual overrides

**Access**: **Payroll → Audit Trail** (admin only)

## Post-Payroll Tasks

### Day After Payroll
- Confirm salary credited to employees
- Check for bank errors or failed transfers
- Address any complaints from employees

### Week After Payroll
- Generate compliance reports (tax, statutory)
- File payroll data with regulatory authorities (if required)
- Archive all documentation

### Month-End
- Complete all payroll cycles
- Finalize ledger entries
- Prepare for next month payroll

## Related Documents

- [Payroll Overview](./payroll-overview.md)
- [Payroll Calculation Methods](./payroll-calculation-methods.md)
- [Payroll Reports](./payroll-reports.md)
- [FAQ - Payroll](./faq-payroll.md)

## FAQ

**Q: Can I run payroll twice in one month?**
A: No, payroll runs once per month. But you can create adjustment payroll for corrections.

**Q: What if some employees are on unpaid leave?**
A: Payroll automatically deducts salary for unpaid leave days.

**Q: Can I undo payroll after bank submission?**
A: Not recommended. You'd need to ask bank to recall transfers. Better to use adjustment payroll.

**Q: What if an employee never receives salary?**
A: Check bank transfer failure in payment file. Bank may have rejected account. Update bank details and resubmit.

**Q: How long to keep payroll records?**
A: Typically 7 years per labor law requirements. Archive securely.
