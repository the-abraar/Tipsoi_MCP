---
title: "Shift Swaps and Changes"
description: "Managing shift changes, swaps, and special requests"
category: "Shift Management"
difficulty: "beginner"
tags: ["shift", "swap", "change", "flexibility", "management"]
version: "1.0"
updated_at: "2026-04-26"
---

# Shift Swaps and Changes

## What is a Shift Swap?

A **shift swap** is when two employees exchange their scheduled shifts for the same or different dates.

**Example**:
- Ali scheduled: May 1 - Morning Shift
- Fatima scheduled: May 1 - Evening Shift
- **Swap**: Ali takes Evening, Fatima takes Morning

## Shift Swap Request Process

### Step 1: Employee Initiates Request

**Employee perspective**:
1. Log into Tipsoi
2. Go to **My Shifts/Roster**
3. Find shift they want to swap
4. Click "Request Swap"
5. Select employee they want to swap with
6. Provide reason (optional): "Need evening for personal commitment"
7. Submit request

**System sends notification** to the other employee.

### Step 2: Other Employee Accepts/Rejects

**Other employee perspective**:
1. Receives notification: "Ali Hassan requested to swap shifts with you"
2. Go to **My Shifts/Roster → Pending Swaps**
3. View swap details:
   - Ali: May 1 - Evening
   - You: May 1 - Morning
4. Click "Accept" or "Reject"

**If rejected**: Requester is notified, swap cancelled.

### Step 3: Manager Approval

**Manager approval needed** if configured:

1. Manager sees pending swap in dashboard
2. Review swap details
3. Check:
   - Coverage not affected
   - Both employees eligible to work swapped shifts
   - No compliance issues
4. Click "Approve" or "Reject"

**If approved**: Shifts are swapped, both employees notified.

### Step 4: Final Confirmation

Swapped shifts are now active:
- Ali works Evening Shift on May 1
- Fatima works Morning Shift on May 1
- Attendance tracked against new shifts

## Direct Shift Change (Manager-Initiated)

Managers can directly change an employee's shift without swap.

### Step 1: Access Roster

1. Go to **Shifts → Roster**
2. Select roster
3. View employee row

### Step 2: Change Shift

1. Click on date-employee cell
2. Select new shift from dropdown:
   - Morning Shift
   - Evening Shift
   - Off
   - Custom shift
3. Enter reason (optional): "Production need"
4. Click "Save"

**Employee is notified** of the change.

### Step 3: Confirmation

Change is effective immediately (or from specified date).

**Note**: Changing without employee agreement may cause morale issues. Best practice: communicate before changing.

## Shift Swap Scenarios

### Scenario 1: Simple Same-Day Swap
```
Ali: May 1 Morning ↔ Fatima: May 1 Morning shift end
Result: Ali takes Evening, Fatima takes Morning on May 1
```

### Scenario 2: Multi-Date Swap
```
Ali: May 1-3 Morning shift ↔ Fatima: May 1-3 Evening shift
Result: All 3 days swapped
```

### Scenario 3: Cascading Swap
Multiple swaps needed:
```
Ali wants Evening → needs Fatima to take Morning
Fatima takes Morning but wants to give Night → needs Ahmed
Ahmed takes Night but wants Ahmed gives Morning → back to original

Solution: Create 3-way swap:
- Ali: Morning → Evening
- Fatima: Evening → Night
- Ahmed: Night → Morning

Manager approves 3-way swap as package deal.
```

## Special Shift Requests

### Last-Minute Change Request

Employee needs urgent shift change (not a swap):

1. Go to **Shifts → Request → Special Request**
2. Select shift change type:
   - **Swap with specific employee**
   - **Request to change to different shift**
   - **Request to mark as off**
3. Provide details and reason
4. Manager reviews (marked as "urgent")
5. Manager approves/rejects

**Manager considerations**:
- Is coverage adequate without this employee?
- Is the reason legitimate?
- What's the business impact?

### Temporary Shift Change

Employee needs to change shift for a period (not permanent).

1. Go to **Shifts → Request → Temporary Change**
2. Enter:
   - **Current Shift**: Morning
   - **New Shift**: Evening
   - **Duration**: June 1 - June 30, 2026
   - **Reason**: Personal commitment
3. Submit
4. Manager approves
5. After end date, revert to original shift automatically

## Shift Coverage Checks

System helps ensure coverage is maintained:

### Before Approval
System checks:
- Are both shifts covered?
- Will min staff be available?
- Any legal working hour violations?

**Example Alert**:
```
⚠️ WARNING: If this swap approved:
- May 1 Evening: Will have only 2 staff (need 3)
- Override approval? [Yes] [No] [Check Alternatives]

Alternatives:
- Ask another employee to come in
- Approve swap and add temp staff
- Reject swap and offer different date
```

### After Rejection
System suggests alternatives:
```
Swap rejected due to coverage.

Alternatives:
1. Swap on May 2 instead (full coverage)
2. Both take evening on May 1 (need temp Morning staff)
3. Find another Evening employee to swap with Fatima

Recommended: Option 1 (May 2)
```

## Shift Swap Policies

Managers can set rules for swaps:

### Policy 1: Open Swaps
```
- Employees can swap freely
- Manager notified but not required to approve
- System checks coverage automatically
```

### Policy 2: Managed Swaps
```
- Employees can request swaps
- Manager must approve before effective
- Manager can reject if coverage compromised
```

### Policy 3: Restricted Swaps
```
- Only manager can initiate swaps
- Employees cannot request
- Used in tight staffing situations
```

### Policy 4: No Swaps
```
- Shifts are fixed
- No swaps allowed
- Used for critical positions (security, compliance)
```

**Configuration**: Go to **Shifts → Settings → Swap Policy**.

## Tracking Swap History

### View Swap History

1. Go to **Shifts → Swap History**
2. Filter by:
   - Employee
   - Date
   - Status (Pending, Approved, Rejected)
3. View all swaps (approved or rejected)

### Swap Audit Trail

Track for compliance:
```
Swap ID: SWAP-00123
Employee 1: Ali Hassan
Employee 2: Fatima Khan
Original Assignment:
  - Ali: May 1 Morning
  - Fatima: May 1 Evening
Swapped Assignment:
  - Ali: May 1 Evening
  - Fatima: May 1 Morning
Requested: May 15, 2:30 PM (Ali initiated)
Approved by: Manager Name
Approved: May 15, 3:00 PM
Status: Approved & Active
```

## Swap Statistics & Trends

### Monitor Swap Patterns
```
Employee | Swaps Initiated | Swaps Accepted | % Approved |
Ali | 8 | 7 | 87% |
Fatima | 5 | 5 | 100% |
Ahmed | 12 | 8 | 67% |

Insight: Ahmed frequently swaps (67% success). Consider if this indicates
scheduling issues or just personal preferences.
```

### Red Flags
- Same employees swapping frequently (scheduling pattern issue?)
- High rejection rate (coverage constraints?)
- Always same direction swaps (someone dislikes shift?)

## Best Practices for Shift Swaps

1. **Establish clear policy**
   - Define approval process
   - Set deadlines (e.g., 48-hour notice)
   - Document coverage requirements

2. **Communicate expectations**
   - Employees understand policy
   - Manager knows what to approve
   - Clear escalation path

3. **Monitor fairness**
   - Ensure all employees can request swaps
   - Track approval rates
   - Address biased approvals

4. **Maintain coverage**
   - Never compromise minimum staffing
   - Have backup plan for rejections
   - Cross-train employees

5. **Document everything**
   - Keep swap history for audit
   - Document reasons for rejections
   - Track patterns over time

6. **Use data**
   - Identify problem shifts (frequently swapped)
   - Adjust scheduling to reduce swaps
   - Make data-driven staffing decisions

## Related Documents

- [Shift Overview](./shift-overview.md)
- [Creating Shifts](./creating-shifts.md)
- [Shift Groups and Rosters](./shift-groups-and-rosters.md)
- [FAQ - Shifts](./faq-shifts.md)

## FAQ

**Q: Can I swap with someone on a different shift type?**
A: Yes, as long as both shifts are assigned. Example: Swap with someone on morning shift even if it's a different date's evening.

**Q: What if someone rejects my swap request?**
A: The swap doesn't happen. You can request again with a different person or different date.

**Q: Can I swap shifts after they've already happened?**
A: No, swaps only work for future shifts. Past shifts are recorded.

**Q: What if my swap is rejected due to coverage?**
A: Try alternative dates/shifts, or ask another employee, or request a different time slot.

**Q: Do swaps affect my attendance record?**
A: No, attendance is tracked against whatever shift you actually work. Swapped shift is just a change of assignment.

**Q: Can manager force a swap on an employee?**
A: Not recommended, but manager can directly change shifts (not a swap). Better to communicate and request.

**Q: Are shift swaps recorded for compliance audit?**
A: Yes, all swaps are logged with timestamp, approval, and audit trail.
