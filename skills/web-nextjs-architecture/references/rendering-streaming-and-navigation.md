# Rendering, streaming, and navigation

Model initial load, full reload, direct deep link, soft route transition, browser
back/forward, refresh, and recovery separately. Next.js can serve HTML, a React
Server Component payload, and client JavaScript at different stages.

## Shape the rendering path

- Start independent data work eagerly and await it in parallel when ordering is
  not required. A sequential `await` chain is a waterfall unless one result is
  a real dependency of the next request.
- Use `loading` for an instant segment-level state and Suspense nearer to slow or
  request-time work when a whole segment fallback would hide useful content.
- Keep fallback UI meaningful, accessible, and structurally compatible with the
  resolved content. Streaming changes delivery order, not business correctness.
- Place `error` and `global-error` boundaries at recoverable ownership seams.
  Keep expected application failures distinct from unexpected exceptions and
  use `not-found` for the verified absence of a resource.
- Account for layouts that persist across a route transition. Do not assume
  layout code reruns or shared client state resets on navigation.
- Evaluate prefetch behavior against route dynamism, user intent, bandwidth,
  authorization, and server cost. Do not describe prefetch as a universal win.

Verify the route transition as well as the direct URL. Cover loading, partial
stream completion, thrown error, retry or reset, not-found, cancellation, stale
client state, and hydration. Inspect the production build because development
rendering and caching behavior are not production evidence.

## Primary sources

- [Fetching data and streaming](https://nextjs.org/docs/app/getting-started/fetching-data)
- [Linking and navigating](https://nextjs.org/docs/app/getting-started/linking-and-navigating)
- [Error handling](https://nextjs.org/docs/app/getting-started/error-handling)
- [`loading.js`](https://nextjs.org/docs/app/api-reference/file-conventions/loading)
