#!/usr/bin/env python3
"""
WGZimmer Ad Booster - Educational Automation Script
Automatically refreshes room advertisements to keep them at the top
"""

import asyncio
import random
from datetime import datetime, time
from playwright.async_api import async_playwright, Page
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('wgzimmer_boost.log'),
        logging.StreamHandler()
    ]
)

# Configuration
CODES = [
    "SCCHCM11YXB7QAN9",  # German December
    "3KKG38MGNTFXARDW",  # German February
    "FGDE7R3Z6SV52PWB"   # 200 Franken
]

BASE_URL = "https://www.wgzimmer.ch/wgzimmer.html"
ACTIVE_HOURS_START = 7  # 7 AM
ACTIVE_HOURS_END = 22   # 10 PM


class WGZimmerBooster:
    """Automates the process of boosting WGZimmer advertisements"""
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser = None
        self.context = None
        self.playwright = None
        
    async def init_browser(self):
        """Initialize the browser instance"""
        try:
            self.playwright = await async_playwright().start()
            
            # Browser launch arguments for better compatibility
            launch_args = [
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',  # Needed for WSL and some Linux environments
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',  # Overcome limited resource problems
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu'  # Helps with WSL
            ]
            
            logging.info("Launching browser...")
            self.browser = await self.playwright.chromium.launch(
                headless=self.headless,
                args=launch_args,
                timeout=60000  # Increased timeout to 60 seconds
            )
            
            # Create context with realistic settings
            self.context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                locale='de-CH',
                timezone_id='Europe/Zurich'
            )
            
            logging.info("Browser initialized successfully")
            
        except Exception as e:
            logging.error(f"Failed to initialize browser: {e}")
            logging.error("Try running: playwright install chromium")
            raise
        
    async def close_browser(self):
        """Close the browser instance"""
        try:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if hasattr(self, 'playwright') and self.playwright:
                await self.playwright.stop()
        except Exception as e:
            logging.error(f"Error closing browser: {e}")
    
    async def random_delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0):
        """Add random human-like delay"""
        delay = random.uniform(min_seconds, max_seconds)
        await asyncio.sleep(delay)
    
    async def human_type(self, page: Page, selector: str, text: str):
        """Type text with human-like delays"""
        await page.fill(selector, '')  # Clear first
        for char in text:
            await page.type(selector, char, delay=random.uniform(50, 150))
            
    async def boost_ad(self, code: str) -> bool:
        """
        Boost a single advertisement using its code
        
        Args:
            code: The advertisement code
            
        Returns:
            bool: True if successful, False otherwise
        """
        page = None
        try:
            page = await self.context.new_page()
            logging.info(f"Starting boost for code: {code[:4]}****")
            
            # Navigate to homepage
            await page.goto(BASE_URL, wait_until='networkidle', timeout=30000)
            await self.random_delay(1, 2)
            
            # Scroll down to the form section
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.5)")
            await self.random_delay(0.5, 1.5)
            
            # Find and fill the "Mein Inserat ändern" (Edit Ad) form
            # The form is in the first column
            edit_code_input = 'input#editCode'
            
            # Wait for the input to be visible
            await page.wait_for_selector(edit_code_input, state='visible', timeout=10000)
            
            # Type the code with human-like behavior
            await self.human_type(page, edit_code_input, code)
            await self.random_delay(0.5, 1.0)
            
            # Click the "Code prüfen" button
            submit_button = 'input[type="submit"][value="Code prüfen"]'
            
            # Wait for reCAPTCHA to potentially load
            await self.random_delay(2, 3)
            
            # Click submit
            await page.click(submit_button)
            logging.info(f"Submitted code verification for {code[:4]}****")
            
            # Wait for navigation to the edit page
            await page.wait_for_load_state('networkidle', timeout=30000)
            await self.random_delay(2, 4)
            
            # Check if we're on the edit page
            current_url = page.url
            if 'mate.html' not in current_url and 'advertise' not in current_url:
                logging.warning(f"Unexpected URL after submission: {current_url}")
                # Take screenshot for debugging
                await page.screenshot(path=f'/home/claude/debug_{code[:4]}.png')
                return False
            
            logging.info("Successfully navigated to edit page")
            
            # Scroll to bottom where the "INSERAT AUFGEBEN" button is
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await self.random_delay(1, 2)
            
            # Find and click the "Inserat aufgeben" button
            # This button is in the form with id="formSearchMate"
            submit_ad_button = 'input[type="button"][value="Inserat aufgeben"]'
            
            await page.wait_for_selector(submit_ad_button, state='visible', timeout=10000)
            
            # Random scroll up a bit then back down (human behavior)
            await page.evaluate("window.scrollBy(0, -200)")
            await self.random_delay(0.3, 0.7)
            await page.evaluate("window.scrollBy(0, 200)")
            await self.random_delay(0.5, 1.0)
            
            # Click the button
            await page.click(submit_ad_button)
            logging.info(f"Clicked 'Inserat aufgeben' button for {code[:4]}****")
            
            # Wait for the submission to process
            await page.wait_for_load_state('networkidle', timeout=30000)
            await self.random_delay(2, 3)
            
            # Verify success (you might want to check for a success message)
            final_url = page.url
            logging.info(f"Final URL: {final_url}")
            
            # Take a success screenshot
            await page.screenshot(path=f'/home/claude/success_{code[:4]}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
            
            logging.info(f"✅ Successfully boosted ad: {code[:4]}****")
            return True
            
        except Exception as e:
            logging.error(f"❌ Error boosting ad {code[:4]}****: {str(e)}")
            if page:
                try:
                    await page.screenshot(path=f'/home/claude/error_{code[:4]}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
                except:
                    pass
            return False
        finally:
            if page:
                await page.close()
    
    async def boost_all_ads(self):
        """Boost all configured advertisements"""
        success_count = 0
        
        # Randomize the order of codes
        codes_shuffled = CODES.copy()
        random.shuffle(codes_shuffled)
        
        for i, code in enumerate(codes_shuffled):
            logging.info(f"Processing ad {i+1}/{len(codes_shuffled)}")
            
            success = await self.boost_ad(code)
            if success:
                success_count += 1
            
            # Random delay between ads (3-8 minutes)
            if i < len(codes_shuffled) - 1:
                delay = random.uniform(180, 480)
                logging.info(f"Waiting {delay/60:.1f} minutes before next ad...")
                await asyncio.sleep(delay)
        
        logging.info(f"Completed boosting session: {success_count}/{len(codes_shuffled)} successful")
        return success_count


def is_active_hours() -> bool:
    """Check if current time is within active hours"""
    current_hour = datetime.now().hour
    return ACTIVE_HOURS_START <= current_hour < ACTIVE_HOURS_END


def calculate_next_run_time() -> float:
    """Calculate when the next run should occur (in seconds)"""
    now = datetime.now()
    current_hour = now.hour
    
    # If outside active hours, wait until next active period
    if current_hour >= ACTIVE_HOURS_END or current_hour < ACTIVE_HOURS_START:
        # Calculate time until next morning
        if current_hour >= ACTIVE_HOURS_END:
            # Wait until tomorrow morning
            next_run = now.replace(hour=ACTIVE_HOURS_START, minute=0, second=0, microsecond=0)
            next_run = next_run + asyncio.timedelta(days=1)
        else:
            # Wait until this morning
            next_run = now.replace(hour=ACTIVE_HOURS_START, minute=0, second=0, microsecond=0)
        
        wait_seconds = (next_run - now).total_seconds()
        return wait_seconds
    
    # During active hours: 5-7 times per day
    # Calculate random interval between runs
    # Active hours = 15 hours (7 AM to 10 PM)
    # For 5-7 runs, average interval = 15 hours / 6 runs = 2.5 hours
    # Use range of 1.5 to 4 hours for randomness
    
    min_interval = 1.5 * 3600  # 1.5 hours
    max_interval = 4.0 * 3600  # 4 hours
    
    wait_seconds = random.uniform(min_interval, max_interval)
    
    # Ensure we don't go past active hours
    next_time = now.timestamp() + wait_seconds
    end_of_active = now.replace(hour=ACTIVE_HOURS_END, minute=0, second=0, microsecond=0).timestamp()
    
    if next_time > end_of_active:
        # Schedule for next morning instead
        next_run = now.replace(hour=ACTIVE_HOURS_START, minute=0, second=0, microsecond=0)
        next_run = next_run + asyncio.timedelta(days=1)
        wait_seconds = (next_run.timestamp() - now.timestamp())
    
    return wait_seconds


async def run_continuous():
    """Run the booster continuously with random intervals"""
    booster = WGZimmerBooster(headless=True)
    
    try:
        await booster.init_browser()
        logging.info("🚀 WGZimmer Ad Booster started!")
        
        run_count = 0
        while True:
            run_count += 1
            
            if is_active_hours():
                logging.info(f"=" * 60)
                logging.info(f"Starting boost cycle #{run_count}")
                logging.info(f"=" * 60)
                
                await booster.boost_all_ads()
                
                # Calculate next run time
                wait_seconds = calculate_next_run_time()
                next_run = datetime.now() + asyncio.timedelta(seconds=wait_seconds)
                
                logging.info(f"Next boost scheduled for: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
                logging.info(f"Waiting {wait_seconds/3600:.2f} hours...")
                
                await asyncio.sleep(wait_seconds)
            else:
                # Outside active hours, wait until next morning
                wait_seconds = calculate_next_run_time()
                next_run = datetime.now() + asyncio.timedelta(seconds=wait_seconds)
                
                logging.info(f"Outside active hours. Next run at: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
                await asyncio.sleep(wait_seconds)
                
    except KeyboardInterrupt:
        logging.info("Received shutdown signal")
    except Exception as e:
        logging.error(f"Unexpected error in main loop: {e}")
    finally:
        await booster.close_browser()
        logging.info("Ad Booster stopped")


async def run_once():
    """Run the booster once (for testing)"""
    # Check if we have a display, if not use headless
    import os
    has_display = os.environ.get('DISPLAY') is not None
    
    booster = WGZimmerBooster(headless=not has_display)  # Headless if no display
    
    try:
        await booster.init_browser()
        logging.info("Running single boost cycle...")
        await booster.boost_all_ads()
        logging.info("Single boost cycle completed")
    finally:
        await booster.close_browser()


if __name__ == "__main__":
    import sys
    import os
    
    # Check for display availability
    has_display = os.environ.get('DISPLAY') is not None
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--once":
            # Run once for testing
            # Use headless if no display available
            asyncio.run(run_once())
        elif sys.argv[1] == "--once-visible":
            # Force visible browser (will fail if no display)
            async def run_visible():
                booster = WGZimmerBooster(headless=False)
                try:
                    await booster.init_browser()
                    logging.info("Running single boost cycle...")
                    await booster.boost_all_ads()
                    logging.info("Single boost cycle completed")
                finally:
                    await booster.close_browser()
            
            if not has_display:
                print("❌ No display available. Use --once instead or install xvfb")
                sys.exit(1)
            asyncio.run(run_visible())
        elif sys.argv[1] == "--help":
            print("""
WGZimmer Ad Booster - Usage:

  python3 wgzimmer_boost.py              Run continuously (headless)
  python3 wgzimmer_boost.py --once       Run once (auto-detect display)
  python3 wgzimmer_boost.py --once-visible   Run once with visible browser
  python3 wgzimmer_boost.py --help       Show this help

For servers without display, use --once (default) or run normally.
For local testing with display, use --once-visible.
            """)
            sys.exit(0)
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Use --help for usage information")
            sys.exit(1)
    else:
        # Run continuously (always headless for production)
        asyncio.run(run_continuous())