import json
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time
import re
from selenium import webdriver
options = Options()
options.headless = True



class Movielist:
    class Movie:
        title = ""
        description = ""
        link = ""
        thumbnail = ""
        genres = ""
        release = ""
        runtime = ""
    movies = []

    def next_page(self, driver):
        try:
            elem = driver.find_element_by_partial_link_text('NEXT')
        except:
            return False
        link = elem.get_attribute("href")
        driver.get(link)
        return True

    def __init__(self, driver):
        breakcond = False
        while not breakcond:
            try:
                nextpage = driver.find_element_by_partial_link_text('NEXT').get_attribute("href")
            except:
                breakcond = True

            elem = driver.find_element_by_id('movie-grid-wrapper')
            children = elem.find_elements_by_css_selector("ul.cbp-rfgrid > div")

            for child in children:
                curr_movie = self.Movie()

                elem = child.find_element_by_id("mv")

                links = elem.find_elements_by_tag_name("a")[1]

                curr_movie.thumbnail = links.find_element_by_tag_name("img").get_attribute("src")


                # movie details
     
                details = child.find_element_by_class_name("movie-grid-list")
                parent = details.find_element_by_class_name("movie-grid-title")
                parent_text = driver.execute_script("return arguments[0].firstChild.textContent", parent)
                
                curr_movie.title = parent_text.strip()

                curr_movie.description = details.find_element_by_class_name("movie-grid-description")
                curr_movie.description = curr_movie.description.find_element_by_tag_name("p").get_attribute("textContent")

                
                # get movie mp4
                sitelink = links.get_attribute("href")
                tmpdriver = {}
                while True:
                    try:
                        tmpdriver = webdriver.Firefox(options=options)
                    except:
                        continue
                    break

                tmpdriver.get(sitelink)
                tmpdriver.execute_script("playMovie();")

                videolink = ""
                while True:
                    try:
                        videolink = tmpdriver.find_element_by_tag_name("video").get_attribute("src")
                        
                        #More relevant information
                        infolist = tmpdriver.find_element_by_id("description-ul")
                        infolist = infolist.find_element_by_tag_name("table")
                        infolist = infolist.find_elements_by_tag_name("li")
                        curr_movie.release = infolist[1].get_attribute("textContent")
                        curr_movie.runtime = infolist[3].get_attribute("textContent")
                        curr_movie.genres = infolist[5].get_attribute("textContent")
                
                    except:
                        continue
                    linklen = len(videolink)
                    if linklen:
                        break
                print(videolink)
                curr_movie.link = videolink
                tmpdriver.close()

                self.movies.append(curr_movie)
            if not breakcond:
                driver.get(nextpage)

if __name__ == "__main__":
    
    driver = webdriver.Firefox(options=options)
    driver.get("http://www.streamlord.com/movies.php")
    assert "No results found." not in driver.page_source

    mvobj = Movielist(driver)

    file = open("movies.json", "w")
    json.dump([mvs.__dict__ for mvs in mvobj.movies], file)
    file.close()
    driver.close()
