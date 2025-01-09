from sqlalchemy import create_engine, Column, Integer, String, Boolean, Tuple
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Preset(Base):
    __tablename__ = 'presets'

    name = Column(String, default='Default', primary_key=True)
    film_type = Column(Integer, default=0)
    dark_threshold = Column(Integer, default=25)
    light_threshold = Column(Integer, default=100)
    border_crop = Column(Integer, default=1)
    flip = Column(Boolean, default=False)
    white_point = Column(Integer, default=0)
    black_point = Column(Integer, default=0)
    gamma = Column(Integer, default=0)
    shadows = Column(Integer, default=0)
    highlights = Column(Integer, default=0)
    temp = Column(Integer, default=0)
    tint = Column(Integer, default=0)
    sat = Column(Integer, default=100)
    base_detect = Column(Integer, default=0)
    base_rgb = Column(Tuple, default=(255, 255, 255))
    remove_dust = Column(Boolean, default=False)
    selected = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Preset(name={self.name}, film_type={self.film_type}, dark_threshold={self.dark_threshold}, light_threshold={self.light_threshold}, border_crop={self.border_crop}, flip={self.flip}, white_point={self.white_point}, black_point={self.black_point}, gamma={self.gamma}, shadows={self.shadows}, highlights={self.highlights}, temp={self.temp}, tint={self.tint}, sat={self.sat}, base_detect={self.base_detect}, base_rgb={self.base_rgb}, remove_dust={self.remove_dust}, selected={self.selected})>"

class PresetDatabase:
    def __init__(self):
        # Create an engine and sessionmaker
        engine = create_engine('sqlite:///presets.db')
        self._session = sessionmaker(bind=engine)
        self.default_preset = Preset()

        # Create tables and add default preset
        Base.metadata.create_all(engine)
        with self._session() as session:
            if not session.get(Preset, 'Default'):
                session.add(self.default_preset)
                session.commit()

    def get_presets(self) -> list[Preset]:
        with self._session() as session:
            return session.query(Preset).order_by(Preset.name).all()

    def add_preset(self, preset: Preset) -> None:
        with self._session() as session:
            session.add(preset)
            session.commit()

    def update_preset(self, preset: Preset) -> None:
        with self._session() as session:
            session.query(Preset).filter(Preset.name == preset.name).update(preset)
            session.commit()

    def rename_preset(self, old_name: str, new_name: str) -> None:
        with self._session() as session:
            session.query(Preset).filter(Preset.name == old_name).update({Preset.name: new_name})
            session.commit()

    def delete_preset(self, name: str) -> None:
        with self._session() as session:
            session.query(Preset).filter(Preset.name == name).delete()
            session.commit()

    def get_selected(self) -> Preset:
        with self._session() as session:
            return session.query(Preset).filter(Preset.selected).first()
