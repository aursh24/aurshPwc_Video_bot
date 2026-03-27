from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time


# --- IMPORTANT Instructions Before using this code ---

# just make sure its not a ML model ki tumhara quiz bhi de dega, ye sirf video ke liye hai
# also, it might fail if the website changes its UI, so be careful, guarantee nahi leta mai :)

# please install the required libraries before running this, mentioned in the requirements.txt file

# ------------------xoxo------------------------------------

# bkl yaha pe apna video ka link daal dena, baaki AURSH vaii ka code sambhal lega <33
URL = "Paste Link Here"
SPEED = 2.0
CHECK_INTERVAL = 2


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(URL)

time.sleep(5)



def switch_to_video_iframe():
    driver.switch_to.default_content()
    iframes = driver.find_elements("tag name", "iframe")

    for i, frame in enumerate(iframes):
        driver.switch_to.default_content()
        driver.switch_to.frame(frame)

        try:
            has_video = driver.execute_script(
                "return document.querySelector('video') != null"
            )
            if has_video:
                print(f"Video found in iframe {i}")
                return True
        except:
            pass

    driver.switch_to.default_content()
    return False



def handle_video():
    result = driver.execute_script("""
    let v = document.querySelector('video');
    if (!v) return "NO_VIDEO";

    v.muted = true;

    // If video is stuck at 0, seek to 1s to force load/play
    if (v.currentTime === 0 && v.duration > 0) {
        v.currentTime = 1;
    }

    v.play();
    v.playbackRate = arguments[0];

    return {
        duration: v.duration || 0,
        current: v.currentTime || 0,
        ended: v.ended
    };
    """, SPEED)

    return result



def click_next():
    """Find the 'Next activity' popup and navigate to the next video."""
    driver.switch_to.default_content()
    current_url = driver.current_url

    href = driver.execute_script("""
        // Search all <a> tags for one containing "Next activity" text
        let links = document.querySelectorAll('a');
        for (let a of links) {
            if (a.textContent.includes('Next activity')) {
                return a.href;
            }
        }

        // Broader: find any element with "Next activity" and look for parent/child <a>
        let allEls = document.querySelectorAll('*');
        for (let el of allEls) {
            let text = el.textContent.trim();
            if (text.startsWith('Next activity') && text.length < 100) {
                let link = el.closest('a') || el.querySelector('a');
                if (link && link.href) return link.href;
            }
        }

        return null;
    """)

    if href and href != current_url:
        print(f"Found next activity URL: {href}")
        driver.get(href)
        time.sleep(5)
        return True

    
    try:
        elements = driver.find_elements(By.XPATH,
            "//*[contains(text(), 'Next activity')]")
        for el in elements:
            
            try:
                link = el.find_element(By.XPATH, ".//ancestor-or-self::a")
            except:
                try:
                    link = el.find_element(By.XPATH, ".//a")
                except:
                    link = el

            link.click()
            time.sleep(5)

    
            if driver.current_url != current_url:
                print(f"Navigated to: {driver.current_url}")
                return True
            else:
                print("Click didn't navigate, trying next element...")
    except Exception as e:
        print(f"Selenium click failed: {e}")

    href2 = driver.execute_script("""
        let popup = document.querySelector(
            '[data-region="next-activity"], .completion-next-activity, .activity-navigation a[title]'
        );
        if (popup) {
            let link = popup.closest('a') || popup.querySelector('a') || popup;
            return link.href || null;
        }
        return null;
    """)

    if href2 and href2 != current_url:
        print(f"Found next URL (Moodle selector): {href2}")
        driver.get(href2)
        time.sleep(5)
        return True

    print("Could not find next activity link")
    return False


print("Hi beautiful, sup? My bot starts...")

while True:
    try:
        result = handle_video()

        if result == "NO_VIDEO":
            print("Searching video in iframe...")
            found = switch_to_video_iframe()

            if not found:
                print("No video found")
                time.sleep(5)
                continue

            result = handle_video()

        duration = result["duration"]
        current = result["current"]

        if duration and current is not None:
            print(f"{current:.1f} / {duration:.1f}")
        else:
            print("Loading video...")

        if duration > 0 and current > 0 and (result.get("ended") or duration - current < 1):
            print("Video ending, waiting for popup...")

            driver.switch_to.default_content()
            time.sleep(3)  

            for i in range(5):
                print(f"Attempt {i+1}")

                if click_next():
                    print("Navigated to next activity!")
                    time.sleep(3)  
                    break

                time.sleep(2)  

        time.sleep(CHECK_INTERVAL)

    except Exception as e:
        print("Error:", e)
        time.sleep(5)