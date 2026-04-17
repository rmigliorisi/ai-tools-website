<?php
/**
 * Template: Profession Hub Page (matches static site layout exactly)
 *
 * @package AIFP
 */

get_header();

$post_id   = get_the_ID();
$data      = aifp_get_data($post_id);
$prof_name = $data['profession_name'] ?? get_the_title();
$eyebrow   = $data['eyebrow_text'] ?? '';
$lede      = $data['lede'] ?? '';
$pub_date_raw = $data['publish_date'] ?? '';
if ($pub_date_raw && preg_match('/^\d{4}-\d{2}-\d{2}$/', $pub_date_raw)) {
    $pub_date = date('F j, Y', strtotime($pub_date_raw));
} elseif ($pub_date_raw) {
    $pub_date = $pub_date_raw;
} else {
    $pub_date = get_the_date('F j, Y');
}
$tool_count = $data['tool_count'] ?? 0;
?>

<main>

  <!-- HERO -->
  <section style="padding:min(5rem,7vw) min(6.5rem,8vw) min(4rem,5vw);">
    <div style="max-width:760px;">
      <?php if ($eyebrow) : ?>
      <div style="display:inline-flex;align-items:center;background:#eff6ff;color:#2563EB;font-size:9px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;padding:7px 16px;border-radius:999px;margin-bottom:24px;">
        <?php echo esc_html($eyebrow); ?>
      </div>
      <?php endif; ?>

      <h1 class="font-heading" style="font-size:clamp(2.4rem,5vw,3.6rem);font-weight:700;line-height:1.08;color:#111111;margin:0 0 20px;">
        AI Tools for <?php echo esc_html($prof_name); ?>
      </h1>

      <?php if ($lede) : ?>
      <p style="color:#636363;font-size:15px;line-height:1.75;max-width:600px;margin:0 0 32px;"><?php echo esc_html($lede); ?></p>
      <?php endif; ?>

      <p style="font-size:13px;color:#636363;margin:12px 0 20px;">By <strong style="color:#111111;font-weight:600;">Richard Migliorisi</strong><a href="https://www.linkedin.com/in/richardmigliorisi/" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn" style="display:inline-flex;align-items:center;margin-left:4px;color:#0a66c2;text-decoration:none;vertical-align:middle;"><svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a>&nbsp;&middot;&nbsp;Fact-checked by <strong style="color:#111111;font-weight:600;">Ryan Cooper</strong><a href="https://www.linkedin.com/in/ryan-cooper-nyc/" target="_blank" rel="noopener noreferrer" aria-label="Ryan Cooper LinkedIn" style="display:inline-flex;align-items:center;margin-left:4px;color:#0a66c2;text-decoration:none;vertical-align:middle;"><svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a>&nbsp;&middot;&nbsp;<?php echo esc_html($pub_date); ?></p>

      <?php if ($tool_count > 0) : ?>
      <div style="display:flex;align-items:center;gap:20px;flex-wrap:wrap;">
        <span style="font-size:13px;color:#636363;"><strong style="color:#111111;font-weight:600;"><?php echo esc_html($tool_count); ?> tools</strong> reviewed for this profession</span>
        <a href="<?php echo esc_url(home_url('/our-process')); ?>" style="font-size:12px;color:#2563EB;text-decoration:none;font-weight:500;">How we test &rarr;</a>
      </div>
      <?php endif; ?>
    </div>
  </section>

  <!-- USE CASES -->
  <?php
  $use_cases = $data['use_cases'] ?? [];
  $uc_title = $data['use_cases_title'] ?? '';
  $uc_intro = $data['use_cases_intro'] ?? '';
  if (!empty($use_cases)) : ?>
  <section style="padding:0 min(6.5rem,8vw) min(4rem,5vw);">
    <div style="max-width:900px;">
      <?php if ($uc_title) : ?>
      <h2 class="font-heading" style="font-size:clamp(1.8rem,3vw,2.4rem);font-weight:700;line-height:1.1;color:#111111;margin:0 0 16px;"><?php echo esc_html($uc_title); ?></h2>
      <?php endif; ?>
      <?php if ($uc_intro) : ?>
      <p style="font-size:15px;color:#636363;line-height:1.75;max-width:680px;margin:0 0 36px;"><?php echo esc_html($uc_intro); ?></p>
      <?php endif; ?>
      <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:20px;margin-bottom:40px;">
        <?php foreach ($use_cases as $uc) : ?>
        <div style="background:#ffffff;border:1px solid #f0f0f0;border-radius:12px;padding:24px 26px;">
          <?php if (!empty($uc['category'])) : ?>
          <div style="font-size:9px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#2563EB;margin-bottom:10px;"><?php echo esc_html($uc['category']); ?></div>
          <?php endif; ?>
          <h3 class="font-heading" style="font-size:17px;font-weight:700;color:#111111;margin:0 0 10px;"><?php echo esc_html($uc['title'] ?? ''); ?></h3>
          <p style="font-size:13px;color:#636363;line-height:1.7;margin:0 0 14px;"><?php echo esc_html($uc['description'] ?? ''); ?></p>
          <?php if (!empty($uc['recommended'])) : ?>
          <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">
            <span style="font-size:11px;color:#059669;font-weight:600;letter-spacing:0.03em;">Try:</span>
            <span style="font-size:11px;color:#636363;"><?php echo esc_html($uc['recommended']); ?></span>
          </div>
          <?php endif; ?>
        </div>
        <?php endforeach; ?>
      </div>

      <?php $caution = $data['caution_notice'] ?? ''; ?>
      <?php if ($caution) : ?>
      <div style="background:#fefce8;border:1px solid #fde68a;border-radius:12px;padding:20px 24px;max-width:760px;">
        <p style="font-size:9px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#92400e;margin:0 0 8px;">PROFESSIONAL LIABILITY</p>
        <p style="font-size:13px;color:#78350f;line-height:1.7;margin:0;"><?php echo esc_html($caution); ?></p>
      </div>
      <?php endif; ?>
    </div>
  </section>
  <?php endif; ?>

  <!-- TOOL CARDS -->
  <?php $tool_cards = $data['tool_cards'] ?? []; ?>
  <?php if (!empty($tool_cards)) : ?>
  <section style="padding:0 min(6.5rem,8vw) min(6rem,7vw);">
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:20px;">
      <?php foreach ($tool_cards as $tc) :
        $is_specialized = ($tc['verdict'] ?? '') === 'specialized';
        $badge_bg = $is_specialized ? '#f5f3ff' : '#eff6ff';
        $badge_color = $is_specialized ? '#7c3aed' : '#2563EB';
        $badge_label = $is_specialized ? 'Specialized' : 'Recommended';
      ?>
      <div class="tool-card">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">
          <h3 class="font-heading" style="font-size:22px;font-weight:700;color:#111111;margin:0;"><?php echo esc_html($tc['name'] ?? ''); ?></h3>
          <span style="font-size:9px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:<?php echo esc_attr($badge_color); ?>;background:<?php echo esc_attr($badge_bg); ?>;padding:4px 10px;border-radius:999px;"><?php echo esc_html($badge_label); ?></span>
        </div>
        <p style="font-size:11px;color:#9ca3af;font-weight:500;margin:0 0 14px;text-transform:uppercase;letter-spacing:0.1em;">Made by <?php echo esc_html($tc['maker'] ?? ''); ?></p>
        <p style="font-size:13px;color:#636363;line-height:1.7;margin:0 0 16px;"><?php echo esc_html($tc['description'] ?? ''); ?></p>
        <?php if (!empty($tc['features'])) : ?>
        <ul style="list-style:none;padding:0;margin:0 0 20px;display:flex;flex-direction:column;gap:6px;">
          <?php foreach ($tc['features'] as $feat) : ?>
          <li style="font-size:13px;color:#636363;line-height:1.6;"><?php echo esc_html($feat); ?></li>
          <?php endforeach; ?>
        </ul>
        <?php endif; ?>
        <?php if (!empty($tc['link'])) : ?>
        <a href="<?php echo esc_url(home_url($tc['link'])); ?>" class="read-review">Read the review <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M2 6h8M6 2l4 4-4 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
        <?php endif; ?>
      </div>
      <?php endforeach; ?>
    </div>
  </section>
  <?php endif; ?>

  <!-- FAQ -->
  <?php
  $faqs = $data['faq'] ?? [];
  if (!empty($faqs)) : ?>
  <section style="padding:0 min(6.5rem,8vw) min(3rem,4vw);">
    <div style="max-width:720px;">
      <h2 style="font-size:22px;font-weight:700;color:#111111;margin:0 0 8px;">Common Questions</h2>
      <p style="color:#636363;font-size:13px;margin:0 0 36px;">What professionals ask before adopting AI tools.</p>
      <?php foreach ($faqs as $item) : ?>
      <div style="border-top:1px solid #e5e7eb;padding:24px 0;">
        <h3 style="font-size:15px;font-weight:600;color:#111111;margin:0 0 10px;"><?php echo esc_html($item['question'] ?? ''); ?></h3>
        <p style="color:#636363;font-size:13px;line-height:1.75;margin:0;"><?php echo wp_kses_post($item['answer'] ?? ''); ?></p>
      </div>
      <?php endforeach; ?>
    </div>
  </section>
  <?php endif; ?>

</main>

<?php get_footer(); ?>
