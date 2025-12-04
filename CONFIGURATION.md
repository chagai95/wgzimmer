# Configuration Examples

This file shows different configuration options for the WGZimmer Ad Booster.

## Basic Configuration (Current Default)

```python
# In wgzimmer_boost.py

CODES = [
    "SCCHCM11YXB7QAN9",  # German December
    "3KKG38MGNTFXARDW",  # German February
    "FGDE7R3Z6SV52PWB"   # 200 Franken
]

ACTIVE_HOURS_START = 7   # 7 AM
ACTIVE_HOURS_END = 22    # 10 PM

# In calculate_next_run_time():
min_interval = 1.5 * 3600  # 1.5 hours
max_interval = 4.0 * 3600  # 4 hours
# Results in: 5-7 runs per day
```

## Conservative Mode (Safer, Less Detection Risk)

```python
# Fewer runs, longer intervals

ACTIVE_HOURS_START = 8   # 8 AM
ACTIVE_HOURS_END = 20    # 8 PM

# In calculate_next_run_time():
min_interval = 3.0 * 3600  # 3 hours
max_interval = 5.0 * 3600  # 5 hours
# Results in: 2-4 runs per day
```

## Aggressive Mode (More Frequent, Higher Risk)

```python
# More runs, shorter intervals
# WARNING: Higher risk of detection

ACTIVE_HOURS_START = 6   # 6 AM
ACTIVE_HOURS_END = 23    # 11 PM

# In calculate_next_run_time():
min_interval = 1.0 * 3600  # 1 hour
max_interval = 2.5 * 3600  # 2.5 hours
# Results in: 8-12 runs per day
```

## Business Hours Only

```python
# Only during typical business hours

ACTIVE_HOURS_START = 9   # 9 AM
ACTIVE_HOURS_END = 18    # 6 PM

# In calculate_next_run_time():
min_interval = 2.0 * 3600  # 2 hours
max_interval = 3.0 * 3600  # 3 hours
# Results in: 3-4 runs per day
```

## Night Owl Mode

```python
# For those who prefer evening/night runs

ACTIVE_HOURS_START = 14  # 2 PM
ACTIVE_HOURS_END = 24    # Midnight

# In calculate_next_run_time():
min_interval = 2.0 * 3600  # 2 hours
max_interval = 4.0 * 3600  # 4 hours
# Results in: 3-5 runs per day
```

## Weekend Warrior

```python
# Only run on weekends
# Add this check to run_continuous():

import datetime

def is_weekend():
    return datetime.datetime.now().weekday() >= 5  # 5=Saturday, 6=Sunday

# In run_continuous(), add:
if is_weekend() and is_active_hours():
    # Run boosting
    await booster.boost_all_ads()
```

## Specific Days Only

```python
# Run only on specific days of the week
# Add to run_continuous():

import datetime

ACTIVE_DAYS = [0, 2, 4]  # Monday, Wednesday, Friday (0=Monday, 6=Sunday)

def is_active_day():
    return datetime.datetime.now().weekday() in ACTIVE_DAYS

# In run_continuous():
if is_active_day() and is_active_hours():
    await booster.boost_all_ads()
```

## Ultra-Cautious Mode (Stealth)

```python
# Maximum stealth with lots of randomness

ACTIVE_HOURS_START = 8
ACTIVE_HOURS_END = 20

# Add extra randomness to delays:
async def random_delay(self, min_seconds: float = 2.0, max_seconds: float = 8.0):
    delay = random.uniform(min_seconds, max_seconds)
    await asyncio.sleep(delay)

# In calculate_next_run_time():
min_interval = 4.0 * 3600  # 4 hours
max_interval = 8.0 * 3600  # 8 hours
# Results in: 1-3 runs per day

# Add random "skip days":
if random.random() < 0.3:  # 30% chance to skip today
    wait_until_tomorrow()
```

## Custom Timing Pattern

```python
# Run at specific times of day
import datetime

PREFERRED_HOURS = [8, 12, 16, 20]  # 8 AM, 12 PM, 4 PM, 8 PM

def calculate_next_run_time():
    now = datetime.datetime.now()
    
    # Find next preferred hour
    for hour in PREFERRED_HOURS:
        if now.hour < hour:
            next_run = now.replace(hour=hour, minute=0, second=0, microsecond=0)
            # Add random offset ±30 minutes
            offset = random.randint(-30, 30) * 60
            return (next_run - now).total_seconds() + offset
    
    # If past all times today, use first time tomorrow
    next_run = now.replace(hour=PREFERRED_HOURS[0], minute=0, second=0, microsecond=0)
    next_run += datetime.timedelta(days=1)
    offset = random.randint(-30, 30) * 60
    return (next_run - now).total_seconds() + offset
```

## Dynamic Adjustment Based on Success Rate

```python
# Adjust frequency based on success

class AdaptiveBooster(WGZimmerBooster):
    def __init__(self):
        super().__init__()
        self.success_rate = 1.0
        self.runs_today = 0
        self.successes_today = 0
    
    def calculate_adaptive_interval(self):
        # If success rate is low, reduce frequency
        if self.success_rate < 0.5:
            min_interval = 4.0 * 3600
            max_interval = 6.0 * 3600
        elif self.success_rate < 0.8:
            min_interval = 2.0 * 3600
            max_interval = 4.0 * 3600
        else:
            min_interval = 1.5 * 3600
            max_interval = 3.0 * 3600
        
        return random.uniform(min_interval, max_interval)
```

## Multiple Ad Groups (Prioritization)

```python
# Different timing for different ads

HIGH_PRIORITY_CODES = ["SCCHCM11YXB7QAN9"]  # Boost more often
NORMAL_PRIORITY_CODES = ["3KKG38MGNTFXARDW", "FGDE7R3Z6SV52PWB"]

async def boost_with_priority():
    # Boost high priority every run
    for code in HIGH_PRIORITY_CODES:
        await booster.boost_ad(code)
    
    # Boost normal priority with 70% probability
    if random.random() < 0.7:
        for code in NORMAL_PRIORITY_CODES:
            await booster.boost_ad(code)
```

## Rotating Schedule

```python
# Different schedule for each day of the week

WEEKLY_SCHEDULE = {
    0: (8, 18, 3),   # Monday: 8 AM - 6 PM, 3-4 runs
    1: (9, 20, 4),   # Tuesday: 9 AM - 8 PM, 4-5 runs
    2: (8, 18, 3),   # Wednesday: 8 AM - 6 PM, 3-4 runs
    3: (9, 20, 4),   # Thursday: 9 AM - 8 PM, 4-5 runs
    4: (8, 22, 5),   # Friday: 8 AM - 10 PM, 5-6 runs
    5: (10, 20, 2),  # Saturday: 10 AM - 8 PM, 2-3 runs
    6: (10, 18, 2),  # Sunday: 10 AM - 6 PM, 2-3 runs
}

def get_daily_schedule():
    day = datetime.datetime.now().weekday()
    start_hour, end_hour, target_runs = WEEKLY_SCHEDULE[day]
    
    active_hours = end_hour - start_hour
    avg_interval = active_hours / target_runs
    min_interval = (avg_interval * 0.8) * 3600
    max_interval = (avg_interval * 1.2) * 3600
    
    return start_hour, end_hour, min_interval, max_interval
```

## Testing Configurations

### Quick Test Mode
```python
# For rapid testing (don't use in production)

ACTIVE_HOURS_START = 0   # All day
ACTIVE_HOURS_END = 24

min_interval = 60        # 1 minute
max_interval = 120       # 2 minutes
# Results in: Many runs per hour (testing only!)
```

### Simulation Mode
```python
# Simulate runs without actually executing

async def boost_ad(self, code: str) -> bool:
    logging.info(f"SIMULATION: Would boost ad {code}")
    await asyncio.sleep(5)  # Simulate delay
    return True  # Simulate success
```

## How to Apply Configurations

1. **Edit wgzimmer_boost.py**
2. **Find the configuration section** (near the top)
3. **Replace with your chosen configuration**
4. **Save the file**
5. **Restart the script**

```bash
# Stop current instance
pkill -f wgzimmer_boost.py

# Start with new configuration
nohup python3 wgzimmer_boost.py > output.log 2>&1 &
```

## Recommendations by Use Case

### "I want maximum safety and minimal detection risk"
→ Use **Conservative Mode** or **Ultra-Cautious Mode**

### "I need my ads to stay very visible"
→ Use **Default Configuration** (5-7 runs/day)

### "I only care about business hours visibility"
→ Use **Business Hours Only**

### "I want to test if everything works"
→ Use `--once` flag first, then **Conservative Mode**

### "The ads are time-sensitive"
→ Use **Aggressive Mode** but monitor closely for issues

## Monitoring Your Configuration

Check your current performance:

```bash
# Count successful runs today
grep "Successfully boosted" wgzimmer_boost.log | grep "$(date +%Y-%m-%d)" | wc -l

# View timing between runs
grep "Next boost scheduled" wgzimmer_boost.log | tail -10

# Check success rate
grep -E "Successfully|Error boosting" wgzimmer_boost.log | tail -20
```

## Final Tips

1. **Start conservative** - You can always increase frequency later
2. **Monitor for a week** - See what works before adjusting
3. **Respect the platform** - Don't abuse with excessive runs
4. **Adjust based on results** - If ads stay visible, reduce frequency
5. **Keep logs** - They help you understand what's working
