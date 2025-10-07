products_mapping = {
    "mappings": {
        "properties": {
            # --- Identifiers and Numerical ---
            "id": {
                "type": "long"
            },
            "user_id": {
                "type": "long"
            },
            "category_id": {
                "type": "keyword"
            },
            "brand_id": {
                "type": "keyword"
            },
            "country": {
                "type": "keyword"
            },
            "price": {
                "type": "float"
            },
            "whole_sale": {
                "type": "integer"
            },

            # --- Text Fields for Search and Filtering ---
            "name": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "name_fr": {
                "type": "text"
            },
            "currency": {
                "type": "keyword"
            },
            "description": {
                "type": "text"
            },
            "description_fr": {
                "type": "text"
            },
            "search_index": {
                "type": "text"
            },

            # --- Image/Hash Fields ---
            "hash": {
                "type": "keyword"
            },
            "image": {
                "type": "keyword"
            },
            "image_original": {
                "type": "keyword"
            },
            "image_thumb": {
                "type": "keyword"
            },
            "image_medium": {
                "type": "keyword"
            },

            "created_at": {
                "type": "date",
                "format": "yyyy-MM-dd HH:mm:ss"
            },
            "updated_at": {
                "type": "date",
                "format": "yyyy-MM-dd HH:mm:ss"
            },
            "deleted_at": {
                "type": "date",
                "format": "yyyy-MM-dd HH:mm:ss"
            },

            # --- Geospatial Fields ---
            "latitude": {
                "type": "float",
                "index": False
            },
            "longitude": {
                "type": "float",
                "index": False
            },
            "location": {
                "type": "geo_point"
            }
        }
    }
}