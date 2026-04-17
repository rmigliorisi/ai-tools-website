<?php
/**
 * Template Part: What Most Reviews Miss
 * Matches the static site layout: insight cards + banner + one-thing paragraphs.
 *
 * @package AIFP
 */

$post_id    = $post_id ?? get_the_ID();
$data       = aifp_get_data($post_id);
$rm         = $data['reviews_miss'] ?? [];
// reviews_miss is stored as {insights:[...], insight_banner:'...'}
$insights   = $rm['insights'] ?? (is_array($rm) && isset($rm[0]) ? $rm : []);
$banner     = $rm['insight_banner'] ?? ($data['insight_banner'] ?? '');
$extras     = $data['reviews_miss_extras'] ?? '';

if (empty($insights) && empty($banner)) return;
?>

<h2 style="font-size:26px;font-weight:700;color:#111111;margin:0 0 20px;">What Most Reviews Miss</h2>

<?php if (!empty($insights)) : ?>
<div style="display:flex;flex-direction:column;gap:20px;margin-bottom:28px;">
  <?php foreach ($insights as $i => $insight) : ?>
  <div style="background:#f9fafb;border-radius:10px;padding:20px 24px;">
    <div style="font-size:10px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#9ca3af;margin:0 0 8px;">Insight <?php echo $i + 1; ?></div>
    <?php if (!empty($insight['insight_title'])) : ?>
    <h4 style="font-size:14px;font-weight:700;color:#111111;margin:0 0 8px;"><?php echo esc_html($insight['insight_title']); ?></h4>
    <?php endif; ?>
    <p style="font-size:14px;color:#444444;line-height:1.75;margin:0;"><?php echo wp_kses_post($insight['insight_body'] ?? ''); ?></p>
  </div>
  <?php endforeach; ?>
</div>
<?php endif; ?>

<?php if ($banner) : ?>
<div class="insight-banner"><p><?php echo wp_kses_post($banner); ?></p></div>
<?php endif; ?>

<?php if ($extras) : ?>
<div style="font-size:14px;color:#444444;line-height:1.75;"><?php echo wp_kses_post($extras); ?></div>
<?php endif; ?>
