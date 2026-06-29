---
title: "Shifts FAQ"
description: "Frequently asked questions about shift management"
category: "Shift Management"
difficulty: "beginner"
tags: ["shift", "faq", "questions", "management"]
version: "1.0"
updated_at: "2026-04-26"
---

# Shifts FAQ

## Shift Creation & Configuration

**Q: What's the minimum shift duration?**
A: Typically 4 hours, but configurable. Some organizations allow 2-hour shifts for part-time roles.

**Q: Can I have overlapping shifts?**
A: Yes, for handover periods. 5-10 minute overlap is normal and doesn't count as double work.

**Q: What if I need 24-hour operations with 8-hour shifts?**
A: Create 3 shifts (morning 8-4, evening 4-12, night 12-8) rotating through employees.

**Q: Can shift start time be before midnight and end after midnight?**
A: Yes. Example: Night shift 10 PM - 6 AM (next day). System handles date rollover.

**Q: Do I need to configure shifts for part-time employees?**
A: Yes, create part-time shift (e.g., 2 PM - 6 PM). Assign same way as full-time.

## Shift Assignment & Rosters

**Q: How far in advance should I create rosters?**
A: Best practice: 1 month advance. Gives employees time to plan and request changes.

**Q: Can I assign same shift to entire department at once?**
A: Yes, use Bulk Assign feature. Select department, shift, date range, and apply.

**Q: What happens if I change shift after roster is published?**
A: New shift only applies to future assignments. Past roster remains unchanged.

**Q: Can employee be on multiple rosters?**
A: No, one roster assignment at a time. If transferred, update roster and remove from old.

**Q: How do I handle seasonal staffing changes?**
A: Create separate rosters per season, publish on transition date. Archive old rosters.

**Q: What if an employee works 2 different jobs (morning in tipsoi, evening elsewhere)?**
A: Tipsoi tracks one job. For dual-job employees, configure shift that matches Tipsoi hours only.

## Shift Swaps & Changes

**Q: How much notice is needed for a shift swap?**
A: Depends on policy. Common: 48 hours. Urgent: as-needed with manager approval.

**Q: Can employees swap shifts with anyone they want?**
A: Depends on policy. Some allow free swaps, others require manager approval. Check your settings.

**Q: What if both employees request to swap with each other?**
A: Perfect! Both agree. Manager can auto-approve if policy allows.

**Q: Can I undo a swap after it's been approved?**
A: Yes, go to Swap History, select swap, click "Revert Swap". Both employees reverted to original.

**Q: What if an employee calls in sick on a swapped shift?**
A: They're marked absent from the swapped shift (the one they're assigned to that day).

## Attendance & Tracking

**Q: How is attendance marked for employees on rotating shifts?**
A: Based on assigned shift that day. System knows current rotation position and expected shift.

**Q: What if punch times are very different from shift?**
A: System marks LATE/EARLY/ABSENT based on punch vs. shift time.

Example:
```
Shift: 8 AM - 5 PM
Punch: 10 AM - 5 PM
Result: 2 hours LATE
```

**Q: Do break times affect attendance marking?**
A: Breaks are unpaid time. Attendance based on total hours (shift hours - break duration).

**Q: What if an employee works beyond shift end time?**
A: Overtime is recorded. Attendance marked as "Present + OT".

**Q: How is half-day shift handled?**
A: Create a "Half-Day" shift (e.g., 8 AM - 12 PM or 1 PM - 5 PM) and assign as needed.

## Overtime & Working Hours

**Q: Is OT calculated on every shift?**
A: No, only if employee works beyond shift end time. Shift defines the baseline.

**Q: What if employee switches shifts mid-month?**
A: Each shift has its own OT calculation. New shift baseline applies from switch date.

**Q: Can OT multiplier be different per shift?**
A: Yes. Example: Night shift OT = 2× (vs. 1.5× for day shift). Configure in shift settings.

**Q: What if employee is on flexible shift?**
A: OT calculated based on actual hours worked vs. minimum required hours.

Example: Flexible shift requires 8 hours/day. If work 9 hours, 1 hour is OT.

## Compliance & Legal

**Q: How do I ensure legal working hour compliance?**
A: Tipsoi has configurable limits (weekly, monthly hours). It alerts you if limits exceeded.

**Q: What's the maximum working hours per week per law?**
A: Varies by country:
- Most: 48 hours/week
- Some: 40 hours/week
- Some: No limit, but OT rules apply

Configure in your region settings.

**Q: How do I handle mandatory rest days by law?**
A: Create rosters with "Off" days. System can enforce min rest days per law.

**Q: Are shift records auditable for compliance?**
A: Yes. All shift assignments, changes, swaps logged with timestamp, user, reason.

## Troubleshooting

**Q: Attendance marked ABSENT but employee says they worked - why?**
A: Likely didn't punch in/out, or punched at wrong time. Check punch records vs. shift time.

**Check**: Punch records, device sync, manual override if punch device failed.

**Q: Shift swap request shows "Coverage alert" - what does that mean?**
A: Approving this swap would leave that shift understaffed. 

**Options**: 
- Choose different date
- Find another employee to cover
- Approve anyway and manually find coverage

**Q: OT not showing up in payroll even though worked past shift?**
A: Check OT eligibility. Is employee eligible? Is shift duration correctly configured?

**Check**: Employee OT eligibility, Shift duration setup, OT threshold (min hours to count).

**Q: Cannot create rotating shift - what's wrong?**
A: Likely missing shift configuration. Create individual shifts first, then create rotation.

**Check**: Have all shifts in rotation been created? Are dates configured correctly?

**Q: Employee showing on multiple rosters - how to fix?**
A: Delete from one roster. Go to that roster, remove employee.

**Q: Roster not publishing - what's the issue?**
A: Likely validation errors (coverage gaps, conflicts). Review validation report and fix.

## Performance & Optimization

**Q: Is there a limit to how many shifts I can create?**
A: No hard limit, but keep it reasonable (10-20 main shifts). Too many confuses scheduling.

**Q: How many rosters can I create?**
A: Unlimited. Archive old rosters to keep system clean.

**Q: What's the max employees in a shift group?**
A: No hard limit. But large groups (500+ employees) may be unwieldy. Consider sub-groups.

**Q: Does shift management affect system performance?**
A: No, shifts are lightweight. Even 1000s of shift assignments run smoothly.

## Best Practices

**Q: How often should I review roster coverage?**
A: Weekly during the month. Check for unplanned absences affecting coverage.

**Q: When should I make roster changes?**
A: Minimize changes. Plan 1 month ahead, then lock roster. Emergency-only changes after that.

**Q: Should I allow unlimited shift swaps?**
A: No. Policy should be: swaps OK but must maintain coverage and minimum notice.

**Q: How do I handle employees who frequently swap?**
A: May indicate:
- Their original shift doesn't work for them → Consider reassigning
- They're flexible (good for coverage) → Keep as on-call
- Scheduling issues → Review your shift patterns

**Q: What's the best shift pattern for fairness?**
A: Depends on operations:
- 24/7 ops: Rotating 3-shift (fair rotation)
- Day operations: Same shift (simpler)
- Mixed: Some rotating, some fixed (balance)

## Support & Escalation

**Q: Where can I get help with complex shift scheduling?**
A: Contact support. Tipsoi can help design shift patterns for your needs.

**Q: Can I import rosters from Excel?**
A: Not directly, but you can:
1. Use Bulk Assign feature
2. Create rosters via API (for tech teams)
3. Manual entry (for small teams)

**Q: Is there a tool to optimize shift assignment?**
A: Tipsoi doesn't have AI optimization, but you can:
- Use suggested patterns (2-2-3, 3-3-3, etc.)
- Manually balance using analytics
- Request help from support team

**Q: How do I handle unusual shift requirements?**
A: Contact support. Examples:
- 12-hour shifts
- Split shifts with big gaps
- On-call with guaranteed minimum
- Seasonal variations

Tipsoi can be configured for most scenarios.

## Contact Support

**Shift-Related Issues?**
- **Chat**: In-app chat support
- **Email**: support@inovacetech.com
- **Phone**: +8809638017170
- **Ticket**: Create support ticket in app
