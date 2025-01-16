from models import get_session, InfoData, NewsData

def delete_entries():
    with get_session() as session:
        session.query(InfoData).filter(InfoData.id >= 659).delete(synchronize_session=False)
        
        session.query(NewsData).filter(NewsData.news_id >= 659).delete(synchronize_session=False)
        
        session.commit()
        print("Rows with id >= 659 have been deleted.")

delete_entries()

"""
Used this to delete entries from the database with id >= 659.
there is something wrong with the code but i am tired of looking for it.
i will check it out later
"""
