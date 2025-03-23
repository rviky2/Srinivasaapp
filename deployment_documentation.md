# Azure Deployment Documentation for Question Paper Management System

## Overview
This document outlines the steps taken to deploy the Question Paper Management System to Azure App Service with PostgreSQL database and Azure Blob Storage for media files.

## 1. Project Configuration

### 1.1 Environment Setup
- Created necessary configuration files for Azure deployment:
  - `.azure/deploy.sh` - Deployment script for post-deployment tasks
  - `.deployment` - Configuration for Azure App Service deployment
  - `Procfile` - Web server configuration
  - `runtime.txt` - Python version specification
  - Updated `requirements.txt` with Azure dependencies

### 1.2 Dependencies Added
```
psycopg2-binary==2.9.9
django-storages==1.14.2
azure-storage-blob==12.17.0
gunicorn==21.2.0
```

### 1.3 Settings Configuration
- Updated `settings.py` to handle different environments:
  - Configured PostgreSQL for production
  - Set up Azure Blob Storage for media files
  - Added CSRF trusted origins
  - Modified DEBUG setting to properly parse environment variables

## 2. Azure Resource Creation

### 2.1 Resources Created
- Resource Group: `questionpaper-rg`
- App Service Plan: `qpaper-plan` (B1, Linux)
- Web App: `qpaper-app` (Python 3.11)
- PostgreSQL Server: `qpaper-db`
- Database: `questionpaper_db`
- Storage Account: `qpaperstorage`
- Storage Container: `media`

### 2.2 Commands Used
```bash
# Create Resource Group
az group create --name questionpaper-rg --location westus2

# Create PostgreSQL Server
az postgres server create --resource-group questionpaper-rg --name qpaper-db --location westus2 --admin-user postgres --admin-password YourPassword123! --sku-name B_Gen5_1

# Create Database
az postgres db create --resource-group questionpaper-rg --server-name qpaper-db --name questionpaper_db

# Create Storage Account
az storage account create --name qpaperstorage --resource-group questionpaper-rg --location westus2 --sku Standard_LRS

# Create Storage Container
az storage container create --name media --account-name qpaperstorage --account-key YOUR_STORAGE_KEY --public-access blob

# Create App Service Plan
az appservice plan create --name qpaper-plan --resource-group questionpaper-rg --sku B1 --is-linux --location westus2

# Create Web App
az webapp create --resource-group questionpaper-rg --plan qpaper-plan --name qpaper-app --runtime "PYTHON:3.11"
```

## 3. Environment Variables Configuration

Environment variables were set in Azure App Service:

```bash
az webapp config appsettings set --resource-group questionpaper-rg --name qpaper-app --settings \
  DEBUG="False" \
  SECRET_KEY="YourSecretKey" \
  DBENGINE="django.db.backends.postgresql" \
  DBNAME="questionpaper_db" \
  DBUSER="postgres@qpaper-db" \
  DBPASS="YourDatabasePassword" \
  DBHOST="qpaper-db.postgres.database.azure.com" \
  DBPORT="5432" \
  AZURE_ACCOUNT_NAME="qpaperstorage" \
  AZURE_ACCOUNT_KEY="YourStorageKey" \
  AZURE_CONTAINER="media" \
  CSRF_TRUSTED_ORIGINS="https://qpaper-app.azurewebsites.net"
```

## 4. GitHub Integration

- Connected GitHub repository to Azure App Service using GitHub Actions
- Automatically created `.github/workflows/master_qpaper-app.yml` workflow file
- Configured automatic deployment on pushes to the master branch

## 5. Post-Deployment Tasks

### 5.1 Database Migrations
```bash
az webapp ssh --resource-group questionpaper-rg --name qpaper-app
cd site/wwwroot
source /antenv/bin/activate
python manage.py migrate
```

### 5.2 Superuser Creation
```bash
python manage.py createsuperuser
# Created user: root, email: rvikramfour@gmail.com
```

### 5.3 CSRF Configuration
Added the following to settings.py:
```python
# CSRF settings
CSRF_TRUSTED_ORIGINS = ['https://qpaper-app.azurewebsites.net']
```

### 5.4 DEBUG Setting Fix
Updated DEBUG setting to properly parse environment variables:
```python
DEBUG = os.environ.get('DEBUG', 'True').lower() != 'false'
```

## 6. Troubleshooting

### 6.1 CSRF Issues
- Added CSRF_TRUSTED_ORIGINS to both settings.py and environment variables
- Pushed changes to GitHub to trigger automatic deployment

### 6.2 Media Storage
- Updated settings.py to properly handle DEBUG setting for Azure Blob Storage configuration
- Configured Azure Blob Storage for media files in production mode

## 7. Final Application

- Web Application URL: https://qpaper-app.azurewebsites.net/
- Admin Interface: https://qpaper-app.azurewebsites.net/admin/
- Database: PostgreSQL on Azure
- Media Storage: Azure Blob Storage when DEBUG is False

## 8. Maintenance Notes

- Database migrations should be run when models change
- GitHub pushes automatically trigger deployment
- Superuser already created for admin access
- DEBUG is set to False in production for security and to enable Azure Blob Storage 