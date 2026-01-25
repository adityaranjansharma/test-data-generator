# Persistent VTS (Virtual Table Server) Alternative

A modern, scalable, and persistent alternative to LoadRunner VTS, built with NestJS, React, and PostgreSQL.

## Features

*   **Persistence**: All data is stored in PostgreSQL (or SQLite for dev).
*   **Concurrency**: Atomic record leasing with `SKIP LOCKED` support.
*   **Management UI**: React-based admin dashboard to create ports and upload data.
*   **LoadRunner Compatible**: Includes C helper library for VuGen.
*   **Scalable**: Stateless backend, dockerized.
*   **Auto-Recovery**: Expired leases are automatically reset.

## Prerequisites

*   Node.js 18+
*   Docker & Docker Compose

## Quick Start (Local)

1.  **Start Database**
    ```bash
    docker-compose up -d postgres
    ```
    *(Note: Default configuration uses SQLite for local dev if Postgres is not available or configured)*

2.  **Start Backend**
    ```bash
    cd backend
    npm install
    npx prisma migrate dev --name init
    npm run start:dev
    ```
    Backend runs on `http://localhost:3000`.
    Default API Key: `secret-key-123` (seeded).

3.  **Start Frontend**
    ```bash
    cd frontend
    npm install
    npm run dev
    ```
    Frontend runs on `http://localhost:5173`.
    Login with `secret-key-123`.

## Architecture

*   **Backend**: NestJS (TypeScript), Prisma ORM.
*   **Frontend**: React (Vite), Material UI.
*   **Database**: PostgreSQL (Production), SQLite (Dev).

## LoadRunner Integration

Include `loadrunner/vts.h` in your VuGen script.

```c
#include "vts.h"

vuser_init() {
    vts_init("http://localhost:3000", "secret-key-123");
}

Action() {
    if (vts_lease_record("my-port", "RecID", "RecData") == 0) {
        // Use {RecData}
        vts_consume_record(lr_eval_string("{RecID}"));
    }
}
```

## API Endpoints

*   `POST /api/ports`: Create a port.
*   `GET /api/ports`: List ports.
*   `POST /api/ports/:name/records`: Add record (JSON).
*   `POST /api/ports/:name/records/lease`: Lease a record.
*   `POST /api/records/:id/consume`: Consume record.
*   `POST /api/records/:id/release`: Release record.

## License

MIT
