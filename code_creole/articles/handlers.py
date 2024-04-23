from django.utils.translation import get_language 
def format_content(content):
    # Simple Python function to replace markdown code blocks with HTML
    content = content.replace("```python", "<pre class='code-block'><code>")
    content = content.replace("```", "</code></pre>")
    return content