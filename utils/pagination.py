def get_total_pages(total_items, page_size):
    if page_size <= 0:
        return 1
    return max(1, (total_items + page_size - 1) // page_size)


def clamp_page(page, total_pages):
    return max(1, min(page, total_pages))


def get_offset(page, page_size):
    return (page - 1) * page_size
