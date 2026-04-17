<?php
/**
 * ACF Field Group Definitions
 * Registered in PHP for version control.
 *
 * NOTE: This file requires ACF Pro for repeater and group fields.
 * With the free version of ACF, these fields must be created manually
 * in the ACF admin GUI. This file serves as the blueprint.
 *
 * @package AIFP
 */

defined('ABSPATH') || exit;

/* ══════════════════════════════════════════════
   TOOL REVIEW FIELDS
   ══════════════════════════════════════════════ */
acf_add_local_field_group([
    'key'      => 'group_tool_review',
    'title'    => 'Tool Hub Content',
    'location' => [[[
        'param'    => 'post_type',
        'operator' => '==',
        'value'    => 'tool_review',
    ]]],
    'menu_order' => 0,
    'fields'     => [

        /* ── Core Fields ── */
        ['key' => 'field_tr_tool_name',    'label' => 'Tool Name',    'name' => 'tool_name',    'type' => 'text', 'required' => 1, 'instructions' => 'e.g., ChatGPT, Claude, Perplexity AI'],
        ['key' => 'field_tr_tool_slug',    'label' => 'Tool Slug',    'name' => 'tool_slug',    'type' => 'text', 'required' => 1, 'instructions' => 'e.g., chatgpt, claude, perplexity'],
        ['key' => 'field_tr_verdict_type', 'label' => 'Verdict Type', 'name' => 'verdict_type', 'type' => 'select', 'choices' => ['recommended' => 'Recommended (Blue)', 'specialized' => 'Specialized (Purple)'], 'default_value' => 'recommended'],
        ['key' => 'field_tr_subtitle',     'label' => 'Subtitle',     'name' => 'subtitle',     'type' => 'textarea', 'rows' => 2, 'instructions' => 'One-line description below H1'],
        ['key' => 'field_tr_publish_date', 'label' => 'Publish Date', 'name' => 'publish_date', 'type' => 'date_picker', 'display_format' => 'F j, Y', 'return_format' => 'F j, Y'],

        /* ── Consistency Blocks ── */
        ['key' => 'field_tr_consistency', 'label' => 'Consistency Blocks', 'name' => 'consistency_blocks', 'type' => 'group', 'layout' => 'block', 'sub_fields' => [
            ['key' => 'field_tr_cb_bottom_line',   'label' => 'Bottom Line',   'name' => 'bottom_line',   'type' => 'textarea', 'rows' => 3],
            ['key' => 'field_tr_cb_key_takeaway',  'label' => 'Key Takeaway',  'name' => 'key_takeaway',  'type' => 'textarea', 'rows' => 4, 'instructions' => 'One takeaway per line (4 lines)'],
            ['key' => 'field_tr_cb_best_for',      'label' => 'Best For',      'name' => 'best_for',      'type' => 'textarea', 'rows' => 4, 'instructions' => 'One item per line'],
            ['key' => 'field_tr_cb_avoid_if',      'label' => 'Avoid If',      'name' => 'avoid_if',      'type' => 'textarea', 'rows' => 3, 'instructions' => 'One item per line'],
            ['key' => 'field_tr_cb_mini_workflow',  'label' => 'Mini Workflow', 'name' => 'mini_workflow', 'type' => 'textarea', 'rows' => 5, 'instructions' => 'First line = lead-in, remaining lines = steps'],
        ]],

        /* ── Quick Facts ── */
        ['key' => 'field_tr_facts', 'label' => 'Quick Facts', 'name' => 'quick_facts', 'type' => 'group', 'layout' => 'block', 'sub_fields' => [
            ['key' => 'field_tr_qf_made_by',            'label' => 'Made By',            'name' => 'made_by',            'type' => 'text'],
            ['key' => 'field_tr_qf_best_for',           'label' => 'Best For',           'name' => 'best_for_fact',      'type' => 'text'],
            ['key' => 'field_tr_qf_pricing',            'label' => 'Pricing',            'name' => 'pricing_fact',       'type' => 'text'],
            ['key' => 'field_tr_qf_custom_label',       'label' => 'Custom Fact Label',  'name' => 'custom_fact_label',  'type' => 'text', 'instructions' => 'e.g., Context Window'],
            ['key' => 'field_tr_qf_custom_value',       'label' => 'Custom Fact Value',  'name' => 'custom_fact_value',  'type' => 'text'],
            ['key' => 'field_tr_qf_hipaa',              'label' => 'HIPAA',              'name' => 'hipaa_fact',         'type' => 'text'],
        ]],

        /* ── Main Content Sections ── */
        ['key' => 'field_tr_what_it_is',       'label' => 'What It Is (and Is Not)', 'name' => 'what_it_is',       'type' => 'wysiwyg', 'tabs' => 'all', 'toolbar' => 'full', 'media_upload' => 0],
        ['key' => 'field_tr_who_its_right_for', 'label' => 'Who It\'s Right For',     'name' => 'who_its_right_for', 'type' => 'wysiwyg', 'tabs' => 'all', 'toolbar' => 'full', 'media_upload' => 0],

        /* ── Features (repeater — requires ACF Pro) ── */
        ['key' => 'field_tr_features', 'label' => 'Features That Matter', 'name' => 'features', 'type' => 'repeater', 'min' => 7, 'max' => 7, 'layout' => 'block', 'sub_fields' => [
            ['key' => 'field_tr_feat_name', 'label' => 'Feature Name', 'name' => 'feature_name', 'type' => 'text'],
            ['key' => 'field_tr_feat_icon', 'label' => 'Icon',         'name' => 'feature_icon', 'type' => 'text', 'instructions' => 'Emoji or icon class'],
            ['key' => 'field_tr_feat_desc', 'label' => 'Description',  'name' => 'feature_description', 'type' => 'wysiwyg', 'tabs' => 'all', 'toolbar' => 'basic', 'media_upload' => 0],
        ]],

        /* ── Pricing (repeater — requires ACF Pro) ── */
        ['key' => 'field_tr_pricing', 'label' => 'Pricing Tiers', 'name' => 'pricing_tiers', 'type' => 'repeater', 'min' => 1, 'max' => 6, 'layout' => 'table', 'sub_fields' => [
            ['key' => 'field_tr_price_name',     'label' => 'Tier Name',  'name' => 'tier_name',     'type' => 'text'],
            ['key' => 'field_tr_price_price',    'label' => 'Price',      'name' => 'tier_price',    'type' => 'text'],
            ['key' => 'field_tr_price_features', 'label' => 'Features',   'name' => 'tier_features', 'type' => 'textarea', 'rows' => 3],
        ]],

        /* ── Verdict ── */
        ['key' => 'field_tr_verdict', 'label' => 'Our Verdict', 'name' => 'verdict_text', 'type' => 'wysiwyg', 'tabs' => 'all', 'toolbar' => 'full', 'media_upload' => 0],

        /* ── FAQ (repeater — requires ACF Pro) ── */
        ['key' => 'field_tr_faq', 'label' => 'FAQ', 'name' => 'faq', 'type' => 'repeater', 'min' => 6, 'max' => 6, 'layout' => 'block', 'sub_fields' => [
            ['key' => 'field_tr_faq_q', 'label' => 'Question', 'name' => 'question', 'type' => 'text'],
            ['key' => 'field_tr_faq_a', 'label' => 'Answer',   'name' => 'answer',   'type' => 'wysiwyg', 'tabs' => 'all', 'toolbar' => 'basic', 'media_upload' => 0],
        ]],

        /* ── Sources (repeater — requires ACF Pro) ── */
        ['key' => 'field_tr_sources', 'label' => 'Sources Checked', 'name' => 'sources', 'type' => 'repeater', 'min' => 5, 'max' => 5, 'layout' => 'table', 'sub_fields' => [
            ['key' => 'field_tr_src_name', 'label' => 'Source Name', 'name' => 'source_name', 'type' => 'text'],
            ['key' => 'field_tr_src_url',  'label' => 'Source URL',  'name' => 'source_url',  'type' => 'url'],
        ]],

        /* ── What Most Reviews Miss (repeater — requires ACF Pro) ── */
        ['key' => 'field_tr_reviews_miss', 'label' => 'What Most Reviews Miss', 'name' => 'reviews_miss', 'type' => 'repeater', 'min' => 3, 'max' => 3, 'layout' => 'block', 'sub_fields' => [
            ['key' => 'field_tr_rm_title', 'label' => 'Insight Title', 'name' => 'insight_title', 'type' => 'text'],
            ['key' => 'field_tr_rm_body',  'label' => 'Insight Body',  'name' => 'insight_body',  'type' => 'textarea', 'rows' => 3],
        ]],
        ['key' => 'field_tr_insight_banner', 'label' => 'Insight Banner', 'name' => 'insight_banner', 'type' => 'textarea', 'rows' => 2],
    ],
]);

/* ══════════════════════════════════════════════
   PROFESSION HUB FIELDS
   ══════════════════════════════════════════════ */
acf_add_local_field_group([
    'key'      => 'group_profession_hub',
    'title'    => 'Profession Hub Content',
    'location' => [[[
        'param'    => 'post_type',
        'operator' => '==',
        'value'    => 'profession_hub',
    ]]],
    'menu_order' => 0,
    'fields'     => [
        ['key' => 'field_ph_profession_name', 'label' => 'Profession Name', 'name' => 'profession_name', 'type' => 'text', 'required' => 1, 'instructions' => 'e.g., Legal Counsel, Physicians'],
        ['key' => 'field_ph_profession_slug', 'label' => 'Profession Slug', 'name' => 'profession_slug', 'type' => 'text', 'required' => 1, 'instructions' => 'e.g., legal, physicians'],
        ['key' => 'field_ph_eyebrow',         'label' => 'Eyebrow Text',    'name' => 'eyebrow_text',    'type' => 'text', 'instructions' => 'e.g., AI Tools for Legal Professionals'],
        ['key' => 'field_ph_lede',            'label' => 'Lede Paragraph',  'name' => 'lede',            'type' => 'textarea', 'rows' => 4],

        /* ── Use Cases (repeater — requires ACF Pro) ── */
        ['key' => 'field_ph_use_cases', 'label' => 'Use Cases', 'name' => 'use_cases', 'type' => 'repeater', 'min' => 1, 'max' => 10, 'layout' => 'block', 'sub_fields' => [
            ['key' => 'field_ph_uc_title',       'label' => 'Title',             'name' => 'use_case_title',       'type' => 'text'],
            ['key' => 'field_ph_uc_description', 'label' => 'Description',       'name' => 'use_case_description', 'type' => 'wysiwyg', 'tabs' => 'all', 'toolbar' => 'basic', 'media_upload' => 0],
        ]],

        /* ── FAQ (repeater — requires ACF Pro) ── */
        ['key' => 'field_ph_faq', 'label' => 'FAQ', 'name' => 'faq', 'type' => 'repeater', 'min' => 4, 'max' => 6, 'layout' => 'block', 'sub_fields' => [
            ['key' => 'field_ph_faq_q', 'label' => 'Question', 'name' => 'question', 'type' => 'text'],
            ['key' => 'field_ph_faq_a', 'label' => 'Answer',   'name' => 'answer',   'type' => 'wysiwyg', 'tabs' => 'all', 'toolbar' => 'basic', 'media_upload' => 0],
        ]],
    ],
]);

/* ══════════════════════════════════════════════
   CROSS-REFERENCE FIELDS
   ══════════════════════════════════════════════ */
acf_add_local_field_group([
    'key'      => 'group_cross_reference',
    'title'    => 'Cross-Reference Content',
    'location' => [[[
        'param'    => 'post_type',
        'operator' => '==',
        'value'    => 'cross_reference',
    ]]],
    'menu_order' => 0,
    'fields'     => [

        /* ── Linked Tool & Profession ── */
        ['key' => 'field_xr_linked_tool',       'label' => 'Linked Tool',       'name' => 'linked_tool',       'type' => 'post_object', 'post_type' => ['tool_review'], 'return_format' => 'object', 'required' => 1],
        ['key' => 'field_xr_linked_profession', 'label' => 'Linked Profession', 'name' => 'linked_profession', 'type' => 'post_object', 'post_type' => ['profession_hub'], 'return_format' => 'object', 'required' => 1],
        ['key' => 'field_xr_verdict_type',      'label' => 'Verdict Type',      'name' => 'verdict_type',      'type' => 'select', 'choices' => ['recommended' => 'Recommended (Blue)', 'specialized' => 'Specialized (Purple)'], 'default_value' => 'recommended'],
        ['key' => 'field_xr_subtitle',          'label' => 'Subtitle',          'name' => 'subtitle',          'type' => 'textarea', 'rows' => 2],

        /* ── Consistency Blocks ── */
        ['key' => 'field_xr_consistency', 'label' => 'Consistency Blocks', 'name' => 'consistency_blocks', 'type' => 'group', 'layout' => 'block', 'sub_fields' => [
            ['key' => 'field_xr_cb_bottom_line',   'label' => 'Bottom Line',   'name' => 'bottom_line',   'type' => 'textarea', 'rows' => 3],
            ['key' => 'field_xr_cb_key_takeaway',  'label' => 'Key Takeaway',  'name' => 'key_takeaway',  'type' => 'textarea', 'rows' => 4],
            ['key' => 'field_xr_cb_best_for',      'label' => 'Best For',      'name' => 'best_for',      'type' => 'textarea', 'rows' => 4],
            ['key' => 'field_xr_cb_avoid_if',      'label' => 'Avoid If',      'name' => 'avoid_if',      'type' => 'textarea', 'rows' => 3],
            ['key' => 'field_xr_cb_mini_workflow',  'label' => 'Mini Workflow', 'name' => 'mini_workflow', 'type' => 'textarea', 'rows' => 5],
        ]],

        /* ── Quick Facts (4 columns for cross-reference) ── */
        ['key' => 'field_xr_facts', 'label' => 'Quick Facts', 'name' => 'quick_facts', 'type' => 'group', 'layout' => 'block', 'sub_fields' => [
            ['key' => 'field_xr_qf_best_for',    'label' => 'Best For',    'name' => 'best_for',    'type' => 'text'],
            ['key' => 'field_xr_qf_pricing',     'label' => 'Pricing',     'name' => 'pricing',     'type' => 'text'],
            ['key' => 'field_xr_qf_compliance',  'label' => 'Compliance',  'name' => 'compliance',  'type' => 'text'],
            ['key' => 'field_xr_qf_compared_to', 'label' => 'Compared To', 'name' => 'compared_to', 'type' => 'text'],
        ]],

        /* ── Content Sections (repeater — requires ACF Pro) ── */
        ['key' => 'field_xr_sections', 'label' => 'Content Sections', 'name' => 'content_sections', 'type' => 'repeater', 'min' => 1, 'max' => 10, 'layout' => 'block', 'sub_fields' => [
            ['key' => 'field_xr_sec_title', 'label' => 'Section Title', 'name' => 'section_title', 'type' => 'text'],
            ['key' => 'field_xr_sec_body',  'label' => 'Section Body',  'name' => 'section_body',  'type' => 'wysiwyg', 'tabs' => 'all', 'toolbar' => 'full', 'media_upload' => 0],
        ]],

        /* ── Prompts (repeater — requires ACF Pro) ── */
        ['key' => 'field_xr_prompts', 'label' => 'Prompts That Work', 'name' => 'prompts', 'type' => 'repeater', 'min' => 0, 'max' => 10, 'layout' => 'block', 'sub_fields' => [
            ['key' => 'field_xr_prompt_title', 'label' => 'Prompt Title', 'name' => 'prompt_title', 'type' => 'text'],
            ['key' => 'field_xr_prompt_text',  'label' => 'Prompt Text',  'name' => 'prompt_text',  'type' => 'textarea', 'rows' => 4],
        ]],

        /* ── Verdict & Comparison ── */
        ['key' => 'field_xr_comparison_notes', 'label' => 'Comparison Notes', 'name' => 'comparison_notes', 'type' => 'wysiwyg', 'tabs' => 'all', 'toolbar' => 'full', 'media_upload' => 0],
        ['key' => 'field_xr_verdict',          'label' => 'My Verdict',       'name' => 'verdict_text',     'type' => 'wysiwyg', 'tabs' => 'all', 'toolbar' => 'full', 'media_upload' => 0],

        /* ── FAQ (repeater — requires ACF Pro) ── */
        ['key' => 'field_xr_faq', 'label' => 'FAQ', 'name' => 'faq', 'type' => 'repeater', 'min' => 4, 'max' => 6, 'layout' => 'block', 'sub_fields' => [
            ['key' => 'field_xr_faq_q', 'label' => 'Question', 'name' => 'question', 'type' => 'text'],
            ['key' => 'field_xr_faq_a', 'label' => 'Answer',   'name' => 'answer',   'type' => 'wysiwyg', 'tabs' => 'all', 'toolbar' => 'basic', 'media_upload' => 0],
        ]],

        /* ── Sources (repeater — requires ACF Pro) ── */
        ['key' => 'field_xr_sources', 'label' => 'Sources Checked', 'name' => 'sources', 'type' => 'repeater', 'min' => 3, 'max' => 5, 'layout' => 'table', 'sub_fields' => [
            ['key' => 'field_xr_src_name', 'label' => 'Source Name', 'name' => 'source_name', 'type' => 'text'],
            ['key' => 'field_xr_src_url',  'label' => 'Source URL',  'name' => 'source_url',  'type' => 'url'],
        ]],

        /* ── What Most Reviews Miss (repeater — requires ACF Pro) ── */
        ['key' => 'field_xr_reviews_miss', 'label' => 'What Most Reviews Miss', 'name' => 'reviews_miss', 'type' => 'repeater', 'min' => 3, 'max' => 3, 'layout' => 'block', 'sub_fields' => [
            ['key' => 'field_xr_rm_title', 'label' => 'Insight Title', 'name' => 'insight_title', 'type' => 'text'],
            ['key' => 'field_xr_rm_body',  'label' => 'Insight Body',  'name' => 'insight_body',  'type' => 'textarea', 'rows' => 3],
        ]],
        ['key' => 'field_xr_insight_banner', 'label' => 'Insight Banner', 'name' => 'insight_banner', 'type' => 'textarea', 'rows' => 2],
    ],
]);
