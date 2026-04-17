<?php
/**
 * Template: Cross-Reference Page (matches static site layout exactly)
 *
 * @package AIFP
 */

get_header();

$post_id   = get_the_ID();
$data      = aifp_get_data($post_id);
$tool      = aifp_get_linked_post($post_id, 'linked_tool');
$prof      = aifp_get_linked_post($post_id, 'linked_profession');
$tool_data = $tool ? aifp_get_data($tool->ID) : [];
$tool_name = $tool_data['tool_name'] ?? ($tool ? $tool->post_title : '');
$prof_name = $prof ? (aifp_get_data($prof->ID)['profession_name'] ?? $prof->post_title) : '';
$subtitle  = $data['subtitle'] ?? '';
$pub_date_raw = $data['publish_date'] ?? '';
// Format ISO dates (2026-02-01) to readable format; pass through already-formatted dates
if ($pub_date_raw && preg_match('/^\d{4}-\d{2}-\d{2}$/', $pub_date_raw)) {
    $pub_date = date('F j, Y', strtotime($pub_date_raw));
} elseif ($pub_date_raw) {
    $pub_date = $pub_date_raw;
} else {
    $pub_date = get_the_date('F j, Y');
}
$read_time = aifp_reading_time($post_id);
$verdict_type = $data['verdict_type'] ?? 'recommended';
$accent    = ($verdict_type === 'specialized') ? '#7c3aed' : '#2563EB';
$badge_class = ($verdict_type === 'specialized') ? 'verdict-badge-specialized' : 'verdict-badge-recommended';
$badge_label = ($verdict_type === 'specialized') ? 'Specialized' : 'Recommended';

// Get tool company name for the badge
$made_by = $tool_data['quick_facts']['made_by'] ?? '';
?>

<main class="prose-page">

  <!-- BREADCRUMB -->
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <a href="<?php echo esc_url(home_url('/')); ?>">Home</a>
    <span>›</span>
    <?php if ($tool) : ?>
    <a href="<?php echo esc_url(get_permalink($tool->ID)); ?>"><?php echo esc_html($tool_name); ?></a>
    <span>›</span>
    <?php endif; ?>
    <span><?php echo esc_html($prof_name); ?></span>
  </nav>

  <!-- TOOL BADGE -->
  <div class="tool-badge">
    <span class="dot"></span>
    <?php echo esc_html($tool_name); ?><?php if ($made_by) : ?> by <?php echo esc_html($made_by); ?><?php endif; ?>
  </div>

  <!-- H1 -->
  <h1><?php echo esc_html($tool_name); ?> for <?php echo esc_html($prof_name); ?> &mdash; An Honest Review (<?php echo esc_html(date('Y')); ?>)</h1>

  <!-- SUBTITLE -->
  <?php if ($subtitle) : ?>
  <p class="page-subtitle"><?php echo esc_html($subtitle); ?></p>
  <?php endif; ?>

  <!-- META ROW -->
  <div class="meta-row">
    <span class="<?php echo esc_attr($badge_class); ?>"><?php echo esc_html($badge_label); ?></span>
    <span class="meta-date"><?php echo esc_html($pub_date); ?></span>
    <span class="meta-read"><?php echo esc_html($read_time); ?> min read</span>
  </div>

  <!-- BYLINE -->
  <p style="font-size:13px;color:#636363;margin:4px 0 0;">By <strong style="color:#111111;font-weight:600;">Richard Migliorisi</strong><a href="https://www.linkedin.com/in/richardmigliorisi/" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn" style="display:inline-flex;align-items:center;margin-left:4px;color:#0a66c2;text-decoration:none;vertical-align:middle;"><svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a>&nbsp;&middot;&nbsp;Fact-checked by <strong style="color:#111111;font-weight:600;">Ryan Cooper</strong><a href="https://www.linkedin.com/in/ryan-cooper-nyc/" target="_blank" rel="noopener noreferrer" aria-label="Ryan Cooper LinkedIn" style="display:inline-flex;align-items:center;margin-left:4px;color:#0a66c2;text-decoration:none;vertical-align:middle;"><svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a>&nbsp;&middot;&nbsp;<?php echo esc_html($pub_date); ?></p>

  <!-- VERDICT BANNER -->
  <?php $blocks = $data['consistency_blocks'] ?? []; ?>
  <?php if (!empty($blocks['bottom_line'])) : ?>
  <div class="verdict-banner">
    <p><strong>Bottom line:</strong> <?php echo esc_html($blocks['bottom_line']); ?></p>
  </div>
  <?php endif; ?>

  <!-- CONSISTENCY BLOCKS (Key Takeaway, Best For / Avoid If, Mini Workflow) -->
  <?php if (!empty($blocks['key_takeaway'])) : ?>
  <div class="consistency-block" style="background:#f5f3ff;border-color:#7c3aed;">
    <div class="cb-label">Key Takeaway</div>
    <div class="cb-text"><?php echo esc_html($blocks['key_takeaway']); ?></div>
  </div>
  <?php endif; ?>

  <?php if (!empty($blocks['best_for']) || !empty($blocks['avoid_if'])) : ?>
  <div class="cb-grid">
    <?php if (!empty($blocks['best_for'])) : ?>
    <div class="consistency-block" style="margin-bottom:0; background:#f0fdf4; border-color:#bbf7d0;">
      <div class="cb-label" style="color:#166534;">Best For</div>
      <div class="cb-text" style="color:#166534;"><?php echo esc_html($blocks['best_for']); ?></div>
    </div>
    <?php endif; ?>
    <?php if (!empty($blocks['avoid_if'])) : ?>
    <div class="consistency-block" style="margin-bottom:0; background:#fef2f2; border-color:#fecaca;">
      <div class="cb-label" style="color:#991b1b;">Avoid If</div>
      <div class="cb-text" style="color:#991b1b;"><?php echo esc_html($blocks['avoid_if']); ?></div>
    </div>
    <?php endif; ?>
  </div>
  <?php endif; ?>

  <?php if (!empty($blocks['mini_workflow'])) : ?>
  <div class="consistency-block" style="margin-top:10px;background:#ffffff;border:1px solid #bfdbfe;">
    <div class="cb-label">Mini Workflow</div>
    <div class="cb-text">
      <div class="cb-workflow-highlight" style="font-size:14px; color:#1e3a5f; line-height:1.6;">
        <?php echo esc_html($blocks['mini_workflow']); ?>
      </div>
    </div>
  </div>
  <?php endif; ?>

  <!-- QUICK FACTS BAR -->
  <?php $facts = $data['quick_facts'] ?? []; ?>
  <?php if (!empty($facts)) : ?>
  <div class="fact-bar">
    <?php if (!empty($facts['made_by'])) : ?>
    <div class="fact-item">
      <div class="fact-label">Made By</div>
      <div class="fact-value"><?php echo esc_html($facts['made_by']); ?></div>
      <?php if (!empty($facts['made_by_sub'])) : ?><div class="fact-sub"><?php echo esc_html($facts['made_by_sub']); ?></div><?php endif; ?>
    </div>
    <?php endif; ?>
    <?php if (!empty($facts['best_for'])) : ?>
    <div class="fact-item">
      <div class="fact-label">Best For</div>
      <div class="fact-value"><?php echo esc_html($facts['best_for']); ?></div>
      <?php if (!empty($facts['best_for_sub'])) : ?><div class="fact-sub"><?php echo esc_html($facts['best_for_sub']); ?></div><?php endif; ?>
    </div>
    <?php endif; ?>
    <?php if (!empty($facts['pricing'])) : ?>
    <div class="fact-item">
      <div class="fact-label">Pricing</div>
      <div class="fact-value"><?php echo esc_html($facts['pricing']); ?></div>
      <?php if (!empty($facts['pricing_sub'])) : ?><div class="fact-sub"><?php echo esc_html($facts['pricing_sub']); ?></div><?php endif; ?>
    </div>
    <?php endif; ?>
    <?php if (!empty($facts['compliance'])) : ?>
    <div class="fact-item">
      <div class="fact-label">Confidentiality</div>
      <div class="fact-value"><?php echo esc_html($facts['compliance']); ?></div>
      <?php if (!empty($facts['compliance_sub'])) : ?><div class="fact-sub"><?php echo esc_html($facts['compliance_sub']); ?></div><?php endif; ?>
    </div>
    <?php endif; ?>
    <?php if (!empty($facts['compared_to'])) : ?>
    <div class="fact-item">
      <div class="fact-label">Compared To</div>
      <div class="fact-value"><?php echo esc_html($facts['compared_to']); ?></div>
    </div>
    <?php endif; ?>
  </div>
  <?php endif; ?>

  <!-- CONTENT SECTIONS -->
  <?php $sections = $data['content_sections'] ?? []; ?>
  <?php foreach ($sections as $section) : ?>
    <h2><?php echo esc_html($section['section_title'] ?? ''); ?></h2>
    <?php echo $section['section_body'] ?? ''; // trusted migration content ?>
  <?php endforeach; ?>

  <!-- PROMPTS THAT WORK (if extracted separately from content) -->
  <?php $prompts = $data['prompts'] ?? []; ?>
  <?php if (!empty($prompts) && empty($sections)) : ?>
  <h2>Prompts That Work for <?php echo esc_html($prof_name); ?></h2>
  <?php foreach ($prompts as $prompt) : ?>
    <div class="prompt-label"><?php echo esc_html($prompt['prompt_title'] ?? 'Try this prompt'); ?></div>
    <div class="prompt-block"><?php echo $prompt['prompt_text'] ?? ''; // trusted migration content ?></div>
  <?php endforeach; ?>
  <?php endif; ?>

  <!-- COMPARISON -->
  <?php if (!empty($data['comparison_notes'])) : ?>
    <h2>How <?php echo esc_html($tool_name); ?> Compares for <?php echo esc_html($prof_name); ?></h2>
    <?php echo $data['comparison_notes']; // trusted migration content ?>
  <?php endif; ?>

  <!-- MY VERDICT -->
  <?php if (!empty($data['verdict_text'])) : ?>
    <h2>My Verdict</h2>
    <?php echo $data['verdict_text']; // trusted migration content ?>
  <?php endif; ?>

  <!-- FAQ -->
  <?php
  $faqs = $data['faq'] ?? [];
  if (!empty($faqs)) : ?>
  <h2>Frequently Asked Questions</h2>
  <div itemscope itemtype="https://schema.org/FAQPage">
    <?php foreach ($faqs as $item) : ?>
    <div class="faq-item" itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
      <h3 class="faq-q" itemprop="name"><?php echo esc_html($item['question'] ?? ''); ?></h3>
      <div class="faq-a" itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
        <span itemprop="text"><?php echo $item['answer'] ?? ''; // trusted migration content ?></span>
      </div>
    </div>
    <?php endforeach; ?>
  </div>
  <?php endif; ?>

  <!-- SOURCES CHECKED -->
  <?php
  $sources = $data['sources'] ?? [];
  if (!empty($sources)) : ?>
  <h2>Sources Checked</h2>
  <ul class="sources-list">
    <?php foreach ($sources as $i => $source) : ?>
    <li>
      <span class="source-badge"><?php echo esc_html($i + 1); ?></span>
      <span><?php echo esc_html($source['source_name'] ?? ''); ?></span>
    </li>
    <?php endforeach; ?>
  </ul>
  <?php endif; ?>

  <!-- RELATED GUIDES -->
  <?php
  $tool_xrefs = $tool ? aifp_get_cross_references_for_tool($tool->ID) : [];
  $related = array_filter($tool_xrefs, fn($p) => $p->ID !== $post_id);
  $related = array_slice($related, 0, 6);
  if (!empty($related)) : ?>
  <h2>Related Guides</h2>
  <div class="related-grid">
    <?php foreach ($related as $guide) :
      $g_prof = aifp_get_linked_post($guide->ID, 'linked_profession');
      $g_prof_name = $g_prof ? (aifp_get_data($g_prof->ID)['profession_name'] ?? $g_prof->post_title) : '';
    ?>
    <a href="<?php echo esc_url(get_permalink($guide->ID)); ?>" class="related-card">
      <div class="rc-label"><?php echo esc_html($tool_name); ?></div>
      <div class="rc-title"><?php echo esc_html($tool_name); ?> for <?php echo esc_html($g_prof_name); ?></div>
      <span class="read-guide-link">Read guide →</span>
    </a>
    <?php endforeach; ?>
    <?php if ($tool) : ?>
    <a href="<?php echo esc_url(get_permalink($tool->ID)); ?>" class="related-card">
      <div class="rc-label"><?php echo esc_html($tool_name); ?> Hub</div>
      <div class="rc-title"><?php echo esc_html($tool_name); ?> for All Professions</div>
      <span class="read-guide-link">Read guide →</span>
    </a>
    <?php endif; ?>
    <?php if ($prof) : ?>
    <a href="<?php echo esc_url(get_permalink($prof->ID)); ?>" class="related-card">
      <div class="rc-label">All <?php echo esc_html($prof_name); ?> Tools</div>
      <div class="rc-title">All AI tools for <?php echo esc_html(strtolower($prof_name)); ?></div>
      <span class="read-guide-link">View overview →</span>
    </a>
    <?php endif; ?>
  </div>
  <?php endif; ?>

  <!-- WHAT MOST REVIEWS MISS -->
  <?php
  $reviews_miss = $data['reviews_miss'] ?? [];
  $insights = $reviews_miss['insights'] ?? (isset($reviews_miss[0]) ? $reviews_miss : []);
  $banner = $reviews_miss['insight_banner'] ?? ($data['insight_banner'] ?? '');
  if (!empty($insights) || $banner) : ?>
  <h2>What Most Reviews Miss</h2>
  <?php if (!empty($insights)) :
    foreach ($insights as $i => $insight) : ?>
  <div class="insight-card">
    <div class="insight-number">Insight <?php echo $i + 1; ?></div>
    <?php if (!empty($insight['insight_title'])) : ?>
    <h4><?php echo esc_html($insight['insight_title']); ?></h4>
    <?php endif; ?>
    <p><?php echo wp_kses_post($insight['insight_body'] ?? ''); ?></p>
  </div>
  <?php endforeach;
  endif; ?>

  <?php if ($banner) : ?>
  <div class="insight-banner">
    <p><?php echo wp_kses_post($banner); ?></p>
  </div>
  <?php endif; ?>
  <?php endif; ?>

  <!-- Author card is rendered by footer.php via template-parts/author-card.php -->

</main>

<?php get_footer(); ?>
