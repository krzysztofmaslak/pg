from pg import model

__author__ = 'root'

class ImageService:
     def __init__(self, ioc):
        super().__init__()
        self.ioc = ioc

     def find_by_id(self, id):
        return model.Image.query.get(id)

     def delete(self, image):
        if isinstance(image, model.Image):
            model.base.db.session.delete(image)
            model.base.db.session.commit()
        else:
            raise TypeError("Expected Image type in ImageService.delete %s"%type(image))
