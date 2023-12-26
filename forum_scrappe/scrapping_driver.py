import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

# function returning element text or empty string for StaleElementReferenceException (when element no longer exist in webpage)
def safe_get_element_text(element):
    try:
        return element.text
    except StaleElementReferenceException:
        return ''

# function returning relevant content from urls + cleaned
def extract_content_from_url(driver, base_url, num_pages):
    # list to store all the extracted content
    all_content = []  

    # loop creating subsequent urls (no need use driver clicker)
    for page_num in range(1, num_pages + 1): 
        if page_num == 1:
            url = base_url
        else:
            url = f"{base_url}?page={page_num}"

        # open browser
        driver.get(url)

        # browser open 2 minutes
        wait = WebDriverWait(driver, 120)                                               # CHANGE IF NEEDED

        post_containers = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@data-key]")))

        # list for post information
        user_posts = []         # post by user
        quotes = []             # creator of commment being referenced
        quote_replies = []      # comment being referenced
        usernames_list = []     # name of post creator
        user_types_list = []    # level of post creator

        for container in post_containers:
            
            # find username, level, post content element in container
            username_element = container.find_element(By.XPATH, ".//div[contains(@class, 'username-text')]")
            user_type_element = container.find_element(By.XPATH, ".//div[contains(@class, 'subti-muted')][contains(text(), 'Level')]")
            post_element = container.find_element(By.XPATH, ".//div[@class='contain-post slds-rich-text-editor__output']")
            
            # append to list 
            usernames_list.append(safe_get_element_text(username_element))
            user_types_list.append(safe_get_element_text(user_type_element))

            # find post & post creator being referenced 
            quote_elements = post_element.find_elements(By.XPATH, ".//div[@class='quote-reply']/b")
            quote_reply_elements = post_element.find_elements(By.XPATH, ".//div[@class='quote-reply']/p")

            # clean posts elements for duplicates
            quote_text = safe_get_element_text(quote_elements[0]) if quote_elements else ""
            quote_reply_text = "\n".join([safe_get_element_text(elem) for elem in quote_reply_elements if elem.text.strip() and elem.text.strip() != quote_text])
            main_post_text = post_element.text.replace(quote_text, '').replace(quote_reply_text, '').strip()

            # append user post, reference post creator, and referenced post to list
            user_posts.append(main_post_text)
            quotes.append(quote_text)
            quote_replies.append(quote_reply_text)

        content = []  # list to store content for the current URL
        
        # append content to contents list to match order in forum
        for username, user_type, user_post, quote, quote_reply in zip(usernames_list, user_types_list, user_posts, quotes, quote_replies):
            content.append(f"URL:         {url}")
            content.append(f"Username:    {username}")
            content.append(f"User Type:   {user_type}")
            content.append(f"User Post:\n{user_post}")  # added new line for better clarity
            if quote:
                content.append(f"\nUser Referenced:\n{quote}")
            if quote_reply:
                content.append(f"\nUser's Comment Referenced:\n{quote_reply}")
            content.append("---------------------------------------------------")

        all_content.extend(content)  # add content for the current URL to the overall list

    return all_content

# set the path to the Chrome Driver executable (ensure it matches your Chrome version)
chrome_driver_path = "C:/Users/rolar/selenium-drivers/chromedriver-win64"               #CHANGE TO YOUR DRIVER PATH
os.environ['PATH'] += os.pathsep + chrome_driver_path

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", False)

driver = webdriver.Chrome(options=options)

base_url = "https://forum.microchip.com/s/topic/a5C3l000000MZfYEAW/t367172"             #CHNAGE FORUM URL
num_pages = 5                                                                           #CHANGE PAGE NUMBER

all_content = extract_content_from_url(driver, base_url, num_pages)                     #SEE LINE 15 FUNCTION DETAILS

# desired file name (with .txt extension)
file_name = "test.txt"                                                                  #SET UNIQUE NAME, AVOID SPECIAL CHARACTERS

# save all content to the specified text file
with open(file_name, "w", encoding="utf-8") as file:
    file.write("\n".join(all_content))

# close driver
driver.quit()
