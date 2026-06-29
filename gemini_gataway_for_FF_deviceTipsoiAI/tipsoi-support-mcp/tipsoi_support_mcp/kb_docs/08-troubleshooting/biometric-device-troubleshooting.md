---
title: "Biometric Device Troubleshooting"
description: "Solutions for device communication and synchronization problems for all Tipsoi device types"
category: "Troubleshooting"
difficulty: "intermediate"
tags: ["troubleshooting", "biometric", "device", "sync", "TF80", "fast face", "prompt series"]
version: "2.0"
updated_at: "2026-04-26"
---

# Biometric Device Troubleshooting

## Tipsoi Device Types

Tipsoi supports three types of biometric attendance devices:

| Device | Connection | Biometric |
|---|---|---|
| **TF 80 Fingerprint Device** | SIM Card (cellular network) | Fingerprint |
| **Fast Face Device** | WiFi | Face recognition |
| **Prompt Series Device** | WiFi | Fingerprint / Face |

Knowing your device type is the first step in troubleshooting.

---

## Step 1: Check Device Communication Status

Before troubleshooting, check if the device is communicating:

1. Log in to the Tipsoi Admin Panel at **https://hrm.tipsoi.pro/login**
2. From the left sidebar, click **Devices**
3. Find your device in the list
4. Check the **Last Communication Time**

- If Last Communication Time is recent (within last few minutes) → Device is communicating
- If Last Communication Time is hours or days old → Device is offline or not syncing

---

## TF 80 Fingerprint Device (SIM Based)

This device uses a SIM card to send data over the cellular network.

### Common Problem: Device Not Communicating

**Cause:** SIM card issue — no network, inactive SIM, or expired recharge.

**Solution:**

1. Check the SIM number that is inside the device
2. Verify the SIM is active (not deactivated)
3. Check the SIM recharge/due date — if it has passed, the SIM is disconnected
4. **Recharge the SIM** (amount depends on carrier plan)
5. After recharging, the device will usually start communicating automatically within a few minutes

**Verification:**
- Check Last Communication Time again in Admin Panel → Devices
- If updated → device is back online
- Then check dashboard for new attendance data

---

## Fast Face Device (WiFi Based)

This device uses WiFi to send data. If the WiFi connection is lost, attendance data stops syncing.

### Common Problem: Device Not Communicating

**Cause:** WiFi disconnected — router changed, password changed, power outage.

**Solution — Reconnect to WiFi:**

1. On the device screen, enter the **Password**: try numbers 1 through 6 (the device unlock PIN is usually between 1-6)
2. Go to **Settings**
3. Go to **Network**
4. Select **WiFi**
5. Connect using your office WiFi password

**Verification:**
- After reconnection, check Last Communication Time in Admin Panel → Devices
- Attendance data should start syncing

---

## Prompt Series Device (WiFi Based)

Similar to Fast Face, this device uses WiFi.

### Common Problem: Device Not Communicating

**Cause:** WiFi disconnected.

**Solution:**
- Contact Tipsoi support for a video guide specific to your Prompt Series model
- Support will provide step-by-step video instructions to reconnect to WiFi

**Support Contact:**
- **Phone:** +8809638017170
- **Email:** support@inovacetech.com

---

## Fingerprint Issues (TF 80 / Prompt Series)

### Problem: Fingerprint Not Recognized

**Causes:**
- Finger is dirty or wet
- Finger has a cut or injury
- Fingerprint was enrolled poorly
- Sensor is dirty

**Solutions:**

1. **Clean the sensor:** Wipe the fingerprint sensor gently with a dry cloth
2. **Clean the finger:** Ensure the finger is clean and dry
3. **Re-enroll the fingerprint:**
   - Go to the employee's profile in Tipsoi Admin Panel
   - Click **Enroll Employee** tab
   - Select the device
   - Select finger and click **Start**
   - Scan the fingerprint 3–5 times for better quality
4. **Try a different finger:** If one finger has an injury, enroll another finger
5. **Use PIN as backup:** If fingerprint cannot work, employee can punch using their PIN

---

## Face Recognition Issues (Fast Face Device)

### Problem: Face Not Being Detected

**Causes:**
- Photo allocated to device is not the right format
- Lighting is too bright or too dark
- Employee is too far from the device or at wrong angle
- Face photo was not approved/allocated properly

**Solutions:**

1. **Check photo quality:** The face photo must be passport-size style with clear face and solid background
2. **Re-allocate face photo:**
   - Go to employee profile in Admin Panel
   - Click **Enroll Employee** tab
   - Select the Fast Face device
   - Allocate a new clear photo
3. **Check device placement:** Device should be at eye level, employee standing directly in front
4. **Improve lighting:** Avoid placing device facing a window or bright light

### Photo Requirements for Face Enrollment
- Passport-size style (face close-up)
- Clear, forward-facing face
- Solid/plain background
- Good lighting — no shadows on face
- Not blurry

---

## General Device Maintenance

### Monthly Checks
- Verify Last Communication Time is recent
- Clean device sensor with dry cloth
- Test punch with a known employee

### What to Do If Device Has Power Outage
- After power is restored, device usually reconnects automatically
- Wait 5 minutes, then check Last Communication Time
- If still offline: reconnect WiFi (Fast Face / Prompt) or check SIM (TF 80)

---

## When to Contact Support

Contact Tipsoi support if:
- Device is not communicating after following all steps above
- SIM appears active but device still not syncing
- WiFi is connected but device still offline
- Fingerprint/face enrollment is failing repeatedly
- Device hardware appears damaged

**Tipsoi Customer Support**
- **Phone:** +8809638017170
- **Email:** support@inovacetech.com

---

## FAQ

**Q: How do I know which device type I have?**
A: Check the device label or the Devices section in Admin Panel. TF 80 devices have a SIM card slot. Fast Face and Prompt Series devices connect to WiFi.

**Q: SIM was recharged but device still not communicating — what next?**
A: Wait 10–15 minutes for network to reconnect. If still not working, contact support with the device's Last Communication Time.

**Q: Can employees use both fingerprint and face on the same device?**
A: Depends on device type. Prompt Series may support multiple methods. Fast Face is primarily face-based. Check your device specifications or contact support.

**Q: Device shows punch but data is not in the system — why?**
A: The device may have stored the punch locally but not yet synced (offline). Once communication is restored, it will upload the stored data.

**Q: How long does punch data stay stored in the device if it is offline?**
A: Most Tipsoi devices store up to 100,000 records locally. Data will sync when communication is restored.
