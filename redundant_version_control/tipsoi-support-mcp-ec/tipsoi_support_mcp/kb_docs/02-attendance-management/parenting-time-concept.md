---
title: "Parenting Time — Why Punch Does Not Show as In/Out Time"
description: "Understanding Parenting Time and why punches appear in logs but not in attendance summary"
category: "Attendance Management"
difficulty: "intermediate"
tags: ["attendance", "parenting time", "punch", "in time", "out time", "allowed window"]
version: "1.0"
updated_at: "2026-04-26"
---

# Parenting Time — Why Punch Does Not Show as In/Out Time

## The Most Common Attendance Confusion

Many Tipsoi users report:

> "The employee punched in, but the In Time is not showing in the attendance report."
> "The punch is in the log, but the attendance summary shows absent."

This is almost always caused by **Parenting Time** (the Allowed Punch Time Window).

---

## What Is Parenting Time?

**Parenting Time** is a time window that Tipsoi uses to determine which punches count as valid **In Time** or **Out Time** for attendance.

The system only accepts a punch as a valid attendance record if it falls **within** the allowed time window around the employee's shift.

**Punches outside this window are recorded in the Punch Log, but do NOT appear in the attendance summary as In Time or Out Time.**

---

## How It Works

### Shift-Based Time Window

Each punch is compared against the employee's assigned shift:

```
Shift: 9:00 AM – 6:00 PM
Parenting Time: ±6 hours (example)

Valid In Time window:  3:00 AM – 3:00 PM
Valid Out Time window: 12:00 PM – 12:00 AM (midnight)
```

If an employee punches outside these windows, the punch is stored in the **Detail Attendance Log** but not shown as In/Out Time in the attendance summary.

### Example 1: Punch Within Window (Shows in Attendance)

```
Shift: 9:00 AM – 6:00 PM
Employee punches: In at 8:55 AM, Out at 6:10 PM

Result: In Time = 8:55 AM, Out Time = 6:10 PM ✓ (shows in attendance)
```

### Example 2: Punch Outside Window (Does NOT Show)

```
Shift: 9:00 AM – 6:00 PM
Employee punches at: 8:00 PM (checking something late at night)

Result: Punch stored in Detail Log, but NOT shown as Out Time in summary
        Attendance may show "No Out Punch" or remain as earlier status
```

---

## Why This Feature Exists

Without a time window, any accidental or unrelated punch would incorrectly update attendance. For example:

- An employee who stays late for a personal reason at midnight would have that midnight punch counted as their "Out Time"
- A security guard who walks past a fingerprint device at random times would generate false attendance records

Parenting Time prevents false or accidental punches from corrupting the attendance record.

---

## How to Diagnose a Parenting Time Issue

If a client says "punch happened but In Time / Out Time is not showing":

**Step 1:** Confirm the employee actually punched
**Step 2:** Ask what time the employee punched
**Step 3:** Find out the employee's shift time (start and end)
**Step 4:** Check if the punch time falls within the allowed window
**Step 5:** Go to the employee's **Detail Attendance Log** to verify the punch exists

### Where to View Detail Attendance Log

1. Go to **Employees → Manage Employees**
2. Click the employee's name to open their profile
3. Look for the **Detail Attendance Log** section
4. This shows every punch: how many times and at what time

---

## Interpreting the Detail Attendance Log

The Detail Attendance Log shows:
- How many times the employee punched
- The exact timestamp of each punch
- Whether each punch was accepted or falls outside the window

If the punch is in the log but NOT in the attendance summary → the punch time is outside the Parenting Time window.

---

## Resolution Options

### Option 1: Employee Must Punch Within Shift Window
Train employees to punch within the normal shift hours. Late-night or very early punches outside the allowed window will not count.

### Option 2: Adjust Parenting Time Settings
If legitimate punches are being rejected (e.g., for employees with irregular hours), the admin can adjust the Parenting Time window. Contact support for guidance on adjusting this setting.

### Option 3: Manual Entry
For a single incident where a valid punch was missed, the admin can add a manual punch record:
- Go to the employee's profile
- Find the attendance entry for that date
- Edit the In Time or Out Time manually

---

## Common Scenarios

### Scenario 1: Night Shift Employee
Employee works night shift 10 PM – 6 AM. If Parenting Time is set for a day shift window (9 AM – 6 PM), the night shift punches may not show.

**Fix:** Ensure the employee is assigned to the correct shift (Night Shift). The system uses the assigned shift to calculate the Parenting Time window.

### Scenario 2: Employee Works Overtime Very Late
Employee's shift ends at 6 PM but stays until 11 PM. If the Parenting Time window only allows punches until 9 PM, the 11 PM Out punch will not show.

**Fix:** Either expand the Parenting Time window or add the Out Time manually.

### Scenario 3: Employee Accidentally Punches at Wrong Time
Employee walks past the device at 2 AM while doing a late-night task. This random punch falls outside the window.

**Correct behavior:** This punch should NOT show in attendance. The Parenting Time feature is working correctly here.

---

## Frequently Asked Questions

**Q: How do I check the current Parenting Time setting?**
A: Contact support or check the shift configuration in Shift Management. The Parenting Time (allowed window) is typically set per shift.

**Q: Can the Parenting Time be different for different shifts?**
A: Yes, each shift can have its own Parenting Time configuration.

**Q: If the punch is outside the window, is it completely lost?**
A: No. The punch is always stored in the Detail Attendance Log. Only the attendance summary excludes it.

**Q: Who can manually correct attendance that was lost due to Parenting Time?**
A: Admin users can make manual corrections. Go to the employee profile and edit the attendance record for that date.

**Q: Is Parenting Time the same as "grace period"?**
A: No. Grace period is the short buffer (e.g., 10 minutes) before marking someone as "Late." Parenting Time is the larger time window that determines if a punch counts at all.

---

## Related Documents

- [Attendance Overview](./attendance-overview.md)
- [Common Issues](../08-troubleshooting/common-issues.md)
- [Tipsoi Support FAQs](../08-troubleshooting/tipsoi-support-faqs.md)

## Support

If Parenting Time issues persist after trying the above:

**Phone:** +8809638017170
**Email:** support@inovacetech.com
