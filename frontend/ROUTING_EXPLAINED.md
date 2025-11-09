# 🎯 What Determines Which Component Shows at `/`?

## Simple Answer

**The route definition in `App.tsx` determines what shows at `/`.**

Currently, line 14 in `App.tsx`:
```tsx
<Route path="/" element={<LandingPage />} />
```

This means: **`/` always shows `LandingPage`**, regardless of:
- Whether you're running locally or deployed
- What environment you're in
- Any other conditions

---

## Current Code

```tsx
// frontend/src/App.tsx
<Routes>
  <Route path="/" element={<LandingPage />} />      // ← This line determines / 
  <Route path="/app" element={<Home />} />
  <Route path="/saved" element={<SavedMoodboards />} />
  <Route path="/privacy" element={<PrivacyPolicy />} />
</Routes>
```

**Result:** 
- Visit `/` → Always shows `LandingPage`
- Visit `/app` → Always shows `Home`
- Visit `/saved` → Always shows `SavedMoodboards`

---

## How to Make It Environment-Based

If you want **different behavior** for local vs deployed, you need to add **conditional logic**:

### Option 1: Environment Variable Check

```tsx
const App: React.FC = () => {
  // Check if we're in production
  const isProduction = process.env.NODE_ENV === 'production';
  // OR check a custom env variable
  const showMainApp = process.env.REACT_APP_SHOW_MAIN_APP === 'true';
  
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Conditional routing */}
          <Route 
            path="/" 
            element={showMainApp ? <Home /> : <LandingPage />} 
          />
          <Route path="/app" element={<Home />} />
          <Route path="/saved" element={<SavedMoodboards />} />
          <Route path="/privacy" element={<PrivacyPolicy />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
};
```

### Option 2: URL-Based Check

```tsx
const App: React.FC = () => {
  // Check if we're on the production domain
  const isProductionDomain = window.location.hostname === 'mooreamood.com';
  
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route 
            path="/" 
            element={isProductionDomain ? <Home /> : <LandingPage />} 
          />
          {/* ... other routes */}
        </Routes>
      </Router>
    </AuthProvider>
  );
};
```

---

## Current Behavior (No Conditions)

**Right now, there are NO conditions.** The route is **hardcoded**:

```
/ → LandingPage (always, everywhere)
```

This means:
- ✅ Local: `http://localhost:3000/` → LandingPage
- ✅ Deployed: `https://mooreamood.com/` → LandingPage
- ✅ Both are identical

---

## To Change It

**If you want `/` to show different content:**

1. **Change the route definition** in `App.tsx`
2. **Add conditional logic** (if you want different behavior for local vs deployed)
3. **Or simply swap the components**:
   ```tsx
   <Route path="/" element={<Home />} />  // Main app at /
   <Route path="/waitlist" element={<LandingPage />} />  // Waitlist at /waitlist
   ```

---

## Summary

**What determines `/`?**
- ✅ The `<Route path="/" element={...} />` definition in `App.tsx`
- ❌ NOT environment variables (currently)
- ❌ NOT deployment location (currently)
- ❌ NOT any conditions (currently)

**It's simply hardcoded to show `LandingPage`.**

