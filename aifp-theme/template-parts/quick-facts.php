<?php
/**
 * Template Part: Quick Facts Bar
 * Matches the static site fact-bar exactly.
 *
 * @package AIFP
 */

$post_id   = $post_id ?? get_the_ID();
$data      = aifp_get_data($post_id);
$facts     = $data['quick_facts'] ?? [];
$post_type = get_post_type($post_id);

if (empty($facts)) return;

$is_cross_ref = ($post_type === 'cross_reference');
?>

<div class="fact-bar" style="max-width:900px;">
  <?php if (!$is_cross_ref) : ?>
    <div class="fact-item">
      <p style="font-size:9px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#9ca3af;margin:0 0 6px;">Made by</p>
      <p style="font-size:14px;font-weight:600;color:#111111;margin:0;"><?php echo esc_html($facts['made_by'] ?? ''); ?></p>
    </div>
    <div class="fact-item">
      <p style="font-size:9px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#9ca3af;margin:0 0 6px;">Best for</p>
      <p style="font-size:14px;font-weight:600;color:#111111;margin:0;"><?php echo esc_html($facts['best_for_fact'] ?? ''); ?></p>
    </div>
    <div class="fact-item">
      <p style="font-size:9px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#9ca3af;margin:0 0 6px;">Starting price</p>
      <p style="font-size:14px;font-weight:600;color:#111111;margin:0;"><?php echo esc_html($facts['pricing_fact'] ?? ''); ?></p>
    </div>
    <div class="fact-item">
      <p style="font-size:9px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#9ca3af;margin:0 0 6px;"><?php echo esc_html($facts['custom_fact_label'] ?? 'Details'); ?></p>
      <p style="font-size:14px;font-weight:600;color:#111111;margin:0;"><?php echo esc_html($facts['custom_fact_value'] ?? ''); ?></p>
    </div>
    <div class="fact-item">
      <p style="font-size:9px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#9ca3af;margin:0 0 6px;">HIPAA/Compliance</p>
      <p style="font-size:14px;font-weight:600;color:#111111;margin:0;"><?php echo esc_html($facts['hipaa_fact'] ?? ''); ?></p>
    </div>
  <?php else : ?>
    <div class="fact-item">
      <p style="font-size:9px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#9ca3af;margin:0 0 6px;">Best For</p>
      <p style="font-size:14px;font-weight:600;color:#111111;margin:0;"><?php echo esc_html($facts['best_for'] ?? ''); ?></p>
    </div>
    <div class="fact-item">
      <p style="font-size:9px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#9ca3af;margin:0 0 6px;">Pricing</p>
      <p style="font-size:14px;font-weight:600;color:#111111;margin:0;"><?php echo esc_html($facts['pricing'] ?? ''); ?></p>
    </div>
    <div class="fact-item">
      <p style="font-size:9px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#9ca3af;margin:0 0 6px;">Compliance</p>
      <p style="font-size:14px;font-weight:600;color:#111111;margin:0;"><?php echo esc_html($facts['compliance'] ?? ''); ?></p>
    </div>
    <div class="fact-item">
      <p style="font-size:9px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#9ca3af;margin:0 0 6px;">Compared To</p>
      <p style="font-size:14px;font-weight:600;color:#111111;margin:0;"><?php echo esc_html($facts['compared_to'] ?? ''); ?></p>
    </div>
  <?php endif; ?>
</div>
