---
title: "Payroll Calculation Methods"
description: "Understanding salary structures and how payroll is calculated"
category: "Payroll"
difficulty: "intermediate"
tags: ["payroll", "salary", "structure", "calculation", "gross", "net"]
version: "1.0"
updated_at: "2026-04-26"
---

# Payroll Calculation Methods

## Understanding Salary Structure

A **salary structure** defines how an employee's monthly salary is composed. It consists of:
- **Earnings** (Basic, Allowances)
- **Deductions** (Statutory, voluntary)
- **Net** (What employee receives)

## Basic Salary vs Gross Salary

### Basic Salary
- The fixed base salary amount
- Used as reference for calculating overtime
- Forms the foundation of gross salary
- Example: ₹20,000/month

### Gross Salary
- Basic + all allowances (before deductions)
- Used for tax calculation
- Sum of all positive earnings
- Example: ₹25,000 (Basic ₹20,000 + House Allowance ₹3,000 + Travel ₹2,000)

### Net Salary
- Gross - all deductions
- Amount actually paid to employee
- Takes home amount
- Example: ₹22,500 (after tax ₹1,500, insurance ₹1,000)

## Earnings Components

### Fixed Allowances
Allowances that remain constant every month:

| Allowance Type | Description | Example | Taxable? |
|---|---|---|---|
| House Rent Allowance (HRA) | Housing assistance | ₹5,000 | Yes |
| Travel Allowance | Transport costs | ₹2,000 | Yes |
| Medical Allowance | Healthcare costs | ₹1,000 | No (up to limit) |
| Special Allowance | Role-specific benefits | ₹3,000 | Yes |
| Communication Allowance | Phone/internet | ₹500 | No |

### Variable Allowances
Allowances that change based on conditions:

| Type | Based On | Example |
|---|---|---|
| Attendance Bonus | Perfect attendance | ₹500/month |
| Shift Allowance | Night/weekend shifts | ₹2,000 + basic |
| Production Incentive | Output achievement | 5% of sales |
| Performance Bonus | KPI achievement | 10-50% of basic |

### Leave Encashment
Payout for unused leave days:
- **Calculation**: Daily salary × Unused leave days
- **Daily Salary**: Gross salary ÷ 30 (or working days in month)
- **Eligibility**: Usually at year-end or on resignation
- **Limit**: Most policies cap carry-forward (e.g., 5 days max)

## Deduction Components

### Statutory Deductions
Mandatory deductions as per law:

| Deduction | Basis | Notes |
|---|---|---|
| Income Tax | Annual income | Depends on tax slab |
| Employee Provident Fund (EPF) | % of gross salary | Usually 12% |
| Employee State Insurance (ESI) | Salary below threshold | Usually 0.75% |
| Professional Tax | Annual income | Varies by state |

### Voluntary Deductions
Optional deductions employee consents to:

| Deduction | Description | Example |
|---|---|---|
| Loan Repayment | Monthly loan installment | ₹5,000 |
| Health Insurance | Employee share | ₹2,000 |
| Gratuity Fund | Retirement contribution | ₹1,000 |
| Union Dues | Trade union fees | ₹200 |

## Attendance-Based Calculation

### Full Attendance
If employee worked all scheduled days:
```
Gross Salary = As configured in salary structure
```

### Partial Attendance
If employee was absent for some days:
```
Daily Rate = Gross Salary ÷ Working Days in Month
Deduction = Daily Rate × Absent Days
Adjusted Gross = Gross Salary - Deduction
```

### Example:
- Gross Salary: ₹30,000
- Working Days in Month: 26
- Absent Days: 2
- Daily Rate: ₹30,000 ÷ 26 = ₹1,153.85
- Deduction: ₹1,153.85 × 2 = ₹2,307.70
- **Adjusted Gross: ₹27,692.30**

## Leave Impact on Salary

### Paid Leave (e.g., Annual Leave, Casual Leave)
- **Salary impact**: NONE (employee still paid 100%)
- **Leave balance impact**: Deducted from leave balance
- **Attendance**: Marked as "On Leave" (not "Absent")
- **Payroll**: Gross salary unchanged

### Unpaid Leave
- **Salary impact**: Deducted from gross (calculated as daily rate × days)
- **Leave balance impact**: Deducted from balance
- **Attendance**: Marked as "Leave"
- **Payroll**: Gross salary reduced

### Half-Day Leave
- **Salary impact**: Half of daily rate deducted
- **Attendance**: Half-day marked with status
- **Payroll**: Gross reduced by 0.5 × daily rate

### Leave Encashment
- **When**: End of financial year or on resignation
- **Amount**: Daily salary × unused days
- **Added to**: Final payslip as separate line item
- **Tax**: Taxable as per law

## Overtime Calculation

### Overtime Rate
```
Hourly Rate = Basic Salary ÷ 160 (typical working hours/month)
OT Amount = Overtime Hours × Hourly Rate × Multiplier
```

### Multiplier
- Regular OT: 1.5× the hourly rate (time and a half)
- Weekend OT: 2× the hourly rate (double time)
- Night OT: 1.25× to 2× depending on policy

### Example:
- Basic: ₹20,000
- Hourly Rate: ₹20,000 ÷ 160 = ₹125/hour
- Overtime Hours: 10 hours
- OT Multiplier: 1.5×
- **OT Amount: 10 × 125 × 1.5 = ₹1,875**

## Pro-Rata Salary (New Joiner / Separation)

### New Joiner Mid-Month
```
Pro-Rata Days = Days worked in month
Pro-Rata Salary = Gross Salary × (Pro-Rata Days ÷ Total Days in Month)
```

### Example:
- Join Date: May 15
- Days in May: 31
- Pro-Rata Days: 17 (May 15-31)
- Gross Salary: ₹30,000
- **Pro-Rata: ₹30,000 × (17 ÷ 31) = ₹16,613**

## Net Salary Calculation

### Full Formula
```
Net Salary = Gross Salary 
           - Income Tax
           - Statutory Deductions (EPF, ESI, etc.)
           - Voluntary Deductions
           + Overtime (if any)
           + Encashment (if any)
           + Bonuses/Incentives
           - Penalties/Adjustments
```

### Step-by-Step Example

**Employee: Ali Hassan**

| Component | Amount |
|---|---|
| Basic Salary | ₹20,000 |
| HRA | ₹5,000 |
| Travel Allowance | ₹2,000 |
| **Gross Salary** | **₹27,000** |
| Absent Days: 1 | |
| Daily Rate | ₹27,000 ÷ 26 = ₹1,038 |
| Deduction for absence | -₹1,038 |
| Adjusted Gross | ₹25,962 |
| Income Tax (10%) | -₹2,596 |
| EPF (12%) | -₹3,115 |
| ESI (0.75%) | -₹195 |
| Health Insurance | -₹1,000 |
| **Net Salary** | **₹19,056** |

## Tax Calculation Methods

### Slab-Based Tax
Tax calculated on annual income based on brackets:

```
Annual Income: ₹360,000
Tax Brackets (Example):
- ₹0 - ₹250,000: 0%
- ₹250,001 - ₹500,000: 5%

Tax = ₹0 (first 250,000) + (₹110,000 × 5%) = ₹5,500
Monthly Tax = ₹5,500 ÷ 12 = ₹458
```

### Fixed Percentage Tax
Simple percentage of gross salary:
```
Monthly Tax = Gross Salary × Tax Rate
Example: ₹27,000 × 10% = ₹2,700/month
```

### No Tax Threshold
If annual gross < tax exemption limit:
```
Annual Income: ₹200,000 (below ₹250,000 threshold)
Tax: ₹0 (no tax applicable)
```

## Related Documents

- [Payroll Overview](./payroll-overview.md)
- [Custom Payroll Rules](./custom-payroll-rules.md)
- [Deductions and Allowances](./deductions-and-allowances.md)
- [Overtime Management](./overtime-management.md)

## FAQ

**Q: What's the difference between basic and gross?**
A: Basic is the fixed base salary. Gross is basic + all allowances combined.

**Q: Is overtime added to gross or net?**
A: Overtime is calculated separately and added to gross. Then deductions apply to the total.

**Q: How is leave encashment taxed?**
A: It depends on your country's tax law. Some allow partial exemption (first ₹10 lakh), others tax fully.

**Q: Can I change salary structure mid-year?**
A: Yes, but new structure applies from the effective date onward. Previous months use old structure.

**Q: What if actual working hours differ from standard shift?**
A: Tipsoi auto-calculates based on actual punch times. If less than shift duration, pro-rata is applied.
