<?php
/**
 * Template: Homepage (front-page.php)
 *
 * @package AIFP
 */

get_header();

$tools       = aifp_get_tool_reviews();
$professions = aifp_get_profession_hubs();
?>

<!-- HERO -->
<section style="padding: min(6rem,8vw) min(6.5rem, 8vw) min(2.5rem,3vw); text-align:center;">
  <div style="display:inline-flex;align-items:center;background:#111111;color:#ffffff;font-size:9px;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;padding:8px 20px;border-radius:999px;margin-bottom:52px;">
    150+ AI Tools, Independently Reviewed
  </div>

  <h1 class="font-heading" style="font-size:clamp(3.4rem,7.5vw,5.8rem);font-weight:700;line-height:1.04;margin:0 0 28px;color:#111111;">
    Work with<br>
    <span style="background:linear-gradient(90deg, #2563EB 0%, #0ea5e9 40%, #14b8a6 75%, #22c55e 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">Absolute Intelligence.</span>
  </h1>

  <p style="color:#636363;font-size:14px;line-height:1.75;max-width:430px;margin:0 auto 44px;">
    We test AI tools the way you actually use them, by profession. Whether you're a lawyer, a doctor, a real estate agent, or an engineer, we'll tell you which tools are worth your time and which ones fall short.
  </p>

  <div style="display:flex;align-items:center;justify-content:center;gap:14px;">
    <a href="<?php echo esc_url(home_url('/our-process')); ?>" style="background:#ffffff;color:#111111;font-size:14px;font-weight:500;padding:13px 32px;border-radius:999px;border:1.5px solid #e5e7eb;text-decoration:none;transition:border-color 0.15s;" onmouseover="this.style.borderColor='#9ca3af'" onmouseout="this.style.borderColor='#e5e7eb'">
      How We Test Tools
    </a>
  </div>
</section>

<!-- HOW WE WORK -->
<section style="padding: min(3rem,3.5vw) min(6.5rem, 8vw) min(6rem,7vw);">
  <div style="text-align:center;margin-bottom:52px;">
    <h2 class="font-heading" style="font-size:clamp(1.8rem,3vw,2.4rem);font-weight:700;color:#111111;margin:0 0 14px;">How We Work</h2>
    <p style="color:#636363;font-size:14px;margin:0;max-width:420px;margin-left:auto;margin-right:auto;line-height:1.7;">
      There are thousands of AI tools out there. Most reviews don't tell you much. Here's what makes ours different.
    </p>
  </div>

  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:32px;">
    <div style="background:#ffffff;border-radius:16px;padding:32px;border:1px solid #f0f0f0;">
      <div style="width:40px;height:40px;background:#eff6ff;border-radius:10px;display:flex;align-items:center;justify-content:center;margin-bottom:20px;">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M4 10l4 4 8-8" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>
      <h3 style="font-size:16px;font-weight:600;color:#111111;margin:0 0 10px;">We Test Every Tool Ourselves</h3>
      <p style="color:#636363;font-size:13px;line-height:1.7;margin:0;">Every tool in our directory gets put through real professional workflows, not just product demos. We use them the way you would, note where they shine, and report back honestly when they fall short.</p>
    </div>
    <div style="background:#ffffff;border-radius:16px;padding:32px;border:1px solid #f0f0f0;">
      <div style="width:40px;height:40px;background:#eff6ff;border-radius:10px;display:flex;align-items:center;justify-content:center;margin-bottom:20px;">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><rect x="3" y="6" width="14" height="11" rx="2" stroke="#2563EB" stroke-width="2"/><path d="M7 6V5a3 3 0 016 0v1" stroke="#2563EB" stroke-width="2" stroke-linecap="round"/></svg>
      </div>
      <h3 style="font-size:16px;font-weight:600;color:#111111;margin:0 0 10px;">Reviews Built for Your Profession</h3>
      <p style="color:#636363;font-size:13px;line-height:1.7;margin:0;">A tool that works well in marketing might be completely wrong for a courtroom or a clinic. Our reviews are structured around the specific tasks, compliance requirements, and standards of each profession.</p>
    </div>
    <div style="background:#ffffff;border-radius:16px;padding:32px;border:1px solid #f0f0f0;">
      <div style="width:40px;height:40px;background:#eff6ff;border-radius:10px;display:flex;align-items:center;justify-content:center;margin-bottom:20px;">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 2l2 6h6l-5 3.6 1.9 6L10 14l-4.9 3.6L7 11.6 2 8h6L10 2z" stroke="#2563EB" stroke-width="1.8" stroke-linejoin="round" fill="none"/></svg>
      </div>
      <h3 style="font-size:16px;font-weight:600;color:#111111;margin:0 0 10px;">Completely Independent</h3>
      <p style="color:#636363;font-size:13px;line-height:1.7;margin:0;">We don't accept payment for rankings, placements, or positive coverage. No sponsored results, no undisclosed relationships. Our only job is to give you an honest answer to the question: is this tool worth it?</p>
    </div>
  </div>
</section>

<!-- EXPLORE BY PROFESSION -->
<?php if (!empty($professions)) : ?>
<section style="padding: 0 min(6.5rem, 8vw) min(8rem,10vw);">
  <h2 style="font-size:22px;font-weight:700;color:#111111;margin:0 0 8px;">Explore by Profession</h2>
  <p style="color:#636363;font-size:13px;margin:0 0 40px;">Find AI tools reviewed specifically for your field, not generic rankings.</p>

  <div class="professions-grid" style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;">
    <?php foreach ($professions as $prof) :
      $pd = aifp_get_data($prof->ID);
      $name = $pd['profession_name'] ?? $prof->post_title;
      $xref_count = count(aifp_get_cross_references_for_profession($prof->ID));
    ?>
    <a href="<?php echo esc_url(get_permalink($prof->ID)); ?>" class="industry-card" style="text-decoration:none;display:block;">
      <span style="color:#2563EB;font-size:9px;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;display:block;margin-bottom:16px;"><?php echo esc_html($xref_count); ?> Tools Reviewed</span>
      <h3 class="font-heading" style="font-size:24px;font-weight:700;color:#111111;margin:0 0 10px;"><?php echo esc_html($name); ?></h3>
      <span style="font-size:12px;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;color:#2563EB;">View Toolkit <span>→</span></span>
    </a>
    <?php endforeach; ?>
  </div>
</section>
<?php endif; ?>

<!-- AI TOOLS -->
<?php if (!empty($tools)) : ?>
<section style="padding: 0 min(6.5rem, 8vw) min(8rem,10vw);">
  <h2 style="font-size:22px;font-weight:700;color:#111111;margin:0 0 8px;">AI Tools We Review</h2>
  <p style="color:#636363;font-size:13px;margin:0 0 40px;">In-depth, independent assessments of the tools professionals are actually using.</p>

  <div class="tools-grid" style="display:grid;grid-template-columns:repeat(2,1fr);gap:20px;">
    <?php foreach ($tools as $tool) :
      $td = aifp_get_data($tool->ID);
      $name    = $td['tool_name'] ?? $tool->post_title;
      $best_for = $td['quick_facts']['best_for_fact'] ?? '';
    ?>
    <a href="<?php echo esc_url(get_permalink($tool->ID)); ?>" style="background:#ffffff;border:1px solid #f0f0f0;border-radius:16px;padding:28px 32px;text-decoration:none;transition:box-shadow 0.2s;display:flex;justify-content:space-between;align-items:center;" onmouseover="this.style.boxShadow='0 4px 20px rgba(0,0,0,0.06)'" onmouseout="this.style.boxShadow='none'">
      <div>
        <h3 style="font-size:18px;font-weight:600;color:#111111;margin:0 0 6px;"><?php echo esc_html($name); ?></h3>
        <p style="font-size:12px;color:#636363;margin:0;"><?php echo esc_html($best_for); ?></p>
      </div>
      <?php echo aifp_verdict_badge($tool->ID); ?>
    </a>
    <?php endforeach; ?>
  </div>
</section>
<?php endif; ?>

<?php get_footer(); ?>
