# Environment Secrets for Cloud Deployment

This document lists all environment variables that must be manually configured in cloud platforms (Vercel and Railway) based on local development files.

## Vercel (Frontend) Environment Variables

Set these in the Vercel dashboard under your project's Environment Variables section.

### Required for Frontend Only:

```
NEXT_PUBLIC_API_URL=[Backend Live URL from Railway]
```

**Value Source:** Check your backend deployment (Railway) and use the live API URL (e.g., `https://your-app.up.railway.app`)

**Purpose:** Allows the Next.js frontend to communicate with the FastAPI backend

---

## Railway (Backend) Environment Variables

Set these in the Railway dashboard under your project's Variables section.

### Required Backend Variables:

#### 1. DATABASE_URL
```
DATABASE_URL=[Your PostgreSQL Connection String]
```

**Value Sources:**
- **Local/dev:** `sqlite:///./database.db` (SQLite)
- **Production:** Get from PostgreSQL provider (Supabase, Neon, AWS RDS)
- **Format:** `postgresql://user:password@host:port/database_name`

**Purpose:** Database connection for storing users, tasks, and chat history

---

#### 2. BETTER_AUTH_SECRET
```
BETTER_AUTH_SECRET=[Generate New Secret]
```

**How to Generate:**
```bash
# Run this command in terminal
openssl rand -base64 32
```

**Purpose:** Secret key used for JWT token signing and encryption

**Security Notes:**
- **Never reuse** the development secret from .env.local
- **Do not commit** this secret to Git
- **Use different secrets** for production vs staging vs development
- **Required length:** 32+ characters recommended

---

#### 3. BETTER_AUTH_URL
```
BETTER_AUTH_URL=[Railway Backend Live URL]
```

**Value Source:** Use the same URL as your Railway deployment
- Example: `https://your-app.up.railway.app`

**Purpose:** Used for cookie domain settings and redirect URLs

---

#### 4. OPENAI_API_KEY (or OPENROUTER_API_KEY)
```
OPENAI_API_KEY=sk-proj-...
# OR if using OpenRouter:
OPENROUTER_API_KEY=sk-or-v1-...
```

**Value Source:**
- **OpenAI:** https://platform.openai.com/api-keys
- **OpenRouter:** https://openrouter.ai/keys

**Purpose:** Enables AI chat functionality in the application

**Critical Security Setting:**
- Add **spending limits** to your OpenAI/OpenRouter account
- Monitor usage in your OpenAI/OpenRouter dashboard
- Use OpenRouter if you want alternative models (Anthropic, etc.)

---

#### 5. ALLOWED_ORIGINS
```
ALLOWED_ORIGINS=[Vercel Frontend URL]
```

**Value Format:**
- Single URL: `https://your-app.vercel.app`
- Multiple URLs (comma-separated): `https://staging.vercel.app,https://prod.vercel.app`
- Remove trailing slashes

**Value Source:** Your Vercel deployment URL (found in Vercel dashboard)

**Purpose:** CORS policy to allow frontend to access backend API

**Common Mistake:**
- ❌ Wrong: `https://your-app.vercel.app/`
- ✅ Correct: `https://your-app.vercel.app`

---

#### 6. OPENROUTER_BASE_URL (if using OpenRouter)
```
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

**Default Value:** `https://openrouter.ai/api/v1`

**Purpose:** API endpoint for OpenRouter integration

---

#### 7. PORT (Optional)
```
PORT=8000
```

**Default Value:** `8000` (or Railway will auto-assign via $PORT variable)

**Purpose:** Port for FastAPI server to listen on

---

#### 8. ENVIRONMENT
```
ENVIRONMENT=production
```

**Values:** `production`, `staging`, `development`

**Purpose:** Application environment indicator for logging and feature flags

---

## Variable Entry Instructions

### For Vercel (Frontend):

1. Go to vercel.com and select your project
2. Navigate to Settings → Environment Variables
3. Add:
   - Name: `NEXT_PUBLIC_API_URL`
   - Value: `[Your Railway Backend URL]`
   - Environment: Production (and Preview if you have staging)
4. Click **Save**
5. Redeploy your frontend for changes to take effect

### For Railway (Backend):

1. Go to railway.app and select your project
2. Navigate to Variables
3. Add each variable from the list above
4. Click **Deploy** after all variables are set
5. Wait for deployment to complete and note the live URL
6. Return to Vercel and update `NEXT_PUBLIC_API_URL` with this URL
7. Redeploy Vercel frontend

---

## Secret Management Best Practices

### ⚠️ Critical Security Rules:

1. **Never commit secrets** - Use environment variables only
2. **Use different secrets** for each environment (dev/staging/prod)
3. **Rotate secrets** regularly (quarterly recommended)
4. **Generate new secrets** for each deployment environment
5. **Don't reuse** development secrets in production
6. **Monitor API usage** to prevent unexpected costs
7. **Use platform secret management** (not .env files)

### Platform-Specific Notes:

**Vercel:**
- Variables prefixed with `NEXT_PUBLIC_` are exposed to browser
- Only use `NEXT_PUBLIC_` prefix for non-sensitive, client-side values
- Regular variables stay on server only

**Railway:**
- Variables marked as "Shared" apply to all environments
- Use environment-specific variables for different deployment types
- Toggle "Add to Service Domains" for domain-based variables

---

## Troubleshooting

### If authentication fails:
- Verify `BETTER_AUTH_SECRET` is set and matches between calls
- Ensure `BETTER_AUTH_URL` matches your backend URL exactly
- Check that `ALLOWED_ORIGINS` includes your frontend URL

### If AI chat doesn't work:
- Verify `OPENAI_API_KEY` or `OPENROUTER_API_KEY` is set
- Check API key has sufficient credits/balance
- Review backend logs for API errors

### If database connection fails:
- Verify `DATABASE_URL` format is correct
- Ensure database is accessible (not IP-restricted)
- Check SSL requirements for managed databases

### If CORS errors appear:
- Verify `ALLOWED_ORIGINS` is set correctly
- Ensure no trailing slashes in URLs
- Check that protocol (http/https) matches

---

## Environment Variable Validation

After deployment, test the following:

1. **Backend Health:** `GET /health` → Should return 200
2. **Auth Flow:** Register → Login → Access protected routes
3. **AI Chat:** Send message → Get response from AI
4. **Task CRUD:** Create, read, update, delete tasks
5. **Database:** Verify data persists across restarts

---

**Document Version:** 1.0
**Last Updated:** 2025-01-21
**Platforms:** Vercel (Frontend) + Railway (Backend)
