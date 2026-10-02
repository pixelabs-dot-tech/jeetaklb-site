(function () {
  "use strict";

  // Paste the store links here once each app is live.
  // While a link is empty, its button shows "Coming soon".
  var STORE_LINKS = {
    customer: { ios: "", android: "" },  // Jeetak customer app
    vendor:   { ios: "", android: "" },  // vendor app for restaurants and shops
    driver:   { ios: "", android: "" }   // driver app
  };

  var T = {
    en: {
      heroEyebrow: "Upper Metn · 21 villages",
      heroTitle: "From the village shop to your door.",
      heroLede: "Food, groceries and anything else nearby, ordered in one app. No calls. No voice notes.",
      storeSoon: "Coming soon on",
      storeLiveIos: "Download on the",
      storeLiveAndroid: "Get it on",
      storeNoteSoon: "The app is launching soon on iPhone and Android.",
      storeNoteLive: "Available now on iPhone and Android.",
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
      covTitle: "21 villages. One app.",
      covLede: "Jeetak delivers to all of these villages in the Upper Metn.",
      joinLink: "Join Jeetak",
      joinEyebrow: "Work with Jeetak",
      joinTitle: "Join Jeetak.",
      joinLede: "Own a restaurant or shop, or want to deliver? Download the app made for you and apply from your phone.",
      vendorKicker: "Restaurants & shops",
      vendorTitle: "Become a partner",
      vendorBody: "Get orders from customers across 21 villages. Accept and prepare them in the vendor app, and a Jeetak driver picks them up.",
      vendorApplySoon: "The vendor app is coming soon. You’ll download it and apply right here.",
      vendorApplyLive: "Download the vendor app and apply.",
      driverKicker: "Drivers",
      driverTitle: "Become a driver",
      driverBody: "Deliver orders around the Upper Metn and earn on every delivery. The driver app shows your deliveries and earnings.",
      driverApplySoon: "The driver app is coming soon. You’ll download it and apply right here.",
      driverApplyLive: "Download the driver app and apply.",
      ctaTitle: "Get Jeetak on your phone.",
      ctaBodySoon: "The app launches soon on iPhone and Android. The download links will appear right here.",
      ctaBodyLive: "Download the app and place your first order.",
      footCopy: "© 2026 Jeetak",
      langBtn: "عربي",
      langBtnLang: "ar",
      langAria: "اقرأ الصفحة بالعربي",
      docTitle: "Jeetak · Delivery across the Upper Metn"
    },
    ar: {
      heroEyebrow: "المتن الأعلى · 21 ضيعة",
      heroTitle: "من دكّانة الضيعة لعند بابك.",
      heroLede: "أكل، أغراض البيت، وكل شي بدّك ياه من المحلات اللي حدّك، بتطلبه من تطبيق واحد. بلا تلفونات، وبلا فويسات.",
      storeSoon: "قريباً على",
      storeLiveIos: "نزّلو من",
      storeLiveAndroid: "نزّلو من",
      storeNoteSoon: "التطبيق نازل قريباً على آيفون وأندرويد.",
      storeNoteLive: "التطبيق موجود هلّق على آيفون وأندرويد.",
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
      covTitle: "21 ضيعة. تطبيق واحد.",
      covLede: "جيتك بيوصل لكل هالضيع بالمتن الأعلى.",
      joinLink: "انضمّ لجيتك",
      joinEyebrow: "اشتغل مع جيتك",
      joinTitle: "انضمّ لجيتك.",
      joinLede: "عندك مطعم أو محل، أو بدّك تشتغل دليفري؟ نزّل التطبيق المخصّص إلك وقدّم طلبك من تلفونك.",
      vendorKicker: "مطاعم ومحلات",
      vendorTitle: "صير شريك",
      vendorBody: "وصّل محلّك لزباين بـ21 ضيعة. بتقبل الطلبيات وبتجهّزها من تطبيق المحلات، ودليفري جيتك بيمرق ياخدها.",
      vendorApplySoon: "تطبيق المحلات نازل قريباً، ورح تنزّلو وتقدّم طلبك من هون.",
      vendorApplyLive: "نزّل تطبيق المحلات وقدّم طلبك.",
      driverKicker: "سائقين",
      driverTitle: "اشتغل دليفري",
      driverBody: "وصّل طلبيات بالمتن الأعلى واربح عن كل توصيلة. تطبيق الدليفري بيورجيك توصيلاتك ومدخولك.",
      driverApplySoon: "تطبيق الدليفري نازل قريباً، ورح تنزّلو وتقدّم طلبك من هون.",
      driverApplyLive: "نزّل تطبيق الدليفري وقدّم طلبك.",
      ctaTitle: "نزّل جيتك على تلفونك.",
      ctaBodySoon: "التطبيق نازل قريباً على آيفون وأندرويد، وروابط التنزيل رح تكون هون.",
      ctaBodyLive: "نزّل التطبيق واطلب أوّل طلبية.",
      footCopy: "© 2026 جيتك",
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
      var live = isLive(el.getAttribute("data-app"));
      var value = dict[el.getAttribute("data-i18n-state") + (live ? "Live" : "Soon")];
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
    var t0 = null, raf = 0, running = false, inView = true;

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
      if (running || !inView || document.hidden) return;
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

  orderStores();
  initLanguage();
  initRoute();
  initStatus();
  initOverscroll();
})();
