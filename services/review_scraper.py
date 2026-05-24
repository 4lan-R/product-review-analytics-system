from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import html
import logging
import re

from schemas.review import ReviewBase
from schemas.product import ProductResponse

logger = logging.getLogger(__name__)


async def scrape_review_from_link(link: str) -> ProductResponse:
    # logger.info("Starting Amazon scrape")
    # logger.info("URL: %s", link)

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
            ],
        )

        context = await browser.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
        )

        page = await context.new_page()

        await page.goto(
            str(link),
            wait_until="domcontentloaded",
            timeout=60000,
        )

        await page.wait_for_timeout(8000)

        # logger.info("Final URL: %s", page.url)
        # logger.info("Page Title: %s", await page.title())

        # await page.screenshot(
        #     path="product_page.png",
        #     full_page=True,
        # )

        # logger.info("Saved screenshot: product_page.png")

        html_text = await page.content()

        # with open(
        #     "product_page.html",
        #     "w",
        #     encoding="utf-8",
        # ) as f:
        #     f.write(html_text)

        # logger.info("Saved HTML: product_page.html")

        await browser.close()

    soup = BeautifulSoup(html_text, "html.parser")

    # --------------------------------------------------
    # Product Title
    # --------------------------------------------------

    title = ""

    title_tag = soup.select_one("#productTitle")

    if title_tag:
        title = title_tag.get_text(strip=True)

    if not title:
        page_title = soup.find("title")
        title = (
            page_title.get_text(strip=True)
            if page_title
            else "Unknown Product"
        )

    # logger.info("Product Title: %s", title)

    # --------------------------------------------------
    # Product Description
    # --------------------------------------------------

    description_parts = []

    for bullet in soup.select("#feature-bullets li"):
        text = bullet.get_text(" ", strip=True)

        if text and text != "":
            description_parts.append(text)

    description = " ".join(description_parts)

    # logger.info(
    #     "Description Length: %s",
    #     len(description),
    # )

    # --------------------------------------------------
    # Reviews
    # --------------------------------------------------

    reviews = []

    review_blocks = soup.select(
        '[data-hook="reviewContainer"]'
    )

    if not review_blocks:
        review_blocks = soup.select(
            '[data-hook="review"]'
        )

    # logger.info(
    #     "Review blocks found: %s",
    #     len(review_blocks),
    # )

    for idx, review in enumerate(review_blocks):
        try:
            review_title = ""
            review_text = ""
            rating = None

            # ------------------------------------------
            # Title
            # ------------------------------------------

            title_tag = (
                review.select_one(
                    '[data-hook="reviewTitle"]'
                )
                or review.select_one(
                    'h5[data-hook="reviewTitle"]'
                )
                or review.select_one(
                    '[data-hook="review-title"]'
                )
            )

            if title_tag:
                review_title = title_tag.get_text(
                    " ",
                    strip=True,
                )

            # ------------------------------------------
            # Review Text
            # ------------------------------------------

            body_tag = (
                review.select_one(
                    '[data-hook="reviewRichContentContainer"]'
                )
                or review.select_one(
                    '[data-hook="reviewText"]'
                )
                or review.select_one(
                    '[data-hook="review-body"]'
                )
            )

            if body_tag:
                review_text = body_tag.get_text(
                    " ",
                    strip=True,
                )

            # ------------------------------------------
            # Rating
            # ------------------------------------------

            rating_tag = (
                review.select_one(
                    '[data-hook="review-star-rating"]'
                )
                or review.select_one(
                    '[data-hook="cmps-review-star-rating"]'
                )
            )

            if rating_tag:
                rating_text = rating_tag.get_text(
                    " ",
                    strip=True,
                )

                match = re.search(
                    r"(\d+(?:\.\d+)?)",
                    rating_text,
                )

                if match:
                    rating = int(
                        float(match.group(1))
                    )

            # ------------------------------------------
            # Verified Purchase
            # ------------------------------------------

            verified_purchase = bool(
                review.select_one(
                    '[data-hook="avp-badge"]'
                )
            )

            # ------------------------------------------
            # Skip empty reviews
            # ------------------------------------------

            if not review_text.strip():
                continue

            # logger.info(
            #     "Review %s | Rating=%s | Title=%s",
            #     idx + 1,
            #     rating,
            #     review_title[:80],
            # )

            # logger.info(
            #     "Review Text Preview: %s",
            #     review_text[:200],
            # )

            reviews.append(
                ReviewBase(
                    review_title=html.unescape(
                        review_title
                    ),
                    review_text=html.unescape(
                        review_text
                    ),
                    rating=rating,
                    verified_purchase=verified_purchase,
                    color=None,
                    storage_size=None,
                )
            )

        except Exception as e:
            # logger.exception(
            #     "Error parsing review %s: %s",
            #     idx + 1,
            #     e,
            # )
            pass

    # logger.info(
    #     "Total extracted reviews: %s",
    #     len(reviews),
    # )

    return ProductResponse(
        name=title,
        description=description,
        reviews=reviews,
    )