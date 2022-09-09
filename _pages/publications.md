---
layout: archive
permalink: /publications/
author_profile: true
---

{% if author.googlescholar %}
  You can also find my articles on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>
{% endif %}

{% include base_path %}

{% assign show_preprints = false %}
{% for post in site.publications reversed %}
  {% if post.status == "in review" %}
    {% assign show_preprints = true %}
  {% endif %}
{% endfor %}

{% if show_preprints %}
Pre-prints
======
{% endif %}
{% for post in site.publications reversed %}
  {% if post.status == "in review" %}
    {% if post.include_on_website %}
      {% include publication-single.html %}
    {% endif %}
  {% endif %}
{% endfor %}

Peer-Reviewed Publications
======
{% for post in site.publications reversed %}
  {% if post.status == "published" or post.status == "to appear" or post.status == "accepted" %}
    {% unless post.type contains "thesis" %}
      {% if post.include_on_website %}
        {% include publication-single.html %}
      {% endif %}
    {% endunless %}
  {% endif %}
{% endfor %}

Theses
======
{% for post in site.publications reversed %}
  {% if post.type contains "thesis" %}
    {% if post.include_on_website %}
      {% include publication-single.html %}
    {% endif %}
  {% endif %}
{% endfor %}
