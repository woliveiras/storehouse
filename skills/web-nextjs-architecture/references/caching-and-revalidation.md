# Caching and revalidation

Inspect the exact Next.js version and `cacheComponents` flag before selecting a
cache API. Next.js 16 introduced the Cache Components model, while applications
without it can use the previous model. Do not combine their defaults or route
configuration assumptions.

## Cache Components model

With Cache Components enabled, compose static, cached, and request-time content
inside one route. Use `use cache` only for results that can be safely reused.
Define freshness with `cacheLife`, associate invalidation domains with
`cacheTag`, and select `updateTag`, `revalidateTag`, or `revalidatePath` from the
required read-after-write and propagation behavior.

Keep request-time or personalized data outside a shared cache unless identity,
tenant, authorization, locale, and other relevant inputs are deliberately part
of the cache key. Put uncached work behind an appropriate Suspense boundary.

## Previous model

Without Cache Components, inspect `fetch` cache options, route segment config,
`unstable_cache`, revalidation times, tags, and path invalidation as one model.
Do not infer production caching from development, where routes can behave
differently. Use the official migration guide before replacing `dynamic`,
`revalidate`, or `fetchCache` behavior.

## Consistency and topology

For every cache, record owner, key inputs, value, authorization scope, maximum
staleness, invalidation trigger, failure behavior, observability, and deletion
or rollback. Verify concurrent mutation, failure after commit, retry, and stale
navigation behavior. In a multi-instance or multi-region deployment, determine
whether cached values and invalidations are shared by the adapter; local memory
or filesystem is not automatically coherent.

## Primary sources

- [Cache Components](https://nextjs.org/docs/app/getting-started/partial-prerendering)
- [Revalidating cached data](https://nextjs.org/docs/app/getting-started/revalidating)
- [Caching and revalidating: previous model](https://nextjs.org/docs/app/guides/caching-without-cache-components)
- [Migrating to Cache Components](https://nextjs.org/docs/app/guides/migrating-to-cache-components)
