# Elasticsearch Learning Project

This repository contains Python scripts demonstrating various Elasticsearch operations and data types. The project is organized into two main directories: `basics` and `data_types`, each containing practical examples for learning Elasticsearch concepts.

## Project Structure

```
alx-elastic_search/
├── scripts/
│   ├── basics/           # Fundamental Elasticsearch operations
│   └── data_types/       # Examples of different Elasticsearch data types
└── README.md
```

## Prerequisites

- Elasticsearch server running on `localhost:9200`
- Python 3.x
- `elasticsearch` Python package installed (`pip install elasticsearch`)
- Valid Elasticsearch credentials (default in scripts: username: "elastic", password: "4CMkmoDx")

## Getting Started

1. Ensure Elasticsearch is running locally
2. Install the required Python package:
   ```bash
   pip install elasticsearch
   ```
3. Navigate to the appropriate script directory
4. Run any script with Python:
   ```bash
   python script_name.py
   ```

---

## 📁 Basics Folder

The `basics` folder contains fundamental Elasticsearch operations that every developer should know. These scripts demonstrate core CRUD operations, search functionality, and index management.

### 🔧 Core Operations

#### **create_index.py**
- **Purpose**: Creates a new Elasticsearch index with custom settings
- **Features**:
  - Deletes existing index if present
  - Creates index with specified shards and replicas
  - Example index name: `test-index`

#### **insert_doc.py**
- **Purpose**: Inserts a single document into an index
- **Features**:
  - Demonstrates basic document insertion
  - Uses sample document with title, text, and timestamp fields

#### **insert_multiple_docs.py**
- **Purpose**: Inserts multiple documents from JSON data
- **Features**:
  - Loads documents from `dummy_data.json`
  - Iterates through documents for batch insertion
  - Provides response feedback for each insertion

#### **get_document.py**
- **Purpose**: Retrieves specific documents by ID
- **Features**:
  - Demonstrates document retrieval by ID
  - Shows how to extract document IDs from insertion responses

### 🔍 Search Operations

#### **search_api_1.py**
- **Purpose**: Basic search operations across multiple indices
- **Features**:
  - Creates multiple test indices (`test_index_1`, `test_index_2`)
  - Demonstrates various search patterns:
    - Single index search
    - Multiple indices search (`index1,index2`)
    - Wildcard search (`test_index_*`)
    - All indices search (`_all`)
  - Uses `match_all` query

#### **search_api_2.py**
- **Purpose**: Advanced search queries and filtering
- **Features**:
  - **Term Query**: Exact match searches
  - **Match Query**: Full-text search
  - **Range Query**: Date/numeric range filtering
  - **Bool Query**: Complex compound queries with `must` clauses

#### **search_api_3.py**
- **Purpose**: Search pagination, timeouts, and aggregations
- **Features**:
  - **Pagination**: `size` and `from` parameters
  - **Timeouts**: Query timeout handling
  - **Aggregations**: Maximum value calculations
  - Uses bulk operations for large dataset creation

### 🔄 Update & Delete Operations

#### **update_api.py**
- **Purpose**: Document modification using scripts
- **Features**:
  - Field value updates using Painless scripts
  - Adding new fields to existing documents
  - Field removal operations
  - Version tracking and result verification

#### **delete_doc.py**
- **Purpose**: Document deletion operations
- **Features**:
  - Single document deletion by ID
  - Result verification and error handling

#### **bulk_api.py**
- **Purpose**: Bulk operations for efficiency
- **Features**:
  - Multiple operations in single request
  - Supports update, delete operations
  - Batch processing for better performance

### 📊 Utility Operations

#### **count_doc.py**
- **Purpose**: Document counting with queries
- **Features**:
  - Uses range queries for filtering
  - Date-based counting with specific formats
  - Index refresh for accurate counts

#### **exist_api.py**
- **Purpose**: Checks existence of indices and documents
- **Features**:
  - Index existence verification
  - Document existence checking by ID

#### **mapping.py**
- **Purpose**: Retrieves index mapping information
- **Features**:
  - Shows field types and index structure
  - Useful for schema inspection

### 📄 Sample Data Files

#### **dummy_data.json**
Sample documents with fields:
- `title`: Document titles
- `text`: Document content
- `created_on`: Creation dates

#### **dummy_data_2.json**
Extended sample data with:
- `message`: Search-optimized text content
- `age`: Numeric field for range queries
- `price`: Float values for aggregations

---

## 🏗️ Data Types Folder

The `data_types` folder demonstrates various Elasticsearch field types and their usage patterns. Each script shows how to create indices with specific data types and insert appropriate data.

### 📝 Text and Search Types

#### **text.py**
- **Data Type**: `text`
- **Purpose**: Full-text search capabilities
- **Use Case**: Email bodies, articles, descriptions
- **Features**:
  - Analyzed and tokenized for search
  - Supports fuzzy matching and relevance scoring

#### **completion.py**
- **Data Type**: `completion`
- **Purpose**: Auto-completion and suggestion features
- **Use Case**: Search suggestions, autocomplete
- **Features**:
  - Optimized for prefix matching
  - Supports multiple input suggestions per document

### 🗂️ Structured Data Types

#### **object.py**
- **Data Type**: `object`
- **Purpose**: Nested JSON objects with defined structure
- **Use Case**: Author information, user profiles
- **Features**:
  - Maintains object structure
  - Individual field querying possible

#### **nested.py**
- **Data Type**: `nested`
- **Purpose**: Array of objects with independent querying
- **Use Case**: Multiple user records, product variants
- **Features**:
  - Preserves object relationships
  - Supports nested queries

#### **flattened.py**
- **Data Type**: `flattened`
- **Purpose**: Dynamic objects with unknown structure
- **Use Case**: Metadata, configuration objects
- **Features**:
  - Flattens nested objects into key-value pairs
  - Memory efficient for sparse data

### 🌍 Geographic Data Types

#### **geo_point.py**
- **Data Type**: `geo_point`
- **Purpose**: Geographic coordinates (latitude/longitude)
- **Use Case**: Location tracking, proximity searches
- **Features**:
  - Supports various input formats
  - Enables distance and bounding box queries

#### **geo_shape.py**
- **Data Type**: `geo_shape`
- **Purpose**: Complex geographic shapes
- **Use Case**: Geographic boundaries, polygons, lines
- **Features**:
  - Supports multiple geometry types (Polygon, LineString)
  - Spatial relationship queries

#### **point.py**
- **Data Type**: `point`
- **Purpose**: Cartesian coordinate points
- **Use Case**: 2D coordinate systems, floor plans
- **Features**:
  - Non-geographic coordinate storage
  - Simpler than geo_point for non-Earth coordinates

### 💾 Binary and Specialized Types

#### **binary.py**
- **Data Type**: `binary`
- **Purpose**: Binary data storage (images, files)
- **Use Case**: File attachments, image storage
- **Features**:
  - Base64 encoded data storage
  - Includes image file handling example
  - Uses sample image: `img.jpeg`

#### **other.py**
- **Data Type**: Mixed (keyword, float, date, boolean)
- **Purpose**: Common data types demonstration
- **Use Cases**:
  - `keyword`: Exact match fields (ISBN, IDs)
  - `float`: Decimal numbers (prices)
  - `date`: Temporal data with formatting
  - `boolean`: True/false values
- **Features**:
  - Multiple data types in single mapping
  - Practical real-world examples

---

## 🛠️ Index Configuration

All scripts use consistent index settings:
- **Shards**: 1-2 primary shards
- **Replicas**: 0-3 replica shards
- **Connection**: Local Elasticsearch instance

## 🔧 Common Patterns

### Index Management
```python
# Delete existing index
es.indices.delete(index="index_name", ignore_unavailable=True)

# Create new index with settings
es.indices.create(
    index="index_name",
    settings={"index": {"number_of_shards": 1, "number_of_replicas": 0}},
    mappings={"properties": {...}}
)
```

### Document Operations
```python
# Insert document
response = es.index(index="index_name", body=document)

# Get document
response = es.get(index="index_name", id=document_id)

# Update document
response = es.update(index="index_name", id=document_id, script={...})

# Delete document
response = es.delete(index="index_name", id=document_id)
```

### Search Operations
```python
# Basic search
response = es.search(index="index_name", body={"query": {...}})

# Count documents
response = es.count(index="index_name", query={...})
```

## 📚 Learning Path

1. **Start with Basics**: Begin with `create_index.py` and `insert_doc.py`
2. **Search Operations**: Progress through `search_api_1.py` → `search_api_2.py` → `search_api_3.py`
3. **CRUD Operations**: Practice with `get_document.py`, `update_api.py`, `delete_doc.py`
4. **Bulk Operations**: Learn efficiency with `bulk_api.py`
5. **Data Types**: Explore different field types based on your use case

## ⚠️ Important Notes

- **Security**: Update credentials before production use
- **Index Names**: Some scripts have mismatched index names in operations (e.g., creating one index but inserting into another)
- **Error Handling**: Scripts include basic error handling with `ignore_unavailable=True`
- **Data Refresh**: Some operations require `es.indices.refresh()` for immediate visibility

## 🤝 Contributing

Feel free to add more examples or improve existing scripts. Each script should:
- Include clear comments
- Use consistent naming conventions
- Handle basic error cases
- Provide meaningful output

## 📖 Resources

- [Elasticsearch Python Client Documentation](https://elasticsearch-py.readthedocs.io/)
- [Elasticsearch Official Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Elasticsearch Data Types Reference](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html)
