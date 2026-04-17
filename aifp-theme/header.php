<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
  <meta charset="<?php bloginfo('charset'); ?>">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<nav style="padding:18px min(6.5rem,8vw);position:sticky;top:0;z-index:50;background:#ffffff;border-bottom:1px solid #f0f0f0;display:flex;align-items:center;justify-content:space-between;">
  <a href="<?php echo esc_url(home_url('/')); ?>" style="display:flex;align-items:center;gap:10px;text-decoration:none;">
    <img src="<?php echo esc_url(get_theme_file_uri('assets/svg/logo.svg')); ?>" width="32" height="32" alt="<?php bloginfo('name'); ?>" style="border-radius:8px;display:block;">
    <span style="font-size:13px;font-weight:500;color:#111111;">AI Tools for Pros</span>
  </a>
  <div id="nav-desktop" style="display:flex;align-items:center;gap:36px;">
    <a href="<?php echo esc_url(home_url('/our-process')); ?>" class="nav-link">Our Process</a>

    <!-- AI Tools Dropdown -->
    <div class="nav-dropdown">
      <span class="nav-link-caret">AI Tools <svg width="8" height="5" viewBox="0 0 8 5" fill="none"><path d="M1 1l3 3 3-3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
      <div class="dropdown-menu">
        <?php
        $tools = aifp_get_tool_reviews();
        foreach ($tools as $tool) :
          $td = aifp_get_data($tool->ID);
          $name = $td['tool_name'] ?? $tool->post_title;
        ?>
          <a href="<?php echo esc_url(get_permalink($tool->ID)); ?>" class="dropdown-item"><?php echo esc_html($name); ?></a>
        <?php endforeach; ?>
      </div>
    </div>

    <!-- Professions Dropdown -->
    <div class="nav-dropdown">
      <span class="nav-link-caret">Professions <svg width="8" height="5" viewBox="0 0 8 5" fill="none"><path d="M1 1l3 3 3-3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
      <div class="dropdown-menu">
        <?php
        $professions = aifp_get_profession_hubs();
        foreach ($professions as $prof) :
          $pd = aifp_get_data($prof->ID);
          $prof_name = $pd['profession_name'] ?? $prof->post_title;
          $prof_xrefs = aifp_get_cross_references_for_profession($prof->ID);
        ?>
          <div class="submenu-item">
            <a href="<?php echo esc_url(get_permalink($prof->ID)); ?>" class="submenu-trigger"><?php echo esc_html($prof_name); ?> <svg width="5" height="8" viewBox="0 0 5 8" fill="none"><path d="M1 1l3 3-3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
            <?php if (!empty($prof_xrefs)) : ?>
            <div class="submenu">
              <?php foreach ($prof_xrefs as $xref) :
                $xt = aifp_get_linked_post($xref->ID, 'linked_tool');
                if ($xt) :
                  $xtd = aifp_get_data($xt->ID);
              ?>
                <a href="<?php echo esc_url(get_permalink($xref->ID)); ?>"><?php echo esc_html($xtd['tool_name'] ?? $xt->post_title); ?></a>
              <?php endif; endforeach; ?>
            </div>
            <?php endif; ?>
          </div>
        <?php endforeach; ?>
      </div>
    </div>

    <a href="<?php echo esc_url(home_url('/newsletter')); ?>" class="nav-link">Newsletter</a>
  </div>
</nav>
