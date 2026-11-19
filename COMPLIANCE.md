# Compliance checklist

What the site does to keep privacy, accessibility and licensing in order: what's **done**, what's **not needed yet**, and **what change would make it needed**. Check the "Not needed yet" section before adding any new script, form, embed or tool.

_Not legal advice. Have an attorney review `terms.html` and `privacy.html` before launch._

## Done

| Item | How it's handled | Where |
|---|---|---|
| **Form consent** | The quote form has a required checkbox agreeing to the Terms and Privacy Policy and to being contacted about the request. The time of agreement is included with the request. | `index.html` (quote form), `script.js` |
| **Data minimization** | Only name and email are required. Phone and address are marked optional and say why they're asked for. No hidden fields, fingerprinting or tracking IDs. Unbooked requests are deleted after 12 months (Privacy Policy). | `index.html`, `privacy.html` |
| **Third-party audit** | The page loads **zero** third-party resources on page view, so no cookies, no Google Fonts, no analytics. YouTube/Vimeo load only after a visitor presses play (YouTube privacy-enhanced mode, Vimeo `dnt=1`). Auto-loading YouTube thumbnails is **off** by default (`autoYouTubeThumbnails: false`). | `script.js`, `config.js` |
| **Data deletion** | The Privacy Policy has a "Your choices and rights" section with an "Email a deletion request" button (pre-filled subject). It's linked from every page footer as "Privacy choices & data deletion". | `privacy.html#your-rights` |
| **Do Not Sell / Share** | The Privacy Policy states we don't sell or share data for targeted ads, and that Global Privacy Control signals are honored. There are no ad trackers, so there's nothing to opt out of. | `privacy.html` |
| **Alt text & contrast** | Decorative images and icons are hidden from screen readers. Video cards have descriptive labels. Custom thumbnails get alt text (`thumbnailAlt` in config, defaults to the title). All text meets WCAG AA contrast (darker orange `#b04e1f` for buttons). | `styles.css`, `script.js` |
| **Keyboard navigation** | Skip link, visible focus outlines, real `<button>`s for cards and filters (`aria-pressed`). The mobile menu closes with Esc. The video dialog closes with Esc and returns focus to the card. All four pages pass an automated **axe WCAG 2.1 AA** scan. | all pages |
| **Licensed assets** | See the asset inventory below. Everything is original or open-licensed. | `assets/` |
| **No secrets in code** | The site has no API keys or tokens. The Formspree endpoint (if added) is public by design and isn't a secret. `.gitignore` blocks `.env` and key files. | `.gitignore` |

## Not needed yet: add when the trigger happens

| Item | Why not now | Add it when… | What to add |
|---|---|---|---|
| **Cookie consent banner** | The site sets no cookies and loads no trackers before a visitor chooses to play a video. | …you add **analytics** (Google Analytics, Meta Pixel, Hotjar, etc.), **ad/retargeting pixels**, a **chat widget**, turn on `autoYouTubeThumbnails`, or embed anything (maps, calendars, reviews) that loads on page view. | Opt-in banner that blocks those scripts until "Accept". "Reject" must be as easy as "Accept". Link to change choices in the footer. Update the Privacy Policy's Cookies section. _Cookieless tools like Cloudflare Web Analytics usually don't need a banner, but still update the policy._ |
| **"Do Not Sell or Share" opt-out link** | Nothing is sold or shared. Laws like California's CCPA also only apply above revenue or volume thresholds (e.g. >$25M revenue or 100k+ consumers). | …you add **ad pixels / retargeting**, upload client lists to ad platforms ("custom audiences"), sell or swap leads, or the business grows past state-law thresholds. | "Your Privacy Choices / Do Not Sell or Share" link in the footer, an opt-out mechanism, and honoring GPC in code (not just in the policy). |
| **Separate marketing-email opt-in** | The form is only used to reply to that request. There's no newsletter. | …you start a **newsletter** or send promotions. | An **unticked**, optional "Send me tips and offers" checkbox, separate from the required one. An unsubscribe link in every email (CAN-SPAM). |
| **SMS / text consent** | Replying by hand to someone who asked for a quote is fine. | …you send **automated or marketing texts**. | An explicit, unticked SMS checkbox with "Msg & data rates may apply, reply STOP to opt out" (TCPA / A2P 10DLC). |
| **Self-serve deletion form** | Email requests are enough at this size. | …the business gets frequent requests, or adds accounts (e.g. the agent portal). | A request form or a delete button in the account. Log requests and completion dates. |
| **Captions on videos** | There are no real videos yet. | …real walkthroughs are posted. | Captions (YouTube auto-captions, then correct them). The Accessibility page already promises this. Ideas PDF item F7. |
| **Server-side secrets** | There's no server code. | …you add the GitHub-issues inbox (C1), payments (D3), or any API. | Keep tokens in the host's secret store (e.g. Cloudflare Worker secrets), **never** in `config.js`, HTML or the repo. |
| **Photo / music licenses** | The site uses only original SVGs and no stock photos or music. | …you add **stock photos**, **background music** in videos, or third-party footage. | Keep license receipts in `assets/LICENSES.md`. Use royalty-free music licensed for commercial use. Get written permission from the property owner or agent for every published walkthrough. |
| **Drone footage** | It isn't mentioned on the site. | …you offer aerial shots. | An FAA Part 107 license, a mention in the Terms, and checks on local airspace rules. |

## Asset inventory

| Asset | Source | License |
|---|---|---|
| `assets/logo*.svg`, `assets/favicon.svg`, everything in `brand/` | Original fox-crest mark and wordmark made for Foxcrest (the wordmark is drawn from the Fraunces/Inter fonts, which OFL permits) | Owned by Foxcrest Property Media |
| Icons (inline SVG in `index.html`) | Hand-drawn for this site | Owned by Foxcrest Property Media |
| `assets/fonts/inter-*.woff2` | Inter, via Fontsource | SIL Open Font License 1.1 (`assets/fonts/LICENSE-Inter.txt`) |
| `assets/fonts/fraunces-*.woff2` | Fraunces, via Fontsource | SIL Open Font License 1.1 (`assets/fonts/LICENSE-Fraunces.txt`) |
| Walkthrough videos and thumbnails | Filmed by Foxcrest | Owned by Foxcrest. Published with the property owner's or agent's permission (Terms §2 and §4) |

## Before adding anything new, ask

1. Does it load anything from another company's servers before the visitor clicks something? → It probably needs consent. See the cookie banner row.
2. Does it collect a new piece of personal data? → Is it really needed? Add it to the Privacy Policy.
3. Does it need a key or token? → It must live on a server, never in this repo.
4. Is it someone else's image, font, music or code? → Check the license and add it to the inventory above.
