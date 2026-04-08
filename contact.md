---
layout: page
title: Contact
permalink: /contact/
---

Use the form below to send a message to the BayRidge HOA board. We aim to respond within 3&ndash;5 business days.

<div class="info-box">
  <strong>Note:</strong> For urgent maintenance issues (e.g., broken gate, pool emergency),
  please contact our property management company directly.
</div>

<form class="contact-form" action="https://formspree.io/f/REPLACE_WITH_YOUR_FORM_ID" method="POST">
  <div class="form-group">
    <label for="name">Your Name</label>
    <input type="text" id="name" name="name" required placeholder="Jane Smith">
  </div>

  <div class="form-group">
    <label for="email">Email Address</label>
    <input type="email" id="email" name="email" required placeholder="jane@example.com">
  </div>

  <div class="form-group">
    <label for="unit">Unit / Address (optional)</label>
    <input type="text" id="unit" name="unit" placeholder="e.g., 3412-A BayRidge Dr">
  </div>

  <div class="form-group">
    <label for="subject">Subject</label>
    <input type="text" id="subject" name="subject" required placeholder="e.g., Pool maintenance concern">
  </div>

  <div class="form-group">
    <label for="message">Message</label>
    <textarea id="message" name="message" required placeholder="Describe your question or concern..."></textarea>
  </div>

  <button type="submit" class="btn btn-primary">Send Message</button>
  <p class="form-note">Your message is sent securely via Formspree. You will receive a confirmation email.</p>
</form>
