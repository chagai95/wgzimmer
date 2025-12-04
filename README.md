# WGZimmer Ad Booster

Automated script to keep your WGZimmer room advertisements at the top of listings.

## Features

- ✅ **Smart Scheduling**: Runs 5-7 times per day during active hours (7 AM - 10 PM)
- ✅ **Random Timing**: Uses variable intervals to appear natural
- ✅ **Human-like Behavior**: Random delays, typing speed, scrolling patterns
- ✅ **Multiple Ads**: Supports multiple advertisement codes
- ✅ **Error Handling**: Automatic retry logic and detailed logging
- ✅ **Screenshot Capture**: Saves screenshots for debugging and verification

## Installation

### 1. Run the setup script:

```bash
./setup.sh
```

This will:
- Install Python dependencies (Playwright)
- Download Chromium browser
- Make scripts executable

## Configuration

Edit `wgzimmer_boost.py` to customize:

```python
# Your advertisement codes
CODES = [
    "SCCHCM11YXB7QAN9",  # German December
    "3KKG38MGNTFXARDW",  # German February
    "FGDE7R3Z6SV52PWB"   # 200 Franken
]

# Active hours (7 AM to 10 PM)
ACTIVE_HOURS_START = 7
ACTIVE_HOURS_END = 22
```

## Usage

### Test Mode (Single Run)

Run once with visible browser to verify everything works:

```bash
python3 wgzimmer_boost.py --once
```

### Continuous Mode

Run continuously with random scheduling:

```bash
python3 wgzimmer_boost.py
```

### Background Mode

Run in the background (survives terminal closing):

```bash
nohup python3 wgzimmer_boost.py > output.log 2>&1 &
```

To check the process:
```bash
ps aux | grep wgzimmer
```

To stop the process:
```bash
pkill -f wgzimmer_boost.py
```

## How It Works

1. **Navigation**: Opens wgzimmer.ch homepage
2. **Code Entry**: Enters your ad code in "Mein Inserat ändern" form
3. **Verification**: Submits the code and navigates to edit page
4. **Boost**: Clicks "Inserat aufgeben" button to refresh the ad
5. **Scheduling**: Waits random interval before next run

### Timing Algorithm

- **Daily Runs**: 5-7 times per day
- **Interval Range**: 1.5 to 4 hours between runs
- **Active Hours**: Only runs between 7 AM and 10 PM
- **Randomization**: Each day has slightly different number of runs
- **Ad Order**: Processes ads in random order each time

## Logs and Debugging

### Log Files

- `wgzimmer_boost.log` - Detailed activity log
- `output.log` - stdout/stderr when running in background

### Screenshots

Automatically saved in the current directory:
- `success_[CODE]_[TIMESTAMP].png` - Successful boosts
- `error_[CODE]_[TIMESTAMP].png` - Failed attempts
- `debug_[CODE].png` - Debugging information

### Log Example

```
2024-12-04 09:15:23 - INFO - Starting boost for code: SCCH****
2024-12-04 09:15:25 - INFO - Submitted code verification
2024-12-04 09:15:28 - INFO - Successfully navigated to edit page
2024-12-04 09:15:31 - INFO - Clicked 'Inserat aufgeben' button
2024-12-04 09:15:34 - INFO - ✅ Successfully boosted ad: SCCH****
```

## Troubleshooting

### Issue: Browser won't start

**Solution**: Install Playwright browsers manually:
```bash
playwright install chromium
```

### Issue: Script stops unexpectedly

**Solution**: Check logs for errors:
```bash
tail -f wgzimmer_boost.log
```

### Issue: reCAPTCHA blocking

The script includes:
- Realistic user agent
- Human-like typing speeds
- Random delays and scrolling
- Browser fingerprint masking

If still blocked, try:
1. Increase delay times in the script
2. Run less frequently
3. Use residential IP address

### Issue: Code not working

**Solution**: Verify your codes are correct:
- Check email for correct codes
- Ensure codes haven't expired
- Test manually on the website first

## Advanced Configuration

### Change Run Frequency

Edit `calculate_next_run_time()` function:

```python
# For 3-5 runs per day (less frequent)
min_interval = 3.0 * 3600  # 3 hours
max_interval = 5.0 * 3600  # 5 hours

# For 8-10 runs per day (more frequent)
min_interval = 1.0 * 3600  # 1 hour
max_interval = 2.0 * 3600  # 2 hours
```

### Change Active Hours

```python
ACTIVE_HOURS_START = 8   # Start at 8 AM
ACTIVE_HOURS_END = 20    # End at 8 PM
```

### Headless vs Visible Browser

```python
# Test with visible browser
booster = WGZimmerBooster(headless=False)

# Production with hidden browser
booster = WGZimmerBooster(headless=True)
```

## System Requirements

- Python 3.8+
- Internet connection
- 500MB disk space for browser
- Runs on: Linux, macOS, Windows

## Running as System Service (Linux)

Create `/etc/systemd/system/wgzimmer-boost.service`:

```ini
[Unit]
Description=WGZimmer Ad Booster
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/script
ExecStart=/usr/bin/python3 /path/to/script/wgzimmer_boost.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable wgzimmer-boost
sudo systemctl start wgzimmer-boost
sudo systemctl status wgzimmer-boost
```

## Legal & Ethical Notes

This script is for **educational purposes only**. Please:

- Ensure you own the advertisements you're boosting
- Respect the website's terms of service
- Don't run excessively (default settings are conservative)
- Monitor for any issues and adjust accordingly

## Support

For issues or questions:
1. Check the log files
2. Run in test mode (`--once`) to debug
3. Review screenshots in the working directory
4. Verify your codes are still valid

## License

Educational use only. Use responsibly and ethically.
# wgzimmer
