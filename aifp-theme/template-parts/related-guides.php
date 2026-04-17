<?php
/**
 * Template Part: Related Guides Grid
 *
 * @package AIFP
 */

$post_id   = $post_id ?? get_the_ID();
$post_type = get_post_type($post_id);

$related = [];

if ($post_type === 'tool_review') {
    $related = aifp_get_cross_references_for_tool($post_id);
} elseif ($post_type === 'cross_reference') {
    $tool = aifp_get_linked_post($post_id, 'linked_tool');
    if ($tool) {
        $all = aifp_get_cross_references_for_tool($tool->ID);
        $related = array_filter($all, fn($p) => $p->ID !== $post_id);
    }
} elseif ($post_type === 'profession_hub') {
    $related = aifp_get_cross_references_for_profession($post_id);
}

if (empty($related)) return;

$related = array_slice($related, 0, 8);
?>

<section style="padding:48px 0;max-width:760px;">
  <h2 class="font-heading" style="font-size:28px;font-weight:700;color:#111111;margin:0 0 24px;">Related Guides</h2>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px;">
    <?php foreach ($related as $guide) :
      $tool = aifp_get_linked_post($guide->ID, 'linked_tool');
      $prof = aifp_get_linked_post($guide->ID, 'linked_profession');
      $tool_name = $tool ? (aifp_get_data($tool->ID)['tool_name'] ?? $tool->post_title) : '';
      $prof_name = $prof ? (aifp_get_data($prof->ID)['profession_name'] ?? $prof->post_title) : '';
    ?>
    <a href="<?php echo esc_url(get_permalink($guide->ID)); ?>" style="background:#ffffff;border:1px solid #f0f0f0;border-radius:12px;padding:20px;text-decoration:none;transition:box-shadow 0.2s;" onmouseover="this.style.boxShadow='0 4px 20px rgba(0,0,0,0.06)'" onmouseout="this.style.boxShadow='none'">
      <p style="font-size:13px;font-weight:600;color:#111111;margin:0 0 4px;"><?php echo esc_html($tool_name); ?></p>
      <p style="font-size:12px;color:#636363;margin:0;">for <?php echo esc_html($prof_name); ?></p>
    </a>
    <?php endforeach; ?>
  </div>
</section>
