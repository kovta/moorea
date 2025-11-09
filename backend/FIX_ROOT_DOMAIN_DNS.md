# Fix Root Domain DNS Configuration

## Problem
`mooreamood.com` shows "Invalid Configuration" in Vercel, while `www.mooreamood.com` works fine.

## Solution: Configure DNS in Cloudflare

### Step 1: Get Vercel's DNS Configuration
1. In Vercel, click on the `mooreamood.com` domain (the one showing "Invalid Configuration")
2. Look for DNS instructions or click "View DNS Records"
3. You should see something like:
   - **Type**: A or ALIAS
   - **Name**: `@` (or blank for root domain)
   - **Value**: Vercel's IP addresses or hostname

### Step 2: Configure in Cloudflare

#### Option A: Use ALIAS Record (Recommended)
1. Go to Cloudflare Dashboard → Your Domain → DNS → Records
2. **Delete** any existing A or CNAME record for `mooreamood.com` (root domain)
3. Click **"Add record"**
4. Configure:
   - **Type**: `ALIAS` (or `CNAME` if ALIAS not available)
   - **Name**: `@` (represents root domain)
   - **Target**: `cname.vercel-dns.com` (or the value Vercel shows you)
   - **Proxy status**: **DNS only** (gray cloud ☁️, NOT orange)
   - **TTL**: Auto
5. Click **"Save"**

#### Option B: Use A Records (If ALIAS not available)
1. In Vercel, check what IP addresses they provide for the root domain
2. In Cloudflare, add **multiple A records**:
   - **Type**: `A`
   - **Name**: `@`
   - **IPv4 address**: `76.76.21.21` (Vercel's IP - check Vercel dashboard for exact IPs)
   - **Proxy status**: **DNS only** (gray cloud)
   - **TTL**: Auto
3. Add 2-4 A records if Vercel provides multiple IPs

### Step 3: Verify Configuration

#### Current Setup Should Be:
```
Type    Name    Content                          Proxy
----    ----    -------                          -----
ALIAS   @       cname.vercel-dns.com             DNS only (gray)
CNAME   www     mooreamood.vercel.app            DNS only (gray)
```

**OR** (if using A records):
```
Type    Name    Content                          Proxy
----    ----    -------                          -----
A       @       76.76.21.21                      DNS only (gray)
A       @       76.76.21.22                      DNS only (gray)
CNAME   www     mooreamood.vercel.app            DNS only (gray)
```

### Step 4: Wait for DNS Propagation
- DNS changes can take **5-60 minutes** to propagate
- Cloudflare usually updates within 1-2 minutes
- Check status in Vercel dashboard

### Step 5: Verify in Vercel
1. Go back to Vercel → Domains
2. Click "Refresh" next to `mooreamood.com`
3. Wait 1-2 minutes
4. The status should change from "Invalid Configuration" to "Valid Configuration" ✅

## Troubleshooting

### If Still Invalid After 10 Minutes:

1. **Check DNS Propagation:**
   ```bash
   # In terminal, check if DNS is resolving:
   dig mooreamood.com
   # Should show Vercel's IP addresses
   ```

2. **Verify Proxy Status:**
   - Make sure ALL records have **gray cloud** (DNS only)
   - NOT orange cloud (proxied)

3. **Check for Conflicting Records:**
   - Delete any duplicate A, CNAME, or ALIAS records for root domain
   - Only ONE record should exist for `@` (root domain)

4. **Contact Vercel Support:**
   - If still not working after 30 minutes
   - They can check their DNS verification on their end

## Common Mistakes to Avoid

❌ **Don't use CNAME for root domain** (if your DNS provider doesn't support ALIAS)
- Some providers don't allow CNAME on root domain
- Use A records instead

❌ **Don't proxy the root domain** (orange cloud)
- Must be DNS only (gray cloud) for Vercel

❌ **Don't have multiple conflicting records**
- Only one record type for root domain

✅ **Do use ALIAS if available** (best option)
✅ **Do use A records if ALIAS not available**
✅ **Do keep www as CNAME** (this is working fine)

