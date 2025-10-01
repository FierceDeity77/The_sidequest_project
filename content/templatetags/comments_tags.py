from django import template

register = template.Library()

@register.inclusion_tag("content/comments/comment.html", takes_context=True) # inclusion tag lets you pass data to another template
def render_comment(context, comment, topic):
    return {"comment": comment,
            "topic": topic,  # passed the topic variable to the comment.html for the slug reverse
            "request": context["request"]} # to access request.user at every level,

    # in topic_detail.html loops thru top-level comments
    # for each calls {% render_comment comment %}
    # render_comment calls comments/comment.html via comment_tags.py with the current comment
    # comment.html renders the comment checks if it has children if yes then calls the same tag again

    # takes_context=True allows access to the full template context, including request object
    # "context" must be the first argument in the function when using takes_context=True
