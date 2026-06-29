---
title: "Employee Management Guide"
description: "Complete guide for managing employee records and profiles in Tipsoi"
category: "Employee Management"
difficulty: "beginner"
tags: ["employees", "profiles", "onboarding", "offboarding", "management"]
version: "1.0"
updated_at: "2024-04-26"
---

# Employee Management Guide

## Overview

Employee management in Tipsoi handles the complete employee lifecycle from hiring to retirement, including profile management, department assignment, role configuration, and offboarding.

---

## Creating Employees

### Method 1: Individual Employee Creation

**Path**: Employees → Manage Employees → Create Employee

**Steps**:
1. Click "Create Employee" button
2. Enter employee information:
   - Full Name (required)
   - Email Address (required)
   - Employee ID (optional, auto-generated)
   - Gender (Male/Female/Other)
   - Designation
   - Department
   - Employment Type (Permanent/Contract/Temporary)
   - Reporting Manager
3. Set login password
4. Click "Create Employee"

**Information Captured**:
- Personal details (name, email, phone)
- Employment details (ID, designation, department)
- Organizational hierarchy (reporting structure)
- Status (Active/Inactive)
- Profile picture (optional)

### Method 2: Bulk Employee Upload

**Path**: Employees → Create Batch

**Steps**:
1. Go to "Create Batch"
2. Download sample Excel template
3. Fill in employee information:
   - Name
   - Email
   - Employee ID
   - Department
   - Designation
   - Employment Type
4. Upload the file
5. Review and confirm
6. System creates all employees at once

**Advantages**:
- Fast setup for large organizations
- Reduces manual data entry
- Batch processing saves time
- Reduces errors with template format

### Employee Profile Information

**Required Fields**:
- Employee Name
- Email Address
- Department
- Designation

**Optional Fields**:
- Phone Number
- Mobile Number
- Address
- Date of Joining
- Date of Birth
- Gender
- Religion (if applicable)
- Nationality
- Bank Account Details
- Emergency Contact
- Employee Photo

---

## Managing Employee Profiles

### Viewing Employee Profile

**Path**: Employees → Manage Employees → Click Employee Name

**Profile Sections**:
1. **Personal Information**
   - Name, email, phone
   - Date of birth
   - Address

2. **Employment Details**
   - Employee ID
   - Designation
   - Department
   - Employment type
   - Reporting manager

3. **Attendance Information**
   - Shift assignment
   - Work location
   - Biometric enrollment status

4. **Leave Information**
   - Leave balance
   - Leave policy assigned
   - Leave history

5. **Payroll Information**
   - Salary components
   - Bank account
   - Tax ID

6. **Documents**
   - Attached files
   - Certifications
   - Agreements

### Editing Employee Information

1. Open employee profile
2. Click "Edit" button
3. Update necessary fields
4. Save changes
5. Changes reflect immediately

**Note**: Some fields (like Employee ID) may be locked after creation.

### Deactivating Employees

**When to Deactivate**:
- Employee resignation
- Termination
- Leave of absence
- Retirement

**Steps**:
1. Open employee profile
2. Change status to "Inactive"
3. Save changes
4. Employee can no longer log in
5. Historical data preserved for reporting

**Impact**:
- Employee cannot access Tipsoi
- Not included in new reports
- Historical attendance/leave records remain
- Can be reactivated if needed

---

## Organizational Structure

### Departments

Departments organize employees by functional areas.

**Creating Departments**:
- Path: Settings → Departments
- Enter department name
- Assign department head/manager
- Set budget (optional)

**Department Hierarchy**:
- Main department (e.g., Sales)
- Sub-departments (e.g., Field Sales, Inside Sales)
- Nested structure possible
- Supports complex organizations

### Designations

Job titles and roles for employees.

**Creating Designations**:
- Path: Settings → Designation
- Enter designation name (e.g., Sales Executive)
- Assign to department
- Set salary range (optional)
- Define responsibilities

### Employee Types

Different employment categories.

**Types Available**:
- Permanent: Full-time permanent employees
- Contract: Fixed-term contract employees
- Temporary: Short-term temporary staff
- Intern: Unpaid or fixed-stipend interns
- Consultant: External consultants

**Configuration**:
- Default benefits per type
- Leave entitlements
- Salary structure
- Contract end handling

---

## Employee Onboarding

### Pre-Onboarding Checklist

**HR Preparation**:
- Create employee record in system
- Assign initial password
- Configure access permissions
- Assign shift and location
- Enroll in leave policy
- Add to payroll system

**Admin Preparation**:
- Biometric device setup
- Mobile app installation
- Equipment allocation
- System access provisioning

### Day 1 Activities

**Employee Receives**:
- Welcome email with login credentials
- System user guide
- Mobile app installation link
- Device enrollment instructions

**Employee Does**:
- Log in to verify credentials
- Update personal information
- Review policies and agreements
- Download mobile app
- Enroll biometric if required

### Week 1 Training

**Topics to Cover**:
- System navigation and features
- Attendance punch procedures
- Leave application process
- Mobile app usage
- Report access and interpretation
- Department-specific processes

### First Month

**Verification**:
- System is working correctly
- Attendance being captured properly
- Mobile punch functioning
- Leave balance calculated correctly
- All documents uploaded

---

## Employee Life Cycle

### Active Phase
- Normal employment
- Full system access
- Attendance tracking
- Leave processing
- Payroll deduction

### Leave of Absence
- Employee temporarily not working
- Optional: Maintain system access
- Leave still accrues (depending on policy)
- Attendance not tracked
- Payroll adjustments applied

### Resignation/Termination
- Notice period management
- Final settlement calculation
- Leave encashment
- Document archival

### Offboarding Process

**Before Departure**:
1. Collect all company assets
2. Download/archive employee documents
3. Final payroll run
4. Generate full attendance history
5. Calculate leave encashment
6. Store digital records

**On Last Day**:
1. Disable system access
2. Mark as "Inactive"
3. Process final salary
4. Generate exit documentation

**Post-Departure**:
1. Archive employee folder
2. Retain for audit/legal
3. Generate experience letter
4. Provide reference documents

---

## Employee Reports

### Available Reports

1. **Employee List**
   - All active employees
   - Department-wise breakdown
   - Export to Excel

2. **Employee Directory**
   - Contact information
   - Department assignment
   - Reporting structure

3. **Department Summary**
   - Employee count by department
   - Designations in each department
   - Budget allocation

4. **New Joiners Report**
   - Employees joined in date range
   - By department
   - Onboarding status

5. **Attrition Report**
   - Employees who left
   - Reasons for leaving
   - Retention analysis

### Report Filtering

- Date range
- Department
- Designation
- Employment type
- Status (Active/Inactive)
- Manager/Team

---

## Employee Master Data

### Enrollment (Biometric)

**When**: After employee creation
**How**: Using biometric device or mobile app
**Required**: At least 2 fingerprints or 1 face scan
**Purpose**: For attendance capture

**Steps**:
1. Open employee profile
2. Click "Enroll Employee" tab
3. Select device (fingerprint/face)
4. Capture biometric data
5. Verify enrollment success
6. Employee ready for attendance

### Workplace Assignment

Assign employees to physical locations.

**Options**:
- Main office
- Field site 1
- Field site 2
- Remote/Work from home

**Impact on**:
- Mobile punch geofencing
- Attendance reports
- Location tracking

### Shift Assignment

Assign work schedules to employees.

**Options**:
- Individual shift assignment
- Department shift assignment
- Roster-based (rotating shifts)
- Custom shift creation

**Details Captured**:
- Shift name
- Start time
- End time
- Break duration
- Working days

---

## Best Practices

### For Setting Up Employees
1. Collect complete information upfront
2. Use consistent naming conventions
3. Assign reporting managers properly
4. Configure leave policies early
5. Complete biometric enrollment immediately

### For Managing Employees
1. Keep profile information current
2. Update designations when promoted
3. Review department assignments regularly
4. Monitor active vs. inactive counts
5. Archive documents properly

### For Data Quality
1. Validate email addresses
2. Use standardized department names
3. Maintain consistent Employee ID format
4. Regular audit of employee data
5. Backup employee records

---

## Troubleshooting

### Issue: Employee Can't Log In
- Verify account is Active
- Check password is correct
- Confirm email is correct
- Reset password if needed

### Issue: Attendance Not Capturing
- Verify biometric enrollment
- Check shift assignment
- Confirm workplace location
- Test device communication

### Issue: Leave Balance Wrong
- Verify leave policy assignment
- Check accrual configuration
- Review past leave approvals
- Check for manual adjustments

---

## Next Steps

1. **Create Employee Records**: Add all team members to system
2. **Configure Organization**: Set up departments and designations
3. **Assign Shifts**: Link employees to work schedules
4. **Enroll for Attendance**: Complete biometric setup
5. **Configure Payroll**: Add salary information

**Questions?** Contact support at **support@inovacetech.com**
