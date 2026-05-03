<?php
/**
 * Template: Default Page
 * Used for: About Us, Newsletter, Our Process, Cookie Policy, Privacy Policy
 *
 * Bare layout — content controls its own padding, max-width, and grids.
 * wpautop is disabled site-wide for pages in functions.php.
 *
 * @package AIFP
 */

get_header();
?>

<main>
  <?php the_content(); ?>
</main>

<?php get_footer(); ?>
