# School Communication & Helpdesk OS — Frontend

Next.js (App Router) frontend for the School Helpdesk. Mobile-first; wired to the backend API.

## How to run

From the **repository root** (or from `frontend/`):

```bash
cd frontend
npm install    # required first time and after dependency changes
npm run dev
```

Open [http://localhost:3000](http://localhost:3000). The app calls the backend at **http://localhost:8000** by default. Start the backend first with `docker compose up --build` from the repo root; see [docs/RUNNING.md](../docs/RUNNING.md) for full instructions and troubleshooting.

## Structure

- `app/` — routes and layouts
- `components/` — reusable UI
- `lib/` — utilities
- `services/` — API client
- `styles/` — CSS modules

See `todo.md` in this folder for the frontend checklist.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
