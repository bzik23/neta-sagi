# -*- coding: utf-8 -*-
"""Build lp/privacy.html and lp/accessibility.html for the Neta Sagi landing page.

The pages reuse the landing page's own <style>, header and footer (sliced from lp/index.html at
build time), so they always match the current design. Run after any change to index.html:
    python _tools/build_legal.py
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LP = os.path.join(ROOT, "lp")
INDEX = os.path.join(LP, "index.html")

src = io.open(INDEX, encoding="utf-8").read()
style = re.search(r"<style>.*?</style>", src, re.S).group(0)
head_links = re.search(r'<link rel="icon".*?(?=<style>)', src, re.S).group(0).strip()
header = re.search(r"<header class=\"top\">.*?</header>", src, re.S).group(0)
footer = re.search(r"<footer class=\"site\">.*?</footer>", src, re.S).group(0)
# the self-contained accessibility widget (markup + its own script) rides along with the footer
a11y = re.search(r"<!-- a11y -->.*?<!-- /a11y -->", src, re.S).group(0)
# the legal pages live beside index.html, so relative asset paths stay valid; brand links go home
header = header.replace('href="#top"', 'href="index.html"')

LEGAL_CSS = """
<style>
/* legal pages */
.legal{position:relative;z-index:1;padding:128px 0 64px;background:linear-gradient(180deg,var(--sky-3) 0,#fff 220px)}
.legal .wrap{max-width:820px}
.legal h1{font-size:clamp(2rem,4vw,2.8rem);margin-bottom:6px}
.legal .meta{color:var(--muted);font-size:.9rem;margin:0 0 26px}
.legal h2{font-size:1.3rem;margin:30px 0 8px;color:var(--blue-d)}
.legal p,.legal li{line-height:1.75;color:var(--text);margin:0 0 10px}
.legal ul,.legal ol{padding-inline-start:22px;margin:0 0 12px}
.legal li{margin-bottom:6px}
.legal a{color:var(--blue);text-decoration:underline;text-underline-offset:2px}
.legal .box{background:var(--sky-2);border:1px solid var(--sky);border-radius:var(--radius);padding:16px 18px;margin:18px 0}
.legal .back{display:inline-flex;align-items:center;gap:8px;margin-top:30px;font-weight:700;text-decoration:none}
.legal .back svg{width:18px;height:18px}
@media (max-width:720px){.top{display:block}.legal{padding-top:104px}} /* the landing page hides the header on phones; here it is the way back home */
</style>
"""

BACK = ('<a class="back" href="index.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
        'stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>חזרה לעמוד הראשי</a>')

def page(title, desc, body, slug):
    html = f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | נטע שגיא</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, follow">
{head_links}
{style}
{LEGAL_CSS}
</head>
<body>

{header}

<main class="legal" id="top">
  <div class="wrap">
{body}
    {BACK}
  </div>
</main>

{footer}

{a11y}

</body>
</html>
"""
    out = os.path.join(LP, slug)
    io.open(out, "w", encoding="utf-8", newline="\n").write(html)
    print("wrote", out, len(html), "chars")

# --------------------------------------------------------------------------------------
PRIVACY = """
    <h1>מדיניות פרטיות</h1>
    <p class="meta">עודכן לאחרונה: 8 באוקטובר 2026</p>

    <p>נטע שגיא - חקירות, מודיעין ופוליגרף (ח.פ. 516910031), להלן "המשרד" או "אנחנו", מכבדת את פרטיותכם. מסמך זה מסביר איזה מידע נאסף באתר זה, לאיזו מטרה, כיצד הוא נשמר ואילו זכויות יש לכם. השימוש באתר ומסירת פרטים דרכו מהווים הסכמה למדיניות זו. המדיניות מנוסחת בלשון רבים מטעמי נוחות ומופנית לכל המגדרים.</p>

    <div class="box"><p style="margin:0"><strong>בקצרה:</strong> אנחנו אוספים רק את מה שצריך כדי לחזור אליכם לשיחת ייעוץ. הפרטים לא נמכרים ולא מועברים לגורמים מפרסמים. הפנייה והשיחה מטופלות בסודיות מוחלטת, כמתחייב מרישיון משרד המשפטים למשרד חקירות פרטיות.</p></div>

    <h2>1. איזה מידע נאסף</h2>
    <ul>
      <li><strong>פרטים שאתם מוסרים בטופס הפנייה:</strong> שם (אפשר שם פרטי בלבד) ומספר טלפון לחזרה, וכן אישורכם למדיניות זו. מסירת הפרטים היא רצונית, אך בלי שם וטלפון לא נוכל לחזור אליכם.</li>
      <li><strong>פנייה בטלפון או בוואטסאפ:</strong> כשאתם לוחצים על כפתור חיוג או וואטסאפ, השיחה או ההתכתבות מתנהלות מול המשרד ישירות. התכתבות בוואטסאפ כפופה גם למדיניות הפרטיות של WhatsApp.</li>
      <li><strong>מידע טכני וסטטיסטי:</strong> בעת הגלישה נאספים אוטומטית נתונים כגון כתובת IP, סוג דפדפן ומכשיר, עמודי מקור, זמני ביקור ופעולות באתר (למשל לחיצה על כפתור חיוג). מידע זה נאסף באמצעות כלי מדידה (ראו סעיף 4) ואינו מזהה אתכם בשמכם.</li>
    </ul>

    <h2>2. למה אנחנו משתמשים במידע</h2>
    <ul>
      <li>כדי לחזור אליכם לשיחת ייעוץ ראשונית ולהבין את הצורך שלכם.</li>
      <li>כדי לתת את השירות שביקשתם, אם תחליטו להמשיך איתנו, ולנהל את הקשר השוטף.</li>
      <li>כדי לשפר את האתר ואת אופן הפנייה אלינו, על בסיס נתונים סטטיסטיים מצטברים.</li>
      <li>כדי לעמוד בחובות על פי דין, לרבות הדין החל על משרדי חקירות פרטיות.</li>
    </ul>
    <p>לא נשלח אליכם הודעות שיווקיות, דיוור או הודעות וואטסאפ לפני שדיברנו, ולא נוסיף אתכם לרשימות תפוצה בלי הסכמה מפורשת.</p>

    <h2>3. העברת מידע לאחרים</h2>
    <p>הפרטים שלכם אינם נמכרים ואינם מועברים לגורמים מסחריים. המידע עשוי להיות נגיש לספקים שמפעילים עבורנו את האתר ואת התשתיות (אחסון, שירותי מדידה), וזאת רק לצורך מתן השירות ובכפוף להתחייבויות סודיות. נמסור מידע לרשויות רק כשהדין מחייב זאת, למשל מכוח צו שיפוטי.</p>

    <h2>4. עוגיות וכלי מדידה</h2>
    <p>האתר משתמש ב-Google Analytics ו-Google Tag Manager כדי למדוד תנועה ופעולות באתר (לחיצות על חיוג, וואטסאפ ושליחת טופס). כלים אלה עשויים להציב קובצי עוגיות (Cookies) בדפדפן שלכם. אפשר לחסום או למחוק עוגיות דרך הגדרות הדפדפן, והאתר ימשיך לפעול. אם תחסמו עוגיות, ייתכן שחלק מהמדידות לא יתבצעו.</p>

    <h2>5. אבטחת מידע</h2>
    <p>אנחנו נוקטים אמצעים סבירים ומקובלים כדי להגן על המידע מפני גישה לא מורשית, אובדן או שימוש לרעה, לרבות תקשורת מוצפנת (HTTPS) והגבלת הגישה לפרטי הפונים לצוות המשרד בלבד. עם זאת, אין אמצעי אבטחה מושלם, ואיננו יכולים להבטיח חסינות מוחלטת.</p>

    <h2>6. משך שמירת המידע</h2>
    <p>פרטי פנייה שלא הבשילה לשירות נשמרים לתקופה סבירה הנדרשת לחזרה אליכם ולתיעוד, ולאחר מכן נמחקים. מידע הקשור לשירות שניתן נשמר כנדרש על פי דין ולצורכי הגנה משפטית.</p>

    <h2>7. הזכויות שלכם</h2>
    <p>בהתאם לחוק הגנת הפרטיות, התשמ״א-1981, ולתקנות מכוחו, אתם רשאים לבקש לעיין במידע שנשמר עליכם, לתקן אותו, או לבקש את מחיקתו, בכפוף למגבלות הדין. לצורך כך פנו אלינו בפרטים שבסעיף 10, ונטפל בבקשה בתוך זמן סביר.</p>

    <h2>8. קטינים</h2>
    <p>האתר והשירות מיועדים לבגירים. אם נדע שנמסרו לנו פרטים של קטין ללא אישור הורה או אפוטרופוס, נמחק אותם.</p>

    <h2>9. שינויים במדיניות</h2>
    <p>אנחנו עשויים לעדכן מדיניות זו מעת לעת. הנוסח המחייב הוא זה המפורסם בעמוד זה, ותאריך העדכון האחרון מופיע בראשו.</p>

    <h2>10. יצירת קשר</h2>
    <p>לכל שאלה או בקשה בנושא פרטיות: נטע שגיא - חקירות, מודיעין ופוליגרף, טלפון <a href="tel:0506023000" dir="ltr">050-602-3000</a>, דוא״ל <a href="mailto:neta.sagi.pi@gmail.com">neta.sagi.pi@gmail.com</a>.</p>
"""

ACCESS = """
    <h1>הצהרת נגישות</h1>
    <p class="meta">עודכן לאחרונה: 8 באוקטובר 2026</p>

    <p>נטע שגיא - חקירות, מודיעין ופוליגרף רואה חשיבות רבה במתן שירות שוויוני לכל אדם, לרבות אנשים עם מוגבלות, ופועלת להנגשת האתר כך שכל אדם יוכל לגלוש בו בנוחות ולפנות אלינו בקלות. הצהרה זו מתייחסת לאתר זה.</p>

    <h2>1. תקן הנגישות</h2>
    <p>האתר הונגש בהתאם לתקנות שוויון זכויות לאנשים עם מוגבלות (התאמות נגישות לשירות), התשע״ג-2013, ולתקן הישראלי ת״י 5568, המבוסס על הנחיות WCAG 2.0 ברמה AA של ארגון W3C. ההנגשה מכוונת לפעולה תקינה בדפדפנים הנפוצים ובטכנולוגיות מסייעות כגון קוראי מסך.</p>

    <h2>2. התאמות הנגישות שבוצעו באתר</h2>
    <ul>
      <li>מבנה עמוד סמנטי: כותרות מדורגות, אזורי ניווט ותוכן מסומנים, ותיאור טקסטואלי (alt) לתמונות משמעותיות.</li>
      <li>ניווט מלא במקלדת, עם סימון מיקוד ברור על קישורים, כפתורים ושדות טופס.</li>
      <li>ניגודיות צבעים העומדת בדרישות התקן בין הטקסט לרקע.</li>
      <li>טקסט ניתן להגדלה באמצעות הדפדפן ללא פגיעה בתוכן או בתפקוד.</li>
      <li>שדות הטופס מלווים בתוויות ברורות ובהודעות שגיאה מובנות.</li>
      <li>הפחתת תנועה: אנימציות באתר, לרבות וידאו רקע, מושבתות או מצומצמות כשמופעלת בהעדפות המערכת האפשרות "הפחתת תנועה".</li>
      <li>וידאו הרקע בעמוד הראשי אינו כולל שמע ואינו נושא מידע הכרחי, ולכן אינו דורש כתוביות; תוכן העמוד מוצג במלואו כטקסט.</li>
      <li>האתר מותאם לצפייה במחשב, בטאבלט ובטלפון נייד.</li>
      <li>קישור "דלגו לתוכן" בראש העמוד למשתמשי מקלדת וקורא מסך.</li>
      <li><strong>תפריט נגישות</strong> (הכפתור העגול בצד שמאל של המסך) המאפשר: הגדלת טקסט בשתי דרגות, ניגודיות גבוהה, גווני אפור, הדגשת קישורים, פונט קריא, ריווח טקסט, עצירת אנימציות ווידאו, וסמן עכבר גדול. ההגדרות נשמרות בדפדפן לביקורים הבאים וניתנות לאיפוס בלחיצה אחת. התפריט נפתח ונסגר גם במקלדת (Esc לסגירה).</li>
    </ul>

    <h2>3. דרכי פנייה חלופיות</h2>
    <p>אם נתקלתם בקושי להשתמש בטופס שבאתר, אפשר לפנות אלינו בטלפון או בהודעת וואטסאפ בכל שלב, ונשמח לסייע ולתאם את השיחה בדרך הנוחה לכם.</p>

    <h2>4. סייגים</h2>
    <p>למרות מאמצינו להנגיש את כל עמודי האתר, ייתכן שחלקים מסוימים טרם הונגשו במלואם, או שתכנים של צדדים שלישיים (למשל שירות WhatsApp) אינם בשליטתנו. אנחנו ממשיכים לשפר את נגישות האתר באופן שוטף.</p>

    <h2>5. פנייה בנושא נגישות - רכזת הנגישות</h2>
    <p>אם מצאתם רכיב שאינו נגיש, או שיש לכם הצעה לשיפור, נשמח לשמוע. אנא ציינו את תיאור הבעיה, הפעולה שניסיתם לבצע, הדפדפן והטכנולוגיה המסייעת שבהם השתמשתם, ונטפל בפנייה בהקדם.</p>
    <div class="box">
      <p style="margin:0 0 6px"><strong>רכזת הנגישות:</strong> נטע שגיא</p>
      <p style="margin:0 0 6px"><strong>טלפון:</strong> <a href="tel:0506023000" dir="ltr">050-602-3000</a></p>
      <p style="margin:0"><strong>דוא״ל:</strong> <a href="mailto:neta.sagi.pi@gmail.com">neta.sagi.pi@gmail.com</a></p>
    </div>
"""

page("מדיניות פרטיות", "מדיניות הפרטיות של אתר נטע שגיא - חקירות, מודיעין ופוליגרף: איזה מידע נאסף, למה, וכיצד הוא נשמר.", PRIVACY, "privacy.html")
page("הצהרת נגישות", "הצהרת הנגישות של אתר נטע שגיא - חקירות, מודיעין ופוליגרף: התקן, ההתאמות שבוצעו ודרכי פנייה.", ACCESS, "accessibility.html")
