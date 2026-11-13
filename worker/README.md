# JARVIS public AI backend

The public GitHub Pages demo can use Cloudflare Workers AI for open-ended chat. The backend source is in this folder; it is separate from the local Python/Ollama assistant.

## One-time setup

1. Create a Cloudflare account and enable Workers AI for the account.
2. Create an API token with permission to deploy Workers and use Workers AI.
3. In GitHub, open **Settings → Secrets and variables → Actions**.
4. Add these repository secrets:
   - `CLOUDFLARE_API_TOKEN`
   - `CLOUDFLARE_ACCOUNT_ID`
5. In the same page, open **Variables** and add:
   - `JARVIS_API_URL` = the deployed Worker URL, for example `https://jarvis-assistant-api.<your-workers-subdomain>.workers.dev`

## Deploy

Push a change under `worker/` or run **Actions → Deploy JARVIS AI Worker → Run workflow**. The workflow deploys `worker/index.js` using the AI binding in `wrangler.toml`.

After the first deployment, copy the exact `.workers.dev` URL shown in the deployment logs into the GitHub Actions variable `JARVIS_API_URL`. Then rerun **Deploy public demo to GitHub Pages** so the public page is built with that endpoint.

## Notes

- Never put the Cloudflare API token in source code or in the frontend.
- The public endpoint can consume your Workers AI quota. Review Cloudflare usage and configure appropriate limits before sharing the demo widely.
- The browser demo stores its sample tasks, notes and reminders in browser storage. The AI endpoint handles chat only; it does not connect to your local Python app, SQLite database, computer, or files.
- Microphone input depends on browser support and microphone permission.
