import csv
from io import StringIO
from collections import defaultdict
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.schemas.product import ProductCreate , VariantCreate
from app.Repository.admin_repository import AdminRepository


class AdminService:

    @staticmethod
    async def import_products_csv(db: Session, file: UploadFile):

        if not file.filename.endswith(".csv"):
            raise HTTPException(400, "Only CSV files allowed")

        contents = await file.read()
        csv_data = contents.decode("utf-8")

        reader = csv.DictReader(StringIO(csv_data))

        products_dict = defaultdict(list)

        for row in reader:

            variant = VariantCreate(
                pricing_model=row["pricing_model"],
                base_unit=row["base_unit"],
                value=float(row["value"]),
                base_price=float(row["base_price"]),
                stock_quantity=int(row["stock_quantity"]),
                image_url=row["variant_image_url"] or None,                          # ✅ Fixed
                sales_price=float(row["sales_price"]) if row["sales_price"] else None # ✅ Fixed
            )

            products_dict[row["name"]].append((row, variant))

        products = []

        for name, rows in products_dict.items():

            row = rows[0][0]

            variants = [v for (_, v) in rows]

            product = ProductCreate(
                name=row["name"],
                description=row["description"],
                category_id=int(row["category_id"]),
                brand_id=int(row["brand_id"]) if row["brand_id"] else None,
                image_url=row["image_url"] or None,                                   # ✅ Fixed
                is_active=row["is_active"].lower() == "true",
                variants=variants
            )

            products.append(product)

        return AdminRepository.create_bulk_products(db, products)