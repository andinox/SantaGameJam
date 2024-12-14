from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class MobDatabase:
    def __init__(self, db_name: str = "db.sqlite"):
        # Initialisation de la connexion à SQLite
        self.engine = create_engine(f"sqlite:///{db_name}")
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    class Mob(Base):
        __tablename__ = 'mobs'
        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String, nullable=False)
        xp = Column(Integer, nullable=False)

    def add_mob(self, name: str, xp: int):
        mob = self.Mob(name=name, xp=xp)
        self.session.add(mob)
        self.session.commit()

    def get_mob_by_name(self, name: str):
        return self.session.query(self.Mob).filter_by(name=name).first()

    def get_mobs(self):
        return self.session.query(self.Mob).all()

    def delete_mob(self, mob_id: int):
        mob = self.session.query(self.Mob).filter_by(id=mob_id).first()
        if mob:
            self.session.delete(mob)
            self.session.commit()

    def close(self):
        # Ferme la connexion
        self.session.close()

    def add_xp_to_mob(self, name, param):
        mob = self.get_mob_by_name(name)
        mob.xp += param
        self.session.commit()


