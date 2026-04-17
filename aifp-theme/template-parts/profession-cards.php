<?php
/**
 * Template Part: Profession Cards
 * Matches the static site's profession card grid.
 *
 * @package AIFP
 */

$post_id   = $post_id ?? get_the_ID();
$xrefs     = aifp_get_cross_references_for_tool($post_id);
$tool_data = aifp_get_data($post_id);
$tool_name = $tool_data['tool_name'] ?? '';
$cards     = $tool_data['profession_cards'] ?? [];

if (empty($xrefs)) return;
?>

<h2 style="font-size:26px;font-weight:700;color:#111111;margin:0 0 8px;">How <?php echo esc_html($tool_name); ?> Works for Your Profession</h2>
<p style="color:#636363;font-size:14px;margin:0 0 32px;">I've reviewed <?php echo esc_html($tool_name); ?> across <?php echo count($xrefs); ?> professional fields. Each guide covers real workflows, verified limitations, and copy-paste prompts.</p>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:20px;">
  <?php foreach ($xrefs as $xref) :
    $prof = aifp_get_linked_post($xref->ID, 'linked_profession');
    if (!$prof) continue;
    $prof_data = aifp_get_data($prof->ID);
    $prof_name = $prof_data['profession_name'] ?? $prof->post_title;
    // Find matching card description
    $card_desc = '';
    $prof_slug = $prof->post_name ?? '';
    if (!empty($cards)) {
      foreach ($cards as $card) {
        $card_name = $card['name'] ?? '';
        $card_slug = $card['link_slug'] ?? '';
        $name_match = stripos($card_name, $prof_name) !== false || stripos($prof_name, $card_name) !== false;
        $slug_match = $prof_slug && (str_ends_with($card_slug, '/' . $prof_slug) || $card_slug === $prof_slug);
        if ($name_match || $slug_match) {
          $card_desc = $card['description'] ?? '';
          break;
        }
      }
    }
  ?>
  <div class="industry-card">
    <h3 style="font-size:15px;font-weight:700;color:#111111;margin:0 0 8px;"><?php echo esc_html($prof_name); ?></h3>
    <?php if ($card_desc) : ?>
    <p style="color:#636363;font-size:13px;line-height:1.6;margin:0 0 20px;"><?php echo esc_html($card_desc); ?></p>
    <?php endif; ?>
    <a href="<?php echo esc_url(get_permalink($xref->ID)); ?>" class="read-guide-link"><?php echo esc_html($tool_name); ?> for <?php echo esc_html($prof_name); ?> <span>&#8594;</span></a>
  </div>
  <?php endforeach; ?>
</div>
