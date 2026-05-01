<?php
/**
 * AI Tools for Pros — Theme Functions
 *
 * @package AIFP
 */

defined('ABSPATH') || exit;

/* ──────────────────────────────────────────────
   1. Theme Setup
   ────────────────────────────────────────────── */
add_action('after_setup_theme', function () {
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    add_theme_support('html5', ['search-form', 'comment-form', 'comment-list', 'gallery', 'caption']);

    register_nav_menus([
        'primary' => __('Primary Navigation', 'aifp'),
    ]);
});

/* ──────────────────────────────────────────────
   2. Enqueue Styles & Scripts
   ────────────────────────────────────────────── */
add_action('wp_enqueue_scripts', function () {
    // Google Fonts
    wp_enqueue_style('aifp-google-fonts',
        'https://fonts.googleapis.com/css2?family=Cardo:ital,wght@0,400;0,700;1,400&family=Inter:ital,wght@0,400;0,500;0,600;1,400&display=swap',
        [], null
    );

    // Theme version for cache busting
    $ver = '1.0.0';

    // Main stylesheet (the migrated style.css from the static site)
    wp_enqueue_style('aifp-site',
        get_theme_file_uri('assets/css/site.css'),
        ['aifp-google-fonts'],
        $ver
    );

    // Inline nav/component styles (previously in each page's <style> block)
    wp_enqueue_style('aifp-components',
        get_theme_file_uri('assets/css/components.css'),
        ['aifp-site'],
        $ver
    );

    // Main JS (dark mode, mobile nav, reading time, FAQ toggles)
    wp_enqueue_script('aifp-site-js',
        get_theme_file_uri('assets/js/site.js'),
        [], $ver,
        ['strategy' => 'defer']
    );
});

/* ──────────────────────────────────────────────
   3. Include Modules
   ────────────────────────────────────────────── */
require_once get_theme_file_path('inc/cpt.php');
require_once get_theme_file_path('inc/helpers.php');
require_once get_theme_file_path('inc/json-ld.php');

// ACF field groups (only if ACF Pro is active)
if (function_exists('acf_add_local_field_group') && defined('ACF_PRO')) {
    require_once get_theme_file_path('inc/acf-fields.php');
}

/* ──────────────────────────────────────────────
   3b. Register Post Meta for REST API
   ────────────────────────────────────────────── */
add_action('init', function () {
    $int_args = ['type' => 'integer', 'single' => true, 'show_in_rest' => true, 'default' => 0];
    register_post_meta('cross_reference', 'linked_tool', $int_args);
    register_post_meta('cross_reference', 'linked_profession', $int_args);
});

/* ──────────────────────────────────────────────
   4. Custom Permalink Structures
   ────────────────────────────────────────────── */
add_action('init', function () {
    // Tool Reviews: /chatgpt/, /claude/, etc.
    add_rewrite_rule(
        '^(chatgpt|claude|perplexity|gemini|copilot|midjourney|cursor|notion-ai|grammarly|otter)/?$',
        'index.php?post_type=tool_review&name=$matches[1]',
        'top'
    );

    // Profession Hubs: /legal/, /physicians/, etc.
    add_rewrite_rule(
        '^(legal|physicians|engineers|real-estate|finance|insurance|architects|creatives)/?$',
        'index.php?post_type=profession_hub&name=$matches[1]',
        'top'
    );

    // Cross-Reference: /chatgpt/legal/, /claude/engineers/, etc.
    add_rewrite_rule(
        '^(chatgpt|claude|perplexity|gemini|copilot|midjourney|cursor|notion-ai|grammarly|otter)/([^/]+)/?$',
        'index.php?post_type=cross_reference&name=$matches[1]-$matches[2]',
        'top'
    );
});

/* ──────────────────────────────────────────────
   4. Preserve JSON + inline styles in post_content
   ────────────────────────────────────────────── */
add_filter('wp_insert_post_data', function ($data) {
    if (in_array($data['post_type'] ?? '', ['tool_review', 'profession_hub', 'cross_reference'])) {
        remove_filter('the_content', 'wpautop');
    }
    return $data;
});

// Allow modern CSS properties (grid, flex, clamp, etc.) so wp_kses_post
// doesn't strip layout styles from migration-sourced HTML.
add_filter('safe_style_css', function ($styles) {
    return array_merge($styles, [
        'display', 'flex', 'flex-direction', 'flex-wrap', 'flex-shrink', 'flex-grow',
        'align-items', 'align-self', 'justify-content', 'justify-self',
        'gap', 'row-gap', 'column-gap',
        'grid', 'grid-template-columns', 'grid-template-rows',
        'grid-column', 'grid-row', 'grid-area',
        'max-width', 'min-width', 'max-height', 'min-height',
        'border-radius', 'box-shadow', 'transition',
        'line-height', 'letter-spacing', 'text-transform', 'text-overflow',
        'white-space', 'overflow', 'overflow-x', 'overflow-y',
        'object-fit', 'object-position', 'resize', 'cursor',
        'position', 'top', 'right', 'bottom', 'left', 'z-index',
        'opacity', 'transform', 'font-style', 'font-family',
    ]);
});

/* ──────────────────────────────────────────────
   5. Disable Unnecessary WordPress Features
   ────────────────────────────────────────────── */
// Remove emoji scripts
remove_action('wp_head', 'print_emoji_detection_script', 7);
remove_action('wp_print_styles', 'print_emoji_styles');

// Remove WordPress version meta tag
remove_action('wp_head', 'wp_generator');

// Remove RSD and WLW links
remove_action('wp_head', 'rsd_link');
remove_action('wp_head', 'wlmanifest_link');

/* ──────────────────────────────────────────────
   6. Favicon
   ────────────────────────────────────────────── */
add_action('wp_head', function () {
    echo '<link rel="icon" type="image/svg+xml" href="' . esc_url(get_theme_file_uri('assets/svg/favicon.svg')) . '">' . "\n";
});

/* ──────────────────────────────────────────────
   7. Open Graph + Twitter Card Meta Tags
   ────────────────────────────────────────────── */
add_action('wp_head', function () {
    if (!is_singular()) return;

    $post_id   = get_the_ID();
    $post_type = get_post_type($post_id);
    $data      = aifp_get_data($post_id);
    $site_name = 'AI Tools for Pros';
    $default_img = 'https://aitoolsforpros.com/wp-content/uploads/2025/11/cropped-aitoolsforpros.png';
    $url       = get_permalink($post_id);

    if ($post_type === 'tool_review') {
        $tool_name = $data['tool_name'] ?? get_the_title();
        $title     = $tool_name . ' for Professionals: An Honest Review (' . date('Y') . ')';
        $desc      = wp_strip_all_tags($data['definition_sentence'] ?? $data['positioning_statement'] ?? '');
        if (!$desc) $desc = 'An independent, in-depth review of ' . $tool_name . ' for professional use.';

    } elseif ($post_type === 'cross_reference') {
        $tool = aifp_get_linked_post($post_id, 'linked_tool');
        $prof = aifp_get_linked_post($post_id, 'linked_profession');
        $tool_name = $tool ? (aifp_get_data($tool->ID)['tool_name'] ?? $tool->post_title) : '';
        $prof_name = $prof ? (aifp_get_data($prof->ID)['profession_name'] ?? $prof->post_title) : '';
        $title = $data['title'] ?? ($tool_name . ' for ' . $prof_name . ': Practical AI Guide');
        $desc  = wp_strip_all_tags($data['subtitle'] ?? '');
        if (!$desc) $desc = 'How ' . $tool_name . ' helps ' . $prof_name . ' work smarter.';

    } elseif ($post_type === 'profession_hub') {
        $prof_name = $data['profession_name'] ?? get_the_title();
        $title     = 'Best AI Tools for ' . $prof_name . ' (2026 Guide)';
        $desc      = wp_strip_all_tags($data['intro_text'] ?? $data['subtitle'] ?? '');
        if (!$desc) $desc = 'The top AI tools for ' . $prof_name . ', reviewed and ranked.';

    } else {
        $title = get_the_title();
        $desc  = get_the_excerpt();
    }

    $desc = mb_strimwidth(wp_strip_all_tags($desc), 0, 160, '...');

    echo '<meta name="description" content="' . esc_attr($desc) . '">' . "\n";
    echo '<link rel="canonical" href="' . esc_url($url) . '">' . "\n";
    echo '<meta property="og:title" content="' . esc_attr($title) . '">' . "\n";
    echo '<meta property="og:description" content="' . esc_attr($desc) . '">' . "\n";
    echo '<meta property="og:url" content="' . esc_url($url) . '">' . "\n";
    echo '<meta property="og:type" content="article">' . "\n";
    echo '<meta property="og:site_name" content="' . esc_attr($site_name) . '">' . "\n";
    echo '<meta property="og:image" content="' . esc_url($default_img) . '">' . "\n";
    echo '<meta name="twitter:card" content="summary_large_image">' . "\n";
    echo '<meta name="twitter:title" content="' . esc_attr($title) . '">' . "\n";
    echo '<meta name="twitter:description" content="' . esc_attr($desc) . '">' . "\n";
    echo '<meta name="twitter:image" content="' . esc_url($default_img) . '">' . "\n";
}, 5);
