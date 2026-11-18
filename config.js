/*
 * ============================================================
 *  FOXCREST PROPERTY MEDIA: SITE SETTINGS
 *  Edit this file to update contact info, prices and videos.
 *  No coding knowledge needed: just change the text in quotes.
 * ============================================================
 */
window.FOXCREST = {
  // ---- Contact details (shown on the site) ----
  email: "hello@foxcrestpropertymedia.com",
  phone: "(555) 555-5555",

  // ---- Where quote requests go ----
  // Leave empty ("") and the form opens the visitor's email app with the
  // request pre-filled, addressed to the email above.
  // For a smoother experience, create a free form at https://formspree.io,
  // then paste its endpoint here, e.g. "https://formspree.io/f/abcdwxyz".
  formEndpoint: "",

  // ---- Prices (used by the live estimate on the quote form) ----
  prices: {
    walkthrough: 300,
    campaignFirstMonth: 800,
    campaignMonthly: 1000,
  },

  // ---- Example walkthroughs ----
  // type: "house", "condo" or "land" (used by the filter buttons)
  // video: a YouTube or Vimeo link, or a path to an .mp4 file in /videos.
  //        Leave empty ("") to show a "coming soon" card.
  // thumbnail: optional image path. YouTube thumbnails are fetched automatically.
  portfolio: [
    {
      title: "Modern Family Home",
      details: "4 bed · 3 bath · 2,400 sq ft",
      location: "Maple Ridge",
      type: "house",
      video: "",
      thumbnail: "",
    },
    {
      title: "Downtown Loft",
      details: "2 bed · 2 bath · 1,150 sq ft",
      location: "City Centre",
      type: "condo",
      video: "",
      thumbnail: "",
    },
    {
      title: "Lakeside Cottage",
      details: "3 bed · 2 bath · waterfront",
      location: "Pine Lake",
      type: "house",
      video: "",
      thumbnail: "",
    },
    {
      title: "Starter Townhome",
      details: "3 bed · 1.5 bath · 1,400 sq ft",
      location: "Westfield",
      type: "condo",
      video: "",
      thumbnail: "",
    },
    {
      title: "Country Acreage",
      details: "5 acres · barn · 3 bed home",
      location: "Foxcrest Valley",
      type: "land",
      video: "",
      thumbnail: "",
    },
    {
      title: "Craftsman Bungalow",
      details: "2 bed · 1 bath · renovated",
      location: "Old Town",
      type: "house",
      video: "",
      thumbnail: "",
    },
  ],
};
