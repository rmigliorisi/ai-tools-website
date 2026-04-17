<?php
/**
 * Template Part: FAQ Section
 *
 * @package AIFP
 */

$post_id = $post_id ?? get_the_ID();
$data    = aifp_get_data($post_id);
$faqs    = $data['faq'] ?? [];

if (empty($faqs)) return;
?>

<section style="padding:48px 0 min(3rem,4vw);max-width:760px;">
  <h2 class="font-heading" style="font-size:28px;font-weight:700;color:#111111;margin:0 0 28px;">Frequently Asked Questions</h2>
  <?php foreach ($faqs as $item) : ?>
  <div style="border-bottom:1px solid #f0f0f0;padding:20px 0;">
    <h3 style="font-size:15px;font-weight:600;color:#111111;margin:0 0 10px;"><?php echo esc_html($item['question'] ?? ''); ?></h3>
    <div style="font-size:14px;color:#444444;line-height:1.7;margin:0;">
      <?php echo $item['answer'] ?? ''; // trusted migration content ?>
    </div>
  </div>
  <?php endforeach; ?>
</section>
