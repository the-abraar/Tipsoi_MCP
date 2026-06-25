---
title: "Tipsoi Support FAQs — Real Issues and Solutions"
description: "The most common issues reported by Tipsoi customers with step-by-step solutions"
category: "Troubleshooting"
difficulty: "beginner"
tags: ["faq", "troubleshooting", "support", "issues", "solutions", "device", "attendance", "login"]
version: "1.0"
updated_at: "2026-04-26"
---

# Tipsoi Support FAQs

These are the most common issues reported by Tipsoi clients, collected from the Tipsoi Customer Support Team.

---

## FAQ 01: Data Not Showing / Attendance Not Coming

### What clients typically ask
- Why is no data showing in the system today?
- Attendance punch happened but the dashboard is not showing it
- Device is punching but data is not coming to the software

### How to identify the problem

**Step 1: Check if the device is communicating**
- Log in to the Tipsoi Admin Panel
- From the sidebar, click **Devices**
- Find your device and check the **Last Communication Time**
- Share the last communication time with the support team if needed

**Step 2: Identify your device type**

Tipsoi uses three types of devices:

**TF 80 Fingerprint Device (SIM Based)**
- Check the SIM number in the device
- Check if the SIM is active
- Check if the SIM recharge/due date has passed
- After recharging, the device usually starts communicating again

**Fast Face Device (WiFi Based)**
- Ask the client to reconnect the device to WiFi:
  - On device: Password → 1 to 6 → Settings → Network → WiFi → Connect using your WiFi password

**Prompt Series Device (WiFi Based)**
- Provide the client with a video guide to reconnect to WiFi

### How to confirm the issue is resolved
- After following the steps, check if **Last Communication Time** is updated
- Then check if data appears in the dashboard or reports
- If data is still not appearing, escalate to support

### Tipsoi Customer Support
**Phone:** +8809638017170
**Email:** support@inovacetech.com

---

## FAQ 02: Login Issue — Cannot Log In

### What clients typically ask
- Why can I not log in?
- I am entering the correct email and password but it is not working
- "Incorrect Credentials" error keeps showing

### Tipsoi Login URL
To access Tipsoi: **https://hrm.tipsoi.pro/login**
Enter your **Email/Employee ID** and **Password**.

### How to identify the problem

1. If support can log in using the same credentials → the issue is typing mistake, browser cache, or device problem
2. If support also cannot log in → the credentials are wrong
3. If many users are complaining simultaneously → possible server issue

### Step-by-step solution

**Step 1: Verify Email and Password**
- Ask client to carefully re-enter email and password (watch for caps lock, spacing)

**Step 2: Collect Credentials (if still failing)**
- Ask client to send their email and password via WhatsApp
- Support team logs in from their side to test
- If login works → inform client the credentials are correct; the issue was typing or browser

**Step 3: If Login Works from Support Side**
- Likely cause: network issue, browser cache, or app cache on client's device
- Ask client to try: different browser / clear cache / restart phone

**Step 4: If System is Down**
- Inform client: "There is a temporary issue. Our technical team is working on it. We will update you when resolved."

### Tipsoi Customer Support
**Phone:** +8809638017170
**Email:** support@inovacetech.com

---

## FAQ 03: Location Tracking Not Showing

### What clients typically ask
- Why is my employee's location not visible?
- Location tracking report is blank
- Location update is not coming
- Tracking is turned on but data is not showing

### How to identify the problem

**If only one employee's location is not showing** → Problem is on that employee's mobile (internet off, GPS off, app not in background)

**If all employees' locations are not showing** → Problem is in Admin settings (location tracking is not activated)

### Step-by-step solution

**Step 1: Check Admin Settings**
- Go to **Settings** in Admin Panel
- Check if location tracking is enabled for employees

**Step 2: Check Employee Mobile Settings**
On the employee's phone, verify:
- Mobile Data is ON
- GPS / Location is ON
- App is running in background

**Step 3: If Still Not Working**
- Get the employee's WhatsApp number
- Do a video call or screen share to visually check settings

**Step 4: Permission and App Check**
On the employee's phone, confirm:
- Location permission is **Allowed**
- Mobile data is ON
- GPS is ON
- App background is running
- App is updated to the latest version

**Step 5: Refresh and Recheck**
- Ask client to close and reopen the app
- Then reload the Location Tracking Report

### Best settings for accurate location tracking
- Keep Mobile Data ON at all times
- Keep GPS / Location ON
- Turn Battery Optimization OFF for the Tipsoi app
- Keep app running in background
- Keep app updated

### Tipsoi Customer Support
**Phone:** +8809638017170
**Email:** support@inovacetech.com

---

## FAQ 04: Face Photo Upload Issue

### What clients typically ask
- I am allocating a face photo but it is not being accepted
- Photo upload is not saving
- Face image is given but device is not detecting it
- I cannot add a photo for an employee

### How to identify the problem

- If the image does not have a clear face → image quality issue (blur, low light, low resolution, face not visible)
- If the background has many objects → device cannot detect the face clearly
- If it is a full-body photo → face area is too small to detect

### Step-by-step solution

**Step 1: Check Photo Quality**
- Face must be clearly visible
- Background must be solid/plain color

**Step 2: Review the Photo**
If the client is unsure, ask them to send the photo via WhatsApp so support can check it

**Step 3: Correct Photo Requirements**
The photo must be:
- Passport-size style (face close-up, not full body)
- Face clearly visible and facing forward
- Good lighting — no harsh shadows
- Solid or plain background (no objects behind)
- Not blurry

**Step 4: Photo Crop and Retry**
- If the photo is full-body, crop it to show only the face area clearly
- Then retry the upload/allocation

**Step 5: Support Assistance**
- If all steps are followed and still failing, support team can assist with cropping and allocation

### Tipsoi Customer Support
**Phone:** +8809638017170
**Email:** support@inovacetech.com

---

## FAQ 05: Punch Happened But In Time / Out Time Is Not Showing

### What clients typically ask
- Employee punched in but In Time is not showing
- Only In Time shows, Out Time is not showing
- Punch log shows the entry but attendance summary does not show it

### The Core Concept: Parenting Time

Tipsoi uses a feature called **Parenting Time** (Allowed Time Window).

The system only counts a punch as a valid **In Time** or **Out Time** if it happens within a specific time window around the shift start/end time.

**Example:**
- Shift: 9:00 AM to 6:00 PM
- Parenting Time: 6 hours before or after shift time
- Valid In Time window: 3:00 AM to 3:00 PM (6 hours either side of 9:00 AM)
- If employee punches at 8:00 PM → this falls outside the window → it appears in the punch log but does **NOT** appear as In/Out Time in the attendance summary

### Step-by-step solution

**Step 1: Confirm the Punch Happened**
- Ask the client to confirm the employee did punch

**Step 2: Check the Shift Time**
- Find out the employee's assigned shift start and end time

**Step 3: Check Punch Time**
- Ask what time the employee punched

**Step 4: Compare with Parenting Time**
- Check if the punch time falls within the allowed window around the shift time
- If the punch is outside the window, it will only appear in the **Detail Attendance Log** — not in the attendance summary

**Step 5: View Detail Attendance Log**
- Go to the employee's profile
- Check the **Detail Attendance Log**
- This shows every punch record (time and count)

### Tipsoi Customer Support
**Phone:** +8809638017170
**Email:** support@inovacetech.com

---

## FAQ 06: Cannot Create Employee

### What clients typically ask
- I cannot create a new employee — why?
- Error is showing when I try to add an employee
- Password is not being accepted
- "Employee ID already exists" error

### Employee Create Path
**Employees → Create Employee**

### Required information
- **Employee Name**
- **Employee ID** (must be unique — no duplicates)
- **Email** (must be unique — no other employee can have the same email)
- **Password**

### Password requirements
The password must have:
- Minimum **8 characters**
- At least one **Capital Letter**
- At least one **Small Letter**
- At least one **Number**
- At least one **Special Character** (e.g., @, #, $, !)

If any of these requirements are not met, the employee will not be created.

### Common error causes and fixes

| Error | Cause | Fix |
|---|---|---|
| "Email already in use" | Another employee has this email | Use a different email address |
| "Employee ID already exists" | ID is a duplicate | Use a different, unique ID |
| Password not accepted | Does not meet requirements | Use 8+ chars with uppercase, lowercase, number, special char |

### Tipsoi Customer Support
**Phone:** +8809638017170
**Email:** support@inovacetech.com

---

## FAQ 07: How to View Monthly Attendance Report

### What clients typically ask
- Where can I find the monthly attendance report?
- How do I download one month's report?
- I want to see the monthly report

### Navigation path
**Reports → Attendance Report → (select date range)**

### Step-by-step

1. Log in to the Tipsoi Admin Panel
2. From the sidebar, click **Reports**
3. Click **Attendance Report**
4. Use the **Calendar filter** to select the start date and end date for the month
5. The monthly report will load
6. To download: click **Excel** or **PDF** button

### Reports available under Attendance Report
- Individual Attendance Report
- Detailed Attendance Report
- Department Report
- Monthly Report
- Detailed Monthly Report
- Daily Report

---

## FAQ 08: I Have Two Offices — How to See Separate Data?

### What clients typically ask
- How do I view reports for each of my two offices separately?
- I want to see attendance for a different office location
- Can I see both offices' reports together?

### How Tipsoi handles multiple offices

Tipsoi uses **Workplaces** to separate data from different offices or branches.

**If Workplaces are not created** → branch data cannot be separated.
**If employees are assigned to the wrong Workplace** → report will show incorrect data.

### Step-by-step solution

**Step 1:** Go to **Settings → Workplaces**
- Create a Workplace for each office

**Step 2:** Assign employees to the correct Workplace
- In each employee's profile, set their Workplace

**Step 3:** Filter reports by Workplace
- In any report, use the **Filter** option and select Workplace to see location-specific data

**Short summary:** Create Workplaces in Settings and assign employees correctly. Then all branch reports can be viewed separately using the Workplace filter.

---

## FAQ 09: Office Time is Changing (e.g., Ramadan) — How to Update in System?

### What clients typically ask
- How do I change office timing for Ramadan?
- I want to temporarily change the shift time
- How do I create a new shift and activate it?

### Solution

To change office timing temporarily (such as for Ramadan):

**Step 1: Create a New Shift**
- Go to **Shift Management → Shifts**
- Create a new shift with the updated timings

**Step 2: Edit the Roster**
- Go to **Shift Management → Roster**
- Find the currently running Roster
- Click **Edit** on that Roster
- Select the new Shift you just created
- Set the Off Days and the **Effective Date** for when the new timing should start
- Click **Save Change**

The new shift timing will be active from the effective date onwards.

**Short summary:** Create a new shift → Go to Roster → Edit → Select new shift → Set effective date → Save.

---

## FAQ 11: How to Set Up Leave in the System?

### What clients typically ask
- How do I set up a leave policy?
- How do I add annual leave or sick leave?

### Leave Setup Path in Tipsoi

Leave setup follows this sequence:

**Step 1:** Go to **Leave** from the sidebar
- Click **Leave Category**
- Create leave categories (e.g., "Annual Leave", "Medical Leave", "Earned Leave", "Maternity Leave")

**Step 2:** Create **Leave Policy**
- Go to **Leave → Leave Policy**
- Create a policy and link it to the categories

**Step 3:** Configure the Leave Policy
- Go to **Leave → Configuration**
- Set the number of days, accrual method, carry-forward rules, etc.

**Step 4:** Assign Policy to Employees
- Assign the leave policy to employees (by department, designation, or individually)

**Short summary:** Leave Category → Leave Policy → Configuration → Assign to employees.

### Tipsoi Customer Support
**Phone:** +8809638017170
**Email:** support@inovacetech.com

---

## General Support Escalation Process

If the chatbot or self-service steps do not resolve the issue, escalate to the support team with:

1. **Customer Name**
2. **Company Name**
3. **Contact Number**
4. **Issue Description**
5. **Screenshot or Error Message** (if any)
6. **Troubleshooting steps already taken**

Inform the customer:
> "Your issue has been forwarded to the Tipsoi Customer Support Team. Our representative will contact you shortly."

**Tipsoi Customer Support Contact**
- **Phone:** +8809638017170
- **Email:** support@inovacetech.com
