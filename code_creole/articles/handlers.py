from django.utils.translation import get_language 
def format_content(content):
    # Simple Python function to replace markdown code blocks with HTML
    content = content.replace("<code-block>", "<pre class='code-block'><code>")
    content = content.replace("</code-block>", "</code></pre>")
    content = content.replace("<inline-code>", "<span class='inline-code'>")
    content = content.replace("</inline-code>", "</span>")
    return content