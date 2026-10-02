"""Food items that pop up from under the footer, drawn in a 100 x 100 box with the base at the bottom."""

FOOD = [
    ("manoushe", """
      <g transform="rotate(-14 50 66)">
        <ellipse class="ol c-crust" cx="50" cy="68" rx="42" ry="29"/>
        <ellipse class="c-dough" cx="50" cy="64.5" rx="40.5" ry="26"/>
        <ellipse class="c-zaatar" cx="50" cy="63" rx="31" ry="18.5"/>
        <g class="c-zaatar-dark"><circle cx="38" cy="60" r="2"/><circle cx="47" cy="68" r="1.8"/><circle cx="55" cy="57" r="2.1"/>
          <circle cx="63" cy="66" r="1.8"/><circle cx="70" cy="60" r="1.6"/><circle cx="43" cy="53" r="1.4"/><circle cx="58" cy="73" r="1.5"/></g>
        <g class="c-cream"><ellipse cx="44" cy="58" rx="1.8" ry="1"/><ellipse cx="60" cy="61" rx="1.8" ry="1"/><ellipse cx="51" cy="66" rx="1.8" ry="1"/>
          <ellipse cx="66" cy="70" rx="1.8" ry="1"/><ellipse cx="36" cy="66" rx="1.8" ry="1"/></g>
      </g>"""),
    ("shawarma", """
      <path class="ol c-cream" d="M29 42 C29 35 71 35 71 42 L65 101 H35 Z"/>
      <path class="ln ln-soft" d="M38 54 L62 49 M37 62 L63 56"/>
      <path class="ol c-kraft" d="M32.3 72 L68 62 L65 101 H35 Z"/>
      <path class="ol c-herb" d="M28 43 C28 35 34 30 41 32 C45 24 56 24 60 31 C67 29 73 35 72 43 C63 39 37 39 28 43 Z"/>
      <circle class="c-tomato" cx="43" cy="35" r="3.6"/><circle class="c-tomato" cx="57" cy="34" r="3"/>
      <circle class="c-crust" cx="50" cy="31" r="3.2"/>"""),
    ("coffee", """
      <path class="steam-line" d="M44 21 C40 15 48 11 44 4"/>
      <path class="steam-line s2" d="M56 21 C52 15 60 11 56 4"/>
      <path class="ol c-cream" d="M31 37 H69 L63 101 H37 Z"/>
      <path class="ol c-pine" d="M33.5 57 H66.5 L64.6 79 H35.4 Z"/>
      <svg x="45" y="60.5" width="10" height="12.8" viewBox="0 0 {PIN_W} {PIN_H}"><use href="#jk-pin" class="c-bag-lit"/></svg>
      <rect class="ol c-white" x="27" y="29" width="46" height="10" rx="4"/>
      <rect class="ol c-white" x="34" y="23" width="32" height="7" rx="3.5"/>"""),
    ("kaak", """
      <path class="ol c-dough" fill-rule="evenodd" d="M50 12 C67 12 78 25 77 41 C88 53 89 84 71 93 C60 98 40 98 29 93 C11 84 12 53 23 41 C22 25 33 12 50 12 Z M50 24 C59 24 64.5 31 63.5 40 C57 38 43 38 36.5 40 C35.5 31 41 24 50 24 Z"/>
      <path class="c-crust" d="M22 78 C30 92 70 92 78 78 C74 88 26 88 22 78 Z"/>
      <g class="c-cream"><ellipse cx="34" cy="56" rx="2" ry="1.1" transform="rotate(-20 34 56)"/><ellipse cx="45" cy="50" rx="2" ry="1.1"/>
        <ellipse cx="58" cy="52" rx="2" ry="1.1" transform="rotate(25 58 52)"/><ellipse cx="68" cy="60" rx="2" ry="1.1"/>
        <ellipse cx="40" cy="68" rx="2" ry="1.1" transform="rotate(30 40 68)"/><ellipse cx="53" cy="64" rx="2" ry="1.1"/>
        <ellipse cx="64" cy="74" rx="2" ry="1.1" transform="rotate(-25 64 74)"/><ellipse cx="30" cy="40" rx="2" ry="1.1" transform="rotate(-50 30 40)"/>
        <ellipse cx="70" cy="40" rx="2" ry="1.1" transform="rotate(50 70 40)"/><ellipse cx="50" cy="17.5" rx="2" ry="1.1"/></g>"""),
    ("watermelon", """
      <path class="ol c-herb-dark" d="M50 9 L91 70 Q50 106 9 70 Z"/>
      <path class="c-cream" d="M50 16 L85 68 Q50 98 15 68 Z"/>
      <path class="c-melon" d="M50 21 L81 66 Q50 92 19 66 Z"/>
      <g class="c-seed"><ellipse cx="50" cy="44" rx="1.8" ry="3"/><ellipse cx="40" cy="58" rx="1.8" ry="3" transform="rotate(-15 40 58)"/>
        <ellipse cx="60" cy="58" rx="1.8" ry="3" transform="rotate(15 60 58)"/><ellipse cx="50" cy="68" rx="1.8" ry="3"/>
        <ellipse cx="31" cy="68" rx="1.8" ry="3" transform="rotate(-25 31 68)"/><ellipse cx="69" cy="68" rx="1.8" ry="3" transform="rotate(25 69 68)"/></g>"""),
    ("water", """
      <rect class="ol c-water" x="22" y="40" width="56" height="64" rx="14"/>
      <path class="ol c-water" d="M40 41 V30 H60 V41"/>
      <rect class="ol c-pine" x="36.5" y="20" width="27" height="11" rx="3"/>
      <path class="ln ln-water" d="M24 58 H76 M24 76 H76"/>
      <rect class="c-white" x="29" y="47" width="6" height="36" rx="3" opacity="0.75"/>"""),
    ("booza", """
      <path class="ol c-kraft" d="M33 55 L50 102 L67 55 Z"/>
      <path class="ln ln-crust" d="M40 62 L56 86 M48 58 L62 72 M60 62 L44 86 M52 58 L38 72"/>
      <path class="ol c-herb" d="M28 57 C23 41 35 31 50 32 C65 31 77 41 72 57 C66 62 60 55 55 60 C49 55 43 62 37 58 Z"/>
      <g class="c-herb-dark"><ellipse cx="40" cy="46" rx="2.4" ry="1.5" transform="rotate(-20 40 46)"/><ellipse cx="55" cy="42" rx="2.4" ry="1.5"/>
        <ellipse cx="62" cy="51" rx="2.4" ry="1.5" transform="rotate(25 62 51)"/><ellipse cx="48" cy="52" rx="2.4" ry="1.5"/></g>
      <circle class="ol c-cream" cx="51" cy="24" r="11.5"/>
      <path class="c-white" d="M45 20 C46 16 50 15 52 16 C49 17 47 19 46.5 22 Z" opacity="0.8"/>"""),
    ("groceries", """
      <rect class="ol c-dough" x="53" y="12" width="13" height="52" rx="6.5" transform="rotate(14 59.5 38)"/>
      <path class="ln ln-crust" d="M58 22 L64 20 M57 31 L63 29 M56 40 L62 38" transform="rotate(14 59.5 38)"/>
      <circle class="ol c-herb" cx="37" cy="44" r="10"/>
      <circle class="ol c-herb" cx="46" cy="38" r="10.5"/>
      <path class="ln" d="M41 50 L44 40" opacity="0.45"/>
      <path class="ol c-kraft" d="M25 50 H75 L71 102 H29 Z"/>
      <path class="c-kraft-dark" d="M26.6 51.6 H73.4 L72.9 58 H27.1 Z"/>"""),
]
