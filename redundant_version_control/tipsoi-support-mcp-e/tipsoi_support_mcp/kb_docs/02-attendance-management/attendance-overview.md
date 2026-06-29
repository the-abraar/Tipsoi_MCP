---
title: "Attendance Management Overview"
description: "Complete guide to tracking and managing employee attendance in Tipsoi"
category: "Attendance Management"
difficulty: "beginner"
tags: ["attendance", "tracking", "devices", "punch", "dashboard"]
version: "1.0"
updated_at: "2024-04-26"
---

# Attendance Management Overview

## What is Attendance Management?

Attendance management in Tipsoi tracks when employees are present, absent, late, or on leave. The system automatically captures punch-in and punch-out times from multiple sources and generates comprehensive reports for analysis.

## How Attendance Works in Tipsoi

### Punch Methods
Employees can record attendance through:

1. **Biometric Devices**
   - Fingerprint scanning (TF 80 device with SIM)
   - Face recognition (Fast Face Device)
   - RFID cards (Prompt Series Device)

2. **Mobile Punch**
   - GPS-based geofencing
   - Mobile app push-to-talk
   - Real-time location tracking

3. **Web Punch**
   - Browser-based punch-in
   - Desktop application
   - Manual entry (by HR admin)

### Attendance States

**Present**: Employee marked present during working hours
- Punch-in and punch-out recorded within shift time
- Shows in attendance dashboard as "Present"

**Late**: Employee arrived after shift start time
- Punch-in time is after official shift start
- Late hours calculated and reported separately

**Absent**: No punch record for the scheduled day
- Employee did not record any attendance
- No punch-in or punch-out found

**On Leave**: Employee has approved leave for the day
- System marks the day as "On Leave" instead of absent
- Payroll processes leave deduction automatically

**Half Day**: Employee worked partial shift
- Half of the working day marked as present
- Useful for leave in afternoon or morning

**Holiday**: Company holiday or weekend
- No attendance expected for these days
- Color-coded in calendar for visibility

---

## Attendance Dashboard

### Key Metrics Displayed

The Attendance dashboard shows real-time statistics:

- **Present**: Number of employees present today
- **Absent**: Number of employees absent today
- **On Time**: Number of employees who arrived on schedule
- **Late**: Number of employees who arrived late
- **On Leave**: Number of employees on approved leave

### Department-Wise Attendance

Visual representation of attendance by department:
- Donut charts showing attendance distribution
- Color-coded by status (Late, Absent, Present, On Leave, Holiday)
- Click to view department-specific details

### Attendance Feed

Real-time feed on the right side showing:
- Recent punch entries (employee name, time, method)
- Entry method (fingerprint, face, RFID, mobile)
- Timestamp of each punch
- Live update as employees check in/out

### Calendar View

Monthly calendar showing:
- Holidays highlighted
- Attendance status color-coded for each day
- Quick view of full month at a glance

---

## Attendance Device Types

### 1. TF 80 Fingerprint Device (SIM Based)

**Specifications**:
- Uses fingerprint scanning
- Requires SIM card for connectivity
- Requires internet/network access
- Standalone operation with cloud sync

**Setup**:
- Enroll employee fingerprints
- Activate SIM card with balance
- Configure device network settings
- Test communication with system

**Benefits**:
- Most reliable for attendance capture
- Works offline with sync capability
- Low power consumption
- Widely used and proven technology

### 2. Fast Face Recognition Device

**Specifications**:
- Uses facial recognition technology
- Requires WiFi connectivity
- Real-time face matching
- No physical contact required

**Setup**:
- Connect to WiFi network
- Enroll employee faces (multiple angles)
- Configure network and cloud settings
- Test face recognition accuracy

**Benefits**:
- No-touch solution (hygienic)
- Faster recognition process
- More difficult to spoof than fingerprints
- Professional appearance

### 3. Prompt Series Device (RFID/Card Based)

**Specifications**:
- Uses RFID card or badge
- WiFi connectivity required
- Employee carries card for scanning
- Real-time transmission

**Setup**:
- Issue RFID cards to employees
- Enroll cards in system
- Configure WiFi connection
- Distribute and educate employees

**Benefits**:
- Quick punch process
- Minimal training required
- Card can be replaced if lost
- Works with multiple punch methods

---

## Understanding Attendance Data

### Punch-In and Punch-Out

**Punch-In**: When employee arrives at workplace
- Recorded at entry point or device location
- Marks the start of working time
- Compared against shift start time

**Punch-Out**: When employee leaves workplace
- Recorded at exit point or device location
- Marks the end of working time
- Used to calculate total working hours

### Important: Parenting Time (Allowed Punch Window)

Tipsoi uses a feature called **Parenting Time** — an allowed time window around the shift start/end time. Only punches within this window are counted as valid **In Time** or **Out Time** in the attendance summary.

**Punches outside the window appear in the Detail Attendance Log only — they do NOT update the attendance summary.**

**Example:** Shift is 9:00 AM – 6:00 PM. If an employee punches at 9:45 PM (after hours), that punch appears in the log but is not counted as the Out Time.

This is the most common reason why a punch exists in the log but the attendance shows "No Out Punch" or appears absent.

To check punch logs: Go to **Employee Profile → Detail Attendance Log**

See full explanation: [Parenting Time Concept](./parenting-time-concept.md)

### Working Hours Calculation

**Expected Hours**: Hours the employee was scheduled to work
**Actual Hours**: Hours the employee actually worked (punch-out - punch-in)
**Difference**: Expected minus Actual hours
- Positive = worked less than expected
- Negative = worked more than expected (overtime)

### Late Calculation

**Late Time**: Difference between punch-in time and shift start time
- Only counted if employee is late
- Not applicable if employee arrives on time
- Used for reports and payroll deductions

---

## Common Attendance Scenarios

### Scenario 1: Regular Present
- Employee punches in within 5 minutes of shift start
- Works full shift duration
- Punches out at shift end or after
- Marked as "Present"

### Scenario 2: Late Arrival
- Employee punches in 15 minutes after shift start
- Works remaining hours
- Marked as "Late" with 15 minutes late time
- May affect payroll or increments

### Scenario 3: Early Exit
- Employee punches out 30 minutes before shift ends
- Marked as "Early Exit"
- Working hours show 30 minutes less than expected
- May be for medical or personal reason

### Scenario 4: Leave Day
- Employee has approved leave for the day
- No punch record expected
- System marks as "On Leave"
- Payroll processes leave deduction automatically

### Scenario 5: Absent
- Employee did not punch in on a scheduled day
- No approval for the day
- Marked as "Absent"
- Payroll may apply absent deduction

---

## Attendance Accuracy

### Device Troubleshooting
If attendance is not showing:
1. Verify device is communicating with system
2. Check device last communication time
3. Verify network connectivity
4. Check SIM balance (for SIM-based devices)
5. Restart device if necessary

### Data Verification
- Daily review of attendance entries
- Compare device records with reports
- Check for anomalies or missing entries
- Correct manual entry errors promptly

### Sync Issues
- Device may take time to upload data
- System queues punches and processes in batches
- Refresh dashboard to see latest updates
- Check system logs if sync is delayed

---

## Next Steps

1. **Review Reports**: See "Attendance Reports" section for detailed analytics
2. **Device Setup**: Configure your attendance devices properly
3. **Policy Configuration**: Set up attendance rules and overtime
4. **Employee Training**: Educate employees on punch-in procedures

**Questions?** Check the FAQ section or contact support at **support@inovacetech.com**
