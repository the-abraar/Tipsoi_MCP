---
title: "Common Issues & Solutions"
description: "The most frequently reported Tipsoi issues with step-by-step solutions"
category: "Troubleshooting"
difficulty: "beginner"
tags: ["troubleshooting", "issues", "solutions", "help", "attendance", "login", "device"]
version: "2.0"
updated_at: "2026-04-26"
---

# Common Issues & Solutions

These are the most frequently reported issues by Tipsoi users.

---

## Issue 1: Attendance Data Not Showing / Device Not Syncing

**Symptom:** Employee punched on device but attendance is not visible in the system.

**First step:** Check device communication
1. Log in to Admin Panel at **https://hrm.tipsoi.pro/login**
2. From the left sidebar, click **Devices**
3. Check the **Last Communication Time** for your device

**Based on device type:**

**TF 80 Fingerprint Device (SIM Based)**
- Check if SIM is active
- Check if SIM recharge date has passed
- Recharge the SIM — device will reconnect automatically

**Fast Face Device (WiFi Based)**
- Reconnect device to WiFi: on device → Password → Settings → Network → WiFi → connect using office WiFi password

**Prompt Series Device (WiFi Based)**
- Contact support for a video guide to reconnect WiFi

See: [Biometric Device Troubleshooting](./biometric-device-troubleshooting.md)

---

## Issue 2: Punch Shows in Log But Not in In Time / Out Time

**Symptom:** Punch record exists but attendance summary shows absent or missing In/Out Time.

**Cause:** Punch happened outside the **Parenting Time** (Allowed Time Window).

Tipsoi only counts a punch as valid In Time or Out Time if it falls within the configured time window around the shift start/end. Punches outside this window appear in the **Detail Attendance Log** only.

**Steps to verify:**
1. Go to Employee profile → Detail Attendance Log
2. Confirm the punch exists with exact timestamp
3. Compare punch time against shift start/end time
4. If punch is far outside shift time → it was outside the Parenting Time window

**Fix:**
- For a one-time issue: admin can add a manual attendance entry for that date
- To prevent future: train employees to punch within normal shift hours

See: [Parenting Time Concept](../02-attendance-management/parenting-time-concept.md)

---

## Issue 3: Login Not Working

**Symptom:** Cannot log in despite entering correct credentials.

**Login URL:** https://hrm.tipsoi.pro/login

**Step-by-step:**

1. **Re-enter credentials carefully** — check caps lock, spacing, typing mistakes
2. **Try a different browser** — Chrome, Firefox, Edge
3. **Clear browser cache** — go to browser settings → History → Clear browsing data
4. **Try on mobile app** — if web is blocked, try the Tipsoi mobile app
5. **Check internet connection** — ensure you have stable internet

**If still failing:**
- Send credentials to support via WhatsApp
- Support team will test login from their side
- If they can log in, issue is with your device/browser
- If they cannot log in either, credentials may need resetting

**If many users are affected simultaneously** — possible server maintenance. Contact support.

**Support:** +8809638017170 | support@inovacetech.com

---

## Issue 4: Cannot Create Employee

**Symptom:** Error when trying to add a new employee.

**Path:** Employees → Create Employee

**Required fields:**
- Employee Name
- Employee ID (must be unique — no duplicates)
- Email (must be unique — no two employees can share an email)
- Password

**Password requirements** (must meet ALL):
- Minimum 8 characters
- At least one Capital Letter
- At least one Small Letter
- At least one Number
- At least one Special Character (e.g., @, #, $, !)

**Common errors and fixes:**

| Error | Fix |
|---|---|
| "Email already in use" | Use a different email address |
| "Employee ID already exists" | Use a different Employee ID |
| Password not accepted | Ensure it meets all 5 requirements above |

---

## Issue 5: Location Tracking Not Showing

**Symptom:** Employee location is not visible in the Location Tracking Report.

**If only one employee's location is missing:** Problem is on that employee's phone.

**If all employees' locations are missing:** Problem is in Admin Settings (location tracking may be deactivated).

**Check employee's phone:**
- Mobile Data is ON
- GPS / Location is ON
- App is running in background
- Location permission is set to "Always" for the Tipsoi app
- App is updated to the latest version

**Check Admin Panel:**
- Go to Settings
- Verify location tracking is enabled for employees

See: [Tipsoi Support FAQs — FAQ 03](./tipsoi-support-faqs.md)

---

## Issue 6: Face Photo Upload Failing

**Symptom:** Cannot upload or allocate a face photo for an employee.

**Cause:** Photo does not meet requirements.

**Photo requirements:**
- Passport-size style (face close-up, not full body)
- Face clearly visible and facing forward
- Solid/plain background (no objects or busy background)
- Good lighting — no harsh shadows on face
- Not blurry, not low resolution

**Fix:**
1. Use a clear passport-size photo
2. Crop if the existing photo is full-body
3. Ensure background is plain
4. Try again after adjusting the photo

See: [Tipsoi Support FAQs — FAQ 04](./tipsoi-support-faqs.md)

---

## Issue 7: Cannot View Monthly Report

**Symptom:** Not sure where to find the monthly attendance report.

**Path:** Reports → Attendance Report

1. From sidebar, click **Reports**
2. Click **Attendance Report**
3. In the sub-menu, click **Monthly Report** (or use the calendar filter in any report to set a monthly date range)
4. Select the month using the start and end date calendar
5. Report loads
6. Download as Excel or PDF

See: [Reports Overview](../07-reports/reports-overview.md)

---

## Issue 8: Two Offices — Cannot See Separate Data

**Symptom:** Cannot filter attendance data by office location.

**Solution:** Use the Workplaces feature.

1. Go to **Settings → Workplaces**
2. Create a Workplace for each office/branch
3. Assign each employee to their correct Workplace (in employee profile)
4. In any report, use **Filter → Workplace** to view data per location

**If Workplaces are not created:** All employees appear as one group — no way to separate by location.

---

## Issue 9: Office Timing Changed (e.g., Ramadan)

**Symptom:** Need to change shift timing for a period of time.

**Solution:**

1. **Create a new shift** with the updated timing:
   - Go to **Shift Management → Shifts**
   - Create new shift (e.g., "Ramadan Shift" with new hours)

2. **Update the Roster:**
   - Go to **Shift Management → Roster**
   - Find the currently running Roster
   - Click Edit
   - Select the new shift
   - Set Off Days and **Effective Date**
   - Click Save Change

The new timing will be active from the effective date.

---

## Issue 10: Leave Policy Not Set Up

**Symptom:** Cannot apply leave because there is no leave policy configured.

**Solution — set up in this order:**

1. **Create Leave Category:** Go to **Leave → Leave Category**
   - e.g., Annual Leave, Medical Leave, Earned Leave, Maternity Leave

2. **Create Leave Policy:** Go to **Leave → Leave Policy**
   - Link to categories

3. **Configure the Policy:** Go to **Leave → Configuration**
   - Set entitlement days, accrual method, carry-forward rules

4. **Assign to Employees:** Apply the policy to employees by department or individually

---

## Quick Reference

| Issue | Where to Check | Quick Fix |
|---|---|---|
| No attendance data | Devices → Last Communication Time | Fix device connectivity (SIM/WiFi) |
| Punch in log only | Employee profile → Detail Attendance Log | Check Parenting Time window |
| Login failing | https://hrm.tipsoi.pro/login | Recheck credentials, clear browser cache |
| Cannot create employee | Employees → Create Employee | Check email uniqueness, password requirements |
| Location not showing | Settings → Location Tracking; Employee's phone GPS/Data | Enable GPS and mobile data on employee's phone |
| No monthly report | Reports → Attendance Report | Select date range, download PDF/Excel |
| Two offices data mixed | Settings → Workplaces | Create Workplaces, assign employees |

---

## Contact Support

If the above steps do not resolve your issue:

**Phone:** +8809638017170
**Email:** support@inovacetech.com

When contacting support, please provide:
- Your Company Name
- Contact Number
- Issue Description
- Steps already tried
- Screenshot or error message (if any)
