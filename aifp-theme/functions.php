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
    $ver = '1.0.6';

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

    // AI Updates: /july-2026-updates/, /august-2026-updates/, etc.
    // Slug changes every month, so this matches the shape (month-year-updates)
    // rather than a hardcoded list like the rules above.
    add_rewrite_rule(
        '^([a-z]+-[0-9]{4}-updates)/?$',
        'index.php?post_type=aifp_update&name=$matches[1]',
        'top'
    );
});

/* ──────────────────────────────────────────────
   4b. Disable redirect_canonical for custom post types
   CPTs with rewrite=>false have no default permalink structure,
   so redirect_canonical redirects clean URLs to ?post_type=slug.
   Returning false stops that redirect; clean rewrite rules handle routing.
   ────────────────────────────────────────────── */
add_filter('redirect_canonical', function ($redirect_url) {
    if (is_singular(['tool_review', 'profession_hub', 'cross_reference', 'aifp_update'])) {
        return false;
    }
    return $redirect_url;
});

/* ──────────────────────────────────────────────
   4. Preserve JSON + inline styles in post_content
   ────────────────────────────────────────────── */
add_filter('wp_insert_post_data', function ($data) {
    if (in_array($data['post_type'] ?? '', ['tool_review', 'profession_hub', 'cross_reference', 'page'])) {
        remove_filter('the_content', 'wpautop');
    }
    return $data;
});

// Also disable wpautop on page output — content is raw HTML, not prose paragraphs
add_action('template_redirect', function () {
    if (is_page()) {
        remove_filter('the_content', 'wpautop');
    }
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
   5. Custom sitemap at /sitemap.xml
   Priority 1 fires before Jetpack (priority 10).
   Checks raw REQUEST_URI so it intercepts the URL
   before any plugin can handle it.
   ────────────────────────────────────────────── */
add_action('init', function () {
    $path = parse_url($_SERVER['REQUEST_URI'] ?? '', PHP_URL_PATH);
    if (trim($path, '/') !== 'sitemap-pages.xml') return;

    status_header(200);
    header('Content-Type: application/xml; charset=UTF-8');
    nocache_headers();

    $base    = 'https://aitoolsforpros.com';
    $entries = [];

    $mod = function ($post) {
        return get_post_modified_time('Y-m-d', true, $post);
    };

    // Homepage — use most recently modified post across all types
    $latest = get_posts(['post_type' => ['page','tool_review','profession_hub','cross_reference','aifp_update'], 'post_status' => 'publish', 'posts_per_page' => 1, 'orderby' => 'modified', 'order' => 'DESC']);
    $entries[] = ['url' => $base . '/', 'lastmod' => $latest ? $mod($latest[0]) : current_time('Y-m-d'), 'priority' => '1.0', 'changefreq' => 'daily'];

    // Standard pages
    $page_priority = [
        'newsletter'     => '0.7',
        'about-us'       => '0.6',
        'our-process'    => '0.6',
        'privacy-policy' => '0.3',
        'cookie-policy'  => '0.3',
    ];
    $pages = get_posts(['post_type' => 'page', 'post_status' => 'publish', 'posts_per_page' => -1]);
    foreach ($pages as $p) {
        if (get_permalink($p) === $base . '/') continue;
        $entries[] = [
            'url'        => rtrim(get_permalink($p), '/') . '/',
            'lastmod'    => $mod($p),
            'priority'   => $page_priority[$p->post_name] ?? '0.5',
            'changefreq' => 'monthly',
        ];
    }

    // Tool review hub pages: /{slug}/
    $reviews = get_posts(['post_type' => 'tool_review', 'post_status' => 'publish', 'posts_per_page' => -1]);
    foreach ($reviews as $p) {
        $entries[] = ['url' => $base . '/' . $p->post_name . '/', 'lastmod' => $mod($p), 'priority' => '0.9', 'changefreq' => 'monthly'];
    }

    // Profession hub pages: /{slug}/
    $hubs = get_posts(['post_type' => 'profession_hub', 'post_status' => 'publish', 'posts_per_page' => -1]);
    foreach ($hubs as $p) {
        $entries[] = ['url' => $base . '/' . $p->post_name . '/', 'lastmod' => $mod($p), 'priority' => '0.9', 'changefreq' => 'monthly'];
    }

    // Cross-reference pages: /{tool}/{profession}/
    $xrefs = get_posts(['post_type' => 'cross_reference', 'post_status' => 'publish', 'posts_per_page' => -1]);
    foreach ($xrefs as $p) {
        $url = get_permalink($p);
        if ($url && strpos($url, '?') === false) {
            $entries[] = ['url' => rtrim($url, '/') . '/', 'lastmod' => $mod($p), 'priority' => '0.8', 'changefreq' => 'monthly'];
        }
    }

    // AI Updates pages: /{month}-{year}-updates/ (only ever published manually, see docs/AIFORPROS-AUTOMATED-CONTENT.md)
    $ai_updates = get_posts(['post_type' => 'aifp_update', 'post_status' => 'publish', 'posts_per_page' => -1]);
    foreach ($ai_updates as $p) {
        $entries[] = ['url' => $base . '/' . $p->post_name . '/', 'lastmod' => $mod($p), 'priority' => '0.6', 'changefreq' => 'yearly'];
    }

    echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
    echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
    foreach ($entries as $e) {
        echo "  <url>\n";
        echo "    <loc>" . esc_url($e['url']) . "</loc>\n";
        echo "    <lastmod>" . esc_html($e['lastmod']) . "</lastmod>\n";
        echo "    <changefreq>" . esc_html($e['changefreq']) . "</changefreq>\n";
        echo "    <priority>" . esc_html($e['priority']) . "</priority>\n";
        echo "  </url>\n";
    }
    echo '</urlset>';
    exit;
}, 1);

/* ──────────────────────────────────────────────
   5b. robots.txt
   ────────────────────────────────────────────── */
add_filter('robots_txt', function () {
    // Policy (updated): allow every major AI crawler, citation bots and
    // training bots alike, for OpenAI, Anthropic, Perplexity, and Google.
    // This is a deliberate reversal of the earlier citation-only-allow /
    // training-disallow split — Rich opted for maximum AI visibility/training
    // inclusion instead of opting out of training crawlers. Bot names
    // confirmed against each company's current published crawler docs as of
    // this edit — these tokens do change over time, so re-verify before
    // major changes. See docs/seo-geo-aeo/10_ROBOTS_SITEMAPS_CRAWLER_ACCESS.md
    // section 5 for background on what each bot does.
    // Sitemap points at the real, final URL (Rank Math's sitemap_index.xml)
    // instead of /wp-sitemap.xml, which just 301s there.
    return "User-agent: *\n"
        . "Disallow: /wp-admin/\n"
        . "Allow: /wp-admin/admin-ajax.php\n\n"
        . "# OpenAI\n"
        . "User-agent: OAI-SearchBot\nAllow: /\n\n"
        . "User-agent: GPTBot\nAllow: /\n\n"
        . "# Anthropic\n"
        . "User-agent: ClaudeBot\nAllow: /\n\n"
        . "User-agent: Claude-SearchBot\nAllow: /\n\n"
        . "User-agent: Claude-User\nAllow: /\n\n"
        . "# Perplexity\n"
        . "User-agent: PerplexityBot\nAllow: /\n\n"
        . "User-agent: Perplexity-User\nAllow: /\n\n"
        . "# Google AI\n"
        . "User-agent: Google-Extended\nAllow: /\n\n"
        . "Sitemap: https://aitoolsforpros.com/sitemap_index.xml\n";
}, 99);

/* ──────────────────────────────────────────────
   6. Disable Unnecessary WordPress Features
   ────────────────────────────────────────────── */
// Remove emoji scripts
remove_action('wp_head', 'print_emoji_detection_script', 7);
remove_action('wp_print_styles', 'print_emoji_styles');

// Remove WordPress version meta tag
remove_action('wp_head', 'wp_generator');

// Remove RSD and WLW links
remove_action('wp_head', 'rsd_link');
remove_action('wp_head', 'wlmanifest_link');

// Suppress user archive from sitemap — author page is empty with no content
add_filter('wp_sitemaps_add_provider', function ($provider, $name) {
    return $name === 'users' ? false : $provider;
}, 10, 2);

/* ──────────────────────────────────────────────
   7. Favicon
   ────────────────────────────────────────────── */
add_action('wp_head', function () {
    echo '<link rel="icon" type="image/svg+xml" href="' . esc_url(get_theme_file_uri('assets/svg/favicon.svg')) . '">' . "\n";
});

/* ──────────────────────────────────────────────
   8. Open Graph + Twitter Card Meta Tags
   ────────────────────────────────────────────── */
add_action('wp_head', function () {
    $site_name   = 'AI Tools for Pros';
    $default_img = 'https://aitoolsforpros.com/wp-content/uploads/2025/11/cropped-aitoolsforpros.png';

    // Homepage: explicit metadata — WordPress defaults leave og:title="Home" and description empty
    if (is_front_page()) {
        $title = 'AI Tools for Professionals: Honest Reviews by Pros';
        $desc  = 'Independent AI tool reviews and workflows for professionals in law, medicine, finance, real estate, content, SEO, and more.';
        $url   = home_url('/');
        echo '<meta name="description" content="' . esc_attr($desc) . '">' . "\n";
        echo '<meta property="og:title" content="' . esc_attr($title) . '">' . "\n";
        echo '<meta property="og:description" content="' . esc_attr($desc) . '">' . "\n";
        echo '<meta property="og:url" content="' . esc_url($url) . '">' . "\n";
        echo '<meta property="og:type" content="website">' . "\n";
        echo '<meta property="og:site_name" content="' . esc_attr($site_name) . '">' . "\n";
        echo '<meta property="og:image" content="' . esc_url($default_img) . '">' . "\n";
        echo '<meta name="twitter:card" content="summary_large_image">' . "\n";
        echo '<meta name="twitter:title" content="' . esc_attr($title) . '">' . "\n";
        echo '<meta name="twitter:description" content="' . esc_attr($desc) . '">' . "\n";
        echo '<meta name="twitter:image" content="' . esc_url($default_img) . '">' . "\n";
        return;
    }

    if (!is_singular()) return;

    $post_id   = get_the_ID();
    $post_type = get_post_type($post_id);
    $data      = aifp_get_data($post_id);
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

    $desc = mb_strimwidth(wp_strip_all_tags($desc), 0, 155);

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

/* ──────────────────────────────────────────────
   9. Google Tag Manager
   ────────────────────────────────────────────── */
add_action('wp_head', function () {
    ?>
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-KCVDNRMV');</script>
<!-- End Google Tag Manager -->
    <?php
}, 1);

add_action('wp_body_open', function () {
    ?>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KCVDNRMV"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
    <?php
}, 1);

/* ──────────────────────────────────────────────
   10. Newsletter Subscribe (AJAX)
   ────────────────────────────────────────────── */
function aifp_handle_subscribe() {
    check_ajax_referer('aifp_subscribe', 'nonce');

    $email = sanitize_email(wp_unslash($_POST['email'] ?? ''));
    if (!is_email($email)) {
        wp_send_json_error(['message' => 'Please enter a valid email address.']);
    }

    global $wpdb;
    $exists = $wpdb->get_var($wpdb->prepare(
        "SELECT ID FROM {$wpdb->posts} WHERE post_type = 'aifp_subscriber' AND post_status = 'publish' AND post_title = %s LIMIT 1",
        $email
    ));

    if ($exists) {
        wp_send_json_success(['message' => "You're already on the list. We'll be in touch!"]); // treat as success so UX is clean
    }

    $result = wp_insert_post([
        'post_type'   => 'aifp_subscriber',
        'post_title'  => $email,
        'post_status' => 'publish',
    ]);

    if (is_wp_error($result)) {
        wp_send_json_error(['message' => 'Something went wrong. Please try again.']);
    }

    wp_send_json_success(['message' => "Thanks for subscribing! Keep an eye on your inbox for future updates from AI Tools for Pros."]);
}
add_action('wp_ajax_nopriv_aifp_subscribe', 'aifp_handle_subscribe');
add_action('wp_ajax_aifp_subscribe', 'aifp_handle_subscribe');

/* ──────────────────────────────────────────────
   11. Contact Form (AJAX)
   ────────────────────────────────────────────── */
function aifp_handle_contact() {
    check_ajax_referer('aifp_contact', 'nonce');

    // Honeypot: bots fill this hidden field, humans don't
    if (!empty($_POST['hp'])) {
        wp_send_json_success(['message' => 'Thanks for your message. We will be in touch.']);
    }

    $name    = sanitize_text_field(wp_unslash($_POST['name'] ?? ''));
    $email   = sanitize_email(wp_unslash($_POST['email'] ?? ''));
    $company = sanitize_text_field(wp_unslash($_POST['company'] ?? ''));
    $reason  = sanitize_text_field(wp_unslash($_POST['reason'] ?? ''));
    $message = sanitize_textarea_field(wp_unslash($_POST['message'] ?? ''));

    if (!$name || !is_email($email) || !$reason || !$message) {
        wp_send_json_error(['message' => 'Please fill in all required fields.']);
    }

    $allowed_reasons = [
        'Suggest an AI tool for review',
        'SEO / AI search consulting',
        'Partnership or media inquiry',
        'General question',
    ];
    if (!in_array($reason, $allowed_reasons, true)) {
        wp_send_json_error(['message' => 'Invalid reason selected.']);
    }

    // Store in WordPress admin
    $post_id = wp_insert_post([
        'post_type'   => 'aifp_contact',
        'post_title'  => $name . ' — ' . $reason,
        'post_status' => 'publish',
    ]);

    if (!is_wp_error($post_id)) {
        update_post_meta($post_id, 'contact_name',    $name);
        update_post_meta($post_id, 'contact_email',   $email);
        update_post_meta($post_id, 'contact_company', $company);
        update_post_meta($post_id, 'contact_reason',  $reason);
        update_post_meta($post_id, 'contact_message', $message);
    }

    // Email notification to site admin (address never exposed to frontend)
    $admin_email = get_option('admin_email');
    $subject     = '[AI Tools for Pros] ' . $reason . ' from ' . $name;
    $body        = "Name: {$name}\nEmail: {$email}\n";
    if ($company) {
        $body .= "Company / URL: {$company}\n";
    }
    $body .= "Reason: {$reason}\n\nMessage:\n{$message}";
    $headers = [
        'Content-Type: text/plain; charset=UTF-8',
        'Reply-To: ' . $name . ' <' . $email . '>',
    ];
    wp_mail($admin_email, $subject, $body, $headers);

    wp_send_json_success(['message' => "Thanks, {$name}. Your message has been received. We typically respond within 2 business days."]);
}
add_action('wp_ajax_nopriv_aifp_contact', 'aifp_handle_contact');
add_action('wp_ajax_aifp_contact', 'aifp_handle_contact');

/* ──────────────────────────────────────────────
   12. Weekly Update Digest (custom REST route for the automated
   tool-page update system — see docs/AIFORPROS-AUTOMATED-CONTENT.md)

   aifp_update_log has show_in_rest = false (matches aifp_contact's
   pattern — internal-only data, not meant to be publicly queryable),
   so the scheduled task can't log entries via the standard
   /wp-json/wp/v2/aifp_update_log route. This authenticated custom
   route is the write path instead: it logs each change as its own
   aifp_update_log post (visible in WP Admin, same as Contact
   Submissions) and sends the weekly digest email in one call.
   ────────────────────────────────────────────── */
add_action('rest_api_init', function () {
    register_rest_route('aifp/v1', '/update-digest', [
        'methods'             => 'POST',
        'callback'            => 'aifp_handle_update_digest',
        'permission_callback' => function () {
            return current_user_can('edit_posts');
        },
    ]);
});

function aifp_handle_update_digest(WP_REST_Request $request) {
    // Each item: { tool, field, old_value, new_value, source, status, reason }
    // status is one of: applied | held | flagged
    $changes  = $request->get_param('changes');
    $changes  = is_array($changes) ? $changes : [];
    $run_date = date('F j, Y');

    $counts = ['applied' => 0, 'held' => 0, 'flagged' => 0];
    $body_sections = ['applied' => '', 'held' => '', 'flagged' => ''];

    foreach ($changes as $item) {
        $tool     = sanitize_text_field($item['tool'] ?? '');
        $field    = sanitize_text_field($item['field'] ?? '');
        $old      = sanitize_text_field($item['old_value'] ?? '');
        $new      = sanitize_text_field($item['new_value'] ?? '');
        $source   = esc_url_raw($item['source'] ?? '');
        $status   = in_array($item['status'] ?? '', ['applied', 'held', 'flagged'], true) ? $item['status'] : 'held';
        $reason   = sanitize_text_field($item['reason'] ?? '');

        $counts[$status]++;
        $body_sections[$status] .= "- [{$tool}] {$field}: \"{$old}\" -> \"{$new}\"" . ($reason ? " ({$reason})" : '') . "\n";

        $log_id = wp_insert_post([
            'post_type'   => 'aifp_update_log',
            'post_title'  => "{$tool} — {$field} — {$run_date}",
            'post_status' => 'publish',
        ]);
        if (!is_wp_error($log_id)) {
            update_post_meta($log_id, 'tool',      $tool);
            update_post_meta($log_id, 'field',     $field);
            update_post_meta($log_id, 'old_value', $old);
            update_post_meta($log_id, 'new_value', $new);
            update_post_meta($log_id, 'source',    $source);
            update_post_meta($log_id, 'status',    $status);
            update_post_meta($log_id, 'reason',    $reason);
            update_post_meta($log_id, 'run_date',  $run_date);
        }
    }

    $admin_email = get_option('admin_email');
    $subject     = '[AI Tools for Pros] Weekly Tool Update Digest — ' . $run_date;
    $body  = "Weekly automated tool-page update run — {$run_date}\n\n";
    $body .= "APPLIED ({$counts['applied']}):\n" . ($body_sections['applied'] ?: "- none\n");
    $body .= "\nHELD FOR REVIEW ({$counts['held']}):\n" . ($body_sections['held'] ?: "- none\n");
    if ($counts['flagged'] > 0) {
        $body .= "\nFLAGGED — VERDICT MAY NEED A LOOK ({$counts['flagged']}):\n" . $body_sections['flagged'];
    }
    $body .= "\nFull detail for each change is logged in WP Admin under Weekly Update Log.\n";

    wp_mail($admin_email, $subject, $body);

    return new WP_REST_Response(['sent' => true, 'counts' => $counts], 200);
}

/* Wire up .newsletter-input-wrap buttons (newsletter page content) */
add_action('wp_footer', function () {
    $ajax_url = esc_url(admin_url('admin-ajax.php'));
    $nonce    = wp_create_nonce('aifp_subscribe');
    ?>
<script>
(function(){
  var forms = document.querySelectorAll('.newsletter-form-row');
  if (!forms.length) return;
  forms.forEach(function(wrap){
    var inp = wrap.querySelector('input[type="email"]');
    var btn = wrap.querySelector('button');
    if (!inp || !btn) return;
    btn.addEventListener('click', function(){
      var email = inp.value.trim();
      if (!email) { inp.focus(); return; }
      btn.disabled = true;
      btn.textContent = 'Subscribing…';
      fetch('<?php echo $ajax_url; ?>', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: 'action=aifp_subscribe&nonce=<?php echo $nonce; ?>&email=' + encodeURIComponent(email)
      })
      .then(function(r){ return r.json(); })
      .then(function(data){
        wrap.innerHTML = '<p style="color:#059669;font-size:14px;font-weight:500;margin:0;line-height:1.6;">' + data.data.message + '</p>';
        if (data.success) {
          window.dataLayer = window.dataLayer || [];
          window.dataLayer.push({ event: 'newsletter_subscribe', subscribe_location: 'newsletter_page' });
        }
      })
      .catch(function(){
        btn.disabled = false;
        btn.textContent = 'Subscribe Free';
        var err = wrap.querySelector('.aifp-err');
        if (!err) { err = document.createElement('p'); err.className = 'aifp-err'; err.style.cssText = 'color:#dc2626;font-size:12px;margin:8px 0 0;'; wrap.appendChild(err); }
        err.textContent = 'Something went wrong. Please try again.';
      });
    });
  });
})();
</script>
    <?php
}, 20);
