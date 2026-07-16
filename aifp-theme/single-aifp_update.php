<?php
/**
 * Template: Monthly AI Updates Page (/[month]-[year]-updates/)
 *
 * Data is stored as a JSON object in post_content (same pattern as tool_review /
 * profession_hub / cross_reference), decoded via aifp_get_data(). See
 * docs/AIFORPROS-AUTOMATED-CONTENT.md for the automation that generates these as
 * drafts — this template only renders whatever is published.
 *
 * @package AIFP
 */

get_header();

$post_id       = get_the_ID();
$data          = aifp_get_data($post_id);
$month_label   = $data['month_label'] ?? get_the_title();
$intro         = $data['intro'] ?? '';
$news_items    = $data['news_items'] ?? [];
$what_to_watch = $data['what_to_watch'] ?? '';

// Internal linking is structural, not left to content generation to remember.
// See docs/AIFORPROS-AUTOMATED-CONTENT.md "Content Optimization Guardrails".
$related_tool_slugs       = $data['related_tool_slugs'] ?? [];
$related_profession_slugs = $data['related_profession_slugs'] ?? [];

$related_tools = [];
if (!empty($related_tool_slugs)) {
    foreach (aifp_get_tool_reviews() as $tool) {
        $td = aifp_get_data($tool->ID);
        if (in_array($td['tool_slug'] ?? $tool->post_name, $related_tool_slugs, true)) {
            $related_tools[] = ['name' => $td['tool_name'] ?? $tool->post_title, 'url' => get_permalink($tool->ID)];
        }
    }
}

$related_professions = [];
if (!empty($related_profession_slugs)) {
    foreach (aifp_get_profession_hubs() as $prof) {
        $pd = aifp_get_data($prof->ID);
        if (in_array($pd['profession_slug'] ?? $prof->post_name, $related_profession_slugs, true)) {
            $related_professions[] = ['name' => $pd['profession_name'] ?? $prof->post_title, 'url' => get_permalink($prof->ID)];
        }
    }
}

$pub_date_raw = $data['publish_date'] ?? '';
if ($pub_date_raw && preg_match('/^\d{4}-\d{2}-\d{2}$/', $pub_date_raw)) {
    $pub_date = date('F j, Y', strtotime($pub_date_raw));
} elseif ($pub_date_raw) {
    $pub_date = $pub_date_raw;
} else {
    $pub_date = get_the_date('F j, Y', $post_id);
}
?>

<main>

  <!-- HERO -->
  <section style="padding:min(5rem,7vw) min(6.5rem,8vw) min(4rem,5vw);">
    <div style="max-width:760px;">
      <div style="display:inline-flex;align-items:center;background:#eff6ff;color:#2563EB;font-size:9px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;padding:7px 16px;border-radius:999px;margin-bottom:24px;">
        AI Industry Update
      </div>

      <h1 class="font-heading" style="font-size:clamp(2.4rem,5vw,3.6rem);font-weight:700;line-height:1.08;color:#111111;margin:0 0 20px;">
        AI Updates: <?php echo esc_html($month_label); ?>
      </h1>

      <p style="font-size:13px;color:#636363;margin:12px 0 20px;">By <strong style="color:#111111;font-weight:600;">Richard Migliorisi</strong><a href="https://www.linkedin.com/in/richardmigliorisi/" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn" style="display:inline-flex;align-items:center;margin-left:4px;color:#0a66c2;text-decoration:none;vertical-align:middle;"><svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a>&nbsp;&middot;&nbsp;Fact-checked by <strong style="color:#111111;font-weight:600;">Ryan Cooper</strong><a href="https://www.linkedin.com/in/ryan-cooper-nyc/" target="_blank" rel="noopener noreferrer" aria-label="Ryan Cooper LinkedIn" style="display:inline-flex;align-items:center;margin-left:4px;color:#0a66c2;text-decoration:none;vertical-align:middle;"><svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a>&nbsp;&middot;&nbsp;<?php echo esc_html($pub_date); ?><span id="reading-time"></span></p>

      <?php if ($intro) : ?>
      <div style="color:#444444;font-size:15px;line-height:1.8;max-width:680px;margin:8px 0 0;"><?php echo wp_kses_post($intro); ?></div>
      <?php endif; ?>
    </div>
  </section>

  <!-- NEWS ITEMS -->
  <?php if (!empty($news_items)) : ?>
  <section style="padding:0 min(6.5rem,8vw) min(4rem,5vw);">
    <div style="max-width:760px;display:flex;flex-direction:column;gap:0;">
      <?php foreach ($news_items as $item) :
        $headline    = $item['headline'] ?? '';
        $summary     = $item['summary'] ?? '';
        $source_name = $item['source_name'] ?? '';
        $source_url  = $item['source_url'] ?? '';
        if (!$headline) continue;
      ?>
      <div style="border-top:1px solid #f0f0f0;padding:28px 0;">
        <h2 class="font-heading" style="font-size:19px;font-weight:700;color:#111111;margin:0 0 10px;"><?php echo esc_html($headline); ?></h2>
        <?php if ($summary) : ?>
        <p style="font-size:14px;color:#636363;line-height:1.75;margin:0 0 12px;"><?php echo wp_kses_post($summary); ?></p>
        <?php endif; ?>
        <?php if ($source_name && $source_url) : ?>
        <a href="<?php echo esc_url($source_url); ?>" target="_blank" rel="noopener noreferrer" style="font-size:12px;color:#2563EB;text-decoration:none;font-weight:500;">Source: <?php echo esc_html($source_name); ?> &rarr;</a>
        <?php endif; ?>
      </div>
      <?php endforeach; ?>
    </div>
  </section>
  <?php endif; ?>

  <!-- RELATED REVIEWS (structural internal linking — always present when tools are mentioned) -->
  <?php if (!empty($related_tools) || !empty($related_professions)) : ?>
  <section style="padding:0 min(6.5rem,8vw) min(3rem,4vw);">
    <div style="max-width:760px;">
      <h2 class="font-heading" style="font-size:16px;font-weight:700;color:#111111;margin:0 0 14px;">Related Reviews</h2>
      <div style="display:flex;flex-wrap:wrap;gap:10px;">
        <?php foreach ($related_tools as $rt) : ?>
        <a href="<?php echo esc_url($rt['url']); ?>" style="font-size:13px;color:#2563EB;text-decoration:none;font-weight:500;background:#eff6ff;padding:6px 14px;border-radius:999px;">Our <?php echo esc_html($rt['name']); ?> review &rarr;</a>
        <?php endforeach; ?>
        <?php foreach ($related_professions as $rp) : ?>
        <a href="<?php echo esc_url($rp['url']); ?>" style="font-size:13px;color:#2563EB;text-decoration:none;font-weight:500;background:#eff6ff;padding:6px 14px;border-radius:999px;">AI tools for <?php echo esc_html($rp['name']); ?> &rarr;</a>
        <?php endforeach; ?>
      </div>
    </div>
  </section>
  <?php endif; ?>

  <!-- WHAT TO WATCH -->
  <?php if ($what_to_watch) : ?>
  <section style="padding:0 min(6.5rem,8vw) min(5rem,6vw);">
    <div style="max-width:760px;">
      <h2 class="font-heading" style="font-size:20px;font-weight:700;color:#111111;margin:0 0 12px;">What to Watch Next Month</h2>
      <div class="insight-banner"><p><?php echo wp_kses_post($what_to_watch); ?></p></div>
    </div>
  </section>
  <?php endif; ?>

</main>

<?php get_footer(); ?>
