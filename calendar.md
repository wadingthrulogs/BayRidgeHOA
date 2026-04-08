---
layout: page
title: Calendar
permalink: /calendar/
---

Upcoming HOA meetings and community events. Board meetings are held the **first Tuesday of each month at 6:30 PM** in the Clubhouse.

<ul class="event-list">
  {% for event in site.data.events %}
    <li class="event-item">
      <div class="event-date-badge">
        <div class="event-date-month">{{ event.date | date: "%b" }}</div>
        <div class="event-date-day">{{ event.date | date: "%-d" }}</div>
      </div>
      <div class="event-details">
        <h3>{{ event.title }}</h3>
        {% if event.time %}<div class="event-time">{{ event.time }}</div>{% endif %}
        {% if event.location %}<p>&#x1F4CD; {{ event.location }}</p>{% endif %}
        {% if event.description %}<p>{{ event.description }}</p>{% endif %}
      </div>
    </li>
  {% endfor %}

  {% if site.data.events.size == 0 %}
    <li class="event-item">No upcoming events scheduled.</li>
  {% endif %}
</ul>

<div class="info-box">
  All board meetings are open to BayRidge residents. If you would like to add an agenda item,
  please <a href="{{ '/contact/' | relative_url }}">contact the board</a> at least one week before the meeting.
</div>
