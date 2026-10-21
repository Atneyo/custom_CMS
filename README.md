# Customizable Photo Gallery

## Table of Contents

- [Project Goal](#project-goal)
- [Technical Stack](#technical-stack)
- [Architecture Overview](#architecture-overview)
  - [Global View](#global-view)
  - [Data Model](#data-model)
  - [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
  - [Repository Overview](#repository-overview)
  - [Backend Structure](#backend-structure)
  - [Frontend Structure](#frontend-structure)
- [MVP Roadmap](#mvp-roadmap)

---

## Project Goal

The main goal of this project is to develop a custom, lightweight CMS specialized for photo gallery websites.

## Technical Stack

- **Frontend:** React, Next.js, TypeScript, Tailwind CSS
- **Backend:** Python, Django, Django REST Framework (DRF)
- **Image Processing:** Pillow (with PyVips planned if higher performance is required)
- **Database:** MySQL (migrating to PostgreSQL if needed)
- **Deployment:** Docker

---

## Architecture Overview

### Global View
```text
                    Browser
           ┌───────────┴───────────┐
     Public Site              Admin UI
     (Visitors)        (Client, Authenticated)
           └───────────┬───────────┘
                       │
           ┌───────────▼───────────┐
           │       FRONTEND        │
           │  Next.js + React + TS │  (Only communicates with the API)
           └───────────┬───────────┘
                       │ HTTP / JSON (Session Cookie)
           ┌───────────▼───────────┐
           │        BACKEND        │
           │      Django + DRF     │  Auth, validation, business logic,
           │     + Image Module    │  and image processing
           └─────┬───────────┬─────┘
                 │           │
         ┌───────▼──┐     ┌──▼─────────────┐
         │  MySQL   │     │ media/ (images)│
         │ (Volume) │     │    (Volume)    │
         └──────────┘     └────────────────┘
```

### Data Model

```text
User (Django) ──── Site Administrator

Collection ────── id, name, slug, description, cover (→ Photo), order
Photo ─────────── id, title, description, collection (→ Collection),
                  tags (↔ Tag), original_path, thumb/medium/large paths,
                  width, height, taken_at, order, created_at
Tag ───────────── id, name, slug
Page ──────────── id, slug, title, content, updated_at
SiteSettings ──── site_name, logo, header_menu, footer_text (Singleton)
```

### API Endpoints

| Method | Endpoint | Access Level | Description |
| :--- | :--- | :--- | :--- |
| **GET** | `/api/collections/` | Public | List all collections |
| **GET** | `/api/photos/?collection=travel&tag=nature` | Public | List filtered photos |
| **GET** | `/api/pages/about/` | Public | Get specific page content |
| **GET** | `/api/settings/` | Public | Get global site settings |
| **POST** | `/api/auth/login/` | Public (Rate-limited) | User login |
| **POST** | `/api/auth/logout/` | Authenticated | User logout |
| **POST** | `/api/photos/` | Admin | Upload a new photo |
| **PATCH / DELETE** | `/api/photos/{id}/` | Admin | Update or delete a photo |
| **POST / PATCH / DELETE** | `/api/collections/` | Admin | Manage collections |
| **PUT** | `/api/pages/{slug}/` | Admin | Update custom page content |
| **PUT** | `/api/settings/` | Admin | Update site settings |


---

## Project Structure

### Repository Overview

```text
photo-cms/
├── backend/                  # Django API
├── frontend/                 # Next.js Application
├── docker/                   # Docker configurations (Production)
│   ├── nginx/
│   └── ...
├── docker-compose.yml        # Development environment (MySQL service)
├── docker-compose.prod.yml   # Production environment
├── .env.example              # Environment variables template
├── .gitignore
└── README.md
```

### Backend Structure

```text
backend/
├── manage.py
├── requirements/
│   ├── base.txt              # Django, DRF, Pillow, django-cors-headers, mysqlclient
│   ├── dev.txt               # Development dependencies
│   └── prod.txt              # Gunicorn, production tools
├── config/                   # Project configuration
│   ├── settings/
│   │   ├── base.py           # Common settings
│   │   ├── dev.py            # Debug mode, CORS allowed for local dev
│   │   └── prod.py           # HTTPS, Secure cookies, allowed hosts
│   ├── urls.py               # Main routing (/api/...)
│   ├── wsgi.py
│   └── asgi.py
├── apps/                     # Django applications per domain
│   ├── accounts/             # Authentication module
│   │   ├── views.py          # Login, logout, session check
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── tests/
│   ├── gallery/              # Core gallery application
│   │   ├── models.py         # Collection, Photo, Tag
│   │   ├── serializers.py
│   │   ├── views.py          # DRF ViewSets
│   │   ├── filters.py        # Collection & tag filtering
│   │   ├── permissions.py    # Public read, Admin write
│   │   ├── services.py       # Business logic (e.g., photo creation)
│   │   ├── urls.py
│   │   ├── migrations/
│   │   └── tests/
│   ├── pages/                # Custom editable pages (e.g., About)
│   │   ├── models.py         # Page model (slug, title, content)
│   │   └── ...
│   └── site_settings/        # Global site parameters (Header, Footer, Site Name)
│       ├── models.py         # SiteSettings (Singleton pattern)
│       └── ...
├── core/                     # Shared cross-cutting logic (no business models)
│   ├── images/               # Image processing pipeline
│   │   ├── processing.py     # Validation, EXIF extraction, thumbnails, WebP conversion
│   │   ├── validators.py     # File size, dimensions, MIME-type checks
│   │   └── storage.py        # File handling (Local Disk → AWS S3 migration target)
│   └── permissions.py
├── media/                    # Uploaded media (Ignored by Git, Docker volume)
│   ├── originals/            # Private storage: never served publicly directly
│   └── public/               # Optimized assets: thumbnail / medium / large
└── Dockerfile
```

### Frontend Structure

```text
frontend/
├── package.json
├── tsconfig.json
├── next.config.ts
├── tailwind.config.ts
├── .env.local                # API URL config
├── public/                   # Static assets (Favicon, icons)
└── src/
    ├── app/
    │   ├── (public)/         # Visitor-facing website
    │   │   ├── layout.tsx    # Header & Footer wrapper
    │   │   ├── page.tsx      # Home page (or redirect to gallery)
    │   │   ├── photos/
    │   │   │   ├── page.tsx  # Gallery view with filter controls
    │   │   │   └── [collection]/page.tsx
    │   │   └── about/page.tsx
    │   ├── admin/            # Administration dashboard
    │   │   ├── login/page.tsx
    │   │   ├── layout.tsx    # Session guard & navigation
    │   │   ├── photos/       # Photo management list, upload, edit
    │   │   ├── collections/  # Collection management
    │   │   ├── pages/        # Custom pages editor
    │   │   └── settings/     # Header & footer settings
    │   └── layout.tsx
    ├── components/
    │   ├── public/           # Header, Footer, Gallery, Lightbox, Filters
    │   ├── admin/            # PhotoForm, Uploader, RichTextEditor
    │   └── ui/               # Reusable UI elements (Buttons, Inputs, Modals)
    ├── lib/
    │   ├── api/
    │   │   ├── client.ts     # Base fetch wrapper (Cookies, CSRF, errors)
    │   │   ├── photos.ts     # getPhotos(), createPhoto(), etc.
    │   │   ├── collections.ts
    │   │   ├── pages.ts
    │   │   └── auth.ts
    │   └── utils.ts
    └── types/                # TypeScript interfaces (Photo, Collection, Page, SiteSettings)
```

---

## MVP Roadmap

The primary objective for the Minimum Viable Product (MVP) is to deliver an end-to-end functional pipeline: an admin uploads a photo, which is processed and instantly displayed on the public gallery interface.

| Phase | Task Description | Estimated Duration |
| :---: | :--- | :---: |
| **1** | **Foundations:** Git repository, MySQL via Docker, base Django setup | 1–2 days |
| **2** | **Core Models:** Collection + Photo models, Django Admin registration | 1 day |
| **3** | **Image Module:** Validation, WebP conversion, thumbnail generation, EXIF parsing | 3–4 days |
| **4** | **API Layer:** Public read endpoints, Admin write endpoints, Auth (Login/Logout) | 4–5 days |
| **5** | **Public Frontend:** Photo grid layout + Collection filter components | 3–4 days |
| **6** | **Admin Frontend:** Dashboard login, photo list, upload & edit forms | 4–5 days |
| **7** | **Integration:** End-to-end testing and bug fixing | 1–2 days |