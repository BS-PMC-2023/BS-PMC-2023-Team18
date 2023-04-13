שם המערכת: Hike Buddy 

הסבר על המערכת: המערכת משמשת לתכנון טיולים, שכולל תכנון תקציבי ומסלול הטיול, תוך התחשבות בבטיחות המטיילים אופי המסלול והיעד.
במערכת קיימים שלושה סוגים של משתמשים: מטייל, מדריך טיולים ובעלי מלונות. 

דרישות לשימוש במערכת: המערכת מבוססת WEB לכן בכדי להשתמש במערכת צריך מכשיר סטנדרטי עם גישה לאינטרנט.

הפעלת המערכת: ניתן להפעיל את המערכת דרך ה-cmd. בשורת הכתובת של תיקיית Hike Buddy יש לכתוב את האותיות cmd ואז ללחוץ על מקש ה-Enter. לאחר מכן ייפתח חלון Command Prompt. בחלון זה יש לכתוב: python manage.py runserver

כדי ליצור משתמש Admin, יש לכתוב באותו החלון: python manage.py createsuperuser

איך משתמשים במערכת: בשלב הראשון המשתמש יירשם למערכת, שם הוא יקבע איזה סוג משתמש הוא: מטייל, מדריך טיולים, בעל מיקום אירוח.
לאחר מכן הוא ימלא את הפרטים הנוספים בהתאם לסוג משתמש. בשלב מתקדם יותר המטייל יזין למערכת את זמן הטיול, מיקום ותקציב והמערכת
תבנה לו מסלול טיולים בהתאם לנדרש.

תשתיות המערכת: המערכת נבנתה ב-Django סביבת Pycharm.

##############################################################

תפעול תקלות:
יש לוודא התקנת סביבת Python והבנייתה במערכת PATH של Windows.
יש לוודא התקנת django. כדי להתקין או לוודא התקנה, יש לפתוח חלון Command Prompt ובו לכתוב: pip install django

	1
במידה ומופיע הכיתוב:
ModuleNotFoundError: No module named 'crispy_forms'

יש לכתוב ב-Command Prompt:
pip install django-crispy-forms

במידה ומופיעה שגיאה דומה על אחד מהבאים, יש להתקין גם אותם באותו אופן:
python -m pip install geoip2
python -m pip install Pillow
python -m pip install django-filter
(או לעקוב אחר ההוראות המופיעות ב-CMD)

	2
במידה ומופיע הכיתוב:
Watching for file changes with StatReloader
Exception in thread django-main-thread:
...
או במידה ומופיע הכיתוב:
You have _ unapplied migration(s).
...

יש לכתוב ב-Command Prompt (בתוך תיקיית Hike Buddy):
python manage.py makemigrations
python manage.py migrate


לאחר תפעול תקלות יש לנסות להריץ בשנית:
בשורת הכתובת של תיקיית Hike Buddy יש לכתוב את האותיות cmd ואז ללחוץ על מקש ה-Enter. לאחר מכן ייפתח חלון Command Prompt. בחלון זה יש לכתוב:
python manage.py runserver

##############################################################
לבדיקת טסטים יש לכתוב ב-CMD בתיקיית HikeBuddy:
python manage.py test main.tests_urls.TestsURL