<?php
/**
 * Site Footer
 * Matches the static site footer exactly.
 */
?>

<?php get_template_part('template-parts/author-card'); ?>

<footer style="background:#07091a;border-radius:28px 28px 0 0;padding:56px min(6.5rem,8vw);">
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:40px;margin-bottom:52px;">
    <div>
      <p style="color:#4a5568;font-size:9px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;margin:0 0 16px;">Directory</p>
      <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:10px;">
        <?php
        $professions = aifp_get_profession_hubs();
        foreach ($professions as $prof) :
        ?>
          <li><a href="<?php echo esc_url(get_permalink($prof->ID)); ?>" style="color:#5a6e94;font-size:13px;text-decoration:none;transition:color 0.15s;" onmouseover="this.style.color='#ffffff'" onmouseout="this.style.color='#5a6e94'"><?php $pd = aifp_get_data($prof->ID); echo esc_html($pd['profession_name'] ?? $prof->post_title); ?></a></li>
        <?php endforeach; ?>
      </ul>
    </div>
    <div>
      <p style="color:#4a5568;font-size:9px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;margin:0 0 16px;">Company</p>
      <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:10px;">
        <li><a href="<?php echo esc_url(home_url('/about-us')); ?>" style="color:#5a6e94;font-size:13px;text-decoration:none;transition:color 0.15s;" onmouseover="this.style.color='#ffffff'" onmouseout="this.style.color='#5a6e94'">About</a></li>
        <li><a href="<?php echo esc_url(home_url('/our-process')); ?>" style="color:#5a6e94;font-size:13px;text-decoration:none;transition:color 0.15s;" onmouseover="this.style.color='#ffffff'" onmouseout="this.style.color='#5a6e94'">Our Process</a></li>
      </ul>
    </div>
    <div>
      <p style="color:#4a5568;font-size:9px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;margin:0 0 16px;">Resources</p>
      <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:10px;">
        <li><a href="<?php echo esc_url(home_url('/newsletter')); ?>" style="color:#5a6e94;font-size:13px;text-decoration:none;transition:color 0.15s;" onmouseover="this.style.color='#ffffff'" onmouseout="this.style.color='#5a6e94'">Newsletter</a></li>
      </ul>
    </div>
    <div>
      <p style="color:#4a5568;font-size:9px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;margin:0 0 16px;">Legal</p>
      <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:10px;">
        <li><a href="<?php echo esc_url(home_url('/privacy-policy')); ?>" style="color:#5a6e94;font-size:13px;text-decoration:none;transition:color 0.15s;" onmouseover="this.style.color='#ffffff'" onmouseout="this.style.color='#5a6e94'">Privacy Policy</a></li>
        <li><a href="<?php echo esc_url(home_url('/cookie-policy')); ?>" style="color:#5a6e94;font-size:13px;text-decoration:none;transition:color 0.15s;" onmouseover="this.style.color='#ffffff'" onmouseout="this.style.color='#5a6e94'">Cookie Policy</a></li>
      </ul>
    </div>
  </div>
  <div style="border-top:1px solid #111e38;margin-bottom:48px;"></div>
  <div style="display:flex;align-items:center;justify-content:space-between;">
    <div>
      <p style="color:#1e2a45;font-size:11px;font-weight:500;margin:0 0 4px;letter-spacing:0.05em;opacity:0.6;">AI Tools for Pros</p>
      <p class="font-heading" style="color:#2563EB;font-size:48px;font-weight:700;margin:0 0 10px;line-height:1;"><?php echo esc_html(date('Y')); ?>.</p>
      <p style="color:#4a5568;font-size:13px;margin:0;">Join 15,000+ professionals receiving our monthly tool audit.</p>
    </div>
    <div style="display:flex;align-items:center;gap:10px;">
      <div style="position:relative;display:flex;align-items:center;">
        <input type="email" placeholder="professional@email.com" style="background:#0d1228;color:#4a5568;font-size:13px;padding:13px 48px 13px 18px;border-radius:999px;border:1px solid #1a2444;outline:none;width:248px;font-family:'Inter',sans-serif;">
        <div style="position:absolute;right:8px;width:28px;height:28px;background:#1a2444;border-radius:50%;display:flex;align-items:center;justify-content:center;">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M2 6h8M6 2l4 4-4 4" stroke="#4a5568" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </div>
      </div>
      <button style="background:#ffffff;color:#111111;font-size:13px;font-weight:500;padding:13px 24px;border-radius:999px;border:none;cursor:pointer;font-family:'Inter',sans-serif;" onmouseover="this.style.background='#f0f0f0'" onmouseout="this.style.background='#ffffff'">Subscribe</button>
    </div>
  </div>
</footer>

<?php wp_footer(); ?>
</body>
</html>
