import asyncio
import aiohttp
from typing import Awaitable
from bs4 import BeautifulSoup
from output_data import final_count
from request_data import URL


def write_to_file(filename: str, final_count: dict[str,int]) -> None:
    """Writes to the file in the format specified by task.
    
    filename - Name to give to the created/existing file.
    final_count - Result of the `main()` function.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        for letter, count in final_count.items():
            file.write(letter + ":" + " " + str(count) + "\n")

async def fetch(session: aiohttp.ClientSession, url: str) -> Awaitable | None:
    """Fetches requested web-page.

    session - Client Session used by aiohttp.
    url - Requested url. In our case it just cycles through the wiki pages.
    
    *If some error occurs we stop the event loop
        and print out the error msg.
    *If everything goes OK, the function should
        return an Awaitable of the page's HTML.
    """
    global loop
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        print(str(e))
        loop.close()

async def make_soup(html: str, parser="html.parser") -> BeautifulSoup:
    """Returns a BeautifulSoup object to parse data.
    
    html - Web page we got from `fetch(...)` function.
    parser - Any parser from the docs, standard is 'html.parser'
    (https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser)

    Returns BeautifulSoup object with given params.
    """
    return BeautifulSoup(html, parser)

async def get_correct_element(soup: BeautifulSoup) -> list[str]:
    """Parses through the web-page
    to find the element with animal names.
    
    Returns [multiple] <ul> tags with their corresponding children as
    [
        0:  <ul>
                <li>...Гуативера...</li>
                <li>...Гуахаро...</li>
                ...
            </ul>,
        1:  <ul>
                <li>...Дабб...</li>
                <li>...Дагестанская Ящерица...</li>
                ...
            </ul>
        ...
    ]
    """
    return soup.find(class_="mw-category-generated").find(id="mw-pages")("ul")

async def get_next_page_url(soup: BeautifulSoup) -> str:
    """Returns url of the next page."""

    soup = soup.find(class_="mw-category-generated").find(id="mw-pages")
    url = soup.find("a", text="Следующая страница").get("href")
    return "https://ru.wikipedia.org" + url

async def increment_letter_count(ul_tags: list[str]) -> dict[str, int]:
    """Returns updated dictionary of {letter: count}
    and the status of the main loop.

    li_tags - List of <ul>...</ul> tags, which contain
        <li> elements of animals' names.
    
    *If the first letter in the <ul> element's words is of Russian
        language, the function adds the corresponding number of <li>
        tags to the {letter: count} and returns `True` to indicate
        that the main loop should continue.
    *Else if the first letter in the <ul> element's words
        is not of Russian language, then function's loop breaks and
        returns `False` to indicate that the main loop should be stopped.
    """
    for _, animals in enumerate(ul_tags):
        if animals.text[0] == "A": # English "A", not Russian "А".
            return (final_count, False)
        else:
            final_count[animals.text[0]] += len(animals.find_all("li"))
    return (final_count, True)

async def main():
    async with aiohttp.ClientSession() as session:
        # Needed for the first iteration.
        next_page_url = URL
        while True:
            html = await fetch(session, next_page_url)
            soup = await make_soup(html)

            soup_ul_tags = await get_correct_element(soup)
            next_page_url = await get_next_page_url(soup)

            final_count, status = await increment_letter_count(soup_ul_tags)
            # Added for debugging and monitoring.
            print(final_count, "\n")
            
            if status == False:
                print('-----------------------------')
                break
        
        return final_count


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    final_count = loop.run_until_complete(main())
    write_to_file('output.txt', final_count)
