# RAG Search Documentation App

A documentation search application built with Nuxt 3 that uses RAG (Retrieval Augmented Generation) with Google's Gemini AI for intelligent documentation search and responses.

## Features

- 🔐 Authentication
- 🔍 Smart documentation search powered by Gemini AI
- 💻 Code syntax highlighting
- 🎨 Tailwind CSS styling with Typography plugin
- 🚀 Server-side rendering with Nuxt 3

## Prerequisites

- Node.js
- PostgreSQL database
- Google Cloud API key for Gemini AI

## Environment Setup

Create a `.env` file based on [.env.example](.env.example):

```bash
NUXT_DB_URI="your-postgres-connection-string"
NUXT_GEMINI="your-gemini-api-key"
```

## Installation

```bash
# Install dependencies
npm install
```

## Development

```bash
# Start development server
npm run dev
```

The application will be available at `http://localhost:3000`

## Production

```bash
# Build for production
npm run build

# Start production server
npm run preview
```

## Technologies Used

- [Nuxt 3](https://nuxt.com)
- [Lucia Auth](https://lucia-auth.com)
- [Google Generative AI](https://ai.google.dev/)
- [TailwindCSS](https://tailwindcss.com)
- [PostgreSQL](https://postgresql.org)

## License

MIT License
