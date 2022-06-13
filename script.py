from maps_scraping.Scraper import Scraper

with Scraper() as bot:
    bot.land_on_page()
    
    for _ in range(3):
    
        bot.scroll()
        bot.click_to_open()
        bot.click_on_next_page()
        
