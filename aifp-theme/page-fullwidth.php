<?php
/**
 * Template Name: Full Width Page
 * Template Post Type: page
 *
 * Used for: About Us, Newsletter
 * Renders content at full viewport width — content controls its own layout via section padding.
 *
 * @package AIFP
 */

get_header();
?>

<main style="background:#f9f9f9;">
  <?php the_content(); ?>
</main>

<?php get_footer(); ?>
