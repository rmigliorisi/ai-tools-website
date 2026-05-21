<?php
/**
 * Template Name: Contact Page
 *
 * @package AIFP
 */

get_header();
$ajax_url = esc_url(admin_url('admin-ajax.php'));
$nonce    = wp_create_nonce('aifp_contact');
?>

<main style="background:#f9f9f9;">

  <!-- HERO -->
  <section style="padding:min(5rem,7vw) min(6.5rem,8vw) min(3rem,4vw);">
    <div style="max-width:760px;">
      <h1 class="font-heading" style="font-size:clamp(2.4rem,5vw,3.6rem);font-weight:700;line-height:1.08;color:#111111;margin:0 0 20px;">
        Contact AI Tools for Pros
      </h1>
      <p style="font-size:15px;color:#636363;line-height:1.75;margin:0;">
        Use the form below to suggest a tool for review, ask about SEO and AI search consulting, explore a partnership, or send a general question.
        Learn more <a href="<?php echo esc_url(home_url('/about-us')); ?>" style="color:#2563EB;text-decoration:none;">about us</a> and
        <a href="<?php echo esc_url(home_url('/our-process')); ?>" style="color:#2563EB;text-decoration:none;">how we review tools</a> before reaching out.
      </p>
    </div>
  </section>

  <!-- INFO CARDS -->
  <section style="padding:0 min(6.5rem,8vw) min(4rem,5vw);">
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px;max-width:900px;margin-bottom:52px;">

      <div style="background:#ffffff;border:1px solid #f0f0f0;border-radius:12px;padding:28px 30px;">
        <div style="font-size:9px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#2563EB;margin-bottom:12px;">Tool Reviews</div>
        <h2 class="font-heading" style="font-size:19px;font-weight:700;color:#111111;margin:0 0 10px;">Suggest an AI Tool for Review</h2>
        <p style="font-size:13px;color:#636363;line-height:1.75;margin:0;">We evaluate AI tools across ten professions. If you use a tool we have not covered, tell us about it. Include what it does, who it is built for, and why it belongs on this site. We read every suggestion.</p>
      </div>

      <div style="background:#ffffff;border:1px solid #f0f0f0;border-radius:12px;padding:28px 30px;">
        <div style="font-size:9px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#2563EB;margin-bottom:12px;">Consulting</div>
        <h2 class="font-heading" style="font-size:19px;font-weight:700;color:#111111;margin:0 0 10px;">SEO &amp; AI Search Consulting</h2>
        <p style="font-size:13px;color:#636363;line-height:1.75;margin:0;">Rich Migliorisi works with professional services firms on organic visibility, AI-ready content architecture, and search strategy. If you want to grow traffic from both traditional and AI-driven search, start a conversation below.</p>
      </div>

    </div>

    <!-- CONTACT FORM -->
    <div style="max-width:620px;">

      <div id="aifp-contact-form-wrap">
        <h2 class="font-heading" style="font-size:22px;font-weight:700;color:#111111;margin:0 0 8px;">Send a Message</h2>
        <p style="font-size:13px;color:#636363;margin:0 0 32px;">All fields are required except Company, Website, or Tool URL.</p>

        <form id="aifp-contact-form" novalidate style="display:flex;flex-direction:column;gap:20px;">

          <!-- Honeypot: hidden from humans, filled by bots -->
          <div style="position:absolute;left:-9999px;top:-9999px;" aria-hidden="true">
            <label for="aifp-hp">Leave this field blank</label>
            <input type="text" id="aifp-hp" name="hp_field" tabindex="-1" autocomplete="off" value="">
          </div>

          <div>
            <label for="aifp-name" style="display:block;font-size:12px;font-weight:600;color:#374151;margin-bottom:6px;letter-spacing:0.03em;">Name</label>
            <input type="text" id="aifp-name" name="contact_name" autocomplete="name"
              style="width:100%;box-sizing:border-box;background:#ffffff;color:#111111;font-size:14px;padding:12px 16px;border-radius:8px;border:1px solid #d1d5db;outline:none;font-family:'Inter',sans-serif;"
              placeholder="Your name">
          </div>

          <div>
            <label for="aifp-email" style="display:block;font-size:12px;font-weight:600;color:#374151;margin-bottom:6px;letter-spacing:0.03em;">Email</label>
            <input type="email" id="aifp-email" name="contact_email" autocomplete="email"
              style="width:100%;box-sizing:border-box;background:#ffffff;color:#111111;font-size:14px;padding:12px 16px;border-radius:8px;border:1px solid #d1d5db;outline:none;font-family:'Inter',sans-serif;"
              placeholder="you@yourcompany.com">
          </div>

          <div>
            <label for="aifp-company" style="display:block;font-size:12px;font-weight:600;color:#374151;margin-bottom:6px;letter-spacing:0.03em;">
              Company, Website, or Tool URL <span style="font-weight:400;color:#9ca3af;">(optional)</span>
            </label>
            <input type="text" id="aifp-company" name="contact_company"
              style="width:100%;box-sizing:border-box;background:#ffffff;color:#111111;font-size:14px;padding:12px 16px;border-radius:8px;border:1px solid #d1d5db;outline:none;font-family:'Inter',sans-serif;"
              placeholder="Acme Corp or https://example.com">
          </div>

          <div>
            <label for="aifp-reason" style="display:block;font-size:12px;font-weight:600;color:#374151;margin-bottom:6px;letter-spacing:0.03em;">Reason for Reaching Out</label>
            <select id="aifp-reason" name="contact_reason"
              style="width:100%;box-sizing:border-box;background:#ffffff;color:#111111;font-size:14px;padding:12px 16px;border-radius:8px;border:1px solid #d1d5db;outline:none;font-family:'Inter',sans-serif;cursor:pointer;">
              <option value="">Select a reason</option>
              <option value="Suggest an AI tool for review">Suggest an AI tool for review</option>
              <option value="SEO / AI search consulting">SEO / AI search consulting</option>
              <option value="Partnership or media inquiry">Partnership or media inquiry</option>
              <option value="General question">General question</option>
            </select>
          </div>

          <div>
            <label for="aifp-message" style="display:block;font-size:12px;font-weight:600;color:#374151;margin-bottom:6px;letter-spacing:0.03em;">Message</label>
            <textarea id="aifp-message" name="contact_message" rows="6"
              style="width:100%;box-sizing:border-box;background:#ffffff;color:#111111;font-size:14px;padding:12px 16px;border-radius:8px;border:1px solid #d1d5db;outline:none;font-family:'Inter',sans-serif;resize:vertical;line-height:1.6;"
              placeholder="Tell us what's on your mind."></textarea>
          </div>

          <p id="aifp-contact-error" role="alert" aria-live="polite" style="display:none;color:#dc2626;font-size:13px;margin:0;line-height:1.6;"></p>

          <div>
            <button type="submit" id="aifp-contact-btn"
              style="background:#111111;color:#ffffff;font-size:14px;font-weight:500;padding:13px 28px;border-radius:999px;border:none;cursor:pointer;font-family:'Inter',sans-serif;"
              onmouseover="if(!this.disabled)this.style.background='#2563EB'" onmouseout="if(!this.disabled)this.style.background='#111111'">Send Message</button>
          </div>

        </form>
      </div>

      <p id="aifp-contact-success" role="status" style="display:none;color:#059669;font-size:15px;font-weight:500;line-height:1.75;margin:0;padding:24px;background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;"></p>

      <p style="font-size:13px;color:#636363;margin:32px 0 0;">
        Looking for our newsletter? <a href="<?php echo esc_url(home_url('/newsletter')); ?>" style="color:#2563EB;text-decoration:none;">Subscribe here.</a>
      </p>

    </div>
  </section>

</main>

<script>
(function(){
  var form  = document.getElementById('aifp-contact-form');
  var btn   = document.getElementById('aifp-contact-btn');
  var errEl = document.getElementById('aifp-contact-error');
  var okEl  = document.getElementById('aifp-contact-success');
  var wrap  = document.getElementById('aifp-contact-form-wrap');
  if (!form) return;

  form.addEventListener('submit', function(e) {
    e.preventDefault();
    errEl.style.display = 'none';

    var name    = document.getElementById('aifp-name').value.trim();
    var email   = document.getElementById('aifp-email').value.trim();
    var company = document.getElementById('aifp-company').value.trim();
    var reason  = document.getElementById('aifp-reason').value;
    var message = document.getElementById('aifp-message').value.trim();
    var hp      = document.getElementById('aifp-hp').value;

    if (!name)    { showErr('Please enter your name.'); return; }
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { showErr('Please enter a valid email address.'); return; }
    if (!reason)  { showErr('Please select a reason for reaching out.'); return; }
    if (!message) { showErr('Please enter a message.'); return; }

    btn.disabled = true;
    btn.textContent = 'Sending…';
    btn.style.background = '#6b7280';

    fetch('<?php echo $ajax_url; ?>', {
      method: 'POST',
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: 'action=aifp_contact'
          + '&nonce='   + encodeURIComponent('<?php echo esc_js($nonce); ?>')
          + '&hp='      + encodeURIComponent(hp)
          + '&name='    + encodeURIComponent(name)
          + '&email='   + encodeURIComponent(email)
          + '&company=' + encodeURIComponent(company)
          + '&reason='  + encodeURIComponent(reason)
          + '&message=' + encodeURIComponent(message)
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
      if (data.success) {
        wrap.style.display = 'none';
        okEl.textContent = data.data.message;
        okEl.style.display = 'block';
      } else {
        showErr(data.data && data.data.message ? data.data.message : 'Something went wrong. Please try again.');
        btn.disabled = false;
        btn.textContent = 'Send Message';
        btn.style.background = '#111111';
      }
    })
    .catch(function() {
      showErr('Something went wrong. Please try again.');
      btn.disabled = false;
      btn.textContent = 'Send Message';
      btn.style.background = '#111111';
    });
  });

  function showErr(msg) {
    errEl.textContent = msg;
    errEl.style.display = 'block';
    errEl.scrollIntoView({behavior: 'smooth', block: 'nearest'});
  }
})();
</script>

<?php get_footer(); ?>
