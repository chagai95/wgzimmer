# Troubleshooting Guide - WGZimmer Ad Booster

## Common Issues and Solutions

### 1. "playwright: command not found"

**Problem**: Playwright is not installed

**Solution**:
```bash
pip install --break-system-packages playwright
playwright install chromium
```

### 2. Script stops after a few runs

**Problem**: Could be various - check the logs

**Diagnostic**:
```bash
# View recent log entries
tail -50 wgzimmer_boost.log

# View errors only
grep ERROR wgzimmer_boost.log

# Check if process is running
ps aux | grep wgzimmer_boost
```

**Solutions**:
- If reCAPTCHA errors: Increase delays in the script
- If timeout errors: Check internet connection
- If code errors: Verify your ad codes are still valid

### 3. reCAPTCHA is blocking the script

**Problem**: Website detects automation

**Solutions**:

1. **Increase human-like delays** (edit wgzimmer_boost.py):
```python
# Change these values to be slower
async def random_delay(self, min_seconds: float = 2.0, max_seconds: float = 5.0):
    # Increased from 1.0-3.0 to 2.0-5.0
```

2. **Run less frequently**:
```python
# Change to 3-4 runs per day instead of 5-7
min_interval = 3.5 * 3600  # 3.5 hours
max_interval = 6.0 * 3600  # 6 hours
```

3. **Add more randomness**:
```python
# In boost_ad method, add extra delays
await self.random_delay(5, 10)  # Wait 5-10 seconds
```

### 4. No screenshots are being saved

**Problem**: Permission issues or path problems

**Solution**:
```bash
# Make sure the script has write permissions
chmod +w /home/claude/
# Or change screenshot path in script to current directory
```

### 5. Script crashes with "Context closed" error

**Problem**: Browser context issues

**Solution**: The script will automatically restart. If it happens frequently:
```python
# Add this to the run_continuous function
try:
    await booster.boost_all_ads()
except Exception as e:
    logging.error(f"Error in boost cycle: {e}")
    # Reinitialize browser
    await booster.close_browser()
    await booster.init_browser()
```

### 6. Ads not actually getting boosted

**Problem**: Form submission may have changed

**Diagnostic Steps**:
1. Run in test mode with visible browser:
   ```bash
   python3 wgzimmer_boost.py --once
   ```

2. Watch what happens and compare to manual process

3. Check screenshots in output directory

**Solution**: May need to update selectors in script if website changed

### 7. "Connection refused" or network errors

**Problem**: Network issues or website down

**Solutions**:
- Check if website is accessible manually
- Verify internet connection
- Add retry logic (already included in script)
- Increase timeout values

### 8. Memory usage keeps growing

**Problem**: Browser instances not closing properly

**Solution**: Restart the script daily:
```bash
# Create a cron job to restart daily
0 3 * * * pkill -f wgzimmer_boost.py && nohup python3 /path/to/wgzimmer_boost.py > /path/to/output.log 2>&1 &
```

### 9. Getting email notifications about suspicious activity

**Problem**: Website detected automation

**Solutions**:
1. Reduce frequency (run 2-3 times per day)
2. Increase random delays
3. Add more variability to timing
4. Run during normal human hours only

### 10. Code verification fails

**Problem**: Invalid or expired codes

**Diagnostic**:
1. Check the screenshot saved as `error_[CODE]_*.png`
2. Manually test the code on the website
3. Check your email for new codes

**Solution**:
- Update codes in the script
- Ensure no typos in the code entry
- Verify codes haven't expired

## Debugging Tips

### Enable verbose logging

Add to the top of wgzimmer_boost.py:
```python
logging.basicConfig(
    level=logging.DEBUG,  # Changed from INFO to DEBUG
    ...
)
```

### Run with visible browser for debugging

Change this line:
```python
booster = WGZimmerBooster(headless=False)  # False = visible
```

### Add custom logging

```python
logging.info(f"Current URL: {page.url}")
logging.info(f"Page title: {await page.title()}")
```

### Save HTML for inspection

```python
html = await page.content()
with open('debug_page.html', 'w') as f:
    f.write(html)
```

## Performance Optimization

### Reduce resource usage

```python
# Use smaller viewport
self.context = await self.browser.new_context(
    viewport={'width': 1280, 'height': 720},  # Smaller
    ...
)
```

### Faster execution (less safe)

```python
# Reduce delays (may trigger detection)
async def random_delay(self, min_seconds: float = 0.5, max_seconds: float = 1.5):
```

## Getting Help

1. **Check logs first**:
   ```bash
   tail -f wgzimmer_boost.log
   ```

2. **Look at screenshots** in the script directory

3. **Test manually** on the website to verify your codes work

4. **Run in test mode** with visible browser to see what's happening

5. **Check for website changes** - the site may have updated its structure

## Preventive Maintenance

### Weekly checks:
- Review logs for any errors
- Verify ads are still active
- Check success rate
- Update codes if needed

### Monthly maintenance:
- Clear old screenshots
- Rotate log files
- Test manually to ensure process still works
- Update script if website changed

### Best Practices:
- Don't run too frequently (stick to 5-7 times daily max)
- Use random timing (already implemented)
- Monitor for any warnings from the website
- Keep codes secure and private
- Respect the website's resources

## Emergency Shutdown

If something goes wrong:

```bash
# Kill the process immediately
pkill -9 -f wgzimmer_boost.py

# Remove any leftover browser processes
pkill -9 chromium

# Check what's still running
ps aux | grep -E 'wgzimmer|chromium'
```

## Contact Information

For script issues:
- Check the log files
- Review screenshots
- Run in debug mode
- Test with visible browser

For website/account issues:
- Contact wgzimmer.ch support
- Check their FAQ
- Verify your account status
