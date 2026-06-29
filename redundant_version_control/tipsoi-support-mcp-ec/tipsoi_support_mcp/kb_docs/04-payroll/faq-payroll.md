---
title: "Payroll FAQ"
description: "Frequently asked questions about payroll in Tipsoi"
category: "Payroll"
difficulty: "beginner"
tags: ["payroll", "faq", "questions", "troubleshooting"]
version: "1.0"
updated_at: "2026-04-26"
---

# Payroll FAQ

## General Payroll Questions

**Q: What is the difference between gross and net salary?**
A: **Gross salary** = Basic + Allowances (before deductions). **Net salary** = Gross - Deductions = Amount employee takes home.

**Q: How often is payroll run?**
A: Typically monthly, but can be configured as bi-weekly, weekly, or custom cycles per organization policy.

**Q: Can I run payroll multiple times in a month?**
A: No, payroll runs once per cycle. To fix errors, undo approval and recalculate, or create adjustment payroll for next month.

**Q: Can employees see their payslip in Tipsoi?**
A: Yes, after payroll is finalized, employees can log in and view/download payslips from their dashboard.

**Q: How long should I keep payroll records?**
A: Typically 7 years minimum per labor law requirements in most countries.

**Q: Is payroll data encrypted?**
A: Yes, all payroll data is encrypted in transit and at rest. Access is role-based and audited.

## Salary Structure Questions

**Q: What if I need to change an employee's salary mid-year?**
A: You can change salary structure with an effective date. New structure applies from that date onward. Old structure used for previous months.

**Q: Can I have different salary structures for different departments?**
A: Yes, create separate salary structures and assign by department, designation, or individually.

**Q: What's the best way to handle prorated salary for new joiner?**
A: Tipsoi automatically pro-rates based on join date and working days in the month. Example: Join on 15th of 31-day month = 17/31 of monthly salary.

**Q: How do I calculate net salary from gross salary?**
A: Net = Gross - (Tax + EPF + ESI + Voluntary Deductions). The system calculates this automatically based on configured rules.

## Allowances Questions

**Q: Which allowances are taxable?**
A: Typically: Basic, HRA, Dearness Allowance, Special Allowance are taxable. Medical, Conveyance, Meal Vouchers (up to limit) are non-taxable. Check your tax law.

**Q: Can an employee receive an allowance only if they meet a condition?**
A: Yes, use **Variable Allowances** or **Custom Payroll Rules**. Example: Attendance bonus (₹500) only if absence = 0.

**Q: What if I want to give a bonus to only one employee?**
A: Use **Manual Override** in the payroll calculation step, or create a **Custom Rule** scoped to that employee.

**Q: How do I handle HRA for employees who don't pay rent?**
A: Depends on company policy. Some companies pay it regardless, others require rent agreement. Tax treatment also varies by country.

## Deductions Questions

**Q: Which deductions are mandatory?**
A: Mandatory deductions vary by country and salary level:
- Income Tax (on income above threshold)
- EPF (Employee Provident Fund)
- ESI (if salary below threshold)
- Professional Tax (varies by state)

Other deductions are voluntary (employee consent required).

**Q: What if I deduct an employee's loan EMI but they paid it off early?**
A: Disable the deduction in the employee's profile. It won't apply to future payrolls. The last payroll with deduction stands as-is.

**Q: Can employees opt out of voluntary deductions?**
A: Yes, voluntary deductions require employee consent. They can request removal anytime (effective from next payroll).

**Q: How is income tax calculated?**
A: Varies by country:
- **Slab-based** (India): Tax on annual income based on brackets
- **Flat %** (some countries): Fixed % of gross salary
- **No tax** (below threshold): No income tax if annual income below exemption limit

**Q: What if an employee has negative net salary?**
A: This indicates too many deductions. Review and reduce deductions, or adjust salary structure. The system won't disburse negative amounts.

## Overtime Questions

**Q: How is OT calculated?**
A: OT Amount = Overtime Hours × Hourly Rate × Multiplier
- Hourly Rate = Basic Salary ÷ 160 (or working hours in month)
- Multiplier = typically 1.5× for regular, 2× for weekend/holiday

**Q: Are all employees eligible for OT?**
A: No, eligibility depends on designation and shift type. Usually hourly workers and shift workers are eligible, not salaried management.

**Q: What's the cap on OT hours per month?**
A: Varies by country (typically 50 hours/month). Excess OT can be converted to compensatory off or requires approval.

**Q: Can OT be carried forward to next month?**
A: Not typically. OT is paid in the month worked. Excess beyond cap is either comp-off or pending approval (depends on policy).

**Q: How do I track OT manually if biometric not available?**
A: Manager can submit manual OT request in Tipsoi with approval. System adds to next payroll.

## Leave & Encashment Questions

**Q: Does paid leave affect salary?**
A: No, paid leave doesn't reduce salary. Employee still paid 100%. Leave balance is deducted.

**Q: Does unpaid leave affect salary?**
A: Yes, unpaid leave reduces salary. Deduction = Daily Rate × Unpaid Leave Days.

**Q: How is leave encashment calculated?**
A: Encashment = Daily Salary × Unused Leave Days
- Daily Salary = Gross Salary ÷ 30 (or working days in month)
- Triggers: Resignation, year-end carry-forward limit exceeded

**Q: Is leave encashment taxable?**
A: Depends on country. Some allow partial exemption (e.g., first ₹10 lakh in India), others tax fully.

**Q: What if employee has negative leave balance?**
A: System prevents over-use. But admin can manually override if needed (requires approval).

**Q: Can half-day leave affect OT?**
A: Yes, if employee works beyond 8 hours + takes half-day leave, OT is calculated on actual hours worked.

## Payroll Processing Questions

**Q: Can I run payroll before month-end?**
A: You can, but it's usually done on month-end date for complete attendance data. Running early = missing days won't be in payroll.

**Q: What happens if payroll is approved but then we find an error?**
A: Cannot edit approved payroll. Options:
1. Undo approval (if not yet submitted to bank)
2. Create adjustment payroll for next month

**Q: Can I cancel payroll after salaries are disbursed?**
A: No, once paid, it's final. For corrections, use adjustment payroll next month.

**Q: What if bank rejects a salary transfer?**
A: Check bank error reason (invalid account, insufficient balance at company, etc.). Fix and resubmit. Employee won't receive until successful.

**Q: Can I partially process payroll (only some employees)?**
A: Yes, use filters to select specific employees/departments and process separately.

**Q: How long does payroll calculation take?**
A: Usually 1-5 minutes for 300 employees, depends on system load and complexity.

## Bank & Payment Questions

**Q: What file formats does Tipsoi support for bank submission?**
A: NEFT (India), SWIFT, CSV, Excel, and bank-specific formats. Check your bank's accepted formats.

**Q: Can payroll be submitted directly to bank via API?**
A: Yes, if Tipsoi has your bank's API integration enabled. Contact admin for setup.

**Q: What if I submitted wrong bank file?**
A: Contact bank immediately to recall. If not yet processed (within hours), bank can cancel. Otherwise, collect back from employees and resubmit correct amount next month.

**Q: Can I split payroll into multiple bank files?**
A: Yes, create separate payroll cycles per bank or department.

**Q: How do I verify salaries were credited?**
A: Check bank statement (your company account) for outgoing transfers. Or ask employees to confirm receipt.

## Reporting & Compliance Questions

**Q: Can I export payroll data to analyze in Excel?**
A: Yes, all reports (Summary, Department-wise, etc.) can be exported to Excel/CSV.

**Q: How do I file taxes from Tipsoi?**
A: Generate **Tax Compliance Report**, verify figures, then file with tax authority using prescribed format (Form 16 in India, etc.).

**Q: Can external auditors access payroll data?**
A: Yes, generate **Audit Report** and share securely. Contains full trail for audit.

**Q: Is there a year-end payroll reconciliation?**
A: Yes, generate **Year-to-Date (YTD) Report**. Reconcile total YTD against actual expenses for audit.

## Troubleshooting

**Q: Payroll shows 0 salary for an employee - why?**
A: Possible reasons:
1. Employee is not active (marked as inactive)
2. No salary structure assigned
3. Employee was on unpaid leave entire month
4. Attendance data missing

**Check**: Employee profile, Salary structure assignment, Leave records, Attendance data

**Q: OT not showing in payroll?**
A: Possible reasons:
1. Employee not eligible for OT
2. Worked hours = standard hours (no excess)
3. OT hours < minimum threshold (e.g., < 1 hour)

**Check**: OT eligibility in employee profile, Punch records, OT threshold setting

**Q: Cannot approve payroll (button grayed out)?**
A: Possible reasons:
1. Missing permissions (not Payroll Admin)
2. Validation errors (report shows issues)
3. Someone else approving simultaneously

**Check**: Your role, Validation report, Try again later

**Q: Tax deduction too high - why?**
A: Possible reasons:
1. Salary increased mid-year (tax recalculated on full year)
2. Multiple allowances became taxable
3. Tax slab changed

**Check**: Salary history, Allowance tax treatment, Tax slab settings

**Q: Employee never received salary - what to do?**
A: Steps:
1. Verify payroll was approved and submitted to bank
2. Check bank transfer status (failed/pending)
3. Verify employee's bank account details
4. Contact bank if transfer failed
5. Resubmit if needed

## Tips & Best Practices

1. **Validate before approving**: Always review validation report for anomalies.

2. **Keep attendance updated**: Complete attendance data = accurate payroll.

3. **Test first**: For new salary structures/rules, test on draft payroll first.

4. **Maintain audit trail**: Don't delete payrolls. Keep for compliance.

5. **Plan for corrections**: Document any manual overrides for audit.

6. **Backup data**: Regularly backup payroll data and reports.

7. **Communicate changes**: Notify employees of any salary structure changes in advance.

8. **Review trends**: Monthly check OT, deductions, and allowances for anomalies.

9. **Verify bank details**: Before payroll, ensure all employees have valid bank accounts.

10. **Schedule payroll**: Use automated schedule to run payroll on fixed date each month.

## Contact Support

Can't find answer here? Contact:
- **Payroll Support**: support@inovacetech.com
- **Chat Support**: In-app chat available 9 AM - 6 PM
- **Phone**: +8809638017170
- **Ticket**: Create support ticket in Tipsoi admin > Help & Support
