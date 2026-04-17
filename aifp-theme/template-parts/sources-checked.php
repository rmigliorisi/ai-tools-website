<?php
/**
 * Template Part: Sources Checked
 * Matches the static site's [1] [2] badge format.
 *
 * @package AIFP
 */

$post_id = $post_id ?? get_the_ID();
$data    = aifp_get_data($post_id);
$sources = $data['sources'] ?? [];

if (empty($sources)) return;
?>

<h2 style="font-size:26px;font-weight:700;color:#111111;margin:0 0 20px;">Sources Checked</h2>
<ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:10px;">
  <?php foreach ($sources as $i => $source) : ?>
  <li style="font-size:13px;color:#636363;padding-left:20px;position:relative;">
    <span style="position:absolute;left:0;color:#2563EB;font-weight:700;">[<?php echo esc_html($i + 1); ?>]</span>
    <?php echo esc_html($source['source_name'] ?? ''); ?>
  </li>
  <?php endforeach; ?>
</ul>
