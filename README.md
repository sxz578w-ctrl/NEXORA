# NEXORA — نيكسورا

**الشعار:** عوالم متحدة  
**المنصة المستهدفة:** Android  
**المحرك:** Godot 4.x  
**لغة الواجهة:** العربية مع RTL  
**اتجاه العرض الافتراضي:** عمودي (Portrait)

## حالة المشروع

هذا المستودع يحتوي على حزمة المصدر الكاملة لمشروع Godot، محفوظة في أرشيف مضغوط ومجزأ إلى أجزاء نصية داخل `bundle/parts/` لتجاوز قيود نقل الملفات الثنائية في واجهة GitHub المستخدمة أثناء الاستيراد. تجميع الأجزاء وفك الأرشيف وتطبيق تصحيحات المصدر المراجَعة يتم محلياً أو في GitHub Actions بواسطة `scripts/assemble-source.sh`.

**النواة الحالية:**
- واجهة عربية أولية بخمسة تبويبات.
- حملة من 7 مناطق و70 مرحلة.
- أنظمة أولية للبطاقات والندرة والدمج والقتال والمكافآت والجذور.
- حفظ محلي مع نسخ احتياطية واستعادة المواجهة.
- 16 اختبار GDScript وفحص Python ساكن من 113 تحققاً.

هذه حزمة تأسيسية قابلة للتطوير وليست إصداراً نهائياً. لا يوجد حالياً ملف APK منشور أو إعداد Android Export موقّع. لا تدّعي نتائج الفحص الساكن وحدها سلامة التشغيل على جهاز فعلي.

## تجميع المشروع وتشغيله محلياً

المتطلبات: Bash، و`base64`، و`gzip`، و`tar`، وPython 3، وGodot 4.x.

```bash
./scripts/assemble-source.sh
cd .nexora-build/source/NEXORA_Godot
python3 tests/static_contract_check.py
godot --headless --editor --path . --quit
godot --headless --path . --script res://tests/run_tests.gd
```

بعد ذلك افتح مجلد `.nexora-build/source/NEXORA_Godot` في Godot واضغط F5.

## التحقق الآلي في GitHub

ملف `.github/workflows/ci.yml` يعيد تجميع المصدر، ويختبر طبقة التصحيحات، ويشغّل فحص Python الساكن، ويثبّت Godot 4.7.0 على runner، ويجري فحص استيراد/تحليل المشروع ثم يشغّل اختبارات GDScript. عند نجاح جميع الخطوات، يرفع نسخة المصدر المجمّعة كـ Actions artifact.

## بنية المستودع

```text
bundle/parts/             أجزاء أرشيف المصدر المضغوط
scripts/assemble-source.sh تجميع وفحص وفك أرشيف المصدر
.github/workflows/ci.yml  فحوصات GitHub Actions
docs/                      وثائق الاستيراد والبناء
```

## Android والتوقيع

تصدير Android يحتاج قوالب Godot المطابقة، وAndroid SDK، وJDK، وإعداد تصدير Android. يجب إنشاء مفاتيح التوقيع خارج المستودع وإضافتها إلى GitHub Secrets عند إعداد إصدار Release. لا ترفع ملفات keystore أو كلمات المرور أو مفاتيح API إلى Git.

يُعتمد APK فقط بعد نجاح التصدير واختباره على جهاز Android فعلي.
