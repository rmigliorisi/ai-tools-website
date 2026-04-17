<?php
/**
 * Template Part: Tool Cards
 *
 * @package AIFP
 */

$post_id   = $post_id ?? get_the_ID();
$xrefs     = aifp_get_cross_references_for_profession($post_id);

if (empty($xrefs)) return;
?>

<section style="padding:48px 0;max-width:760px;">
  <h2 class="font-heading" style="font-size:28px;font-weight:700;color:#111111;margin:0 0 24px;">AI Tools for This Profession</h2>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:16px;">
    <?php foreach ($xrefs as $xref) :
      $tool = aifp_get_linked_post($xref->ID, 'linked_tool');
      if (!$tool) continue;
      $td = aifp_get_data($tool->ID);
      $tool_name = $td['tool_name'] ?? $tool->post_title;
    ?>
    <a href="<?php echo esc_url(get_permalink($xref->ID)); ?>" class="tool-card" style="text-decoration:none;">
      <p style="font-size:14px;font-weight:600;color:#111111;margin:0 0 6px;"><?php echo esc_html($tool_name); ?></p>
      <span class="read-guide-link">Read the review →</span>
    </a>
    <?php endforeach; ?>
  </div>
</section>
