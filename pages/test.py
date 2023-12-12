"""TEST PAGE."""

from deps.news.news import show_news
from deps.page_config import PageConfig

# Must be at top of page: https://github.com/xcollantes/stock-analysis-frontend/issues/29
PageConfig().get_config()


def main():
    """"""
    show_news("MSFT", 1000)


if __name__ == "__main__":
    main()
