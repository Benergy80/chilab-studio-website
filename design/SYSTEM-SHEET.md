# ChiLab Studio System Sheet

## Route Map

| Route | Job | Layout Family | Shared Shell |
| --- | --- | --- | --- |
| `/` | Establish ChiLab as a high-skill material studio and route visitors into work, capabilities, or contact. | Editorial hero plus project ledger | Masthead, rail, numbered section system |
| `/work/` | Let architects, artists, designers, and collaborators scan projects by category. | Filtered index plus visual preview | Masthead, filter controls, project row system |
| `/work/<slug>.html` | Tell each project as a case study with materials, credits, images, and context. | Project article with rail metadata and image plates | Masthead, project rail, plate system |
| `/studio.html` | Explain the people, practice, and studio history. | Large title, prose, client rail | Masthead, rail, numbered section system |
| `/capabilities.html` | Show what the studio can actually do. | Capability ledger | Masthead, rail, list rows |
| `/pamphlets.html` | Let a visitor find and download a project pamphlet. | Download ledger | Masthead, rail, list rows |
| `/work/<slug>-pamphlet.html` | Give one project as a printable leave-behind. | Sheet document, US Letter portrait | Standalone. Viewer bar only, no masthead |
| `/news.html` | Collect recent work and press notes. | News ledger | Masthead, rail, list rows |
| `/contact.html` | Help a qualified visitor start a commission or collaboration. | Direct contact page | Masthead, rail, contact type scale |

## Component Inventory

| Component | Variants | States |
| --- | --- | --- |
| Text link | default, current, rail, large contact | default, hover, focus-visible, current |
| Button | filter only | default, hover, focus-visible, pressed |
| Work card | standard, feature | default, hover, focus-visible |
| Work row | index row | default, hover, focus-visible, hidden by filter |
| Rail section | default | default |
| Image plate | wide, main, half, feature | default |
| Pager | previous, next | default, hover, focus-visible |
| Download row | pamphlet index row | default, hover |
| Sheet | cover, text, plate, closing | print, screen |
| Plate slot | quad, stack-2, pair-tall, solo-wide, solo-tall, text band | default |

## State Rules

Focus-visible: black outline with offset, never removed.

Hover: underline text links or slightly shift image contrast. No movement-heavy effects.

Current: underlined nav link or active filter with ink color and underline.

Hidden filter result: set display none only on row/card records, not on parent layout.

## Pamphlet Sheets

Pamphlets are a separate document family, not a site page family. They reuse the
site's tokens and Inter Tight but carry no masthead, no theme toggle, and no
dark mode: they are printed.

Rules:

- US Letter portrait, `@page` margin zero, half-inch padding inside the sheet.
- Every sheet is a fixed 8.5 x 11 box with a running head and a running foot.
  Content never reflows across sheets.
- The five-column grid holds. Column 5 is still the rail.
- Plate slots have fixed aspect ratios and crop with `object-fit: cover`.
  Layout is chosen from the run of image orientations, so a sheet fills its page.
- The first plate rides the text sheet as a wide band. Plates are capped at
  `MAX_PLATES` in `build_pamphlets.py`; a pamphlet is a leave-behind, not the archive.

Adding a sheet type or plate slot requires updating this table first.
