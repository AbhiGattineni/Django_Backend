# Development Data Seeding

This folder contains utilities for seeding development databases with dummy data.

## Overview

The seeding command generates 10-30 realistic dummy records for all models in the Django backend application. This helps developers test the application without using production data.

## Usage

### Prerequisites

1. Run all migrations first:
   ```bash
   python manage.py migrate
   ```

2. Ensure your development database is configured in `settings.py`

### Seeding Data

To seed the database with dummy data:

```bash
python manage.py seed_dev_data
```

This will create:
- **Subsidiaries**: 5 records (AMS, ACS, ASS, APS, ATI)
- **Access Roles**: 6 records
- **Users**: 25 records
- **Employers**: 8 records
- **Recruiters**: 15 records
- **Consultants**: 20 records
- **Status Consultants**: 15 records
- **Roles**: 20 records
- **Packages**: 3 records
- **Colleges**: 3 records
- **College Details**: 9 records (3 per college)
- **Persons**: 15 records
- **Part Timers**: 15 records
- **Todos**: 15 records
- **ACS PartTimer Status**: 20 records
- **Status Updates**: 25 records
- **Transactions**: 20 records
- **Team Members**: 10 records
- **Device Allocations**: 15 records
- **Happiness Indexes**: 20 records
- **Shopping Products**: 3 records

### Clearing Existing Data

To clear all existing data before seeding (useful for a fresh start):

```bash
python manage.py seed_dev_data --clear
```

**⚠️ Warning**: The `--clear` flag will delete ALL records from all models. Use with caution!

## Models Covered

The seed command populates all models in:

### `backend_api` app:
- ✅ Todo
- ✅ Person
- ✅ PartTimer
- ✅ Role
- ✅ CollegesList
- ✅ CollegeDetail
- ✅ AccessRoles
- ✅ Employer
- ✅ Recruiter
- ✅ Consultant
- ✅ StatusConsultant
- ✅ User
- ✅ Package
- ✅ AcsParttimerStatus
- ✅ StatusUpdates
- ✅ ShopingProduct
- ✅ TeamMember
- ✅ DeviceAllocation
- ✅ HappinessIndex
- ✅ Subsidiary

### `transaction_api` app:
- ✅ Transaction

## Notes

- **Images**: The `ShopingProduct` model has ImageField that requires actual files. Images are skipped in the seed command. You can add images manually through the admin panel.

- **Foreign Keys**: The command handles dependencies correctly - related models are created first (e.g., Users before Roles, Employers before Consultants).

- **Unique Constraints**: The command uses `ignore_conflicts=True` to avoid errors when re-running the seed command.

- **Realistic Data**: All data is generated with realistic values including:
  - Proper date ranges
  - Valid email formats
  - Realistic phone numbers
  - Consistent relationships between models

## Development Workflow

1. Set up your development database
2. Run migrations: `python manage.py migrate`
3. Seed dummy data: `python manage.py seed_dev_data`
4. Start developing and testing!

## Troubleshooting

### "No module named..." errors
Make sure you're running the command from the project root directory where `manage.py` is located.

### Foreign key constraint errors
This usually means a dependency model wasn't seeded. The command seeds models in the correct order, but if you encounter this, try running `--clear` first and then re-seeding.

### Duplicate key errors
The seed command uses `get_or_create` and `ignore_conflicts=True` to handle duplicates, but if you still see errors, use the `--clear` flag first.

