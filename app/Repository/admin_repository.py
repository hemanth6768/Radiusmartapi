from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.productvariant import ProductVariant


class AdminRepository:

    @staticmethod
    def create_bulk_products(db: Session, products):

        product_mappings = []
        variant_mappings = []

        # Step 1: Prepare product rows
        for product in products:

            product_mappings.append({
                "name": product.name,
                "description": product.description,
                "category_id": product.category_id,
                "brand_id": product.brand_id,
                "image_url": product.image_url,
                "is_active": product.is_active
            })

        # Step 2: Bulk insert products
        db.bulk_insert_mappings(Product, product_mappings)

        db.commit()

        # Step 3: Fetch inserted products
        inserted_products = db.query(Product).order_by(Product.id.desc()).limit(len(product_mappings)).all()

        inserted_products.reverse()

        # Step 4: Prepare variants
        for product_obj, product_data in zip(inserted_products, products):

            for variant in product_data.variants:

                variant_mappings.append({
                    "product_id": product_obj.id,
                    "pricing_model": variant.pricing_model,
                    "base_unit": variant.base_unit,
                    "value": variant.value,
                    "base_price": variant.base_price,
                    "stock_quantity": variant.stock_quantity,
                    "image_url": variant.image_url,
                    "sales_price": variant.sales_price
                })

        # Step 5: Bulk insert variants
        db.bulk_insert_mappings(ProductVariant, variant_mappings)

        db.commit()

        return {
            "products_created": len(product_mappings),
            "variants_created": len(variant_mappings)
        }