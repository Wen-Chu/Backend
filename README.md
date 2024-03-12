# Backend

## Project Structure
```
Backend/
|
├── db/ → Database(Table: admin, task, customer, transaction)
|   ├── dev_mydata.db → Development database
|   ├── mydata.db → Production database
|   └── test_mydata.db → Testing database
|
├── endpoints/ 
|   ├── config/
|   |   ├── __init__.py → Initialize configuration
|   |   ├── development.py → Development configuration
|   |   ├── production.py → Production configuration
|   |   └── testing.py → Testing configuration
|   |
|   ├── routes/
|   |   ├── admin → Admin routes
|   |   |   ├── model.py
|   |   |   └── views.py
|   |   |
|   |   ├── customer → Customer routes
|   |   |   ├── model.py
|   |   |   └── views.py
|   |   |
|   |   ├── task → Task routes
|   |   |   ├── model.py
|   |   |   └── views.py
|   |   | 
|   |   └──  transaction → Transaction routes
|   |       ├── model.py
|   |       └── views.py
|   |
|   └── __init__.py → Initialize endpoints
|
├── migrations/ → Database migration
|   ├── versions/ → Database migration versions
|   |   └── ...
|   ├── alembic.ini → Alembic configuration
|   ├── env.py → Alembic environment
|   ├── README → Alembic README
|   └── script.py.mako → Alembic script
|
├── tests/ → Unit tests
|   ├── test_admin.py
|   ├── test_customer.py
|   ├── test_task.py
|   └── test_transaction.py
|
├── .gitattributes → Git attributes
|
├── .gitignore → Git ignore
|
├── app.py → Application entry point
|
├── docker-compose.yml → Docker compose
|
├── Dockerfile → Dockerfile
|
├── README.md → README
|
└── requirements.txt  → Python dependencies
```

## Application Setup
Ensure that Docker is installed and operational on the system.
### Building the Docker Environment
  ```bash
  docker-compose build
  ```
### Running the Flask Application 
- The application will run in detached mode.
    ```bash
    docker-compose up -d backend
    ```
- To apply database migrations after starting the application, use:
    ```bash
    docker-compose exec backend flask db upgrade
    ```
### Viewing Application Logs
```bash
docker-compose logs -f backend
```
### Running the Unit Tests
```bash
docker-compose up test
```
### Stop the docker container
- Use the following command to stop the Docker container:
  ```bash
    docker-compose down
    ```
### Access the application
  - API endpoints and other related information can be found in the API section below.

## API Overview
This application operates on port 5000. The application requires administrator authentication for accessing sensitive task, transaction and customer-related APIs. Upon successful authentication, an authentication token is generated, granting access to these APIs. 
<br>*Note that the token expires after 10 minutes. In the event of token expiration, a new login is required to obtain a new token.

### Authentication
  | HTTP Method | API Endpoint                               | Payload                                                     | Description                        |
  |:------------|:-------------------------------------------|:------------------------------------------------------------|:-----------------------------------|
  | POST        | /api/v1/admin/register                     | {"admin_name": "string", "password": "string"}              | Register a new admin account       |
  | POST        | /api/v1/admin/login                        | {"admin_name": "string", "password": "string"}              | Log in to an admin account         |

### Task Management
  | HTTP Method | API Endpoint                               | Payload                                                     | Description                        |
  |:------------|:-------------------------------------------|:------------------------------------------------------------|:-----------------------------------|
  | GET         | /api/v1/task                               | -                                                           | Get all tasks                       |
  | GET         | /api/v1/task/{task_id}                     | -                                                           | Get a specific task                     |
  | POST        | /api/v1/task                               | {"task_name": "string"}                                     | Create a task                      |
  | PUT         | /api/v1/task                               | {"task_id": number, task_name": "string", "status": number} | Update an existing task            |
  | DELETE      | /api/v1/task/{task_id}                     | -                                                           | Delete a specific task             |

### Customer Management
  | HTTP Method | API Endpoint                               | Payload                                                     | Description                        |
  |:------------|:-------------------------------------------|:------------------------------------------------------------|:-----------------------------------|
  | GET         | /api/v1/customer                           | -                                                           | Get all customer information       |
  | GET         | /api/v1/customer/{customer_name}           | -                                                           | Get specific  customer information |
  | POST        | /api/v1/customer                           | {"customer_name": "string", "balance": number}              | Create new customer information    |

### Transaction Management
  | HTTP Method | API Endpoint                               | Payload                                                     | Description                         |
  |:------------|:-------------------------------------------|:------------------------------------------------------------|:------------------------------------|
  | GET         | /api/v1/transaction/record/{customer_name} | -                                                           | Get a customer's transaction record |
  | POST        | /api/v1/transaction/credit                 | {"customer_name": "string", "amount": number}               | Credit points to the customer       |
  | POST        | /api/v1/transaction/debit                  | {"customer_name": "string", "amount": number}               | Debit points from the customer      |
