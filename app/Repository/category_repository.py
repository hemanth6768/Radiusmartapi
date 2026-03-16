from sqlalchemy.orm import Session , joinedload
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.models.section import Section

class CategoryRepository:


    @staticmethod
    def create(db: Session, category: CategoryCreate):

        db_category = Category(**category.model_dump())

        db.add(db_category)
        db.commit()
        db.refresh(db_category)

        return db_category


    @staticmethod
    def get_all(db: Session):
        return db.query(Category).order_by(Category.id).all()

    
    @staticmethod
    def get_all(db: Session):
       return (
          db.query(Category)
         .filter(Category.is_active == True)
         .order_by(Category.id)
         .all()
       )

    @staticmethod
    def get_by_id(db: Session, category_id: int):
        return db.query(Category).filter(Category.id == category_id).first()

    @staticmethod
    def get_sections_with_categories(db: Session):

     return (
        db.query(Section)
        .options(joinedload(Section.categories))
        .filter(Section.is_active == True)
        .order_by(Section.display_order)
        .all()
    )
    @staticmethod
    def get_by_section(db: Session, section_id: int):
        return db.query(Category).filter(Category.section_id == section_id).all()


    @staticmethod
    def get_by_name_and_section(db: Session, name: str, section_id: int):
        return db.query(Category).filter(
            Category.name == name,
            Category.section_id == section_id
        ).first()


    @staticmethod
    def update(db: Session, db_category: Category, updates: CategoryUpdate):

        update_data = updates.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_category, key, value)

        db.commit()
        db.refresh(db_category)

        return db_category


    @staticmethod
    def delete(db: Session, db_category: Category):
        db.delete(db_category)
        db.commit()