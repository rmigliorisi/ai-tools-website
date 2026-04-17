<?php
/**
 * Template Part: Consistency Blocks
 * Matches the static site's 5-block layout exactly.
 * Recommended tools: Best Use Cases = green box
 * Specialized tools: Best Use Cases = blue box (same as mini-workflow)
 *
 * @package AIFP
 */

$post_id      = $post_id ?? get_the_ID();
$data         = aifp_get_data($post_id);
$blocks       = $data['consistency_blocks'] ?? [];
$is_spec      = (($data['verdict_type'] ?? 'recommended') === 'specialized');

if (empty($blocks)) return;

// Best Use Cases box colors differ by verdict
$bf_bg     = $is_spec ? '#eff6ff' : '#f0fdf4';
$bf_border = $is_spec ? '#bfdbfe' : '#bbf7d0';
$bf_label  = $is_spec ? '#1e40af' : '#15803d';
$bf_text   = $is_spec ? '#4c1d95'  : '#166534';
?>

<?php if (!empty($blocks['bottom_line'])) : ?>
<div style="background:#ffffff;border:1px solid #f0f0f0;border-radius:12px;padding:24px 28px;margin-bottom:28px;max-width:760px;">
  <p style="font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#2563EB;margin:0 0 10px;">Bottom Line</p>
  <p style="font-size:14px;color:#333333;line-height:1.7;margin:0;"><?php echo esc_html($blocks['bottom_line']); ?></p>
</div>
<?php endif; ?>

<?php if (!empty($blocks['key_takeaway'])) : ?>
<div style="background:#ffffff;border:1px solid #f0f0f0;border-radius:12px;padding:24px 28px;margin-bottom:28px;max-width:760px;">
  <p style="font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#7c3aed;margin:0 0 14px;">Key Takeaways</p>
  <?php if (substr(ltrim($blocks['key_takeaway']), 0, 1) === '<') : ?>
    <?php echo $blocks['key_takeaway']; ?>
  <?php else : ?>
    <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:10px;">
      <?php foreach (explode("\n", trim($blocks['key_takeaway'])) as $item) : if (trim($item)) : ?>
        <li style="display:flex;gap:10px;font-size:14px;color:#333333;line-height:1.6;"><span style="color:#7c3aed;flex-shrink:0;font-weight:700;">&#8594;</span> <?php echo esc_html(ltrim(trim($item), '-> ')); ?></li>
      <?php endif; endforeach; ?>
    </ul>
  <?php endif; ?>
</div>
<?php endif; ?>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;max-width:760px;margin-bottom:28px;">
  <?php if (!empty($blocks['best_for'])) : ?>
  <div style="background:<?php echo $bf_bg; ?>;border:1px solid <?php echo $bf_border; ?>;border-radius:12px;padding:20px 24px;">
    <p style="font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:<?php echo $bf_label; ?>;margin:0 0 12px;">Best Use Cases</p>
    <?php if (substr(ltrim($blocks['best_for']), 0, 1) === '<') : ?>
      <?php echo $blocks['best_for']; ?>
    <?php else : ?>
      <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:8px;">
        <?php foreach (explode("\n", trim($blocks['best_for'])) as $item) : if (trim($item)) : ?>
          <li style="font-size:13px;color:<?php echo $bf_text; ?>;"><?php echo esc_html(trim($item)); ?></li>
        <?php endif; endforeach; ?>
      </ul>
    <?php endif; ?>
  </div>
  <?php endif; ?>
  <?php if (!empty($blocks['avoid_if'])) : ?>
  <div style="background:#fef2f2;border:1px solid #fecaca;border-radius:12px;padding:20px 24px;">
    <p style="font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#dc2626;margin:0 0 12px;">Avoid Using It For</p>
    <?php if (substr(ltrim($blocks['avoid_if']), 0, 1) === '<') : ?>
      <?php echo $blocks['avoid_if']; ?>
    <?php else : ?>
      <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:8px;">
        <?php foreach (explode("\n", trim($blocks['avoid_if'])) as $item) : if (trim($item)) : ?>
          <li style="font-size:13px;color:#991b1b;"><?php echo esc_html(trim($item)); ?></li>
        <?php endif; endforeach; ?>
      </ul>
    <?php endif; ?>
  </div>
  <?php endif; ?>
</div>

<?php if (!empty($blocks['mini_workflow'])) : ?>
<div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:12px;padding:24px 28px;max-width:760px;margin-bottom:0;">
  <p style="font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#1d4ed8;margin:0 0 12px;">If You Only Do One Thing</p>
  <?php if (substr(ltrim($blocks['mini_workflow']), 0, 1) === '<') : ?>
    <?php echo $blocks['mini_workflow']; ?>
  <?php else : ?>
    <?php
      $workflow_lines = array_filter(array_map('trim', explode("\n", trim($blocks['mini_workflow']))));
      $lead_in = array_shift($workflow_lines);
    ?>
    <p style="font-size:13px;color:#1e40af;margin:0 0 12px;"><?php echo esc_html($lead_in); ?></p>
    <?php if (!empty($workflow_lines)) : ?>
    <ol style="padding:0 0 0 18px;margin:0;display:flex;flex-direction:column;gap:6px;">
      <?php foreach ($workflow_lines as $step) : ?>
        <li style="font-size:13px;color:#1e40af;"><?php echo esc_html($step); ?></li>
      <?php endforeach; ?>
    </ol>
    <?php endif; ?>
  <?php endif; ?>
</div>
<?php endif; ?>
