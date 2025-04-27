Here’s the updated README file with the FastAPI Docker Compose command added:

---

# TODO App

**Author:** _Sharukh Rahman S_  
**Portfolio:** [Portfolio](https://sharukhrahman.vercel.app/)

## Overview

The application allows users to create, update, and delete tasks. Each task has a title, description, and status (e.g., "To Do," "In Progress," "Done"). Users can view a list of tasks and filter them by their status.

To view the API documentation, visit [here](https://documenter.getpostman.com/view/11698155/2sA3Qs9rep).

---

## Getting Started

To run the app, it’s recommended to use **nvm** for managing Node.js versions. The app is developed using **Node version 20.12.2**.

### Backend Setup (Express)

1. Open terminal and navigate to the `backend/express` folder:

    ```bash
    cd backend/express
    ```

2. Install dependencies:

    ```bash
    npm install
    ```

3. Run migrations:

    ```bash
    npx prisma migrate dev --name init
    ```

4. Start the development server:

    ```bash
    npm run dev
    ```

### Frontend Setup (React)

1. Open a second terminal and navigate to the `frontend/react` folder:

    ```bash
    cd frontend/react
    ```

2. Install dependencies:

    ```bash
    npm install
    ```

3. Start the React development server:

    ```bash
    npm run dev
    ```

---

### Local Development

- Frontend will be available at: [http://localhost:5173](http://localhost:5173/)
- Backend will be available at: [http://localhost:5000](http://localhost:5000/)

---

## FastAPI Project Setup (Docker)

To run the FastAPI project using Docker Compose, use the following command:

```bash
docker compose -f docker-compose.debug.yml up --build
```

---

## Environment Configuration

- Make sure to use the `env.example` file to generate your `.env` file for all the projects (backend and frontend).
- Follow the instructions in the `.env.example` to set up necessary environment variables for the application.

---

## FastAPI Project
Python version: **3.12.10**

**Pending Tasks:**

- Development Testing
- Kafka Integration
- OpenTelemetry (OTEL) Logging
- Alembic and other migrations
- Claims/RBAC

---

## Other Projects

Work is in progress for the following projects:

- GoFiber
- SpringBoot
- Rocket
- Zig

---

Feel free to explore and contribute to these projects. For more details, refer to the respective project's documentation.

