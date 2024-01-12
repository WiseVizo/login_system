# Database Documentation

## Database Name

users.db

## Tables

### users

#### Columns

1. `id` (INTEGER)

   - Description: Incrementing index for each user.
   - Type: INTEGER
   - Constraints: Primary Key

2. `username` (TEXT)

   - Description: User's username.
   - Type: TEXT

3. `email` (TEXT)
   - Description: User's email address.
   - Type: TEXT

## Sample Queries

### Retrieve All Users

```sql
SELECT * FROM users;
```
