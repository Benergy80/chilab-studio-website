# ChiLab Studio System Sheet

## Route Map

| Route | Job | Layout Family | Shared Shell |
| --- | --- | --- | --- |
| `/` | Establish ChiLab as a high-skill material studio and route visitors into work, capabilities, or contact. | Editorial hero plus project ledger | Masthead, rail, numbered section system |
| `/work/` | Let architects, artists, designers, and collaborators scan projects by category. | Filtered index plus visual preview | Masthead, filter controls, project row system |
| `/work/<slug>.html` | Tell each project as a case study with materials, credits, images, and context. | Project article with rail metadata and image plates | Masthead, project rail, plate system |
| `/studio.html` | Explain the people, practice, and studio history. | Large title, prose, client rail | Masthead, rail, numbered section system |
| `/capabilities.html` | Show what the studio can actually do. | Capability ledger | Masthead, rail, list rows |
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

## State Rules

Focus-visible: black outline with offset, never removed.

Hover: underline text links or slightly shift image contrast. No movement-heavy effects.

Current: underlined nav link or active filter with ink color and underline.

Hidden filter result: set display none only on row/card records, not on parent layout.
