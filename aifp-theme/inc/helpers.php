<?php
/**
 * Helper Functions
 *
 * @package AIFP
 */

defined('ABSPATH') || exit;

/**
 * Get structured data for a post.
 * Data is stored as JSON in post_content.
 */
function aifp_get_data(?int $post_id = null): array {
    if (!$post_id) $post_id = get_the_ID();
    $raw = get_post_field('post_content', $post_id);
    if (!$raw) return [];
    $data = json_decode($raw, true);
    return is_array($data) ? $data : [];
}

/**
 * Get all Tool Review posts, ordered by title.
 */
function aifp_get_tool_reviews(): array {
    return get_posts([
        'post_type'      => 'tool_review',
        'posts_per_page' => -1,
        'orderby'        => 'title',
        'order'          => 'ASC',
        'post_status'    => 'publish',
    ]);
}

/**
 * Get all Profession Hub posts, ordered by title.
 */
function aifp_get_profession_hubs(): array {
    return get_posts([
        'post_type'      => 'profession_hub',
        'posts_per_page' => -1,
        'orderby'        => 'title',
        'order'          => 'ASC',
        'post_status'    => 'publish',
    ]);
}

/**
 * Get cross-reference pages for a specific tool.
 */
function aifp_get_cross_references_for_tool(int $tool_id): array {
    return get_posts([
        'post_type'      => 'cross_reference',
        'posts_per_page' => -1,
        'orderby'        => 'title',
        'order'          => 'ASC',
        'post_status'    => 'publish',
        'meta_query'     => [[
            'key'     => 'linked_tool',
            'value'   => $tool_id,
            'compare' => '=',
        ]],
    ]);
}

/**
 * Get cross-reference pages for a specific profession.
 */
function aifp_get_cross_references_for_profession(int $prof_id): array {
    return get_posts([
        'post_type'      => 'cross_reference',
        'posts_per_page' => -1,
        'orderby'        => 'title',
        'order'          => 'ASC',
        'post_status'    => 'publish',
        'meta_query'     => [[
            'key'     => 'linked_profession',
            'value'   => $prof_id,
            'compare' => '=',
        ]],
    ]);
}

/**
 * Calculate reading time from structured data.
 */
function aifp_reading_time(int $post_id): int {
    $data = aifp_get_data($post_id);
    $content = '';

    foreach (['what_it_is', 'who_its_right_for', 'verdict_text', 'subtitle', 'comparison_notes'] as $field) {
        if (!empty($data[$field])) {
            $content .= ' ' . wp_strip_all_tags($data[$field]);
        }
    }

    if (!empty($data['consistency_blocks'])) {
        foreach ($data['consistency_blocks'] as $val) {
            if (is_string($val)) $content .= ' ' . wp_strip_all_tags($val);
        }
    }

    if (!empty($data['features'])) {
        foreach ($data['features'] as $feat) {
            $content .= ' ' . wp_strip_all_tags($feat['feature_description'] ?? '');
        }
    }

    if (!empty($data['content_sections'])) {
        foreach ($data['content_sections'] as $sec) {
            $content .= ' ' . wp_strip_all_tags($sec['section_body'] ?? '');
        }
    }

    if (!empty($data['faq'])) {
        foreach ($data['faq'] as $item) {
            $content .= ' ' . ($item['question'] ?? '');
            $content .= ' ' . wp_strip_all_tags($item['answer'] ?? '');
        }
    }

    $word_count = str_word_count($content);
    return max(1, (int) ceil($word_count / 238));
}

/**
 * Get the verdict badge HTML for a post.
 */
function aifp_verdict_badge(int $post_id): string {
    $data = aifp_get_data($post_id);
    $type = $data['verdict_type'] ?? 'recommended';
    $class = ($type === 'specialized') ? 'verdict-badge-specialized' : 'verdict-badge-recommended';
    $label = ($type === 'specialized') ? 'Specialized' : 'Recommended';

    return '<span class="' . esc_attr($class) . '">' . esc_html($label) . '</span>';
}

/**
 * Get theme SVG URL.
 */
function aifp_svg_url(string $filename): string {
    return get_theme_file_uri('assets/svg/' . $filename);
}

/**
 * Get linked post object from cross-reference meta.
 */
function aifp_get_linked_post(int $post_id, string $meta_key): ?WP_Post {
    $linked_id = get_post_meta($post_id, $meta_key, true);
    if (!$linked_id) return null;
    $post = get_post((int) $linked_id);
    return ($post && $post->post_status === 'publish') ? $post : null;
}
