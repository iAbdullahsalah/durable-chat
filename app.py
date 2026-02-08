from js import Response, fetch
import json

async def on_fetch(request, env):
    # مسار الصفحة الرئيسية
    if request.method == "GET" and "/" in request.url:
        # جلب الأرشيف من D1
        try:
            # "DB" هو الاسم الذي اخترته في ملف wrangler.toml
            results = await env.DB.prepare("SELECT * FROM messages ORDER BY timestamp ASC").all()
            messages = results.results
        except Exception as e:
            messages = []

        # قراءة ملف index.html (تأكد من وجوده بجانب app.py)
        # ملاحظة: في الـ Workers يفضل وضع الـ HTML داخل الكود أو جلبها كـ Asset
        html_content = """... انسخ محتوى index.html هنا ..."""
        return Response.new(html_content, headers={"Content-Type": "text/html"})

    # مسار إرسال رسالة جديدة (أرشفة)
    if request.method == "POST" and "/send" in request.url:
        data = await request.json()
        content = data.get("content")
        
        # حفظ في D1
        await env.DB.prepare("INSERT INTO messages (content) VALUES (?)").bind(content).run()
        
        return Response.new(json.dumps({"status": "success"}), headers={"Content-Type": "application/json"})

    return Response.new("Not Found", status=404