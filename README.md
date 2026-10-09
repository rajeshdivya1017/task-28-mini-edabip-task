# Inventory & Sales Analytics System

## 📌 Project Overview

The Inventory & Sales Analytics System is a web-based application designed to manage products, track sales, monitor stock levels, and analyze business performance through interactive dashboards and charts.

The system provides role-based access for Admin and Manager users. Admins can manage products and monitor sales analytics, while Managers can view products and record sales.

The application helps businesses maintain accurate inventory records, reduce stock management errors, and make better decisions using sales data.

## 🎯 Project Objectives

* Manage products and product categories efficiently.
* Track sales transactions and inventory levels.
* Provide secure authentication using JWT.
* Implement role-based access control for Admin and Manager.
* Display sales performance using interactive charts.
* Monitor low-stock products.
* Generate analytics based on date ranges and categories.
* Maintain accurate sales records and stock quantities.

## 🛠️ Technologies Used

### Frontend

* React
* TypeScript
* Vite
* React Router DOM
* TanStack Query
* Zustand
* Axios
* React Hook Form
* Zod
* Recharts
* Lucide React
* CSS

### Backend

* Python
* Flask
* Flask-SQLAlchemy
* MySQL
* JWT Authentication

## ✨ Features

### 1. Authentication

* Secure login using JWT authentication.
* Access token and refresh token support.
* User authentication and session management.
* Protected routes for authenticated users.
* Role-based access control.

### 2. Dashboard & Analytics

* Display key performance indicators.
* View total revenue and sales information.
* Monitor total products and low-stock products.
* Visualize revenue trends using a line chart.
* Analyze category-wise sales using bar and pie charts.
* Display top-performing products in a table.
* Filter analytics using available filter options.
* Automatically refresh analytics data every 30 seconds.

### 3. Product Management

* View the list of products.
* Add new products.
* Update existing product details.
* Delete products when deletion is permitted.
* Organize products by category.
* Search and filter products.
* Identify low-stock products.
* Prevent deletion of products associated with sales.
* Restrict product management operations to Admin users.

### 4. Sales Management

* View recorded sales transactions.
* Record new sales.
* Select products with available stock.
* Enter sales quantities and dates.
* Automatically calculate the total sale amount.
* Validate stock availability before recording a sale.
* Automatically reduce stock after a successful sale.
* Store the product price at the time of sale.
* Associate sales with the authenticated user.
* Filter sales using available filter options.

### 5. Role-Based Access Control

**Admin**

* View the dashboard and analytics.
* View products and product categories.
* Add, update, and delete products, subject to business rules.
* View sales transactions.
* Record sales.
* Access administrative product management features.

**Manager**

* View the dashboard and analytics.
* View products and product categories.
* View sales transactions.
* Record sales.
* Cannot add, update, or delete products.
* Cannot manage user accounts.

Administrative actions are restricted based on the authenticated user's role.

### 6. Form Validation

* Use React Hook Form to manage form state.
* Use Zod schemas to validate form inputs.
* Validate login, product, and sales forms.
* Display appropriate validation messages.
* Prevent invalid form submissions.

### 7. State Management & Data Fetching

* Use TanStack Query to fetch and manage server data.
* Cache API responses and refresh data when required.
* Invalidate relevant queries after successful mutations.
* Use Zustand to manage application filters and UI state.
* Use Axios for API communication.
* Automatically attach JWT tokens to authorized requests.
* Handle token refresh through an Axios interceptor.

### 8. User Interface

* Responsive dashboard layout.
* Sidebar navigation.
* Professional tables, forms, and buttons.
* Interactive charts for sales analysis.
* Search and filtering options.
* Toast notifications for user feedback.
* Light and dark theme support.

## 🗄️ Database

**Database Name:** `inventory_sales`

The application uses MySQL to store inventory and sales information.

### Main Tables

**1. Users**

* Stores user details and roles.
* Supports Admin and Manager roles.

**2. Categories**

* Stores product category information.

**3. Products**

* Stores product details, category, price, stock quantity, and unit.

**4. Sales**

* Stores sales transactions, product references, seller information, quantity, unit price, total amount, and sale date.

## 📁 Project Structure

```text
inventory-app/
├── backend/
│   ├── app.py
│   ├── seed.py
│   ├── requirements.txt
│   └── ...
│
└── frontend/
    ├── src/
    │   ├── api/
    │   ├── components/
    │   ├── context/
    │   ├── hooks/
    │   ├── pages/
    │   ├── routes/
    │   ├── schemas/
    │   ├── stores/
    │   ├── types/
    │   ├── App.tsx
    │   ├── main.tsx
    │   └── index.css
    ├── package.json
    └── vite.config.ts
```

*Note: The structure above is illustrative. Update it if your actual project folders or filenames differ.*

## ⚙️ Installation & Setup

### Prerequisites

Install the following before running the application:

* Node.js and npm
* Python
* MySQL Server
* A code editor such as Visual Studio Code

### 1. Clone the Repository

```bash
git clone <your-repository-url>
```

Navigate to the project directory:

```bash
cd inventory-app
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Configure the database connection using your existing backend configuration and create the required MySQL database.

If the project uses environment variables, configure the database credentials and JWT settings in the appropriate environment file.

Run the backend application:

```bash
python app.py
```

The Flask development server will display its local URL in the terminal.

### 3. Frontend Setup

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install the dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open the local URL displayed in the terminal to access the application.

### 4. Build the Frontend

To verify the production build:

```bash
npm run build
```

## 🔐 Security & Validation

* JWT-based authentication.
* Protected frontend routes.
* Role-based authorization.
* Backend validation for restricted operations.
* Parameterized database queries.
* Stock availability validation before recording sales.
* Product deletion restrictions when sales records exist.
* Zod-based frontend form validation.

Frontend restrictions improve the user experience, while the backend enforces authorization and business rules.

## 📊 Business Logic

* A sale can be recorded only when sufficient stock is available.
* The total sale amount is calculated using the quantity and unit price.
* Product stock is reduced after a successful sale.
* The sale record stores the unit price applicable at the time of the transaction.
* The authenticated user's identity is associated with the sale.
* Products linked to existing sales cannot be deleted when the deletion restriction applies.
* Only Admin users can perform product management operations.
* Managers can view products and record sales.

## 🧪 Testing & Verification

The following areas can be tested to verify the application:

* Admin and Manager login.
* Authentication and protected routes.
* Role-based product management restrictions.
* Product creation, editing, and deletion.
* Product
