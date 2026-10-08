(function () {
  "use strict";

  // Paste the store links here once each app is live.
  // While a link is empty, its button shows "Coming soon".
  var STORE_LINKS = {
    customer: { ios: "", android: "https://play.google.com/store/apps/details?id=com.food.jeetak" },     // Jeetak customer app
    vendor:   { ios: "", android: "https://play.google.com/store/apps/details?id=com.jeetak.vendor" },   // vendor app for restaurants and shops
    driver:   { ios: "", android: "https://play.google.com/store/apps/details?id=com.jeetak.drivers" }   // driver app
  };

  var T = {
    en: {
      heroEyebrow: "Upper Metn · 24 villages",
      heroTitle: "From the village shop to your door.",
      heroLede: "Food, groceries and anything else nearby, ordered in one app. No calls. No voice notes.",
      storeSoon: "Coming soon on",
      storeLiveIos: "Download on the",
      storeLiveAndroid: "Get it on",
      storeNoteSoon: "The app is launching soon on iPhone and Android.",
      storeNoteLive: "Available now on iPhone and Android.",
      storeNoteAndroid: "Available now on Android. The iPhone app is coming soon.",
      storeNoteIos: "Available now on iPhone. The Android app is coming soon.",
      svcEyebrow: "What we bring",
      svcTitle: "Everything you need.",
      svcLede: "Order it in the app and we bring it over.",
      svcFoodTitle: "Food",
      svcFoodBody: "Man’oushe, shawarma or a full family lunch from the restaurants near you.",
      svcGrocTitle: "Groceries",
      svcGrocBody: "Bread, labneh, vegetables and water gallons from the shops nearby. No phone call needed.",
      svcAnyTitle: "Anything else",
      svcAnyBody: "If a shop on Jeetak sells it, a driver brings it to your door.",
      howEyebrow: "How it works",
      howTitle: "Order. Wait a bit. Open the door.",
      step1Title: "Order in the app",
      step1Body: "Browse the restaurants and shops in your area, fill your cart and check out.",
      step2Title: "The shop gets it ready",
      step2Body: "You see the moment your order is accepted, and while it’s being prepared.",
      step3Title: "A driver brings it over",
      step3Body: "A Jeetak driver picks it up and brings it to your door.",
      statusTitle: "Your order",
      st1: "Order placed",
      st2: "Accepted by the shop",
      st3: "Being prepared",
      st4: "On the way",
      st5: "Delivered",
      covEyebrow: "Where we deliver",
      covTitle: "24 villages. One app.",
      covLede: "Jeetak delivers to all of these villages in the Upper Metn.",
      joinLink: "Join Jeetak",
      joinEyebrow: "Work with Jeetak",
      joinTitle: "Join Jeetak.",
      joinLede: "Own a restaurant or shop, or want to deliver? Download the app made for you and apply from your phone.",
      vendorKicker: "Restaurants & shops",
      vendorTitle: "Become a partner",
      vendorBody: "Get orders from customers across 24 villages. Accept and prepare them in the vendor app, and a Jeetak driver picks them up.",
      vendorApplySoon: "The vendor app is coming soon. You’ll download it and apply right here.",
      vendorApplyLive: "Download the vendor app and apply.",
      vendorApplyAndroid: "Download the vendor app on Android and apply. The iPhone version is coming soon.",
      vendorApplyIos: "Download the vendor app on iPhone and apply. The Android version is coming soon.",
      driverKicker: "Drivers",
      driverTitle: "Become a driver",
      driverBody: "Deliver orders around the Upper Metn and earn on every delivery. The driver app shows your deliveries and earnings.",
      driverApplySoon: "The driver app is coming soon. You’ll download it and apply right here.",
      driverApplyLive: "Download the driver app and apply.",
      driverApplyAndroid: "Download the driver app on Android and apply. The iPhone version is coming soon.",
      driverApplyIos: "Download the driver app on iPhone and apply. The Android version is coming soon.",
      ctaTitle: "Get Jeetak on your phone.",
      ctaBodySoon: "The app launches soon on iPhone and Android. The download links will appear right here.",
      ctaBodyLive: "Download the app and place your first order.",
      ctaBodyAndroid: "Get it on Google Play and place your first order. The iPhone app is coming soon.",
      ctaBodyIos: "Download it on the App Store and place your first order. The Android app is coming soon.",
      footCopy: "© 2026 Jeetak SARL",
      lnkAbout: "About us",
      lnkTerms: "Terms of use",
      lnkPrivacy: "Privacy policy",
      lnkVendor: "Vendor policy",
      lnkDriver: "Driver policy",
      lnkDelete: "Delete account",
      langBtn: "عربي",
      langBtnLang: "ar",
      langAria: "اقرأ الصفحة بالعربي",
      docTitle: "Jeetak · Delivery across the Upper Metn"
    },
    ar: {
      heroEyebrow: "المتن الأعلى · 24 ضيعة",
      heroTitle: "من دكّانة الضيعة لعند بابك.",
      heroLede: "أكل، أغراض البيت، وكل شي بدّك ياه من المحلات اللي حدّك، بتطلبه من تطبيق واحد. بلا تلفونات، وبلا فويسات.",
      storeSoon: "قريباً على",
      storeLiveIos: "نزّلو من",
      storeLiveAndroid: "نزّلو من",
      storeNoteSoon: "التطبيق نازل قريباً على آيفون وأندرويد.",
      storeNoteLive: "التطبيق موجود هلّق على آيفون وأندرويد.",
      storeNoteAndroid: "التطبيق موجود هلّق على أندرويد، وعلى آيفون قريباً.",
      storeNoteIos: "التطبيق موجود هلّق على آيفون، وعلى أندرويد قريباً.",
      svcEyebrow: "شو منجيبلك",
      svcTitle: "شو ما بدّك؟",
      svcLede: "اطلبه من التطبيق، ونحنا منجيبلك ياه.",
      svcFoodTitle: "أكل",
      svcFoodBody: "منقوشة، شاورما، أو غدا للعيلة كلّها من المطاعم القريبة منك.",
      svcGrocTitle: "أغراض البيت",
      svcGrocBody: "خبز، لبنة، خضرة، وغالونات مي من الدكاكين اللي حدّك. بلا ما تتّصل.",
      svcAnyTitle: "وأي شي تاني",
      svcAnyBody: "إذا في محل على جيتك بيبيعه، الدليفري بيجيبلك ياه لعند بابك.",
      howEyebrow: "كيف بيشتغل",
      howTitle: "اطلب. استنّى شوي. افتح الباب.",
      step1Title: "اطلب من التطبيق",
      step1Body: "تفرّج على المطاعم والمحلات بمنطقتك، عبّي السلّة وكمّل الطلب.",
      step2Title: "المحل بيحضّرلك ياه",
      step2Body: "بتعرف أوّل ما ينقبل طلبك، وبتشوفه وهوّي عم يتحضّر.",
      step3Title: "الدليفري بيوصّلك ياه",
      step3Body: "دليفري جيتك بياخدو من المحل وبيجيبو لباب بيتك.",
      statusTitle: "طلبك",
      st1: "انبعت الطلب",
      st2: "المحل قبل الطلب",
      st3: "عم يتحضّر",
      st4: "عالطريق",
      st5: "وصل",
      covEyebrow: "وين منوصل",
      covTitle: "24 ضيعة. تطبيق واحد.",
      covLede: "جيتك بيوصل لكل هالضيع بالمتن الأعلى.",
      joinLink: "انضمّ لجيتك",
      joinEyebrow: "اشتغل مع جيتك",
      joinTitle: "انضمّ لجيتك.",
      joinLede: "عندك مطعم أو محل، أو بدّك تشتغل دليفري؟ نزّل التطبيق المخصّص إلك وقدّم طلبك من تلفونك.",
      vendorKicker: "مطاعم ومحلات",
      vendorTitle: "صير شريك",
      vendorBody: "وصّل محلّك لزباين بـ24 ضيعة. بتقبل الطلبيات وبتجهّزها من تطبيق المحلات، ودليفري جيتك بيمرق ياخدها.",
      vendorApplySoon: "تطبيق المحلات نازل قريباً، ورح تنزّلو وتقدّم طلبك من هون.",
      vendorApplyLive: "نزّل تطبيق المحلات وقدّم طلبك.",
      vendorApplyAndroid: "نزّل تطبيق المحلات على أندرويد وقدّم طلبك. نسخة الآيفون نازلة قريباً.",
      vendorApplyIos: "نزّل تطبيق المحلات على آيفون وقدّم طلبك. نسخة الأندرويد نازلة قريباً.",
      driverKicker: "سائقين",
      driverTitle: "اشتغل دليفري",
      driverBody: "وصّل طلبيات بالمتن الأعلى واربح عن كل توصيلة. تطبيق الدليفري بيورجيك توصيلاتك ومدخولك.",
      driverApplySoon: "تطبيق الدليفري نازل قريباً، ورح تنزّلو وتقدّم طلبك من هون.",
      driverApplyLive: "نزّل تطبيق الدليفري وقدّم طلبك.",
      driverApplyAndroid: "نزّل تطبيق الدليفري على أندرويد وقدّم طلبك. نسخة الآيفون نازلة قريباً.",
      driverApplyIos: "نزّل تطبيق الدليفري على آيفون وقدّم طلبك. نسخة الأندرويد نازلة قريباً.",
      ctaTitle: "نزّل جيتك على تلفونك.",
      ctaBodySoon: "التطبيق نازل قريباً على آيفون وأندرويد، وروابط التنزيل رح تكون هون.",
      ctaBodyLive: "نزّل التطبيق واطلب أوّل طلبية.",
      ctaBodyAndroid: "نزّلو من Google Play واطلب أوّل طلبية. تطبيق الآيفون نازل قريباً.",
      ctaBodyIos: "نزّلو من App Store واطلب أوّل طلبية. تطبيق الأندرويد نازل قريباً.",
      footCopy: "© 2026 جيتك ش.م.م.",
      lnkAbout: "من نحن",
      lnkTerms: "شروط الاستخدام",
      lnkPrivacy: "سياسة الخصوصية",
      lnkVendor: "سياسة المحلات",
      lnkDriver: "سياسة الدليفري",
      lnkDelete: "حذف الحساب",
      langBtn: "English",
      langBtnLang: "en",
      langAria: "Read this page in English",
      docTitle: "جيتك · توصيل بالمتن الأعلى"
    }
  };

  var root = document.documentElement;
  var isSite = !!document.querySelector('meta[property="og:url"]');
  var reduceMotion = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
  var current = "en";

  function each(selector, fn) {
    Array.prototype.forEach.call(document.querySelectorAll(selector), fn);
  }

  function linksFor(app) {
    return STORE_LINKS[app || "customer"] || {};
  }

  function isLive(app) {
    var links = linksFor(app);
    return !!(links.ios || links.android);
  }

  function setStores(dict) {
    each(".store", function (el) {
      var key = el.getAttribute("data-store");
      var url = linksFor(el.getAttribute("data-app"))[key];
      var small = el.querySelector("small");
      if (url) {
        el.setAttribute("href", url);
        el.setAttribute("target", "_blank");
        el.setAttribute("rel", "noopener");
        el.removeAttribute("aria-disabled");
        el.classList.remove("is-soon");
        small.textContent = key === "ios" ? dict.storeLiveIos : dict.storeLiveAndroid;
      } else {
        el.removeAttribute("href");
        el.setAttribute("aria-disabled", "true");
        el.classList.add("is-soon");
        small.textContent = dict.storeSoon;
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

  function sortSigns(lang) {
    var list = document.getElementById("signs");
    if (!list) return;
    var attr = lang === "ar" ? "data-ar" : "data-lat";
    var collator = (window.Intl && Intl.Collator) ? new Intl.Collator(lang) : null;
    var items = Array.prototype.slice.call(list.children);
    items.sort(function (a, b) {
      var x = a.getAttribute(attr) || "";
      var y = b.getAttribute(attr) || "";
      if (lang === "ar") { x = x.replace(/^ال/, ""); y = y.replace(/^ال/, ""); }
      return collator ? collator.compare(x, y) : (x < y ? -1 : x > y ? 1 : 0);
    });
    items.forEach(function (li) { list.appendChild(li); });
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
    var toggle = document.getElementById("langToggle");
    if (toggle) {
      toggle.textContent = dict.langBtn;
      toggle.setAttribute("lang", dict.langBtnLang);
      toggle.setAttribute("aria-label", dict.langAria);
    }
    if (isSite) document.title = dict.docTitle;
    setStores(dict);
    sortSigns(lang);
  }

  function detectOS() {
    var ua = navigator.userAgent || "";
    if (/iPhone|iPad|iPod/i.test(ua) || (/Macintosh/i.test(ua) && navigator.maxTouchPoints > 1)) return "ios";
    if (/Android/i.test(ua)) return "android";
    return null;
  }

  function orderStores() {
    var os = detectOS();
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

  // The order that climbs the mountain in the hero.
  function initRoute() {
    var svg = document.getElementById("heroArt");
    if (!svg) return;
    var road = svg.querySelector("#route");
    var reveal = svg.querySelector("#trailReveal");
    var pin = svg.querySelector("#movingPin");
    var house = svg.querySelector("#destHouse");
    var badge = svg.querySelector("#deliveredBadge");
    if (!road || !road.getTotalLength) return;
    var length = road.getTotalLength();
    reveal.style.strokeDasharray = length + " " + length;

    function place(p) {
      var pt = road.getPointAtLength(p * length);
      pin.setAttribute("transform", "translate(" + pt.x.toFixed(1) + " " + pt.y.toFixed(1) + ")");
      reveal.style.strokeDashoffset = (length * (1 - p)).toFixed(1);
    }

    if (reduceMotion) {
      place(1);
      house.classList.add("lit");
      badge.classList.add("show");
      return;
    }

    var CYCLE = 9200, START = 700, END = 6500, FADE = 650;
    var t0 = null, raf = 0, running = false, inView = true, held = false;

    function ease(x) { return x < 0.5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2; }

    function frame(now) {
      if (t0 === null) t0 = now;
      var c = (now - t0) % CYCLE;
      var p = c < START ? 0 : (c < END ? ease((c - START) / (END - START)) : 1);
      place(p);
      house.classList.toggle("lit", c >= END);
      badge.classList.toggle("show", c >= END + 150 && c < CYCLE - FADE);
      pin.classList.toggle("landed", c >= END && c < END + 650);
      svg.classList.toggle("is-fading", c >= CYCLE - FADE);
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
      }).observe(svg);
    } else {
      start();
    }
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) stop(); else start();
    });

    // The intro holds the order at the shop until the scooter lands there.
    return {
      hold: function () {
        held = true;
        stop();
        place(0);
        house.classList.remove("lit");
        badge.classList.remove("show");
        pin.classList.remove("landed");
        svg.classList.remove("is-fading");
      },
      release: function () {
        held = false;
        start();
      }
    };
  }

  // Intro: a scooter with the orange bag rides in, then the view pulls back
  // and the scooter becomes the order pin on the mountain road.
  var INTRO_ORIGIN_X = 0.61;   // the scooter's wheel line, as a share of the intro drawing
  var INTRO_ORIGIN_Y = 0.97;
  var INTRO_BODY_W = 146 / 208; // the scooter's width within the drawing
  var INTRO_LANDED_W = 30;      // px wide when it reaches the road, about the pin's size
  var INTRO_AIM = 1900, INTRO_HANDOFF = 2850, INTRO_END = 3100;

  function initIntro(route) {
    var intro = document.getElementById("intro");
    if (!intro) return;
    var rider = document.getElementById("introRider");
    var replay = document.getElementById("introReplay");
    var timers = [];

    function clear() {
      timers.forEach(window.clearTimeout);
      timers = [];
    }

    function aim() {
      var box = rider && rider.getBoundingClientRect();
      if (!box || !box.width) return;
      // Land on the start of the mountain road. When it's below the fold
      // (short screens, laptops), drive off into the hills at the bottom instead.
      var spot = { x: window.innerWidth / 2, y: window.innerHeight - 10 };
      var landed = INTRO_LANDED_W * 0.75;
      var svg = document.getElementById("heroArt");
      var road = svg && svg.querySelector("#route");
      if (road && svg.getScreenCTM && road.getPointAtLength) {
        var start = road.getPointAtLength(0);
        var pt = svg.createSVGPoint();
        pt.x = start.x;
        pt.y = start.y;
        var s = pt.matrixTransform(svg.getScreenCTM());
        if (s.y <= window.innerHeight - 16 && s.y >= 16 && s.x >= 8 && s.x <= window.innerWidth - 8) {
          spot = s;
          landed = INTRO_LANDED_W;
        }
      }
      var ox = box.left + box.width * INTRO_ORIGIN_X;
      var oy = box.top + box.height * INTRO_ORIGIN_Y;
      rider.style.setProperty("--tx", (spot.x - ox).toFixed(1) + "px");
      rider.style.setProperty("--ty", (spot.y - oy).toFixed(1) + "px");
      rider.style.setProperty("--ts", (landed / (box.width * INTRO_BODY_W)).toFixed(3));
    }

    function finish() {
      clear();
      root.classList.remove("intro-on", "intro-skip");
      if (route) route.release();
    }

    function schedule(elapsed) {
      timers.push(window.setTimeout(aim, Math.max(0, INTRO_AIM - elapsed)));
      timers.push(window.setTimeout(function () { if (route) route.release(); }, Math.max(0, INTRO_HANDOFF - elapsed)));
      timers.push(window.setTimeout(finish, Math.max(0, INTRO_END - elapsed)));
    }

    function play() {
      clear();
      root.classList.remove("intro-on", "intro-skip");
      window.scrollTo(0, 0);
      void root.offsetWidth; // restart the CSS animations
      root.classList.add("intro-on");
      if (route) route.hold();
      schedule(0);
    }

    function skip() {
      if (!root.classList.contains("intro-on") || root.classList.contains("intro-skip")) return;
      clear();
      root.classList.add("intro-skip");
      if (route) route.release();
      timers.push(window.setTimeout(finish, 220));
    }

    intro.addEventListener("click", skip);
    if (replay) replay.addEventListener("click", play);

    if (root.classList.contains("intro-on")) {
      try { window.sessionStorage.setItem("jeetak-intro", "1"); } catch (e) { /* not stored */ }
      if (route) route.hold();
      // The CSS animations started at first paint; line the timers up with them.
      var elapsed = 0;
      if (rider && rider.getAnimations) {
        var anims = rider.getAnimations();
        if (anims.length && anims[0].currentTime != null) elapsed = anims[0].currentTime;
      }
      schedule(elapsed);
    }
  }

  // The sample order status card.
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

  // Phones show the page background when you pull past the top or bottom:
  // green above the header, orange below the footer.
  function initOverscroll() {
    var ticking = false;
    function update() {
      ticking = false;
      var max = root.scrollHeight - window.innerHeight;
      root.classList.toggle("at-end", max > 0 && window.scrollY > max / 2);
    }
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
    }, { passive: true });
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
      scooting = true;
      var ride = el.animate([
        { transform: "translateX(" + (-w - 10) + "px)" },
        { transform: "translateX(" + (width + 10) + "px)" }
      ], { duration: Math.max(2200, width * 3.4), easing: "cubic-bezier(.3,.15,.7,.85)" });
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
  initLanguage();
  var route = initRoute();
  initIntro(route);
  initStatus();
  initOverscroll();
  initFooterFun();
  initMap();
})();
