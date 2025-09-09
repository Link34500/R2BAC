def get_all_attrs(cls) -> list:
  """Retourne tout les attributs public d'une class"""
  return [key for key in cls.__dict__.keys() if not key.startswith("_") and key.islower() and getattr(cls,key)]