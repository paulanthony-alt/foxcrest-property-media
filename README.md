# Foxcrest Property Media website

A simple static website (plain HTML/CSS/JS, no build step). It has a portfolio of walkthrough videos, pricing, a "how it works" section, and a quote form that shows a live price estimate.

## Preview locally

Open `index.html` in a browser, or run:

```bash
python3 -m http.server 8000
```

then visit http://localhost:8000.

## Updating content: edit `config.js`

Almost everything the owner will want to change is in **`config.js`**:

| Setting | What it does |
|---|---|
| `email`, `phone` | Contact details shown on the site |
| `formEndpoint` | Where quote requests are sent (see below) |
| `prices` | Prices used by the live estimate ($300 / $800 / $1,000) |
| `portfolio` | The example walkthrough cards |

### Adding a walkthrough video

Add or edit an entry in `portfolio`:

```js
{
  title: "Modern Family Home",
  details: "4 bed · 3 bath · 2,400 sq ft",
  location: "Maple Ridge",
  type: "house",            // "house", "condo" or "land"
  video: "https://www.youtube.com/watch?v=XXXXXXXXXXX",
  thumbnail: "",            // optional; YouTube thumbnails load automatically
}
```

`video` can be a YouTube link, a Vimeo link, or an `.mp4` file placed in `videos/` (e.g. `"videos/maple-ridge.mp4"`). Cards with no video show "Video coming soon". The six cards there now are **placeholders**: replace them with real work.

> Prices on the pricing cards are written directly in `index.html` (search for `$300`, `$800`, `$1,000`). Update both there and in `config.js` if prices change.

## Receiving quote requests

- **Default (no setup):** the form opens the visitor's email app with the request pre-filled to `email`.
- **Recommended:** create a free form at [formspree.io](https://formspree.io), paste the endpoint (like `https://formspree.io/f/abcdwxyz`) into `formEndpoint`, and requests arrive in your inbox directly, without the visitor needing an email app.

## Publishing

Any static host works. Free options: GitHub Pages (Settings → Pages → deploy from branch), Netlify, or Cloudflare Pages. Just upload the folder; there is nothing to build.

## Before going live

- [ ] Replace the placeholder email and phone in `config.js`
- [ ] Replace the placeholder portfolio entries with real videos
- [ ] Set up `formEndpoint` (optional but recommended)
