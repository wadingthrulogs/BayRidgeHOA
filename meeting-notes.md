---
layout: page
title: Meeting Notes
permalink: /meeting-notes/
---

Board meeting notes are published monthly after each meeting. Click any entry to read the full notes.

<ul class="post-list">
  {% for post in site.posts %}
    <li class="post-list-item">
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
      <span class="post-list-date">{{ post.date | date: "%B %Y" }}</span>
    </li>
  {% endfor %}

  {% if site.posts.size == 0 %}
    <li class="post-list-item">No meeting notes have been posted yet.</li>
  {% endif %}
</ul>
