# Deployment Plan

## Overview
This document outlines the production deployment configuration for the Task Web App monorepo, targeting cloud deployment platforms (Vercel for frontend, cloud provider for backend).

---

## Backend Production Configuration

### FastAPI Server Settings
- **Host:** `0.0.0.0` (required for cloud container environments)
- **Port:** `8000` (or `$PORT` environment variable)
- **CORS Origins:** Must be configured via `ALLOWED_ORIGINS` environment variable
  - Format: Comma-separated list of allowed frontend URLs
  - Example: `ALLOWED_ORIGINS=https://your-app.vercel.app,https://www.yourdomain.com`

### Environment Variables
```bash
# Required
DATABASE_URL=postgresql://user:pass@host:5432/dbname
BETTER_AUTH_SECRET=<generate-secure-random-string>
BETTER_AUTH_URL=https://your-backend-domain.com
OPENAI_API_KEY=sk-proj-...

# Optional (with sensible defaults)
PORT=8000
ALLOWED_ORIGINS=<comma-separated-frontend-urls>
ENVIRONMENT=production
```

### Deployment Platforms
- **Recommended:** Railway, Render, Fly.io, or AWS ECS
- **Docker Required:** Use the provided `backend/Dockerfile`
- **Database:** PostgreSQL (managed service like Supabase, Neon, or RDS)

---

## Frontend Production Configuration

### Next.js Build Settings
- **Build Command:** `npm run build` (in frontend directory)
- **Output Directory:** `frontend/.next`
- **Node Version:** 18+ (specified in package.json engines)

### Environment Variables
```bash
# Required for backend API communication
NEXT_PUBLIC_API_URL=https://your-backend-domain.com

# Optional
NODE_ENV=production
```

### Deployment Platform
- **Primary:** Vercel (recommended for Next.js)
- **Alternative:** Netlify, Cloudflare Pages

#### Vercel Configuration
- **Framework Preset:** Next.js
- **Root Directory:** `frontend`
- **Install Command:** `npm install`
- **Build Command:** `npm run build`
- **Output Directory:** `.next`
- **Environment Variables:** Must set `NEXT_PUBLIC_API_URL` in Vercel dashboard

---

## Environment Checklist

### Required Keys for Cloud Deployment

| Variable Name | Description | Backend | Frontend | Example/Format |
|--------------|-------------|---------|----------|----------------|
| `DATABASE_URL` | PostgreSQL connection string | ✓ | ✗ | `postgresql://user:pass@host:5432/dbname` |
| `BETTER_AUTH_SECRET` | Authentication secret key | ✓ | ✗ | Generate: `openssl rand -base64 32` |
| `BETTER_AUTH_URL` | Backend URL for auth cookies | ✓ | ✗ | `https://api.yourapp.com` |
| `OPENAI_API_KEY` | OpenAI API access | ✓ | ✗ | `sk-proj-...` |
| `ALLOWED_ORIGINS` | Frontend domains for CORS | ✓ | ✗ | `https://app.vercel.app,https://app.com` |
| `NEXT_PUBLIC_API_URL` | Backend API base URL | ✗ | ✓ | `https://api.yourapp.com` |
| `PORT` | Server port (backend) | ✓ | ✗ | `8000` or `$PORT` |
| `ENVIRONMENT` | Environment indicator | ✓ | ✗ | `production` |

### Security Notes
- **Never commit `.env` files to git** - add to `.gitignore`
- Use platform secret management (Vercel env vars, Railway secrets, etc.)
- Generate strong random secrets for `BETTER_AUTH_SECRET`
- Restrict `OPENAI_API_KEY` with usage limits
- Ensure `ALLOWED_ORIGINS` only includes your actual frontend domains

---

## Deployment Workflow

### 1. Backend Deployment
```bash
# Example for Railway
railway login
railway init
railway variables set DATABASE_URL="..."
railway variables set BETTER_AUTH_SECRET="..."
railway variables set OPENAI_API_KEY="..."
railway variables set ALLOWED_ORIGINS="https://your-frontend.vercel.app"
railway up
```

### 2. Frontend Deployment (Vercel)
```bash
# Via Vercel CLI
vercel login
vercel --prod
# Set NEXT_PUBLIC_API_URL in Vercel dashboard
```

### 3. Testing Production
- Verify backend health: `https://your-backend.com/health`
- Verify frontend loads and connects to backend
- Test authentication flow
- Test AI chat functionality
- Verify task CRUD operations

---

## Monitoring & Maintenance

### Backend Health Checks
- Add `/health` endpoint for load balancer health checks
- Monitor database connection pool
- Track OpenAI API usage and costs

### Frontend Monitoring
- Check Vercel analytics for performance
- Monitor API error rates in browser console
- Verify authentication persistence

### Database Maintenance
- Regular backups (automated via cloud provider)
- Monitor connection limits
- Clean up old data as needed

---

## Rollback Plan

### Backend
- Use platform rollback features (Railway, Render, etc.)
- Keep previous container images available
- Maintain database migration reversibility

### Frontend
- Vercel provides instant rollbacks via dashboard
- Each deployment is versioned and can be reverted

---

## Cost Considerations

### Backend
- **Compute:** ~$5-20/month (depending on platform and usage)
- **Database:** ~$5-15/month (managed PostgreSQL)
- **OpenAI API:** Variable based on usage

### Frontend (Vercel)
- **Hobby Tier:** Free for personal projects
- **Pro Tier:** $20/month per seat
- **Additional:** Bandwidth overages may apply

---

## Support Contacts

- **Backend Issues:** Check logs in deployment platform dashboard
- **Frontend Issues:** Vercel deployment logs + browser console
- **Database:** Managed provider support (Supabase, Neon, etc.)
- **AI Features:** OpenAI status page and API monitoring

---

**Document Version:** 1.0
**Last Updated:** 2025-01-21
**Next Review:** Before production deployment
