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

A button switches from "Coming soon" to a live download link as soon as its link
is filled in. Change the same lines in `src/script.js` on this branch so the next
build keeps them.

## Change anything else

1. Edit the files in `src/` (`body.html`, `style.css`, `script.js`, `intro.css`).
   The footer food drawings are in `food_items.py`.
2. Build: `pip install playwright pillow numpy && python3 build.py`
   (Playwright renders `og-image.png`, the link preview image).
3. Copy everything in `out/site/` to the root of `main` and push. GitHub Pages
   publishes the change within a minute or two.

`out/jeetaklb.html` is the same page without the document wrapper, for the
Claude artifact preview. It plays the intro on every load and has a Replay
button; the live site plays it once per browser session. `SITE_INTRO` in
`build.py` turns the intro off for the live site.

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
