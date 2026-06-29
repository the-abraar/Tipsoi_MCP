---
title: "Overtime Management"
description: "Understanding, calculating, and managing employee overtime"
category: "Payroll"
difficulty: "intermediate"
tags: ["payroll", "overtime", "ot", "hours", "compensation"]
version: "1.0"
updated_at: "2026-04-26"
---

# Overtime Management

## What is Overtime (OT)?

**Overtime** is compensation for hours worked beyond the standard scheduled shift. In Tipsoi:
- Tracked automatically from punch-in/punch-out records
- Calculated based on daily and monthly thresholds
- Added to payroll as additional earnings
- Subject to statutory limits in many countries

## Key OT Concepts

### Standard Hours
The regular working hours employees are expected to work:
- **Daily**: 8 hours (typical)
- **Monthly**: ~160-180 hours (depending on working days)
- **Configured per shift** in Tipsoi

### Overtime Hours
Hours worked beyond standard:
```
OT Hours = Actual Hours - Standard Hours
```

### OT Rate Multiplier
The multiplier applied to regular hourly rate:
- **Regular OT**: 1.5× (time and a half)
- **Weekend OT**: 2× (double time)
- **Night OT**: 1.25-2× (varies by policy)
- **Holiday OT**: 2-3× (varies by country)

### OT Calculation
```
OT Amount = Overtime Hours × Hourly Rate × Multiplier

Example:
- Basic Salary: ₹20,000
- Hourly Rate: ₹20,000 ÷ 160 = ₹125/hour
- Overtime Hours: 10
- Multiplier: 1.5×
- OT Amount: 10 × 125 × 1.5 = ₹1,875
```

## OT Types in Tipsoi

### Daily Overtime
Excess hours on a specific day:
- **Trigger**: Hours > daily shift duration
- **Example**: 8-hour shift, but worked 10 hours = 2 hours OT that day
- **Rate**: Standard rate × multiplier

### Weekly Overtime
Excess hours in a week (typically 5-day week):
- **Trigger**: Total weekly hours > 40 (5 × 8 hours)
- **Example**: Worked 42 hours in week = 2 hours OT
- **Rate**: Standard rate × multiplier

### Monthly Overtime
Excess hours in a month:
- **Trigger**: Total monthly hours > 160-180 (depending on working days)
- **Example**: Worked 170 hours, expected 160 = 10 hours OT
- **Rate**: Standard rate × multiplier
- **Statutory Cap**: Many countries cap monthly OT (e.g., max 50 hours/month)

### Casual/Ad-hoc Overtime
Unscheduled overtime approved manually:
- **Trigger**: Manager approval
- **Example**: Employee called in on weekend = all hours at 2× rate
- **Documentation**: Requires approval in Tipsoi

## Configuring OT Rules

### Step 1: Define OT Eligibility
Who is eligible for overtime?
- **By Designation**: Usually hourly workers, not salaried managers
- **By Shift Group**: Shift workers typically eligible
- **By Department**: Production staff, support teams
- **By Grade**: Grade A-C eligible, Grade D+ not eligible

**Configuration**:
```
Eligible Designations:
- Machine Operator
- Technician
- Production Helper
- Support Staff

Ineligible Designations:
- Manager
- Team Lead (may vary)
- Executive
```

### Step 2: Set OT Rates
Define multipliers for different scenarios:

| Scenario | Multiplier | Notes |
|---|---|---|
| Regular Weekday OT | 1.5× | Monday-Friday overtime |
| Saturday OT | 1.75× | Partial weekend rate |
| Sunday OT | 2× | Full weekend rate |
| Holiday OT | 2.5× | Public holiday |
| Night Shift OT (10 PM - 6 AM) | 1.25× | Additional to OT rate |

### Step 3: Set Monthly OT Cap
Maximum OT hours allowed per month:
- **Typical cap**: 50 hours/month (varies by country)
- **Excess handling**: Either
  - Compensatory off (employee gets day off)
  - Pending approval (requires manager sign-off)
  - Auto-deactivation (no OT recorded above cap)

### Step 4: Configure Minimum OT Threshold
Minimum hours to trigger OT payment:
- **Threshold**: 0.5 hours (30 minutes) or 1 hour
- **Rounding**: Round up to nearest 0.5 hour or 1 hour

## OT Calculation in Payroll

### Method 1: Straight Time
Every hour gets OT rate:
```
OT Hours: 10
Rate: 1.5×
Amount: 10 × 125 × 1.5 = ₹1,875
```

### Method 2: Compensatory Rate (Some countries)
Only excess amount is paid:
```
Regular Pay: 10 hours × ₹125 = ₹1,250
OT Pay: 10 hours × ₹125 × 0.5 = ₹625 (only the premium)
Total: ₹1,875
```

### Method 3: Time-in-Lieu (Some organizations)
OT converted to paid leave:
```
OT Hours: 10
Conversion: 10 × 1.5 = 15 hours of paid leave
Employee gets 15 hours off at regular rate
```

### Monthly OT Report Example

**Employee: Ali Hassan (May 2026)**

| Date | Shift Hours | Actual Hours | OT Hours | Rate | Amount |
|---|---|---|---|---|---|
| May 5 | 8 | 10 | 2 | 1.5× | ₹250 |
| May 12 | 8 | 9 | 1 | 1.5× | ₹125 |
| May 19 | 8 | 8 | 0 | - | ₹0 |
| May 26 | 8 | 11 | 3 | 1.5× | ₹375 |
| **Total** | **32** | **38** | **6** | - | **₹750** |

## OT and Leave Interaction

### OT on Leave Day
If employee works on a leave day:
- **Scenario**: Employee on half-day leave but works full shift
- **Handling**: 
  - Either half-day leave is canceled (counted as working)
  - Or OT is not paid (leave takes precedence)
- **Configuration**: Set in OT rules

### OT During Sick Leave
If employee works despite being on sick leave:
- **Scenario**: Sick leave approval, but employee works
- **Handling**: OT can be recorded (with manager approval)
- **Payroll**: Sick leave canceled, OT paid instead

## OT and Shift Changes

### Shift Swap with OT
If employee swaps shifts to cover another employee:
- **Scenario**: Works morning and evening shift same day
- **OT Calculation**: Hours > standard daily shift
- **Rate**: Depends on shift type (night OT might be different rate)

### Emergency Call-Out
Employee called in on scheduled off day:
- **Scenario**: Weekend call-out for production emergency
- **All hours**: Counted as OT at holiday/weekend rate
- **Rate**: 2× or 2.5× depending on day

## OT Approval Workflow

### Automatic OT (Biometric-Tracked)
1. **Punch Records**: System captures actual hours
2. **Auto-Calculate**: OT > 0 calculated automatically
3. **Manager Review**: Manager sees OT in payroll validation
4. **Approval**: Included in final payroll

### Manual OT (Ad-hoc)
1. **Request**: Manager submits OT request in Tipsoi
2. **Details**: Specifies date, hours, reason
3. **Approval Chain**: HR/Admin approves
4. **Payroll**: Added to next payroll

### Compensatory Off Request
1. **OT Accumulation**: Employee accrues OT hours
2. **Request**: Employee requests comp-off day
3. **Approval**: Manager approves (subject to business needs)
4. **Adjustment**: OT hours converted to paid leave day

## OT Reporting & Analytics

### Monthly OT Report
Top OT users in organization:

| Employee | Dept | Total OT Hours | OT Amount | % of Salary |
|---|---|---|---|---|
| Ahmed Hassan | Production | 24 | ₹3,000 | 15% |
| Fatima Khan | Production | 20 | ₹2,500 | 12% |
| Ali Hassan | Production | 6 | ₹750 | 3% |

**Summary**:
- Total OT in company: 245 hours
- Total OT cost: ₹30,625
- Average per employee: 8.2 hours
- Departments with high OT: Production (180 hours), Support (65 hours)

### OT Trend Analysis
Track OT over time to identify issues:
- **High OT trend**: Indicates understaffing or high workload
- **Seasonal patterns**: Identify peak OT seasons
- **Cost impact**: Calculate OT as % of payroll

### OT Exceptions
Flag unusual OT patterns:
- Employee X suddenly has 50 hours/month (was 5 hours before)
- High OT concentrated in specific department
- Multiple employees with near-maximum OT

## Compliance & Regulations

### Regional Limits
Different countries have OT regulations:

| Country | Monthly OT Cap | OT Rate |
|---|---|---|
| India | 50 hours | 2× for OT beyond 48 hours/week |
| Bangladesh | 10 hours/week | 1.5-2× depending on context |
| UAE | 2 hours/day max | 1.5× |

**Action**: Configure OT rules per your country requirements.

### Statutory Deductions on OT
Some countries tax OT differently:
- Some: No tax on first ₹10,000 OT per year
- Some: 100% tax on OT amount
- Some: Standard tax rate applies

**Configuration**: Set tax treatment in Tipsoi settings.

## Common OT Scenarios

### Scenario 1: Employee Forgets to Punch Out
**Situation**: Employee worked 9 hours but forgot punch-out. System shows incomplete.
**Solution**:
1. Manager manually adjusts punch-out time
2. System recalculates OT
3. OT added to next payroll

### Scenario 2: OT on Weekend (Holiday)
**Situation**: Employee works Sunday (public holiday).
**Calculation**: 8 hours × ₹125 × 2.5× = ₹2,500

### Scenario 3: Exceeding Monthly Cap
**Situation**: Employee has 52 hours OT (cap is 50).
**Handling**: 
- First option: Extra 2 hours approved as compensatory off
- Second option: Extra 2 hours paid if cap exceeded
- Third option: Extra 2 hours pending manager approval

### Scenario 4: Split Shift OT
**Situation**: Employee works morning shift (8 hrs) + evening shift (4 hrs).
**Calculation**:
- Morning: No OT (standard 8 hours)
- Evening: 4 hours OT (beyond 8-hour shift)
- Total OT: 4 hours

## Related Documents

- [Payroll Overview](./payroll-overview.md)
- [Payroll Calculation Methods](./payroll-calculation-methods.md)
- [Custom Payroll Rules](./custom-payroll-rules.md)
- [Payroll Processing](./payroll-processing.md)

## FAQ

**Q: Is OT calculated on basic or gross salary?**
A: OT is calculated on basic salary ÷ working hours = hourly rate.

**Q: Can an employee refuse OT work?**
A: Depends on local labor law. In most cases, employees can decline voluntary OT but may need to accept emergency OT.

**Q: How is OT handled if employee is on leave part of month?**
A: OT cap is adjusted proportionally. If employee is on 10 days leave (20 days worked), cap is 50 × (20 ÷ 30) = 33 hours.

**Q: Can OT be carried forward to next month?**
A: Not typically. OT is paid in the month worked. Excess OT (beyond cap) converts to comp-off or pending approval.

**Q: What if employee takes leave during high OT period?**
A: OT calculations are independent of leave. If leave is taken on a working day, OT is not calculated for that day.
