import datetime
import logging.config
from sqlalchemy.orm import sessionmaker
from utils.mysql import engine, Posts


def publication_post(product_id, price, url):
    logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
    logger = logging.getLogger('sLogger')

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        with session:
            post = session.query(Posts).filter(Posts.product_id == product_id or Posts.url == url).first()

            if not post:
                session.add(Posts(product_id=product_id, price=price, url=url))
                session.commit()
                return True

            publication_life = post.date + datetime.timedelta(weeks=1)
            if post.price != price or datetime.datetime.now() > publication_life:
                session.delete(post)
                session.add(Posts(product_id=product_id, price=price, url=url))
                session.commit()
                return True

    except Ellipsis as _err:
        logger.error(f"{product_id}=> {_err}")
        return
