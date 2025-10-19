def get_article(config):
    cursor = config.DB_Connection.cursor()
    cursor.execute(
        "update RSSFeed set Read = true where id == ( select id from RSSFeed where read = false limit 1) returning *"
    )
    article = cursor.fetchall()
    config.DB_Connection.commit()
    if len(article) < 1:
        return None
    return article
