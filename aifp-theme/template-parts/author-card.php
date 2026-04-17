<?php
/**
 * Template Part: Author Profile Card
 * Displayed before the footer on content pages (not homepage).
 *
 * @package AIFP
 */

// Don't show on homepage
if (is_front_page()) return;
?>

<section style="padding:0 min(6.5rem,8vw) min(4rem,6vw);">
  <div style="max-width:760px;margin:0 auto;border-top:1px solid #f0f0f0;padding-top:36px;">
    <p style="font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#636363;margin:0 0 20px;">About the Author</p>
    <div style="display:flex;align-items:flex-start;gap:24px;">
      <div style="flex-shrink:0;">
        <img src="<?php echo esc_url(aifp_svg_url('author.svg')); ?>" width="72" height="72" alt="Richard Migliorisi, Founder of AI Tools for Pros" style="border-radius:50%;display:block;">
      </div>
      <div>
        <p style="font-size:15px;font-weight:600;color:#111111;margin:0 0 2px;">Richard Migliorisi <a href="https://www.linkedin.com/in/richardmigliorisi/" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn" style="display:inline-flex;align-items:center;margin-left:4px;color:#0a66c2;text-decoration:none;vertical-align:middle;"><svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a></p>
        <p style="font-size:12px;color:#636363;margin:0 0 12px;">Founder, AI Tools for Pros &nbsp;&middot;&nbsp; 8+ years in SEO</p>
        <p style="font-size:14px;color:#444444;line-height:1.7;margin:0 0 12px;">Richard Migliorisi is an SEO and organic growth leader with 8+ years of experience building search into a primary revenue channel in competitive markets. He most recently led SEO, content, and web operations at The Game Day, helping drive the site from zero to nearly $10M in web revenue in under three years. He built AI Tools for Pros to give working professionals honest, independent assessments of AI tools, without sponsored placements or vendor influence.</p>
        <a href="<?php echo esc_url(home_url('/about-us')); ?>" style="font-size:12px;font-weight:600;color:#2563EB;text-decoration:none;letter-spacing:0.03em;" onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">More about Richard &rarr;</a>
      </div>
    </div>
  </div>
</section>
