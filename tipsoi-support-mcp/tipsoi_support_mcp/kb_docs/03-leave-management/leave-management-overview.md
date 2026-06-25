---
title: "Leave Management Overview"
description: "Complete guide to managing employee leave policies and applications"
category: "Leave Management"
difficulty: "intermediate"
tags: ["leave", "policy", "approval", "entitlement", "workflow"]
version: "1.0"
updated_at: "2024-04-26"
---

# Leave Management Overview

## What is Leave Management?

Leave management in Tipsoi handles employee time-off requests, approvals, balance tracking, and payroll integration. Admins can configure flexible leave policies while employees can apply for and track their leave.

## Leave Policy Configuration

### Key Components

**Leave Types**: Different categories of leave available
- Casual Leave (CL)
- Sick Leave (SL)
- Annual Leave (AL)
- Special Leave (optional)
- Earned Leave (optional)

**Entitlement**: Number of days per year for each type
- Annual allocation (e.g., 12 days casual leave per year)
- Monthly accrual (e.g., 1 day per month)
- Upfront allocation (e.g., all days on January 1)

**Accrual Method**: How leave is credited
- **Monthly**: 1 day added each month
- **Quarterly**: 3 days added each quarter
- **Annually**: Full entitlement given upfront
- **Custom**: Based on company policy

**Carryover Rules**: Unused leave handling
- Maximum days that can be carried forward (e.g., 5 days max)
- Days exceeding maximum are forfeited
- Useful for managing year-end leave

---

## Leave Types and Entitlements

### Standard Leave Policy Example

| Leave Type | Days/Year | Accrual | Carryover | Notes |
|------------|-----------|--------|-----------|-------|
| Casual Leave | 12 | 1/month | 5 days max | For personal reasons |
| Sick Leave | 10 | Monthly | No carryover | Requires proof after 2 days |
| Annual Leave | 15 | Upfront | 10 days max | Planned vacation |
| Maternity Leave | 90 | Special | Not applicable | Legal requirement |

### Configuring Leave Policies

1. Go to: **Leave → Leave Policy**
2. Create a new policy with:
   - Policy name and description
   - Target audience (all employees, departments, etc.)
   - Leave year cycle (calendar or financial)

3. Add leave types with:
   - Type name and code
   - Annual entitlement
   - Accrual method
   - Maximum carryover
   - Approval requirement

4. Apply to employees:
   - Company-wide default
   - Department-specific
   - Designation-specific
   - Individual exceptions

---

## Leave Application Workflow

### Step 1: Employee Applies for Leave

**What employee does**:
- Opens Tipsoi dashboard or mobile app
- Navigates to: Leave → Apply for Leave
- Selects leave type and dates
- Provides reason (optional)
- Reviews leave balance
- Submits for approval

**System checks**:
- Available leave balance
- Date validity (not past dates)
- Overlapping leave requests
- Policy restrictions

### Step 2: Manager Review and Approval

**What manager/HR does**:
- Receives leave request notification
- Reviews in: Pending Approvals section
- Views employee details and reason
- Checks project deadlines or dependencies
- Approves or rejects with optional comments

**Notification**: Employee gets immediate status update

### Step 3: System Updates

**After approval**:
- Attendance marked as "On Leave"
- Leave balance automatically deducted
- Payroll adjusts salary (no deduction for approved leave)
- Calendar shows employee as unavailable

**After rejection**:
- Leave not recorded
- Balance unchanged
- Employee can reapply for different dates

### Step 4: Payroll Processing

**During payroll run**:
- System identifies approved leaves
- Calculates pay for full days worked
- No salary deduction for approved leaves
- Overtime not paid on leave days

---

## Leave Balance Management

### How Balance is Calculated

**Opening Balance** (Jan 1):
- Brought forward from previous year
- Capped at maximum carryover

**Accrual**: 
- Monthly addition (e.g., 1 casual leave/month)
- Quarterly addition (if configured)
- Annual upfront (if configured)

**Used**: 
- Deducted when leave is approved
- Half day counts as 0.5 days

**Closing Balance** (Dec 31):
- Opening + Accrual - Used
- Capped at carryover maximum
- Excess forfeited

### Example Calculation

**Casual Leave Tracking**:
- Opening: 3 days (carried forward from last year)
- Accrual: 1 day per month = 12 days for the year
- Total available: 15 days
- Used: 8 days (6 days approved + 1 half day = 6.5 days)
- Closing: 15 - 6.5 = 8.5 days
- Max carryover: 5 days
- Forfeited: 3.5 days
- Available next year: 5 days

---

## Leave Policy Configuration Scenarios

### Scenario 1: Casual Leave with Carryover
- **Entitlement**: 12 days per year
- **Accrual**: 1 day per month
- **Carryover**: 5 days maximum
- **Use Case**: Flexible leave for personal reasons

### Scenario 2: Sick Leave No Carryover
- **Entitlement**: 10 days per year
- **Accrual**: Monthly
- **Carryover**: 0 days (no carryover allowed)
- **Use Case**: Health-related leave only

### Scenario 3: Annual Leave with Upfront
- **Entitlement**: 20 days per year
- **Accrual**: Upfront on January 1
- **Carryover**: 10 days maximum
- **Use Case**: Planned vacation days

### Scenario 4: Sick Leave with Documentation
- **Entitlement**: 10 days per year
- **Approval**: Auto-approve first day, manual approve after
- **Carryover**: No carryover
- **Requires**: Medical certificate after 2 days

---

## Advanced Leave Features

### Leave Carry Forward
- Unused leaves from previous year rolled into current year
- Subject to maximum carryover limits
- Can be forfeited or encashed
- Configured in leave policy

### Leave Encashment
- Convert unused leave to monetary value
- Calculated as: Leave Days × Daily Wage
- Paid during salary run or final settlement
- Company can set eligibility criteria

### Leave Blocking
- Prevent leave during critical business periods
- Block dates for project deadlines
- Override options for managers
- Email notification to employees

### Bulk Leave Upload
- Upload leave balance adjustments
- Batch leave application processing
- End-of-year leave management
- Excel file format supported

---

## Approval Workflows

### Single-Level Approval
- Employee applies for leave
- Immediate manager approves/rejects
- Fast turnaround for employees

### Multi-Level Approval
- Employee applies
- Department manager reviews
- HR manager approves
- Director gives final sign-off
- Ensures accountability and compliance

### Conditional Approval
- HR approves based on policy
- Department manager approves based on workload
- Executive approval for extended leave
- Each level can add comments

---

## Leave Reporting

### Available Reports

1. **Leave History Report**
   - All leave taken by employee
   - With dates and types
   - Historical record

2. **Leave Balance Report**
   - Current balance for each employee
   - By leave type
   - Monthly snapshot

3. **Leave Approval Status**
   - Pending approvals
   - Approved and rejected
   - Time taken for approval

4. **Department Leave Summary**
   - Aggregate leave by team
   - Peak leave periods
   - Workload planning

### Report Features
- Date range filtering
- Department filtering
- Export to Excel or PDF
- Advanced sorting and grouping

---

## Leave Policy Best Practices

### For Admins
1. Define clear leave policies aligned with labor laws
2. Communicate policies to all employees
3. Ensure fairness across departments
4. Monitor leave patterns for insights
5. Update policies annually

### For Managers
1. Review leave requests promptly
2. Plan for team coverage during peaks
3. Communicate approvals quickly
4. Document reasons for rejections
5. Track team's leave balance

### For Employees
1. Check leave balance before applying
2. Apply in advance when possible
3. Provide valid reason/documentation
4. Follow company leave procedures
5. Plan leave during appropriate times

---

## Integration with Payroll

### Leave Impact on Salary

**Approved Leave** (On Leave Status):
- No salary deduction
- Full salary paid for the month
- Leave balance reduced

**Absent without Leave** (Absent Status):
- Salary deduction applied
- Amount = (Daily Wage × Absent Days)
- No leave balance affected

**Half Day Leave**:
- Half salary deduction (if unpaid)
- Or full pay (if company policy allows)
- Counted as 0.5 days in leave balance

**Sick Leave with Certificate**:
- Full salary paid
- Leave balance reduced
- Certificate stored in system

---

## Troubleshooting Leave Issues

### Issue: Leave Balance Not Showing Correctly
- Check accrual configuration
- Verify leave year settings
- Review past leave approvals
- Check for manual adjustments

### Issue: Leave Not Getting Deducted
- Verify leave approval status
- Check if on correct leave type
- Review payroll process date
- Check system logs for errors

### Issue: Employee Can't Apply for Leave
- Verify employee account is active
- Check permission settings
- Ensure leave policy is assigned
- Verify sufficient balance exists

---

## Next Steps

1. **Configure Your Leave Policies**: Set up types and entitlements
2. **Assign to Departments**: Link policies to teams
3. **Test Application**: Have a pilot group test the workflow
4. **Train Your Team**: Educate staff on applying and approving
5. **Monitor and Adjust**: Review reports and refine policies

**Questions?** Contact support at **support@inovacetech.com** or call **+880 9638017170**
