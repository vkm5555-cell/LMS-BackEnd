from math import ceil

def paginate_query(query, page: int = 1, limit: int = 10):

    total_items = query.count()
    total_pages = ceil(total_items / limit) if total_items else 1

    items = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "success": True,
        "page": page,
        "limit": limit,
        "total_items": total_items,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
        "data": items,
    }
