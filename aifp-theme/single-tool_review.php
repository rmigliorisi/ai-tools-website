<?php
/**
 * Template: Tool Hub Page (matches static site layout exactly)
 *
 * @package AIFP
 */

get_header();

$post_id   = get_the_ID();
$data      = aifp_get_data($post_id);
$tool_name = $data['tool_name'] ?? get_the_title();
$tool_slug = $data['tool_slug'] ?? '';
$definition = $data['definition_sentence'] ?? '';
$positioning = $data['positioning_statement'] ?? '';
$pub_date  = $data['publish_date'] ?? get_the_date('F j, Y');
$verdict_desc = $data['verdict_description'] ?? '';
$read_time = aifp_reading_time($post_id);
?>

<main style="background:#f9f9f9;">

  <!-- Breadcrumb -->
  <div style="padding:14px min(6.5rem,8vw);font-size:12px;color:#9ca3af;background:#ffffff;border-bottom:1px solid #f5f5f5;">
    <a href="<?php echo esc_url(home_url('/')); ?>" style="color:#9ca3af;text-decoration:none;" onmouseover="this.style.color='#636363'" onmouseout="this.style.color='#9ca3af'">Home</a>
    <span style="margin:0 8px;">/</span>
    <span style="color:#111111;"><?php echo esc_html($tool_name); ?></span>
  </div>

  <!-- Page Header -->
  <section style="padding:min(4rem,6vw) min(6.5rem,8vw) min(2rem,3vw);">
    <p style="font-size:10px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:#636363;margin:0 0 16px;">Independent Review &middot; <?php echo esc_html($pub_date); ?></p>
    <h1 class="font-heading" style="font-size:clamp(2rem,3.5vw,2.8rem);font-weight:700;line-height:1.1;margin:0 0 20px;color:#111111;max-width:800px;">
      <?php echo esc_html($tool_name); ?> for Professionals: An Honest Review (<?php echo esc_html(date('Y')); ?>)
    </h1>

    <?php if ($definition) : ?>
    <p style="font-size:16px;color:#444444;line-height:1.75;max-width:680px;margin:0 0 24px;"><?php echo $definition; // trusted migration content ?></p>
    <?php endif; ?>

    <?php if ($positioning) : ?>
    <p style="font-size:13px;color:#636363;font-style:italic;margin:0 0 24px;"><?php echo esc_html($positioning); ?></p>
    <?php endif; ?>

    <!-- Byline -->
    <p style="font-size:13px;color:#636363;margin:0 0 32px;">By <strong style="color:#111111;font-weight:600;">Richard Migliorisi</strong><a href="https://www.linkedin.com/in/richardmigliorisi/" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn" style="display:inline-flex;align-items:center;margin-left:4px;color:#0a66c2;text-decoration:none;vertical-align:middle;"><svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a>&nbsp;&middot;&nbsp;Fact-checked by <strong style="color:#111111;font-weight:600;">Ryan Cooper</strong><a href="https://www.linkedin.com/in/ryan-cooper-nyc/" target="_blank" rel="noopener noreferrer" aria-label="Ryan Cooper LinkedIn" style="display:inline-flex;align-items:center;margin-left:4px;color:#0a66c2;text-decoration:none;vertical-align:middle;"><svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a>&nbsp;&middot;&nbsp;<?php echo esc_html($pub_date); ?></p>

    <!-- Verdict Badge -->
    <?php $verdict_type = $data['verdict_type'] ?? 'recommended'; ?>
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:40px;flex-wrap:wrap;">
      <?php echo aifp_verdict_badge($post_id); ?>
      <?php if ($verdict_desc) : ?>
      <span style="font-size:14px;color:#444444;"><?php echo esc_html($verdict_desc); ?></span>
      <?php endif; ?>
    </div>

    <!-- Consistency Blocks -->
    <?php get_template_part('template-parts/consistency-blocks'); ?>
  </section>

  <!-- Quick Facts Bar -->
  <section style="padding:0 min(6.5rem,8vw) min(3rem,4vw);">
    <?php get_template_part('template-parts/quick-facts'); ?>
  </section>

  <!-- What It Is (and Is Not) -->
  <?php if (!empty($data['what_it_is'])) : ?>
  <section style="padding:min(3rem,4vw) min(6.5rem,8vw);">
    <div style="max-width:760px;">
      <h2 style="font-size:26px;font-weight:700;color:#111111;margin:0 0 20px;">What <?php echo esc_html($tool_name); ?> Is — And What It Isn't</h2>
      <div style="font-size:14px;color:#444444;line-height:1.8;"><?php echo $data['what_it_is']; // trusted migration content ?></div>
    </div>
  </section>
  <?php endif; ?>

  <!-- Who It's Right For -->
  <?php if (!empty($data['who_its_right_for'])) : ?>
  <section style="padding:min(2rem,3vw) min(6.5rem,8vw) min(3rem,4vw);background:#ffffff;">
    <div style="max-width:760px;">
      <h2 style="font-size:26px;font-weight:700;color:#111111;margin:0 0 24px;">Who <?php echo esc_html($tool_name); ?> Is Right For</h2>
      <div style="font-size:14px;color:#444444;line-height:1.8;"><?php echo $data['who_its_right_for']; // trusted migration content ?></div>
    </div>
  </section>
  <?php endif; ?>

  <!-- Features That Matter -->
  <?php $features = $data['features'] ?? []; ?>
  <?php if (!empty($features)) : ?>
  <section style="padding:min(3rem,4vw) min(6.5rem,8vw);">
    <div style="max-width:760px;">
      <h2 style="font-size:26px;font-weight:700;color:#111111;margin:0 0 8px;">Features That Matter for Professional Workflows</h2>
      <p style="font-size:14px;color:#636363;margin:0 0 32px;">An honest assessment of the seven capabilities professionals actually use, with real-world caveats for each.</p>
      <div style="display:flex;flex-direction:column;gap:24px;">
        <?php foreach ($features as $i => $feat) : ?>
        <div<?php echo ($i < count($features) - 1) ? ' style="border-bottom:1px solid #f0f0f0;padding-bottom:24px;"' : ''; ?>>
          <h3 style="font-size:15px;font-weight:700;color:#111111;margin:0 0 8px;"><?php echo esc_html($feat['feature_name'] ?? ''); ?></h3>
          <div style="font-size:14px;color:#444444;line-height:1.75;"><?php echo $feat['feature_description'] ?? ''; // trusted migration content ?></div>
        </div>
        <?php endforeach; ?>
      </div>
    </div>
  </section>
  <?php endif; ?>

  <!-- Pricing -->
  <?php if (!empty($data['pricing_html'])) : ?>
  <section style="padding:min(3rem,4vw) min(6.5rem,8vw);background:#ffffff;">
    <div style="max-width:760px;">
      <?php echo $data['pricing_html']; // trusted migration content ?>
    </div>
  </section>
  <?php elseif (!empty($data['pricing_tiers'])) : ?>
  <section style="padding:min(3rem,4vw) min(6.5rem,8vw);background:#ffffff;">
    <div style="max-width:760px;">
      <h2 style="font-size:26px;font-weight:700;color:#111111;margin:0 0 24px;">Pricing</h2>
      <div style="border:1px solid #f0f0f0;border-radius:12px;overflow-x:auto;">
        <table style="min-width:520px;width:auto;border-collapse:collapse;font-size:13px;">
          <thead>
            <tr style="background:#f9fafb;border-bottom:1px solid #f0f0f0;">
              <th style="text-align:left;padding:12px 16px;font-weight:700;color:#111111;">Plan</th>
              <th style="text-align:left;padding:12px 16px;font-weight:700;color:#111111;">Price</th>
              <th style="text-align:left;padding:12px 16px;font-weight:700;color:#111111;">What You Get</th>
            </tr>
          </thead>
          <tbody>
            <?php foreach ($data['pricing_tiers'] as $tier) : ?>
            <tr style="border-bottom:1px solid #f5f5f5;">
              <td style="padding:12px 16px;color:#444444;font-weight:500;"><?php echo esc_html($tier['tier_name'] ?? ''); ?></td>
              <td style="padding:12px 16px;color:#444444;"><?php echo esc_html($tier['tier_price'] ?? ''); ?></td>
              <td style="padding:12px 16px;color:#636363;"><?php echo esc_html($tier['tier_features'] ?? ''); ?></td>
            </tr>
            <?php endforeach; ?>
          </tbody>
        </table>
      </div>
    </div>
  </section>
  <?php endif; ?>

  <!-- Profession Cards -->
  <section id="professions" style="padding:min(3rem,4vw) min(6.5rem,8vw) min(4rem,5vw);">
    <?php get_template_part('template-parts/profession-cards'); ?>
  </section>

  <!-- Comparison Table -->
  <?php if (!empty($data['comparison_html'])) : ?>
  <section style="padding:min(3rem,4vw) min(6.5rem,8vw);background:#ffffff;">
    <div style="max-width:900px;">
      <?php echo $data['comparison_html']; // trusted migration content ?>
    </div>
  </section>
  <?php else : ?>
  <section style="padding:min(3rem,4vw) min(6.5rem,8vw);background:#ffffff;">
    <div style="max-width:900px;">
      <?php get_template_part('template-parts/comparison-table'); ?>
    </div>
  </section>
  <?php endif; ?>

  <!-- Verdict -->
  <?php if (!empty($data['verdict_text'])) : ?>
  <section id="verdict" style="padding:min(3rem,4vw) min(6.5rem,8vw);">
    <div style="max-width:760px;background:#ffffff;border-radius:16px;padding:36px;border:1px solid #f0f0f0;">
      <h2 style="font-size:26px;font-weight:700;color:#111111;margin:0 0 20px;">My Verdict</h2>
      <div style="font-size:14px;color:#444444;line-height:1.8;"><?php echo $data['verdict_text']; // trusted migration content ?></div>
    </div>
  </section>
  <?php endif; ?>

  <!-- FAQ -->
  <section style="padding:min(3rem,4vw) min(6.5rem,8vw);background:#ffffff;">
    <div style="max-width:760px;">
      <?php get_template_part('template-parts/faq-section'); ?>
    </div>
  </section>

  <!-- Sources Checked -->
  <section style="padding:min(3rem,4vw) min(6.5rem,8vw);">
    <div style="max-width:760px;">
      <?php get_template_part('template-parts/sources-checked'); ?>
    </div>
  </section>

  <!-- What Most Reviews Miss -->
  <section style="padding:min(3rem,4vw) min(6.5rem,8vw);background:#ffffff;">
    <div style="max-width:760px;">
      <?php get_template_part('template-parts/reviews-miss'); ?>
    </div>
  </section>

  <!-- Related Guides -->
  <section style="padding:min(3rem,4vw) min(6.5rem,8vw) min(5rem,6vw);">
    <div style="max-width:760px;">
      <?php get_template_part('template-parts/related-guides'); ?>
    </div>
  </section>

</main>

<?php get_footer(); ?>
