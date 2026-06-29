---
title: "Creating Shifts"
description: "Step-by-step guide to creating different types of shifts"
category: "Shift Management"
difficulty: "intermediate"
tags: ["shift", "creation", "setup", "configuration", "timing"]
version: "1.0"
updated_at: "2026-04-26"
---

# Creating Shifts

## Before You Start

Decide:
- ✓ Shift type (Fixed, Flexible, Rotating, Split, On-Call)
- ✓ Start and end times
- ✓ Break duration and timing
- ✓ Employees to assign
- ✓ Effective date

## Creating a Fixed Shift

**Fixed shifts have the same start/end time every day.**

### Step-by-Step

1. **Go to Shifts → Create New Shift**

2. **Enter Basic Details**:
   - **Shift Name**: "Morning Shift" (or appropriate name)
   - **Shift Type**: Select "Fixed"
   - **Description**: (optional) "Regular 8-hour morning shift"

3. **Set Shift Timing**:
   - **Start Time**: 8:00 AM
   - **End Time**: 5:00 PM
   - **Total Gross Hours**: 9 (auto-calculated)

4. **Configure Breaks**:
   - **Break 1 Name**: "Lunch"
   - **Start**: 12:00 PM
   - **End**: 1:00 PM
   - **Duration**: 1 hour
   - **Paid/Unpaid**: Unpaid (usually)
   - Click "Add Break"

5. **Add Grace Period** (optional):
   - **Grace In**: 10 minutes (can punch in up to 10 min late)
   - **Grace Out**: 5 minutes (can punch out up to 5 min early)
   - **Purpose**: Tolerance for minor delays

6. **Set Working Hours**:
   - System auto-calculates: 9 hours - 1 hour break = 8 working hours
   - Verify correct

7. **Apply To**:
   - **Effective From**: Today (or future date)
   - **Applies to**: Leave blank for now (assign later)

8. **Click "Create Shift"**

### Example: Morning Shift
```
Shift Name: Morning Shift
Type: Fixed
Start: 8:00 AM
End: 5:00 PM
Breaks:
  - Lunch: 12:00 PM - 1:00 PM (1 hour, unpaid)
Grace In: 10 min
Grace Out: 5 min
Working Hours: 8 hours
```

## Creating a Flexible Shift

**Flexible shifts allow employee choice within a range.**

### Step-by-Step

1. **Go to Shifts → Create New Shift**

2. **Enter Basic Details**:
   - **Shift Name**: "Flexible Hours"
   - **Shift Type**: Select "Flexible"
   - **Description**: "Employees choose start time within window"

3. **Set Time Windows**:
   - **Earliest Start**: 8:00 AM (can't start before this)
   - **Latest Start**: 10:00 AM (can't start after this)
   - **Min Duration**: 8 hours (minimum hours to work)
   - **Latest End**: 6:00 PM (can't work past this)

4. **Configure Breaks**:
   - **Break 1**: 12:00 PM - 1:00 PM (1 hour)

5. **Flexibility Rules**:
   - Employees choose within window
   - Example choices:
     - 8:00 AM - 4:00 PM (8 hours)
     - 9:00 AM - 5:00 PM (8 hours)
     - 10:00 AM - 6:00 PM (8 hours)

6. **Click "Create Shift"**

### Example: Flexible Shift
```
Shift Name: Flexible Hours
Type: Flexible
Start Window: 8:00 AM - 10:00 AM
End Window: 4:00 PM - 6:00 PM (after 8 hours)
Min Duration: 8 hours
Breaks: 12:00 PM - 1:00 PM (1 hour)
```

## Creating a Rotating Shift

**Rotating shifts cycle through multiple timings.**

### Step-by-Step

1. **Go to Shifts → Create New Shift Group**

2. **Create Individual Shifts First**:
   - Morning: 8:00 AM - 4:00 PM
   - Evening: 4:00 PM - 12:00 AM
   - Night: 12:00 AM - 8:00 AM

3. **Create Rotation Schedule**:
   - **Rotation Name**: "3-Shift Rotation"
   - **Cycle Duration**: 21 days (3 shifts × 7 days each)
   - **Shift 1**: Morning Shift (Days 1-7)
   - **Shift 2**: Evening Shift (Days 8-14)
   - **Shift 3**: Night Shift (Days 15-21)
   - **Repeat**: Cycle repeats forever

4. **Define Start Date**:
   - **Rotation Starts**: January 1, 2026
   - **Day 1**: Morning Shift

5. **Click "Create Rotation"**

### Example: 3-Shift Rotation
```
Rotation Name: 3-Shift Rotation
Cycle: 21 days

Schedule:
- Days 1-7: Morning Shift (8 AM - 4 PM)
- Days 8-14: Evening Shift (4 PM - 12 AM)
- Days 15-21: Night Shift (12 AM - 8 AM)

Repeats every 21 days
```

### 5-Day Rotation Example
```
Rotation: 5 Days on, 2 Days off

Day 1-5: Work (any shift)
Day 6-7: Off

Pattern repeats
```

## Creating a Split Shift

**Split shifts have two separate work periods.**

### Step-by-Step

1. **Go to Shifts → Create New Shift**

2. **Enter Basic Details**:
   - **Shift Name**: "Split Morning-Evening"
   - **Shift Type**: Select "Split"

3. **Set First Period**:
   - **Period 1 Start**: 8:00 AM
   - **Period 1 End**: 12:00 PM
   - **Duration**: 4 hours

4. **Set Break Between**:
   - **Break Start**: 12:00 PM
   - **Break End**: 2:00 PM
   - **Duration**: 2 hours (unpaid)

5. **Set Second Period**:
   - **Period 2 Start**: 2:00 PM
   - **Period 2 End**: 6:00 PM
   - **Duration**: 4 hours

6. **Total Working Hours**:
   - Period 1: 4 hours
   - Period 2: 4 hours
   - **Total**: 8 hours

7. **Click "Create Shift"**

### Example: Split Shift
```
Shift Name: Split Shift
Type: Split

Period 1:
- Start: 8:00 AM
- End: 12:00 PM
- Hours: 4

Break: 12:00 PM - 2:00 PM (unpaid)

Period 2:
- Start: 2:00 PM
- End: 6:00 PM
- Hours: 4

Total Working: 8 hours
```

## Creating an On-Call Shift

**On-Call shifts have variable hours based on demand.**

### Step-by-Step

1. **Go to Shifts → Create New Shift**

2. **Enter Basic Details**:
   - **Shift Name**: "Support On-Call"
   - **Shift Type**: Select "On-Call"
   - **Description**: "Available 9 AM - 9 PM, work as needed"

3. **Set Availability Window**:
   - **Available From**: 9:00 AM
   - **Available To**: 9:00 PM
   - **Total Window**: 12 hours

4. **Set Minimum Guarantee** (optional):
   - **Min Hours/Day**: 4 hours (minimum paid even if not called)
   - **Max Hours/Day**: 12 hours (max work allowed)

5. **Break Policy**:
   - Breaks as needed during work

6. **Click "Create Shift"**

### Example: On-Call Shift
```
Shift Name: Support On-Call
Type: On-Call
Available: 9:00 AM - 9:00 PM
Min Guarantee: 4 hours/day
Max Hours: 12 hours/day
```

## Shift Template Library

Create templates for reuse:

### Template: Standard Day Shift
```
Name: Day Shift Template
Type: Fixed
Start: 8:00 AM
End: 4:00 PM
Breaks: 12:00 PM - 1:00 PM
Grace: 10 in, 5 out
Working: 7 hours
```

### Template: Evening Shift
```
Name: Evening Shift Template
Type: Fixed
Start: 4:00 PM
End: 12:00 AM
Breaks: 8:00 PM - 8:30 PM
Grace: 10 in, 5 out
Working: 7.5 hours
```

### Template: Night Shift
```
Name: Night Shift Template
Type: Fixed
Start: 12:00 AM
End: 8:00 AM
Breaks: 4:00 AM - 4:30 AM
Grace: 10 in, 5 out
Working: 7.5 hours
```

## Advanced Shift Configuration

### Multi-Break Shifts
Some operations require multiple breaks:

```
Shift: 8:00 AM - 6:00 PM (10 hours)

Break 1: 10:30 AM - 10:45 AM (15 min)
Break 2: 1:00 PM - 2:00 PM (1 hour)
Break 3: 4:00 PM - 4:15 PM (15 min)

Total Breaks: 1.5 hours
Working: 8.5 hours
```

### Shift Allowance
Assign extra pay for certain shifts:

```
Night Shift Allowance: ₹2,000/month extra
Weekend Shift Allowance: ₹1,500/month extra
Emergency Call-Out: ₹500/call
```

Configure in **Shift Settings → Allowances**.

### Shift-Based Leave Policy
Different leave entitlements per shift:

```
Day Shift: 12 casual + 10 sick leave
Night Shift: 15 casual + 12 sick (due to hardship)
On-Call: 10 casual + 8 sick
```

Configure in **Leave Policies → Shift-Based**.

## Testing Your Shift

Before assigning to all employees:

1. **Create test shift**
2. **Assign to 5-10 employees** (test group)
3. **Monitor for 1 week**:
   - Are attendance marks accurate?
   - Is OT calculating correctly?
   - Are break times correct?
4. **Collect feedback**:
   - Are employees satisfied?
   - Any issues?
5. **Adjust if needed**
6. **Roll out to all employees**

## Related Documents

- [Shift Overview](./shift-overview.md)
- [Shift Groups and Rosters](./shift-groups-and-rosters.md)
- [Shift Swaps and Changes](./shift-swaps-and-changes.md)
- [FAQ - Shifts](./faq-shifts.md)

## FAQ

**Q: Can I change shift timing after creating it?**
A: Yes, but it affects future attendance. Existing attendance stands.

**Q: What if I create wrong break timing?**
A: Edit shift, correct break timing, save. Applies to future.

**Q: Can an employee be on multiple shifts simultaneously?**
A: No, one shift at a time. But can be reassigned for different time periods.

**Q: How do I copy a shift to create a similar one?**
A: Go to shift list, click "Duplicate", modify, save as new shift.

**Q: What if shifts overlap (transition time needed)?**
A: Can set 5-15 min overlap for handover, doesn't count as OT.
