# API Documentation

This documentation outlines the functionalities provided by the API implemented in the provided code. The API allows users to interact with a database of products, offering various endpoints for querying and retrieving product data.

## Base URL

The base URL for accessing the API endpoints is `http://yourdomain.com` (replace `yourdomain.com` with the actual domain where the API is hosted).

## Endpoints

1. **Retrieve Products**
   - **Endpoint:** `/api/products`
   - **Method:** GET
   - **Parameters:**
     - `name` (optional): Filter products by name.
     - `brand` (optional): Filter products by brand.
     - `category` (optional): Filter products by category.
     - `start_date` (optional): Filter products added on or after this date (format: YYYY-MM-DD).
     - `end_date` (optional): Filter products added on or before this date (format: YYYY-MM-DD).
     - `min_price` (optional): Filter products with price greater than or equal to this value.
     - `max_price` (optional): Filter products with price less than or equal to this value.
     - `store` (required): Filter products by store name.
     - `page` (optional, default: 1): Page number for pagination.
     - `page_size` (optional, default: 10): Number of items per page.
     - `sort_by` (optional, default: 'add_date'): Field to sort by (`price`, `reference`, `name`, `category`, `brand`, `add_date`).
     - `sort_order` (optional, default: 'desc'): Sorting order (`asc`, `desc`).
   - **Description:** This endpoint retrieves a list of products based on the provided filters.

2. **Retrieve Grouped Products**
   - **Endpoint:** `/api/grouped-products`
   - **Method:** GET
   - **Parameters:**
     - `store` (required): Filter grouped products by store name.
   - **Description:** This endpoint retrieves a list of unique brands and categories available in the specified store.

3. **Retrieve Products by Reference**
   - **Endpoint:** `/api/products-by-reference`
   - **Method:** GET
   - **Parameters:**
     - `reference` (required): Reference code of the product.
     - `store` (required): Store name.
   - **Description:** This endpoint retrieves products by their reference code in the specified store.

4. **Retrieve New Products**
   - **Endpoint:** `/api/new-products`
   - **Method:** GET
   - **Parameters:**
     - `date` (required): Date for which new products are to be retrieved (format: YYYY-MM-DD).
     - `store` (required): Store name.
     - `category` (optional): Filter new products by category.
     - `brand` (optional): Filter new products by brand.
     - `page` (optional, default: 1): Page number for pagination.
     - `page_size` (optional, default: 10): Number of items per page.
   - **Description:** This endpoint retrieves new products added on the specified date in the specified store.

5. **Retrieve Price Changes**
   - **Endpoint:** `/api/price_changes`
   - **Method:** GET
   - **Parameters:**
     - `start_date` (required): Start date for the price change analysis (format: YYYY-MM-DD).
     - `end_date` (required): End date for the price change analysis (format: YYYY-MM-DD).
     - `store` (required): Store name.
     - `category` (optional): Filter products by category.
     - `brand` (optional): Filter products by brand.
   - **Description:** This endpoint retrieves products with price changes within the specified date range.

6. **Retrieve Removed Products**
   - **Endpoint:** `/api/removed-products`
   - **Method:** GET
   - **Parameters:**
     - `date` (required): Date for which removed products are to be retrieved (format: YYYY-MM-DD).
     - `store` (required): Store name.
     - `category` (optional): Filter removed products by category.
     - `brand` (optional): Filter removed products by brand.
     - `page` (optional, default: 1): Page number for pagination.
     - `page_size` (optional, default: 10): Number of items per page.
   - **Description:** This endpoint retrieves products that were removed from the store on the specified date.

## Response Format

The API responses are returned in JSON format, with appropriate status codes indicating the success or failure of the request.

## Error Handling

In case of errors, the API returns appropriate error messages along with the corresponding HTTP status codes to indicate the nature of the error.

## Authentication

Authentication mechanisms are not implemented in this version of the API. Ensure appropriate security measures are in place when deploying in production environments.

## Rate Limiting

Rate limiting is not implemented in this version of the API. Implement rate limiting to prevent abuse or misuse of the API resources in production environments.

## Conclusion

This documentation provides a comprehensive overview of the functionalities offered by the API and guidelines for interacting with it. For any further assistance or inquiries, please contact the API administrator.
