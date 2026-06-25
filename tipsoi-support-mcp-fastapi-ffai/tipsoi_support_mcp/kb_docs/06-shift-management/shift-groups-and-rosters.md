---
title: "Shift Groups and Rosters"
description: "Managing shift groups and creating schedules"
category: "Shift Management"
difficulty: "intermediate"
tags: ["shift", "group", "roster", "schedule", "planning"]
version: "1.0"
updated_at: "2026-04-26"
---

# Shift Groups and Rosters

## What is a Shift Group?

A **shift group** is a collection of shifts assigned to a team or department. It enables:
- **Bulk assignment** — Apply multiple shifts to a group at once
- **Team scheduling** — Coordinated shifts across a team
- **Pattern reuse** — Use same schedule for similar roles

## Creating a Shift Group

### Step 1: Define the Group

1. Go to **Shifts → Shift Groups → Create New**
2. Enter details:
   - **Group Name**: "Production Team A"
   - **Description**: "Morning & Evening shift pattern"
   - **Department**: Production
   - **Supervisor**: Manager name
3. Click "Next"

### Step 2: Select Shifts

1. Select shifts to include:
   - Morning Shift (8 AM - 4 PM)
   - Evening Shift (4 PM - 12 AM)
2. Click "Add to Group"
3. Click "Create Group"

## What is a Roster?

A **roster** is a schedule showing which employees work which shifts on which dates. It's a calendar view of shift assignments.

**Example**:
```
Employee    | May 1 | May 2 | May 3 | May 4 | May 5 |
Ali Hassan  | Morning | Morning | Off | Evening | Evening |
Fatima Khan | Evening | Off | Morning | Morning | Evening |
Ahmed Khan  | Off | Evening | Evening | Morning | Morning |
```

## Creating a Roster

### Method 1: Calendar View

1. Go to **Shifts → Roster → Create New Roster**

2. **Select Details**:
   - **Roster Name**: "May 2026 Production"
   - **Period**: May 1 - May 31, 2026
   - **Shift Group**: "Production Team A"
   - **Employees**: Select all/specific employees

3. **Create Calendar**:
   - System shows month calendar
   - Each cell is a date-employee combination
   - Drag-drop shifts to cells:
     - Drag "Morning" onto "May 1 - Ali"
     - Drag "Evening" onto "May 1 - Fatima"

4. **Add Days Off**:
   - Right-click on cell → "Mark as Off"
   - Or drag "Off" onto cell

5. **Publish**:
   - Click "Publish Roster"
   - System assigns shifts to employees
   - Employees notified

### Method 2: Pattern-Based Roster

Use pre-configured patterns:

1. Go to **Shifts → Roster → Use Pattern**

2. **Select Pattern**:
   - **Pattern**: "2-2-3 Shift Pattern"
     - 2 days morning
     - 2 days evening
     - 3 days off
     - Repeats every 7 days

3. **Apply to Employees**:
   - Select employee(s)
   - Start date: May 1
   - Click "Apply Pattern"

4. **System auto-fills** the roster

### Method 3: Bulk Assignment

Assign same shift to multiple employees:

1. Go to **Shifts → Roster → Bulk Assign**

2. **Select Details**:
   - **Shift**: Morning Shift
   - **Date**: May 1 - May 5
   - **Employees**: All in Production Dept
   - **Pattern**: Every weekday (Mon-Fri)

3. **Assign**:
   - Click "Assign"
   - System assigns Morning to all selected employees

## Common Roster Patterns

### 2-2-3 Pattern
```
Day 1: Morning
Day 2: Morning
Day 3: Off
Day 4: Evening
Day 5: Evening
Day 6: Off
Day 7: Off

Total: 16 hours work, 5 days off per 7 days
```

### 3-3-3 Pattern
```
Day 1: Morning
Day 2: Morning
Day 3: Morning
Day 4: Evening
Day 5: Evening
Day 6: Evening
Day 7: Off
Day 8: Off
Day 9: Off

Total: 24 hours work, 3 days off per 9 days
```

### 4-4-4 Pattern
```
Days 1-4: Day Shift
Days 5-8: Evening Shift
Days 9-12: Night Shift
Days 13-16: Off (4 days)

Cycle: 16 days
```

### 5-2 Pattern
```
Days 1-5: Work (varying shifts)
Days 6-7: Off (weekend)

Repeat weekly
```

## Managing Roster Changes

### Add Employee to Existing Roster

1. Go to **Shifts → Roster → Select Roster**
2. Click "Add Employee"
3. Select employee
4. Select dates for shifts
5. Assign shifts
6. Save

### Remove Employee from Roster

1. Go to **Shifts → Roster → Select Roster**
2. Click employee row
3. Click "Remove from Roster"
4. Confirm removal

### Modify Shift Assignment

1. Go to **Shifts → Roster → Select Roster**
2. Click on cell (date-employee)
3. Change shift:
   - Select new shift from dropdown
   - Or mark as "Off"
4. Save

### Swap Employees

If two employees want to swap shifts:

1. Go to **Shifts → Roster → Select Roster**
2. Select both employees' rows
3. Click "Swap"
4. System swaps their shifts for selected dates
5. Save

## Roster Validation

Before publishing, validate:

### Check for Issues
```
✓ All dates covered (no gaps)
✓ No employee double-booked (same shift twice)
✓ Days off distributed fairly
✓ Min rest between shifts met (8 hours)
✓ Weekly hours within legal limits
✓ Shift pattern consistent (if rotating)
```

### Conflict Resolution
If issues found:
- System highlights conflicts
- You can fix before publishing
- Example: "Ahmed has morning + evening same day"
  - Solution: Change one to different shift

### Publish Roster

Once validated:
1. Click "Publish Roster"
2. System:
   - Assigns shifts to all employees
   - Notifies employees of schedule
   - Activates for attendance tracking
   - Stores in history

## Roster Approval Workflow

### Draft → Approved → Published

1. **Draft**: Created but not active
   - Can edit freely
   - Employees don't see

2. **Manager Review**:
   - Supervisor/Manager reviews draft
   - Requests changes if needed

3. **Approved**:
   - Manager approves
   - Ready to publish

4. **Published**:
   - Active for attendance
   - Employees can see
   - Changes require new version

## Viewing & Sharing Rosters

### View Roster

1. Go to **Shifts → Roster → My Rosters**
2. Select roster
3. View in calendar or list format

### Print Roster

1. Select roster
2. Click "Print"
3. Choose format:
   - Calendar view (color-coded)
   - List view (spreadsheet-like)
   - Employee-centric (one employee per page)

### Share Roster

1. Select roster
2. Click "Share"
3. Choose recipients:
   - All employees
   - Specific department
   - Individual (email)
4. System sends link/attachment

### Employee View

Employees can:
1. Log in to Tipsoi
2. Go to **My Roster**
3. View their shifts for next 30 days
4. Download/print personal schedule

## Roster Analytics

### Fairness Check
Ensure fair distribution:
```
Employee | Morning | Evening | Night | Off Days |
Ali | 10 | 10 | 5 | 5 |
Fatima | 10 | 10 | 5 | 5 |
Ahmed | 10 | 10 | 5 | 5 |

Fairness: ✓ Evenly distributed
```

### Shift Coverage
Ensure adequate staffing:
```
Date | Required | Morning | Evening | Night | Coverage |
May 1 | 20 | 20 | 0 | 0 | ✓ Covered |
May 2 | 20 | 10 | 10 | 0 | ✓ Covered |
May 3 | 20 | 5 | 5 | 10 | ✓ Covered |
```

### Hours Distribution
Total hours per employee:
```
Employee | Jan | Feb | Mar | Avg |
Ali | 168 | 160 | 170 | 166 |
Fatima | 168 | 160 | 170 | 166 |

Status: ✓ Balanced across month
```

## Roster Versioning

Keep history of roster changes:

### Create New Version

1. Go to **Shifts → Roster → Select Roster**
2. Click "Create New Version"
3. System creates copy of current roster
4. Mark as "v2" or "Updated"
5. Make changes to new version
6. Old version becomes "historical"

### Compare Versions

1. Select roster
2. Click "Compare Versions"
3. View side-by-side:
   - Version 1: Original schedule
   - Version 2: Updated schedule
   - Highlight changes

### Rollback to Previous Version

If new schedule had issues:
1. Go to **Shifts → Roster → History**
2. Select old version
3. Click "Restore"
4. Confirm restoration

## Best Practices for Rosters

1. **Create 1 month in advance**
   - Gives employees time to plan
   - Allows for change requests

2. **Distribute fairly**
   - Alternate unpopular shifts
   - Rotate days off

3. **Minimize disruption**
   - Keep patterns consistent
   - Avoid last-minute changes

4. **Communicate early**
   - Share roster with team
   - Allow feedback time

5. **Use patterns when possible**
   - Easier to manage
   - Employees understand pattern
   - Reduces complaints

6. **Validate before publishing**
   - No conflicts
   - No coverage gaps
   - Legal compliance

## Related Documents

- [Shift Overview](./shift-overview.md)
- [Creating Shifts](./creating-shifts.md)
- [Shift Swaps and Changes](./shift-swaps-and-changes.md)
- [FAQ - Shifts](./faq-shifts.md)

## FAQ

**Q: Can I edit a roster after it's published?**
A: Yes, but it creates a new version. Changes apply going forward, not retroactively.

**Q: What if an employee requests a specific date off?**
A: Manager can approve the request. System marks that date as "Off" for the employee in the roster.

**Q: How do I handle emergency shift coverage?**
A: Can create ad-hoc roster change or use shift swap process. Employee notified of new shift.

**Q: Can rosters be auto-generated?**
A: For pattern-based rosters (2-2-3, 3-3-3), yes. For custom schedules, manual creation needed.

**Q: What if coverage is short on a certain date?**
A: System alerts you. Can manually add shift to an employee or request overtime.
