# jeetaklb.com source

This branch holds the source of the landing page. The `main` branch holds the
built files that GitHub Pages serves at https://jeetaklb.com.

## Change the store links only

The links live at the top of the script in `index.html` on `main`. Search for
`STORE_LINKS` and paste each link between the quotes:

```js
var STORE_LINKS = {
  customer: { ios: "", android: "" },  // Jeetak customer app
  vendor:   { ios: "", android: "" },  // vendor app for restaurants and shops
  driver:   { ios: "", android: "" }   // driver app
};
```

A store badge stays hidden while its link is empty and appears as soon as the link
is filled in. Change the same lines in `src/script.js` on this branch so the next
build keeps them.

## Store badges

`src/badge-app-store.svg` and `src/badge-google-play.png` are the official badges,
from https://developer.apple.com/app-store/marketing/guidelines/ and
https://play.google.com/intl/en_us/badges/. The Google Play file is trimmed of its
transparent margin and is otherwise untouched. Keep them as they are: both
guidelines forbid changing the artwork, and that includes dimming a badge for an app
that isn't out yet. The footer carries the trademark credit Apple asks for.

The Arabic page uses the same English badges. Google's public Arabic badge still has
the old Play logo.

## Change anything else

1. Edit the files in `src/` (`body.html`, `style.css`, `script.js`, `intro.css`).
   The footer food drawings are in `food_items.py`.
2. Build: `pip install playwright pillow numpy markdown matplotlib && python3 build.py`
   (Playwright renders `og-image.png`, the link preview image).
3. Copy everything in `out/site/` to the root of `main` and push. GitHub Pages
   publishes the change within a minute or two.

`out/jeetaklb.html` is the same page without the document wrapper, for the
Claude artifact preview. It plays the intro on every load and has a Replay
button; the live site plays it once per browser session. `SITE_INTRO` in
`build.py` turns the intro off for the live site.

## Redesign preview (this branch only)

The `revamp/` folder holds a redesign of the landing page that follows the brand guide
(jeetaklb.com/brand): Saira and Cairo, orange first, the leaning blocks, the pin and the dashed
route. It is a preview. Nothing in it is deployed, and `build.py` still builds the live site.

- Build it: `python3 revamp/build.py` writes `out/revamp.html` (for the Claude artifact preview)
  and `out/revamp-site/index.html` (the same page as a deployable file).
- `revamp/body.html`, `style.css` and `script.js` are the page. The store links, the copy and the
  store badges are read from `src/` at build time, so they always match the live site; copy that
  is new in the redesign is in `EXTRA` at the top of `revamp/script.js`.
- `revamp/assets/`: the logo as vectors (`brand_logo.json`, from the brand guide), the three app
  icons, the delivery bag photo cut out of its white background (`tools/cut_bag.py` made
  `bag.webp` from `bag-source.jpg`) and the QR code shown to desktop visitors (`tools/make_qr.py`).
- The map is the same drawing code as the live site. Its labels are set in Cairo, so they were
  measured again (`tools/measure_labels.py` writes `revamp/label_widths.json`) and the map is
  cached in `revamp/map_cache.json`.

To make it the live site: copy `out/revamp-site/index.html` over `index.html` on `main`. The policy
pages and /driver and /partner still use the old fonts and colours and would need the same restyle.

## Policy pages

`pages_text.py` holds the text of /about-us, /terms, /customer_policy,
/vendor-policy, /driver-policy and /account-deletion, written in Markdown.
`pages.py` (run by `build.py`, needs `pip install markdown`) turns each one into
its own HTML file, served at those exact addresses. The app store listings link
to them, so keep the file names unchanged. Change the "Last updated" date in
`pages_text.py` whenever the text changes.

## App links: /driver and /partner

`app_pages.py` makes jeetaklb.com/driver (the Jeetak Driver app) and jeetaklb.com/partner
(the Jeetak Partner app). Share these instead of the store links: WhatsApp and other apps
show their own preview image (`og-driver.jpg`, `og-partner.jpg`, drawn by `build.py`), and
phones go straight to their store: Android to Google Play, iPhone to the App Store once the
app is listed there (until then iPhones see the page). Add `?stay` to a link to see the page
itself on a phone. The store links come from `STORE_LINKS` in `src/script.js`.

The preview images use the Kanit and Readex Pro fonts, loaded from Google Fonts. Where Google
Fonts is blocked, install them (`npm i @fontsource/kanit @fontsource/readex-pro`) and set
`JEETAK_FONTS` to that `node_modules/@fontsource` folder before running `build.py`.

## Coverage map

The "Where we deliver" section shows a map of the Upper Metn with every village.
Set `SITE_MAP = False` in `build.py` to show the villages as name tags instead
(the artifact preview always shows the map).

- `village_coords.py`: each village's position, from GeoNames.
- `village_map.py`: draws the map as an SVG, in two layouts. "wide" is for screens
  720px and up. "compact" is for phones: it is drawn taller (north-south distances
  1.3x) with its own label layout and short leader lines, so the whole map fits a
  phone without swiping. Both place the English and Arabic labels so they don't
  overlap, and outline the delivery area around the villages. The contour lines
  are decorative, not survey data.
- `label_widths.json`: label widths measured in the page fonts. A village that
  isn't listed gets an estimate.
- `map_cache.json`: the last maps drawn. `build.py` redraws them (about 90 seconds)
  whenever the villages or these files change.
- `src/map.css` styles the map and picks the layout for the screen size. `initMap`
  in `src/script.js` handles taps and runs the pin drops.

To add a village, add its English and Arabic names to `VILLAGES` in `build.py`
and its coordinates to `village_coords.py`. Then update the village count in
`build.py`, `src/body.html`, `src/script.js` and `pages_text.py`.

## Icons

`icon-source.jpg` is the app icon. `make_icons.py` (run by `build.py`) crops it
into `favicon.ico`, `favicon-32.png`, `icon-192.png` (rounded, for browser tabs)
and `apple-touch-icon.png` (full square, iPhones round it themselves).

## Logo

`logo-source.png` is the official logo. `trace_logo.py` turns it into the vector
paths in `logo_paths.json` (needs `pip install potracer scipy pillow`).

## DNS (Hostinger)

- `@` A: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
- `@` AAAA: 2606:50c0:8000::153, 2606:50c0:8001::153, 2606:50c0:8002::153, 2606:50c0:8003::153
- `www` CNAME: pixelabs-dot-tech.github.io.
- `api`, `admin`, `vendor` and their `dev.` versions point to the platform servers. Leave them as they are.
