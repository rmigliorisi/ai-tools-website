<?php
/**
 * Custom Post Types, Taxonomies & Rewrite Rules
 *
 * @package AIFP
 */

defined('ABSPATH') || exit;

add_action('init', function () {

    /* ── Tool Review CPT ── */
    register_post_type('tool_review', [
        'labels' => [
            'name'          => 'Tool Reviews',
            'singular_name' => 'Tool Review',
            'add_new_item'  => 'Add New Tool Review',
            'edit_item'     => 'Edit Tool Review',
            'all_items'     => 'All Tool Reviews',
            'search_items'  => 'Search Tool Reviews',
        ],
        'public'       => true,
        'has_archive'  => false,
        'menu_icon'    => 'dashicons-star-filled',
        'menu_position'=> 5,
        'supports'     => ['title', 'editor', 'custom-fields', 'revisions'],
        'rewrite'      => false, // Handled explicitly in functions.php
        'show_in_rest' => true,
    ]);

    /* ── Profession Hub CPT ── */
    register_post_type('profession_hub', [
        'labels' => [
            'name'          => 'Profession Hubs',
            'singular_name' => 'Profession Hub',
            'add_new_item'  => 'Add New Profession Hub',
            'edit_item'     => 'Edit Profession Hub',
            'all_items'     => 'All Profession Hubs',
            'search_items'  => 'Search Profession Hubs',
        ],
        'public'       => true,
        'has_archive'  => false,
        'menu_icon'    => 'dashicons-groups',
        'menu_position'=> 6,
        'supports'     => ['title', 'editor', 'custom-fields', 'revisions'],
        'rewrite'      => false, // Handled explicitly in functions.php
        'show_in_rest' => true,
    ]);

    /* ── Cross-Reference CPT ── */
    register_post_type('cross_reference', [
        'labels' => [
            'name'          => 'Cross-References',
            'singular_name' => 'Cross-Reference',
            'add_new_item'  => 'Add New Cross-Reference',
            'edit_item'     => 'Edit Cross-Reference',
            'all_items'     => 'All Cross-References',
            'search_items'  => 'Search Cross-References',
        ],
        'public'       => true,
        'has_archive'  => false,
        'menu_icon'    => 'dashicons-networking',
        'menu_position'=> 7,
        'supports'     => ['title', 'editor', 'custom-fields', 'revisions'],
        'rewrite'      => false, // Rewrite rules handled in functions.php
        'show_in_rest' => true,
    ]);

    /* ── AI Tool Taxonomy ── */
    register_taxonomy('ai_tool', ['tool_review', 'profession_hub', 'cross_reference'], [
        'labels' => [
            'name'          => 'AI Tools',
            'singular_name' => 'AI Tool',
            'search_items'  => 'Search AI Tools',
            'all_items'     => 'All AI Tools',
            'edit_item'     => 'Edit AI Tool',
            'add_new_item'  => 'Add New AI Tool',
        ],
        'public'       => true,
        'hierarchical' => false,
        'show_in_rest' => true,
        'rewrite'      => false,
    ]);

    /* ── Profession Taxonomy ── */
    register_taxonomy('profession', ['profession_hub', 'cross_reference'], [
        'labels' => [
            'name'          => 'Professions',
            'singular_name' => 'Profession',
            'search_items'  => 'Search Professions',
            'all_items'     => 'All Professions',
            'edit_item'     => 'Edit Profession',
            'add_new_item'  => 'Add New Profession',
        ],
        'public'       => true,
        'hierarchical' => false,
        'show_in_rest' => true,
        'rewrite'      => false,
    ]);

    /* ── AI Update CPT (monthly "/[month]-[year]-updates/" page) ── */
    register_post_type('aifp_update', [
        'labels' => [
            'name'          => 'AI Updates',
            'singular_name' => 'AI Update',
            'add_new_item'  => 'Add New AI Update',
            'edit_item'     => 'Edit AI Update',
            'all_items'     => 'All AI Updates',
            'search_items'  => 'Search AI Updates',
        ],
        'public'       => true,
        'has_archive'  => false,
        'menu_icon'    => 'dashicons-megaphone',
        'menu_position'=> 8,
        'supports'     => ['title', 'editor', 'custom-fields', 'revisions'],
        'rewrite'      => false, // Handled explicitly in functions.php, same as tool_review/profession_hub
        'show_in_rest' => true,
    ]);

    /* ── Newsletter Subscriber CPT ── */
    register_post_type('aifp_subscriber', [
        'labels' => [
            'name'          => 'Subscribers',
            'singular_name' => 'Subscriber',
            'all_items'     => 'All Subscribers',
            'search_items'  => 'Search Subscribers',
        ],
        'public'        => false,
        'show_ui'       => true,
        'show_in_menu'  => true,
        'menu_icon'     => 'dashicons-email-alt',
        'menu_position' => 9,
        'supports'      => ['title'],
        'show_in_rest'  => false,
    ]);

    /* ── Contact Form Submission CPT ── */
    register_post_type('aifp_contact', [
        'labels' => [
            'name'          => 'Contact Submissions',
            'singular_name' => 'Contact Submission',
            'all_items'     => 'All Contact Submissions',
            'search_items'  => 'Search Submissions',
        ],
        'public'              => false,
        'publicly_queryable'  => false,
        'exclude_from_search' => true,
        'show_ui'             => true,
        'show_in_menu'        => true,
        'show_in_nav_menus'   => false,
        'menu_icon'           => 'dashicons-format-chat',
        'menu_position'       => 10,
        'supports'            => ['title', 'custom-fields'],
        'show_in_rest'        => false,
    ]);

    /* ── Weekly Update Log CPT (audit trail for automated tool-page edits) ── */
    register_post_type('aifp_update_log', [
        'labels' => [
            'name'          => 'Update Log',
            'singular_name' => 'Update Log Entry',
            'all_items'     => 'Weekly Update Log',
            'search_items'  => 'Search Update Log',
        ],
        'public'              => false,
        'publicly_queryable'  => false,
        'exclude_from_search' => true,
        'show_ui'             => true,
        'show_in_menu'        => true,
        'show_in_nav_menus'   => false,
        'menu_icon'           => 'dashicons-clock',
        'menu_position'       => 11,
        'supports'            => ['title', 'custom-fields'],
        'show_in_rest'        => false,
    ]);

});

/* ── Fix permalink conflicts between CPTs sharing "/" slug ── */
add_filter('wp_unique_post_slug', function ($slug, $post_id, $status, $type) {
    return $slug;
}, 10, 4);

/* ── Cross-Reference Pretty Permalinks ── */
// Output /{tool-slug}/{profession-slug}/ instead of /?cross_reference=slug
add_filter('post_type_link', function ($link, $post) {
    if ($post->post_type === 'tool_review' || $post->post_type === 'profession_hub' || $post->post_type === 'aifp_update') {
        return home_url('/' . $post->post_name . '/');
    }

    if ($post->post_type !== 'cross_reference') {
        return $link;
    }

    // Slug format is "chatgpt-legal" → split into tool "chatgpt" + profession "legal"
    $slug = $post->post_name;
    $tool_id = get_post_meta($post->ID, 'linked_tool', true);
    $prof_id = get_post_meta($post->ID, 'linked_profession', true);

    if ($tool_id && $prof_id) {
        $tool_post = get_post($tool_id);
        $prof_post = get_post($prof_id);
        if ($tool_post && $prof_post) {
            return home_url('/' . $tool_post->post_name . '/' . $prof_post->post_name . '/');
        }
    }

    // Fallback: parse slug (tool-slug-profession-slug)
    // Find the split point by checking which tool slug matches the beginning
    $tools = get_posts(['post_type' => 'tool_review', 'posts_per_page' => -1, 'post_status' => 'publish']);
    foreach ($tools as $tool) {
        $prefix = $tool->post_name . '-';
        if (strpos($slug, $prefix) === 0) {
            $prof_slug = substr($slug, strlen($prefix));
            return home_url('/' . $tool->post_name . '/' . $prof_slug . '/');
        }
    }

    return $link;
}, 10, 2);

/* ── Flush rewrite rules on theme activation ── */
add_action('after_switch_theme', function () {
    flush_rewrite_rules();
});
