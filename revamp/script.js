(function () {
  "use strict";

  // The store links and the page copy come from the live site's src/script.js at build time,
  // so the redesign always carries the same links and the same wording.
  /*{{STORE_LINKS}}*/

  /*{{T_BASE}}*/

  // Copy that is new in the redesign. The Arabic lines marked "brand" are the brand guide's own.
  var EXTRA = {
    en: {
      heroPlace: "24 villages in the Upper Metn",
      heroAnswer: "Jeetak",
      heroAria: "Hungry? Jeetak.",
      need1: "Hungry?",
      need2: "Out of bread?",
      need3: "Raining?",
      need4: "Friends over?",
      tripFrom: "The village shop",
      tripTo: "Your door",
      svcTitle: "Everything you {need}.",
      tagCash: "Cash at the door",
      bagAlt: "The orange Jeetak delivery bag",
      qrNote: "On a computer? Point your phone’s camera here.",
      barNote: "Upper Metn delivery",
      barBtn: "Get the app"
    },
    ar: {
      heroPlace: "24 ضيعة بالمتن الأعلى",
      heroAnswer: "جيتك",
      heroAria: "جوعان؟ جيتك.",            // brand
      need1: "جوعان؟",                      // brand
      need2: "خلص الخبز؟",                  // brand
      need3: "عم تشتي برّا؟",                // brand
      need4: "عندك سهرة؟",                  // brand
      tripFrom: "دكّانة الضيعة",
      tripTo: "باب بيتك",
      svcTitle: "شو ما {بدّك}.",             // brand: the tagline, with its full stop
      tagCash: "كاش عالباب",                // brand
      bagAlt: "شنطة دليفري جيتك البرتقالية",
      qrNote: "عالكمبيوتر؟ صوّر الكود بكاميرا تلفونك.",
      barNote: "توصيل بالمتن الأعلى",
      barBtn: "نزّل التطبيق"                // brand
    }
  };
  ["en", "ar"].forEach(function (lang) {
    Object.keys(EXTRA[lang]).forEach(function (key) { T[lang][key] = EXTRA[lang][key]; });
  });
  var NEEDS = ["need1", "need2", "need3", "need4"];

  var root = document.documentElement;
  var isSite = !!document.querySelector('meta[property="og:url"]');
  var reduceMotion = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
  var current = "en";
  var trip = null;

  function each(selector, fn) {
    Array.prototype.forEach.call(document.querySelectorAll(selector), fn);
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; });
  }

  // Headlines: {word} is the one coloured word, and every closing full stop takes the same colour.
  // A headline made of several short sentences only breaks between them.
  function rich(s) {
    var sentences = (esc(s).match(/[^.]+\.?/g) || [esc(s)])
      .map(function (part) { return part.replace(/^\s+|\s+$/g, ""); })
      .filter(Boolean);
    return sentences.map(function (part) {
      var html = part
        .replace(/\{([^}]+)\}/g, '<span class="acc">$1</span>')
        .replace(/\.$/, '<span class="stop">.</span>');
      return sentences.length > 1 ? '<span class="nb">' + html + "</span>" : html;
    }).join(" ");
  }

  // A dashed route always ends on a whole dash: 8 on, 12 off, with round caps.
  function fitDashes() {
    each(".trip-line, .rule", function (svg) {
      var line = svg.querySelector("line");
      var w = svg.getBoundingClientRect().width;
      if (!line || w < 40) return;
      var n = Math.floor((w - 6 - 8) / 20);
      var x1 = (w - (n * 20 + 8)) / 2;
      line.setAttribute("x1", x1.toFixed(1));
      line.setAttribute("x2", (x1 + n * 20 + 8).toFixed(1));
    });
  }

  function linksFor(app) {
    return STORE_LINKS[app || "customer"] || {};
  }

  function detectOS() {
    var ua = navigator.userAgent || "";
    if (/iPhone|iPad|iPod/i.test(ua) || (/Macintosh/i.test(ua) && navigator.maxTouchPoints > 1)) return "ios";
    if (/Android/i.test(ua)) return "android";
    return null;
  }
  var os = detectOS();

  function setStores(dict) {
    each(".store", function (el) {
      var key = el.getAttribute("data-store");
      var url = linksFor(el.getAttribute("data-app"))[key];
      if (url) {
        el.setAttribute("href", url);
        el.setAttribute("target", "_blank");
        el.setAttribute("rel", "noopener");
        el.setAttribute("aria-label", key === "ios" ? dict.storeLiveIos + " App Store" : dict.storeLiveAndroid + " Google Play");
        el.classList.remove("is-soon");
      } else {
        el.removeAttribute("href");
        el.classList.add("is-soon");
      }
    });
    each("[data-i18n-state]", function (el) {
      var links = linksFor(el.getAttribute("data-app"));
      var state = links.ios && links.android ? "Live" : links.android ? "Android" : links.ios ? "Ios" : "Soon";
      var key = el.getAttribute("data-i18n-state");
      var value = dict[key + state] != null ? dict[key + state] : dict[key + "Live"];
      if (value != null) el.textContent = value;
    });
  }

  function apply(lang) {
    current = lang;
    var dict = T[lang];
    root.setAttribute("lang", lang);
    root.setAttribute("dir", lang === "ar" ? "rtl" : "ltr");
    each("[data-i18n]", function (el) {
      var value = dict[el.getAttribute("data-i18n")];
      if (value != null) el.textContent = value;
    });
    each("[data-i18n-rich]", function (el) {
      var value = dict[el.getAttribute("data-i18n-rich")];
      if (value != null) el.innerHTML = rich(value);
    });
    each("[data-i18n-aria]", function (el) {
      var value = dict[el.getAttribute("data-i18n-aria")];
      if (value != null) el.setAttribute("aria-label", value);
    });
    each("[data-i18n-alt]", function (el) {
      var value = dict[el.getAttribute("data-i18n-alt")];
      if (value != null) el.setAttribute("alt", value);
    });
    var toggle = document.getElementById("langToggle");
    if (toggle) {
      toggle.textContent = dict.langBtn;
      toggle.setAttribute("lang", dict.langBtnLang);
      toggle.setAttribute("aria-label", dict.langAria);
    }
    if (isSite) document.title = dict.docTitle;
    setStores(dict);
    if (trip) trip.refresh();
  }

  function orderStores() {
    if (!os) return;
    each(".stores", function (group) {
      var mine = group.querySelector('[data-store="' + os + '"]');
      if (mine) group.insertBefore(mine, group.firstChild);
    });
  }

  function initLanguage() {
    var saved = null;
    try { saved = window.localStorage.getItem("jeetak-lang"); } catch (e) { saved = null; }
    var browserAr = (navigator.language || "").toLowerCase().indexOf("ar") === 0;
    apply(saved === "ar" || saved === "en" ? saved : (browserAr ? "ar" : "en"));
    var toggle = document.getElementById("langToggle");
    if (toggle) {
      toggle.addEventListener("click", function () {
        var next = current === "en" ? "ar" : "en";
        apply(next);
        try { window.localStorage.setItem("jeetak-lang", next); } catch (e) { /* not stored */ }
      });
    }
  }

  // The hero trip. A need comes up ("Hungry?"), the scooter leaves the shop pin, rides the dashed
  // route and reaches the door pin: Jeetak. Then the next need.
  function initTrip() {
    var hero = document.getElementById("top");
    var box = document.getElementById("trip");
    var rider = document.getElementById("tripRider");
    var word = document.getElementById("needWord");
    if (!hero || !box || !rider || !word) return null;
    var row = box.querySelector(".trip-row");
    var pin = box.querySelector(".trip-pin");
    var span = 0, sign = 1, need = 0;

    function measure() {
      var gap = parseFloat(window.getComputedStyle(row).columnGap) || 9;
      var pinW = pin.getBoundingClientRect().width;
      // the scooter itself fills the middle 70% of its box (the rest is room for the speed lines)
      span = Math.max(0, row.clientWidth - 2 * (pinW + gap) - rider.offsetWidth * 0.7 - 4);
      sign = root.getAttribute("dir") === "rtl" ? -1 : 1;
    }
    function place(p) {
      rider.style.transform = "translateX(" + (sign * p * span).toFixed(1) + "px)";
    }
    function showNeed(i, animate) {
      need = i % NEEDS.length;
      var text = T[current][NEEDS[need]];
      if (!animate || !word.animate) { word.textContent = text; return; }
      var out = word.animate([{ opacity: 1, transform: "none" }, { opacity: 0, transform: "translateY(-0.28em)" }],
        { duration: 170, easing: "ease-in", fill: "forwards" });
      out.onfinish = function () {
        word.textContent = T[current][NEEDS[need]];
        out.cancel();
        word.animate([{ opacity: 0, transform: "translateY(0.32em)" }, { opacity: 1, transform: "none" }],
          { duration: 300, easing: "cubic-bezier(.2,.8,.2,1)" });
      };
    }

    measure();
    if (reduceMotion) {
      place(1);
      window.addEventListener("resize", function () { measure(); place(1); });
      return { hold: function () {}, release: function () {}, refresh: function () { measure(); place(1); showNeed(need, false); } };
    }

    var CYCLE = 4700, START = 350, END = 3200, SWAP = 4150;
    var t0 = null, raf = 0, running = false, inView = true, held = false, swapped = false, lastC = 0;

    function ease(x) { return x < 0.5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2; }

    function frame(now) {
      if (t0 === null) { t0 = now; lastC = 0; swapped = false; }
      var c = (now - t0) % CYCLE;
      if (c < lastC) swapped = false;            // a new trip
      lastC = c;
      var riding = c >= START && c < END;
      place(c < START ? 0 : (riding ? ease((c - START) / (END - START)) : 1));
      rider.style.opacity = c < 260 ? (c / 260).toFixed(2) : (c >= SWAP ? Math.max(0, 1 - (c - SWAP) / 260).toFixed(2) : "1");
      rider.classList.toggle("is-parked", !riding);
      var arrived = c >= END && c < END + 700;
      box.classList.toggle("is-arrived", arrived);
      hero.classList.toggle("is-arrived", arrived);
      if (c >= SWAP && !swapped) { swapped = true; showNeed(need + 1, true); }
      raf = window.requestAnimationFrame(frame);
    }
    function start() {
      if (held || running || !inView || document.hidden) return;
      running = true;
      t0 = null;
      raf = window.requestAnimationFrame(frame);
    }
    function stop() {
      running = false;
      window.cancelAnimationFrame(raf);
    }

    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          inView = entry.isIntersecting;
          if (inView) start(); else stop();
        });
      }).observe(box);
    } else {
      start();
    }
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) stop(); else start();
    });
    window.addEventListener("resize", measure);

    return {
      // the intro keeps the scooter at the shop until the page has arrived
      hold: function () {
        held = true;
        stop();
        place(0);
        rider.style.opacity = "0";
        box.classList.remove("is-arrived");
        hero.classList.remove("is-arrived");
      },
      release: function () {
        held = false;
        start();
      },
      refresh: function () {
        measure();
        showNeed(need, false);
      }
    };
  }

  // Intro: the rider crosses a pine screen and the orange page leans in behind it.
  var INTRO_END = 2750;

  function initIntro() {
    var intro = document.getElementById("intro");
    if (!intro) return;
    var replay = document.getElementById("introReplay");
    var timers = [];

    function clear() {
      timers.forEach(window.clearTimeout);
      timers = [];
    }
    function finish() {
      clear();
      root.classList.remove("intro-on", "intro-skip");
      if (trip) trip.release();
    }
    function play() {
      clear();
      root.classList.remove("intro-on", "intro-skip");
      window.scrollTo(0, 0);
      void root.offsetWidth; // restart the CSS animations
      root.classList.add("intro-on");
      if (trip) trip.hold();
      timers.push(window.setTimeout(finish, INTRO_END));
    }
    function skip() {
      if (!root.classList.contains("intro-on") || root.classList.contains("intro-skip")) return;
      clear();
      root.classList.add("intro-skip");
      timers.push(window.setTimeout(finish, 220));
    }

    intro.addEventListener("click", skip);
    if (replay) replay.addEventListener("click", play);

    if (root.classList.contains("intro-on")) {
      try { window.sessionStorage.setItem("jeetak-intro", "1"); } catch (e) { /* not stored */ }
      if (trip) trip.hold();
      // The CSS animations started at first paint; line the timer up with them.
      var elapsed = 0;
      var train = document.getElementById("introTrain");
      if (train && train.getAnimations) {
        var anims = train.getAnimations();
        if (anims.length && anims[0].currentTime != null) elapsed = Number(anims[0].currentTime) || 0;
      }
      timers.push(window.setTimeout(finish, Math.max(0, INTRO_END - elapsed)));
    }
  }

  // The sample order card.
  function initStatus() {
    var list = document.getElementById("statusList");
    if (!list) return;
    var items = list.querySelectorAll("li");
    var last = items.length - 1;
    function setStep(n) {
      Array.prototype.forEach.call(items, function (li, i) {
        li.classList.toggle("done", i < n || (n === last && i === last));
        li.classList.toggle("now", i === n && n < last);
      });
    }
    if (reduceMotion) { setStep(last); return; }
    var n = 0;
    setStep(0);
    window.setInterval(function () {
      n = (n + 1) % (items.length + 2);
      setStep(Math.min(n, last));
    }, 1400);
  }

  // Phones: once the store badges in the hero scroll away, a download bar follows the page.
  // It goes straight to the right store for the phone, and steps aside at the last section.
  function initAppBar() {
    var bar = document.getElementById("appBar");
    var btn = document.getElementById("appBarBtn");
    var first = document.querySelector(".hero .stores");
    var last = document.getElementById("get");
    if (!bar || !btn || !first || !last || !("IntersectionObserver" in window)) return;
    var direct = os ? linksFor("customer")[os] : "";
    if (direct) {
      btn.setAttribute("href", direct);
      btn.setAttribute("target", "_blank");
      btn.setAttribute("rel", "noopener");
    }
    var pastFirst = false, atLast = false;
    function update() {
      var on = pastFirst && !atLast;
      bar.classList.toggle("is-on", on);
      root.classList.toggle("bar-on", on);
      if (on) bar.removeAttribute("inert"); else bar.setAttribute("inert", "");
    }
    new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        pastFirst = !entry.isIntersecting && entry.boundingClientRect.bottom < 0;
      });
      update();
    }).observe(first);
    new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) { atLast = entry.isIntersecting; });
      update();
    }, { rootMargin: "0px 0px -15% 0px" }).observe(last);
    update();
  }

  // Footer: food pops up from under the page, wiggles and ducks back down.
  // Tap one and it jumps. Every so often the scooter rides past along the bottom.
  function initFooterFun() {
    var stage = document.getElementById("footStage");
    var tpl = document.getElementById("footFood");
    if (!stage || !tpl || !tpl.content) return;
    var kinds = Array.prototype.slice.call(tpl.content.querySelectorAll(".food"));
    var scooterTpl = tpl.content.querySelector(".foot-scooter");
    if (!kinds.length) return;

    if (reduceMotion || !stage.animate) {
      [[0.2, -6], [0.5, 4], [0.8, -3]].forEach(function (spot, i) {
        var el = kinds[(i * 3) % kinds.length].cloneNode(true);
        el.classList.add("is-still");
        el.style.left = spot[0] * 100 + "%";
        el.style.setProperty("--tilt", spot[1] + "deg");
        stage.appendChild(el);
      });
      return;
    }

    var live = [];
    var timer = 0, active = false, ticks = 0, scooting = false, scooterNext = false, lastKind = -1;

    function rand(a, b) { return a + Math.random() * (b - a); }

    function pickKind() {
      var k;
      do { k = Math.floor(Math.random() * kinds.length); } while (k === lastKind && kinds.length > 1);
      lastKind = k;
      return k;
    }

    function freeSpot(w) {
      var width = stage.clientWidth;
      for (var tries = 0; tries < 8; tries++) {
        var x = rand(width * 0.04, width * 0.96 - w);
        var clear = live.every(function (it) { return Math.abs(it.x - x) > (it.w + w) * 0.6; });
        if (clear) return x;
      }
      return null;
    }

    function remove(item) {
      var i = live.indexOf(item);
      if (i >= 0) live.splice(i, 1);
      if (item.el.parentNode) item.el.parentNode.removeChild(item.el);
    }

    function hop(item) {
      if (!item.anim || item.hopping) return;
      item.hopping = true;
      try { item.anim.commitStyles(); } catch (e) { /* starts from its resting spot */ }
      item.anim.cancel();
      var from = window.getComputedStyle(item.el).transform;
      var spin = Math.random() < 0.5 ? -1 : 1;
      var jump = item.el.animate([
        { transform: from === "none" ? "translateY(20%)" : from },
        { transform: "translateY(-60%) rotate(" + spin * 200 + "deg)", offset: 0.42, easing: "cubic-bezier(.4,0,.9,.6)" },
        { transform: "translateY(110%) rotate(" + spin * 390 + "deg)" }
      ], { duration: 820, easing: "cubic-bezier(.2,.7,.4,1)", fill: "forwards" });
      jump.onfinish = function () { remove(item); };
    }

    function pop() {
      if (live.length >= 3) return;
      var el = kinds[pickKind()].cloneNode(true);
      stage.appendChild(el);
      var w = el.offsetWidth;
      var x = freeSpot(w);
      if (x === null) { stage.removeChild(el); return; }
      el.style.left = x.toFixed(0) + "px";
      var item = { el: el, x: x, w: w };
      live.push(item);
      var tilt = rand(5, 9) * (Math.random() < 0.5 ? -1 : 1);
      var peek = rand(4, 16).toFixed(1) + "%";
      var up = "translateY(" + peek + ") ";
      item.anim = el.animate([
        { transform: "translateY(102%) rotate(0deg)", easing: "cubic-bezier(.2,.9,.3,1.3)" },
        { transform: up + "rotate(0deg)", offset: 0.2, easing: "ease-in-out" },
        { transform: up + "rotate(" + tilt + "deg)", offset: 0.33, easing: "ease-in-out" },
        { transform: up + "rotate(" + -tilt + "deg)", offset: 0.45, easing: "ease-in-out" },
        { transform: up + "rotate(" + tilt * 0.45 + "deg)", offset: 0.55, easing: "ease-in-out" },
        { transform: up + "rotate(0deg)", offset: 0.63, easing: "cubic-bezier(.5,0,.75,0)" },
        { transform: "translateY(102%) rotate(0deg)" }
      ], { duration: rand(2100, 2900), fill: "forwards" });
      item.anim.onfinish = function () { if (!item.hopping) remove(item); };
      el.addEventListener("pointerdown", function () { hop(item); });
    }

    function rideBy() {
      if (!scooterTpl) return;
      var el = scooterTpl.cloneNode(true);
      stage.appendChild(el);
      var width = stage.clientWidth, w = el.offsetWidth;
      var rtl = root.getAttribute("dir") === "rtl";   // the scooter rides the way the page reads
      scooting = true;
      var from = "translateX(" + (-w - 10) + "px)", to = "translateX(" + (width + 10) + "px)";
      var ride = el.animate([{ transform: rtl ? to : from }, { transform: rtl ? from : to }],
        { duration: Math.max(2200, width * 3.4), easing: "cubic-bezier(.3,.15,.7,.85)" });
      ride.onfinish = function () {
        scooting = false;
        if (el.parentNode) el.parentNode.removeChild(el);
      };
    }

    function tick() {
      timer = 0;
      if (!active) return;
      if (!scooting) {
        ticks++;
        if (scooterNext) {
          if (!live.length) { scooterNext = false; rideBy(); }
        } else if (ticks === 5 || ticks % 12 === 0) {
          scooterNext = true;
        } else {
          pop();
        }
      }
      timer = window.setTimeout(tick, rand(650, 1400));
    }

    function start() {
      if (active || document.hidden) return;
      active = true;
      timer = window.setTimeout(tick, 350);
    }
    function stop() {
      active = false;
      window.clearTimeout(timer);
    }

    var inView = false;
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          inView = entry.isIntersecting;
          if (inView) start(); else stop();
        });
      }, { threshold: 0.1 }).observe(stage);
    } else {
      inView = true;
      start();
    }
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) stop(); else if (inView) start();
    });
  }

  // Coverage map: tap a village to light it up. When the map comes into view the villages
  // ripple out from Hammana, then a Jeetak pin drops on a random village now and then.
  // The page holds a wide and a phone drawing of the map; only one of them is shown.
  function initMap() {
    var card = document.getElementById("mapCard");
    if (!card) return;

    card.addEventListener("click", function (e) {
      var v = e.target.closest ? e.target.closest(".map-v") : null;
      Array.prototype.forEach.call(card.querySelectorAll(".map-v.is-active"), function (el) {
        if (el !== v) el.classList.remove("is-active");
      });
      if (v) v.classList.toggle("is-active");
    });

    if (reduceMotion || !("IntersectionObserver" in window)) return;
    var timer = 0, last = -1;

    function shownMap() {
      var maps = card.querySelectorAll(".village-map");
      for (var i = 0; i < maps.length; i++) {
        if (maps[i].getClientRects().length) return maps[i];
      }
      return null;
    }

    function dropPin() {
      timer = 0;
      var map = shownMap();
      var villages = map ? map.querySelectorAll(".map-v") : [];
      var drop = map && map.querySelector(".map-drop");
      var pin = drop && drop.querySelector(".map-drop-pin");
      if (pin && villages.length) {
        var i;
        do { i = Math.floor(Math.random() * villages.length); } while (i === last && villages.length > 1);
        last = i;
        var v = villages[i];
        var dot = v.querySelector(".map-dot");
        var fall = map.classList.contains("is-compact") ? 24 : 34;
        drop.setAttribute("transform", "translate(" + dot.getAttribute("cx") + " " + dot.getAttribute("cy") + ")");
        if (pin.animate) {
          pin.animate([
            { transform: "translateY(-" + fall + "px) scale(1, 1)", opacity: 0 },
            { transform: "translateY(0) scale(1, 1)", opacity: 1, offset: 0.22, easing: "cubic-bezier(.5,0,.8,.4)" },
            { transform: "translateY(0) scale(1.2, 0.8)", opacity: 1, offset: 0.3 },
            { transform: "translateY(0) scale(1, 1)", opacity: 1, offset: 0.4 },
            { transform: "translateY(0) scale(1, 1)", opacity: 1, offset: 0.82 },
            { transform: "translateY(-6px) scale(1, 1)", opacity: 0 }
          ], { duration: 2300, easing: "ease-out", fill: "both" });
        }
        window.setTimeout(function () { v.classList.add("is-hit"); }, 500);
        window.setTimeout(function () { v.classList.remove("is-hit"); }, 2000);
      }
      timer = window.setTimeout(dropPin, 2600 + Math.random() * 1200);
    }

    new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          card.classList.add("map-on");
          if (!timer) timer = window.setTimeout(dropPin, 1400);
        } else {
          window.clearTimeout(timer);
          timer = 0;
        }
      });
    }, { threshold: 0.3 }).observe(card);
  }

  orderStores();
  fitDashes();
  window.addEventListener("resize", fitDashes);
  trip = initTrip();
  initLanguage();
  initIntro();
  initStatus();
  initAppBar();
  initFooterFun();
  initMap();
})();
