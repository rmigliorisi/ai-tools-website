<?php
/**
 * Template: Default Page (prose pages)
 * Used for: About Us, Our Process, Newsletter, Cookie Policy, Privacy Policy
 *
 * @package AIFP
 */

get_header();
?>

<main class="prose-page" style="background:#f9f9f9;padding:0 min(6.5rem,8vw);">
  <div style="max-width:760px;padding:48px 0;">

    <h1 class="font-heading" style="font-size:clamp(28px,4vw,40px);font-weight:700;color:#111111;margin:0 0 24px;line-height:1.15;">
      <?php the_title(); ?>
    </h1>

    <div style="font-size:15px;color:#333333;line-height:1.75;">
      <?php the_content(); ?>
    </div>

  </div>
</main>

<?php get_footer(); ?>
