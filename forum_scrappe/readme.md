
# Description
This Python code is a script for a web crawler using the Selenium framework. The script was created to scrape data from forum pages, specifically designed for the Microchip Technology forum. It extracts various elements from the forum, such as posts, user names, user types, and referenced comments, to understand community interactions and gather data for analysis.

# Functionality
1. **Import Statements:** 
    * `webdriver` from Selenium to control the browser.
        ```python 
        from selenium import webdriver
        ```
    * `By`, `WebDriverWait`, and `expected_conditions` for locating elements and waiting for conditions.
        ```python 
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        ```
    * `StaleElementReferenceException` to handle exceptions where an element is no longer present on the page.
        ```python 
        from selenium.common.exceptions import StaleElementReferenceException
        ```

2. **Utility Functions:**
    * `safe_get_element_text` function to safely retrieve text from elements, returning an empty string if the element is stale.
        ```python
        def safe_get_element_text(element):
            try:
                return element.text
            except StaleElementReferenceException:
                return ''
        ```
    * `extract_content_from_url` function to navigate through forum pages and extract relevant data.
        ```python
        def extract_content_from_url(driver, base_url, num_pages):
        ```

3. **Web Scraping Logic:**
    * The script uses a Chrome WebDriver to open and navigate through forum pages.
        ```python
        driver.get(url)
        ```
    * It extracts data such as usernames, user types, posts, and referenced comments.
        ```python
        for container in post_containers:
            
            username_element = container.find_element(By.XPATH, ".//div[contains(@class, 'username-text')]")
            user_type_element = container.find_element(By.XPATH, ".//div[contains(@class, 'subti-muted')][contains(text(), 'Level')]")
            post_element = container.find_element(By.XPATH, ".//div[@class='contain-post slds-rich-text-editor__output']")
            
            usernames_list.append(safe_get_element_text(username_element))
            user_types_list.append(safe_get_element_text(user_type_element))

            quote_elements = post_element.find_elements(By.XPATH, ".//div[@class='quote-reply']/b")
            quote_reply_elements = post_element.find_elements(By.XPATH, ".//div[@class='quote-reply']/p")

            quote_text = safe_get_element_text(quote_elements[0]) if quote_elements else ""
            quote_reply_text = "\n".join([safe_get_element_text(elem) for elem in quote_reply_elements if elem.text.strip() and elem.text.strip() != quote_text])
            main_post_text = post_element.text.replace(quote_text, '').replace(quote_reply_text, '').strip()

            user_posts.append(main_post_text)
            quotes.append(quote_text)
            quote_replies.append(quote_reply_text)

        content = [] 
        ```
    * The data is then written to a text file for further analysis.
        ```python
    
        for username, user_type, user_post, quote, quote_reply in zip(usernames_list, user_types_list, user_posts, quotes, quote_replies):
            content.append(f"URL:         {url}")
            content.append(f"Username:    {username}")
            content.append(f"User Type:   {user_type}")
            content.append(f"User Post:\n{user_post}")  
            if quote:
                content.append(f"\nUser Referenced:\n{quote}")
            if quote_reply:
                content.append(f"\nUser's Comment Referenced:\n{quote_reply}")
            content.append("---------------------------------------------------")

        all_content.extend(content)  

        return all_content

        ...

        file_name = "test.txt"                                                                  

        with open(file_name, "w", encoding="utf-8") as file:
        file.write("\n".join(all_content))
        ```

4. **Execution:**
    * Set the path to the Chrome Driver executable and modify the `base_url` and `num_pages` as needed.
        ```python
        chrome_driver_path = "C:/Users/rolar/selenium-drivers/chromedriver-win64"               
    
        ...

        base_url = "https://forum.microchip.com/s/topic/a5C3l000000MZfYEAW/t367172"             
        num_pages = 5                                                                           
        ```
    * Run the script to scrape the data and save it to a text file.
