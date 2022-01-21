from sqlalchemy.orm import Session
import models
import shemas


def add_alias(owner_id, chat_id, alias, db: Session):
    alias = models.Alias(owner_id=owner_id, name=alias, chat_id = chat_id)
    db.add(alias)
    db.commit()
    db.refresh(alias)


def delete_aliases(owner_id, chat_id, db: Session):
    aliases = db.query(models.Alias).filter(models.Alias.owner_id == owner_id,
                                            models.Alias.chat_id == chat_id)
    if aliases:
        aliases.delete(synchronize_session=False)
    db.commit()


def update_aliases(id,  chat_id, aliases, db: Session):
    delete_aliases(id, chat_id, db)
    for alias in aliases:
        add_alias(id,  chat_id, alias, db)


def get_user(id: int, db: Session):
    user = db.query(models.User).filter(models.User.tg_id == id).first()
    if user:
        return user


def get_chat_aliases(chat_id: int, db: Session):
    aliases = db.query(models.Alias).filter(models.Alias.chat_id == chat_id)
    return aliases


def new_user(id: int, tag: str,  db: Session):
    user = models.User(tg_id=id, tag=tag, set_up=False)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(id: int, tag: str, set_up: bool, db: Session):
    user = db.query(models.User).filter(models.User.tg_id == id)
    user_model = shemas.User(tag, set_up)
    user.update(user_model.__dict__)
    db.commit()
    # update_aliases(id, aliases, db)

