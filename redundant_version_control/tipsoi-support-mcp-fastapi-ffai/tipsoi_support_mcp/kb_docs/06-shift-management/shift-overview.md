---
title: "Shift Overview"
description: "Complete guide to shift management and configuration"
category: "Shift Management"
difficulty: "intermediate"
tags: ["shift", "scheduling", "rotation", "management", "configuration"]
version: "1.0"
updated_at: "2026-04-26"
---

# Shift Overview

## What is a Shift?

A **shift** is a defined work period with:
- **Start time**: When employees begin work
- **End time**: When employees end work
- **Break duration**: Rest period(s) during shift
- **Duration**: Total working hours

**Example**:
- Morning Shift: 6:00 AM - 2:00 PM (8 hours with 30-min break = 7.5 working hours)
- Evening Shift: 2:00 PM - 10:00 PM
- Night Shift: 10:00 PM - 6:00 AM

## Why Manage Shifts?

Shift management helps:
- **Track attendance accurately** — Punch times compared to shift times
- **Calculate overtime** — OT triggered when working beyond shift hours
- **Enforce compliance** — Ensure working hour limits per law
- **Enable scheduling** — Assign employees to shifts
- **Manage rosters** — Create rotation schedules
- **Handle shift swaps** — Allow employee flexibility

## Types of Shifts

### 1. Fixed Shifts
Same start and end time every day:
- **Morning**: 8:00 AM - 4:00 PM
- **Evening**: 2:00 PM - 10:00 PM
- **Night**: 10:00 PM - 6:00 AM

**Use case**: Office staff, regular operations

### 2. Flexible Shifts
Employee can choose start/end time within a range:
- **Flexible Window**: 8:00 AM - 10:00 AM start, 4:00 PM - 6:00 PM end
- **Employee chooses**: "I'll work 8:30 AM - 4:30 PM"
- **Tracked for**: Flexible schedule adherence

**Use case**: IT teams, call centers with flex timing

### 3. Rotating Shifts
Employees rotate through multiple shift timings:
- **Day 1-7**: Morning shift
- **Day 8-14**: Evening shift
- **Day 15-21**: Night shift
- **Repeats**: 21-day rotation cycle

**Use case**: Manufacturing, 24/7 operations

### 4. Split Shifts
Employees work two separate periods per day:
- **Period 1**: 8:00 AM - 12:00 PM (4 hours)
- **Break**: 12:00 PM - 2:00 PM (unpaid)
- **Period 2**: 2:00 PM - 6:00 PM (4 hours)
- **Total**: 8 hours with 2-hour unpaid break

**Use case**: Schools, part-time staffing models

### 5. On-Call Shifts
Employee available but work hours variable:
- **Available**: 9 AM - 9 PM daily
- **Actual work**: Only when called (e.g., support team)
- **Minimum guarantee**: May have minimum hours/pay

**Use case**: Support teams, standby staff

## Shift Components

### Start & End Time
```
Start Time: 8:00 AM
End Time: 5:00 PM
Shift Duration: 9 hours (gross)
```

### Breaks
Unpaid break time:
```
Break 1: 12:00 PM - 1:00 PM (1 hour)
Total Breaks: 1 hour
Working Hours: 8 hours (9 - 1)
```

Multiple breaks:
```
Break 1: 12:00 PM - 12:30 PM (30 min)
Break 2: 3:00 PM - 3:30 PM (30 min)
Total Breaks: 1 hour
Working Hours: 8 hours
```

### Buffer Time
Grace period for punch-in/punch-out:
- **Grace In**: 10 minutes (can punch in up to 10 min late, still marked on-time)
- **Grace Out**: 5 minutes (can punch out up to 5 min early)
- **Impact**: Helps with minor delays, not counted as late

## Shift Configuration Steps

### Step 1: Create Shift
1. Go to **Shifts → Create New Shift**
2. Enter details:
   - **Shift Name**: (e.g., "Morning Shift")
   - **Start Time**: 8:00 AM
   - **End Time**: 5:00 PM
   - **Shift Type**: Fixed / Flexible / Rotating / Split / On-Call
3. Add breaks:
   - Break 1: 12:00 PM - 1:00 PM
4. Set buffering:
   - Grace In: 10 minutes
   - Grace Out: 5 minutes
5. Click "Create"

### Step 2: Create Shift Group (Optional)
Group related shifts:
- **Name**: "Morning Group"
- **Shifts**: Morning Shift, Flexible Morning
- **Used for**: Assigning groups of shifts to employees/teams

### Step 3: Assign to Employees
- Individual assignment: Assign shift to specific employee
- Bulk assignment: Assign to entire department
- By designation: All "Production Manager" on evening shift
- Rotation group: Assign rotating schedule

## Shift Rules & Enforcement

### Daily Hour Limits
Ensure no one works too long:
```
Max hours per day: 12 hours
If employee works 13 hours (overtime), alert manager
```

### Weekly Hour Limits
Ensure compliance with labor laws:
```
Max hours per week: 48 hours
If total > 48, trigger warning
```

### Monthly Overtime Cap
```
Max OT per month: 50 hours
Excess flagged for approval/comp-off
```

### Minimum Rest Period
Between shifts, employees need rest:
```
Min rest: 8 hours between end of one shift and start of next
If less (e.g., night shift ends 6 AM, morning shift starts 8 AM = 2 hours), alert manager
```

## Shift Assignment

### Method 1: Direct Assignment
Assign specific shift to employee:
1. Go to **Shifts → Assign**
2. Select employee
3. Select shift
4. Set effective date
5. Save

### Method 2: Roster (Schedule Planning)
Create a monthly/weekly schedule:
1. Go to **Shifts → Roster**
2. View calendar
3. Drag-drop shifts to dates
4. Assign employees to dates
5. Publish roster

### Method 3: Shift Swaps
Allow employees to swap shifts:
1. Employee requests swap
2. Manager approves
3. New shift assigned
4. Attendance tracked against new shift

## Shift Attendance Tracking

Once shift assigned, attendance is tracked against it:

```
Assigned Shift: 8:00 AM - 5:00 PM
Employee Actual: Punch-in 8:15 AM, Punch-out 5:00 PM

Result:
- On-time: NO (15 minutes late)
- Status: LATE
- Work Duration: 8.75 hours
- OT: 0.75 hours (worked until 5:00, shift ends 5:00)
```

## Overtime Calculation Based on Shift

```
Shift: 8:00 AM - 5:00 PM (8 hours)
Actual: 8:00 AM - 6:00 PM (9 hours)

OT Hours: 1 hour (beyond shift end time)
OT Amount: 1 × ₹125/hr × 1.5 = ₹187.50
```

## Common Shift Scenarios

### Scenario 1: New Employee Mid-Day
**Situation**: Employee joins morning shift but on-boarding takes until 2 PM.
**Handling**: 
- First day: Reduced shift (2 PM - 5 PM)
- Next day onwards: Full morning shift

### Scenario 2: Shift Overlap for Handover
**Situation**: Morning shift ends 2 PM, Evening shift starts 2 PM (5-min overlap for handover).
**Handling**:
- 1:55-2:05 PM: Both shifts overlapping
- Attendance: Counted for both shifts
- OT: No OT if coordinated

### Scenario 3: Unexpected Shift Change
**Situation**: Sudden production demand, need to call evening shift employees for morning.
**Handling**:
- Manager requests shift change
- System calculates OT if < 8-hour rest
- Employee notified
- Attendance tracked against new shift

### Scenario 4: Early Finish
**Situation**: Work completed early, sent home 1 hour early.
**Handling**:
- Punch out early: 4:00 PM (vs. 5:00 PM shift end)
- Attendance: Marked as "Early Finish" or "Half Day"
- Payroll: Reduced hours or leave deduction (depends on policy)

## Shift Analytics

### Shift Utilization Report
```
Shift | Employees | Avg Attendance | Avg OT Hours |
Morning | 150 | 95% | 0.5 |
Evening | 100 | 92% | 1.2 |
Night | 50 | 88% | 2.0 |
```

**Insight**: Night shift has higher OT (understaffed?)

### Shift Attendance Trends
Track pattern over weeks:
- Monday: 98% (good)
- Friday: 85% (high absence)
- Weekend: Lower if not operational

### Shift Rotation Fairness
Ensure rotating shifts distributed fairly:
- No one stuck on night shift permanently
- Rotation cycles are even

## Related Documents

- [Creating Shifts](./creating-shifts.md)
- [Shift Groups and Rosters](./shift-groups-and-rosters.md)
- [Shift Swaps and Changes](./shift-swaps-and-changes.md)
- [FAQ - Shifts](./faq-shifts.md)

## FAQ

**Q: Can I have multiple shifts per day (split shift)?**
A: Yes, set up as "Split Shift" type with two time periods and break in between.

**Q: What if employee works beyond shift end time?**
A: Overtime is calculated. Hours beyond shift are OT.

**Q: Can shifts be different on weekends?**
A: Yes, set up different shifts and assign specifically to weekend days.

**Q: What's the minimum gap between two shifts?**
A: Typically 8 hours (configurable). Less gap triggers alert.

**Q: Can employees choose their own shift?**
A: Can be set as flexible shift allowing choice within time window, or manually request shift change.

## Next Steps

1. [Create your first shift](./creating-shifts.md)
2. [Set up shift groups for teams](./shift-groups-and-rosters.md)
3. [Create a roster schedule](./shift-groups-and-rosters.md)
4. [Manage shift swaps](./shift-swaps-and-changes.md)
