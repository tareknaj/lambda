from todo import Todo


def get_dogs(session):
    """ Returns all dogs """
    return session.query(Dog).all()


def get_dog_by_id(session, dog_id):
    """ Returns a specific dog
        :param session database session
        :param dog_id Identifier of the dog
    """
    return session.query(Dog).filter_by(id=dog_id).first()