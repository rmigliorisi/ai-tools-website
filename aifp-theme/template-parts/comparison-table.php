<?php
/**
 * Template Part: Comparison Table
 *
 * @package AIFP
 */

$post_id      = $post_id ?? get_the_ID();
$current_data = aifp_get_data($post_id);
$current_slug = $current_data['tool_slug'] ?? '';
$tools        = aifp_get_tool_reviews();

if (empty($tools)) return;
?>

<section style="padding:48px 0;max-width:760px;">
  <h2 class="font-heading" style="font-size:28px;font-weight:700;color:#111111;margin:0 0 24px;">How It Compares</h2>
  <div style="overflow-x:auto;">
    <table style="width:100%;border-collapse:collapse;font-size:13px;">
      <thead>
        <tr style="border-bottom:2px solid #e5e7eb;">
          <th style="text-align:left;padding:12px 14px;font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#9ca3af;">Tool</th>
          <th style="text-align:left;padding:12px 14px;font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#9ca3af;">Best For</th>
          <th style="text-align:left;padding:12px 14px;font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#9ca3af;">Pricing</th>
          <th style="text-align:left;padding:12px 14px;font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#9ca3af;">Verdict</th>
        </tr>
      </thead>
      <tbody>
        <?php foreach ($tools as $tool) :
          $td = aifp_get_data($tool->ID);
          $slug    = $td['tool_slug'] ?? '';
          $name    = $td['tool_name'] ?? $tool->post_title;
          $facts   = $td['quick_facts'] ?? [];
          $is_current = ($slug === $current_slug);
          $row_bg  = $is_current ? 'background:#EBF2FF;' : '';
        ?>
        <tr style="border-bottom:1px solid #f0f0f0;<?php echo $row_bg; ?>">
          <td style="padding:12px 14px;font-weight:<?php echo $is_current ? '700' : '500'; ?>;color:#111111;">
            <a href="<?php echo esc_url(get_permalink($tool->ID)); ?>" style="color:#111111;text-decoration:none;"><?php echo esc_html($name); ?></a>
          </td>
          <td style="padding:12px 14px;color:#444444;"><?php echo esc_html($facts['best_for_fact'] ?? ''); ?></td>
          <td style="padding:12px 14px;color:#444444;"><?php echo esc_html($facts['pricing_fact'] ?? ''); ?></td>
          <td style="padding:12px 14px;">
            <?php echo aifp_verdict_badge($tool->ID); ?>
          </td>
        </tr>
        <?php endforeach; ?>
      </tbody>
    </table>
  </div>
</section>
