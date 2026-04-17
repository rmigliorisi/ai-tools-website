<?php
/**
 * JSON-LD Structured Data
 * Auto-generates schema.org markup from post data.
 *
 * @package AIFP
 */

defined('ABSPATH') || exit;

add_action('wp_head', function () {
    if (!is_singular(['tool_review', 'profession_hub', 'cross_reference'])) return;

    $post_id   = get_the_ID();
    $post_type = get_post_type($post_id);
    $data      = aifp_get_data($post_id);
    $url       = get_permalink($post_id);
    $date      = get_the_date('Y-m-d', $post_id);
    $modified  = get_the_modified_date('Y-m-d', $post_id);

    $graph = [];

    /* ── Article / CollectionPage ── */
    if ($post_type === 'profession_hub') {
        $graph[] = [
            '@type'              => 'CollectionPage',
            'name'               => get_the_title($post_id),
            'url'                => $url,
            'description'        => $data['lede'] ?? get_the_excerpt($post_id),
            'isAccessibleForFree'=> true,
        ];
    } else {
        $tool_name = '';
        $headline  = get_the_title($post_id);

        if ($post_type === 'tool_review') {
            $tool_name = $data['tool_name'] ?? '';
            $headline  = $tool_name . ' for Professionals: An Honest Review (' . date('Y') . ')';
        } elseif ($post_type === 'cross_reference') {
            $tool = aifp_get_linked_post($post_id, 'linked_tool');
            $prof = aifp_get_linked_post($post_id, 'linked_profession');
            $tool_name = $tool ? (aifp_get_data($tool->ID)['tool_name'] ?? '') : '';
            $prof_name = $prof ? (aifp_get_data($prof->ID)['profession_name'] ?? '') : '';
            $headline  = $tool_name . ' for ' . $prof_name . ' — ' . date('Y') . ' Guide';
        }

        $graph[] = [
            '@type'              => 'Article',
            'headline'           => $headline,
            'description'        => $data['subtitle'] ?? get_the_excerpt($post_id),
            'author'             => ['@type' => 'Person', 'name' => 'Rich M.'],
            'publisher'          => ['@type' => 'Organization', 'name' => 'AI Tools for Pros', 'url' => home_url('/')],
            'datePublished'      => $date,
            'dateModified'       => $modified,
            'mainEntityOfPage'   => ['@type' => 'WebPage', '@id' => $url],
            'isAccessibleForFree'=> true,
        ];
    }

    /* ── BreadcrumbList ── */
    $breadcrumbs = [
        ['@type' => 'ListItem', 'position' => 1, 'name' => 'Home', 'item' => home_url('/')],
    ];

    if ($post_type === 'tool_review') {
        $breadcrumbs[] = ['@type' => 'ListItem', 'position' => 2, 'name' => $data['tool_name'] ?? '', 'item' => $url];
    } elseif ($post_type === 'profession_hub') {
        $breadcrumbs[] = ['@type' => 'ListItem', 'position' => 2, 'name' => $data['profession_name'] ?? '', 'item' => $url];
    } elseif ($post_type === 'cross_reference') {
        $tool = aifp_get_linked_post($post_id, 'linked_tool');
        $prof = aifp_get_linked_post($post_id, 'linked_profession');
        if ($tool) {
            $breadcrumbs[] = ['@type' => 'ListItem', 'position' => 2, 'name' => aifp_get_data($tool->ID)['tool_name'] ?? '', 'item' => get_permalink($tool->ID)];
        }
        if ($prof) {
            $breadcrumbs[] = ['@type' => 'ListItem', 'position' => 3, 'name' => aifp_get_data($prof->ID)['profession_name'] ?? '', 'item' => $url];
        }
    }

    $graph[] = [
        '@type'           => 'BreadcrumbList',
        'itemListElement' => $breadcrumbs,
    ];

    /* ── FAQPage ── */
    $faqs = $data['faq'] ?? [];
    if (!empty($faqs)) {
        $faq_items = [];
        foreach ($faqs as $faq) {
            $faq_items[] = [
                '@type'          => 'Question',
                'name'           => $faq['question'] ?? '',
                'acceptedAnswer' => [
                    '@type' => 'Answer',
                    'text'  => wp_strip_all_tags($faq['answer'] ?? ''),
                ],
            ];
        }
        $graph[] = [
            '@type'      => 'FAQPage',
            'mainEntity' => $faq_items,
        ];
    }

    /* ── Output ── */
    $schema = [
        '@context' => 'https://schema.org',
        '@graph'   => $graph,
    ];

    echo '<script type="application/ld+json">' . "\n";
    echo wp_json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    echo "\n</script>\n";
}, 5);
