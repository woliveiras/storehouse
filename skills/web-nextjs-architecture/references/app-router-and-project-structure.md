# App Router and project structure

Use this reference after inspecting the installed Next.js version and the real
route tree. The App Router maps folders to URL segments, but a route becomes
public only when a `page` or `route` file exposes it.

## Separate three structures

Map these independently before proposing folders:

1. URL and navigation structure: static, dynamic, catch-all, and optional
   catch-all segments.
2. Rendering structure: root and nested `layout`, `template`, `loading`,
   `error`, `not-found`, and `default` files.
3. Business structure: capabilities, invariants, data ownership, and change
   patterns outside or colocated with framework adapters.

A route group can organize routes or select a layout without changing the URL.
A private folder can exclude implementation files from routing. Neither a
route group, private folder, segment, layout, nor top-level `lib` directory is
evidence of a bounded context.

## Use routing mechanisms deliberately

- Use nested layouts for genuinely shared UI and state continuity; account for
  their persistence across route transitions.
- Use parallel routes for independently navigable slots with explicit
  `default` behavior after a full reload.
- Use an intercepting route only when soft navigation should render a different
  presentation, such as a modal, while the canonical URL still supports direct
  navigation and refresh.
- Keep routing adapters thin when domain or application policy has its own
  stable boundary. Colocation is allowed, but locality must not create circular
  imports or make server-only code reachable from the client graph.
- Treat multiple root layouts and crossings between them as full-document
  navigation boundaries and verify the resulting behavior.

Do not impose one universal folder layout. Next.js deliberately permits code
inside or outside `app`, route-specific colocation, route groups, and private
folders. Choose from actual ownership, reuse, build direction, and team change
patterns, then protect the chosen dependency rules mechanically where useful.

## Primary sources

- [Project structure and organization](https://nextjs.org/docs/app/getting-started/project-structure)
- [Layouts and pages](https://nextjs.org/docs/app/getting-started/layouts-and-pages)
- [Parallel routes](https://nextjs.org/docs/app/api-reference/file-conventions/parallel-routes)
- [Intercepting routes](https://nextjs.org/docs/app/api-reference/file-conventions/intercepting-routes)
